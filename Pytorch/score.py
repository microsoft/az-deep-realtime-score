import base64
import json
import logging
import os
import timeit as t
from io import BytesIO

import PIL
import numpy as np
import torch
import torch.nn as nn
import torchvision
from PIL import Image
from torchvision import models, transforms
import sys
from azureml.core.model import Model
from glob import glob
import warnings

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout) # TODO: remove


_LABEL_FILE = os.getenv("LABEL_FILE", "synset.txt")
_MODEL_NAME = os.getenv("MODEL_NAME", "pytorch_resnet152")
_NUMBER_RESULTS = 3


class ModelFileNotFoundError(Exception):
    pass

def _create_label_lookup(label_path):
    with open(label_path, "r") as f:
        label_list = [l.rstrip() for l in f]

    def _label_lookup(*label_locks):
        return [label_list[l] for l in label_locks]

    return _label_lookup


def _load_model():
    logger = logging.getLogger("model_driver")
    # Load the model
    model_path = Model.get_model_path(_MODEL_NAME)
    
    file_list = glob(os.path.join(_MODEL_NAME,'*.pth'))
    if len(file_list)==0:
        raise ModelFileNotFoundError(f'Appropriate model not found in {_MODEL_NAME}')
    elif len(file_list)>1:
        warnings.warn("More than one model found. Selecting first model")

    filename = file_list[0]
    logger.debug(f'Loading {filename}')
    # ResNet 152
    model = models.ResNet(models.resnet.Bottleneck, [3, 8, 36, 3])
    model.load_state_dict(torch.load(filename))
    
    model = model.cuda()
    softmax = nn.Softmax(dim=1).cuda()
    model = model.eval()

    preprocess_input = transforms.Compose(
        [
            torchvision.transforms.Resize((224, 224), interpolation=PIL.Image.BICUBIC),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )

    def predict_for(image):
        image = preprocess_input(image)
        with torch.no_grad():
            image = image.unsqueeze(0)
            image_gpu = image.type(torch.float).cuda()
            outputs = model(image_gpu)
            pred_proba = softmax(outputs)
        return pred_proba.cpu().numpy().squeeze()

    return predict_for


def _base64img_to_pil_image(base64_img_string):
    if base64_img_string.startswith("b'"):
        base64_img_string = base64_img_string[2:-1]
    base64Img = base64_img_string.encode("utf-8")

    # Preprocess the input data
    decoded_img = base64.b64decode(base64Img)
    img_buffer = BytesIO(decoded_img)

    # Load image with PIL (RGB)
    pil_img = Image.open(img_buffer).convert("RGB")
    return pil_img


def create_scoring_func(label_path=_LABEL_FILE):
    logger = logging.getLogger("model_driver")

    start = t.default_timer()
    labels_for = _create_label_lookup(label_path)
    predict_for = _load_model()
    end = t.default_timer()

    loadTimeMsg = "Model loading time: {0} ms".format(round((end - start) * 1000, 2))
    logger.info(loadTimeMsg)

    def _call_model(image, number_results=_NUMBER_RESULTS):
        pred_proba = predict_for(image).squeeze()
        selected_results = np.flip(np.argsort(pred_proba), 0)[:number_results]
        labels = labels_for(*selected_results)
        return list(zip(labels, pred_proba[selected_results].astype(np.float64)))

    return _call_model


def get_model_api():
    logger = logging.getLogger("model_driver")
    scoring_func = create_scoring_func()

    def _process_and_score(images_dict, number_results=_NUMBER_RESULTS):
        start = t.default_timer()

        results = {}
        for key, base64_img_string in images_dict.items():
            rgb_image = _base64img_to_pil_image(base64_img_string)
            results[key] = scoring_func(rgb_image, number_results=number_results)

        end = t.default_timer()

        logger.debug("Predictions: {0}".format(results))
        logger.info("Predictions took {0} ms".format(round((end - start) * 1000, 2)))
        return (results, "Computed in {0} ms".format(round((end - start) * 1000, 2)))

    return _process_and_score

def version():
    return torch.__version__

def init():
    global process_and_score
    process_and_score = get_model_api()

def run(raw_data):
    # make prediction
    return process_and_score(json.loads(raw_data)['input'])
