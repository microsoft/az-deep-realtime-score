import os
import xml.etree.ElementTree as ET
import torch
import transforms as T
from PIL import Image


class BuildDataset(torch.utils.data.Dataset):
    def __init__(self, root, transforms=None):
        self.root = root
        self.transforms = transforms
        # load all image files
        self.imgs = list(sorted(os.listdir(os.path.join(root, "JPEGImages"))))

    def __getitem__(self, idx):
        img_path = os.path.join(self.root, "JPEGImages", self.imgs[idx])
        xml_path = os.path.join(
            self.root, "Annotations", "{}.xml".format(self.imgs[idx].strip(".jpg"))
        )
        img = Image.open(img_path).convert("RGB")

        # parse XML annotation
        tree = ET.parse(xml_path)
        t_root = tree.getroot()

        # get bounding box coordinates
        boxes = []
        for obj in t_root.findall("object"):
            bnd_box = obj.find("bndbox")
            xmin = float(bnd_box.find("xmin").text)
            xmax = float(bnd_box.find("xmax").text)
            ymin = float(bnd_box.find("ymin").text)
            ymax = float(bnd_box.find("ymax").text)
            boxes.append([xmin, ymin, xmax, ymax])
        num_objs = len(boxes)
        boxes = torch.as_tensor(boxes, dtype=torch.float32)

        # there is only one class
        labels = torch.ones((num_objs,), dtype=torch.int64)
        image_id = torch.tensor([idx])

        # area of the bounding box, used during evaluation with the COCO metric for small, medium and large boxes
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])

        # suppose all instances are not crowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.imgs)


def get_transform(train):
    transforms = []
    transforms.append(T.ToTensor())
    if train:
        transforms.append(T.RandomHorizontalFlip(0.5))
    return T.Compose(transforms)
