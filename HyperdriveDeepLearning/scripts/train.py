import os
import sys

sys.path.append("./cocoapi/PythonAPI/")

import torch
import argparse
import utils
from XMLDataset import BuildDataset, get_transform
from maskrcnn_model import get_model
from engine import train_one_epoch, evaluate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PyTorch Object Detection Training")
    parser.add_argument(
        "--data_path", default="./Data/", help="the path to the dataset"
    )
    parser.add_argument("--batch_size", default=2, type=int)
    parser.add_argument(
        "--epochs", default=10, type=int, help="number of total epochs to run"
    )
    parser.add_argument(
        "--workers", default=4, type=int, help="number of data loading workers"
    )
    parser.add_argument(
        "--learning_rate", default=0.005, type=float, help="initial learning rate"
    )
    parser.add_argument("--momentum", default=0.9, type=float, help="momentum")
    parser.add_argument(
        "--weight_decay",
        default=0.0005,
        type=float,
        help="weight decay (default: 1e-4)",
    )
    parser.add_argument(
        "--lr_step_size", default=3, type=int, help="decrease lr every step-size epochs"
    )
    parser.add_argument(
        "--lr_gamma",
        default=0.1,
        type=float,
        help="decrease lr by a factor of lr-gamma",
    )
    parser.add_argument("--print_freq", default=10, type=int, help="print frequency")
    parser.add_argument("--output_dir", default="outputs", help="path where to save")
    parser.add_argument("--anchor_sizes", default="16", type=str, help="anchor sizes")
    parser.add_argument(
        "--anchor_aspect_ratios", default="1.0", type=str, help="anchor aspect ratios"
    )
    parser.add_argument(
        "--rpn_nms_thresh",
        default=0.7,
        type=float,
        help="NMS threshold used for postprocessing the RPN proposals",
    )
    parser.add_argument(
        "--box_nms_thresh",
        default=0.5,
        type=float,
        help="NMS threshold for the prediction head. Used during inference",
    )
    parser.add_argument(
        "--box_score_thresh",
        default=0.05,
        type=float,
        help="during inference only return proposals"
        "with a classification score greater than box_score_thresh",
    )
    parser.add_argument(
        "--box_detections_per_img",
        default=100,
        type=int,
        help="maximum number of detections per image, for all classes",
    )
    args = parser.parse_args()

data_path = args.data_path

# use our dataset and defined transformations
dataset = BuildDataset(data_path, get_transform(train=True))
dataset_test = BuildDataset(data_path, get_transform(train=False))

# split the dataset in train and test set
indices = torch.randperm(len(dataset)).tolist()
dataset = torch.utils.data.Subset(dataset, indices[:-100])
dataset_test = torch.utils.data.Subset(dataset_test, indices[-100:])

batch_size = args.batch_size
workers = args.workers

# define training and validation data loaders
data_loader = torch.utils.data.DataLoader(
    dataset,
    batch_size=2,
    shuffle=True,
    num_workers=workers,
    collate_fn=utils.collate_fn,
)

data_loader_test = torch.utils.data.DataLoader(
    dataset_test,
    batch_size=2,
    shuffle=False,
    num_workers=workers,
    collate_fn=utils.collate_fn,
)

# our dataset has two classes only - background and out of stock
num_classes = 2

model = get_model(
    num_classes,
    args.anchor_sizes,
    args.anchor_aspect_ratios,
    args.rpn_nms_thresh,
    args.box_nms_thresh,
    args.box_score_thresh,
    args.box_detections_per_img,
)

# train on the GPU or on the CPU, if a GPU is not available
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

# move model to the right device
model.to(device)

learning_rate = args.learning_rate
momentum = args.momentum
weight_decay = args.weight_decay

# construct an optimizer
params = [p for p in model.parameters() if p.requires_grad]
optimizer = torch.optim.SGD(
    params, lr=learning_rate, momentum=momentum, weight_decay=weight_decay
)

lr_step_size = args.lr_step_size
lr_gamma = args.lr_gamma

# and a learning rate scheduler
lr_scheduler = torch.optim.lr_scheduler.StepLR(
    optimizer, step_size=lr_step_size, gamma=lr_gamma
)

# number of training epochs
num_epochs = args.epochs
print_freq = args.print_freq

for epoch in range(num_epochs):
    # train for one epoch, printing every 10 iterations
    train_one_epoch(model, optimizer, data_loader, device, epoch, print_freq=print_freq)
    # update the learning rate
    lr_scheduler.step()
    # evaluate on the test dataset after every epoch
    evaluate(model, data_loader_test, device=device)

# save model
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)
torch.save(model.state_dict(), os.path.join(args.output_dir, "model_latest.pth"))

print("That's it!")
