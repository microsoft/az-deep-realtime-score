import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.rpn import AnchorGenerator
from torchvision.models.detection.rpn import RPNHead


def get_model(
    num_classes,
    anchor_sizes,
    anchor_aspect_ratios,
    rpn_nms_threshold,
    box_nms_threshold,
    box_score_threshold,
    num_box_detections,
):

    # load pre-trained mask R-CNN model
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(
        pretrained=True,
        rpn_nms_thresh=rpn_nms_threshold,
        box_nms_thresh=box_nms_threshold,
        box_score_thresh=box_score_threshold,
        box_detections_per_img=num_box_detections,
    )
    # get number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features

    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    anchor_sizes = tuple([float(i) for i in anchor_sizes.split(",")])
    anchor_aspect_ratios = tuple([float(i) for i in anchor_aspect_ratios.split(",")])

    # create an anchor_generator for the FPN which by default has 5 outputs
    anchor_generator = AnchorGenerator(
        sizes=tuple([anchor_sizes for _ in range(5)]),
        aspect_ratios=tuple([anchor_aspect_ratios for _ in range(5)]),
    )
    model.rpn.anchor_generator = anchor_generator

    # get number of input features for the RPN returned by FPN (256)
    in_channels = model.backbone.out_channels

    # replace the RPN head
    model.rpn.head = RPNHead(
        in_channels, anchor_generator.num_anchors_per_location()[0]
    )

    # turn off masks since dataset only has bounding boxes
    model.roi_heads.mask_roi_pool = None

    return model
