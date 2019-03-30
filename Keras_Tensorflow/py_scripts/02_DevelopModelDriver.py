# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py_scripts//py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 1.0.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Develop Model Driver
#
# In this notebook, we will develop the API that will call our model. This module initializes the model, transforms the input so that it is in the appropriate format and defines the scoring method that will produce the predictions. The API will expect the input to be in JSON format. Once a request is received, the API will convert the json encoded request body into the image format. There are two main functions in the API: init() and run(). The init() function loads the model and returns a scoring function. The run() function process the images and uses the first function to score them.
#
#     Note: Always make sure you don't have any lingering notebooks running (Shutdown previous notebooks). Otherwise it may cause GPU memory issue.

from azureml.core import Workspace
from azureml.core.compute import AksCompute, ComputeTarget
from azureml.core.webservice import Webservice, AksWebservice
from azureml.core.image import Image
from azureml.core.model import Model
from dotenv import set_key, get_key, find_dotenv
import logging
from testing_utilities import get_auth

import keras
import tensorflow
print("Keras: ", keras.__version__)
print("Tensorflow: ", tensorflow.__version__)

env_path = find_dotenv(raise_error_if_not_found=True)

# ## Write and save driver script

# + {"magic_args": "driver.py", "language": "writefile"}
#
# import tensorflow as tf
# from resnet152 import ResNet152
# from keras.preprocessing import image
# from keras.applications.imagenet_utils import preprocess_input, decode_predictions
# from azureml.contrib.services.aml_request  import rawhttp
# from azureml.core.model import Model
# from toolz import compose
# import numpy as np
# import timeit as t
# from PIL import Image, ImageOps
# import logging
#
# _NUMBER_RESULTS = 3
#
#
# def _image_ref_to_pil_image(image_ref):
#     """ Load image with PIL (RGB)
#     """
#     return Image.open(image_ref).convert("RGB")
#
#
# def _pil_to_numpy(pil_image):
#     img = ImageOps.fit(pil_image, (224, 224), Image.ANTIALIAS)
#     img = image.img_to_array(img)
#     return img
#
#
# def _create_scoring_func():
#     """ Initialize ResNet 152 Model 
#     """ 
#     logger = logging.getLogger("model_driver")
#     start = t.default_timer()
#     model_name = 'resnet_model'
#     model_path = Model.get_model_path(model_name)
#     model = ResNet152()
#     model.load_weights(model_path)
#     end = t.default_timer()
#     
#     loadTimeMsg = "Model loading time: {0} ms".format(round((end-start)*1000, 2))
#     logger.info(loadTimeMsg)
#     
#     def call_model(img_array_list):
#         img_array = np.stack(img_array_list)
#         img_array = preprocess_input(img_array)
#         preds = model.predict(img_array)
#         # Converting predictions to float64 since we are able to serialize float64 but not float32
#         preds = decode_predictions(preds.astype(np.float64), top=_NUMBER_RESULTS)[0] 
#         return preds
#     
#     return call_model       
#
#     
# def get_model_api():
#     logger = logging.getLogger("model_driver")
#     scoring_func = _create_scoring_func()
#     
#     def process_and_score(images_dict):
#         """ Classify the input using the loaded model
#         """
#         start = t.default_timer()
#         logger.info('Scoring {} images'.format(len(images_dict)))
#         transform_input = compose(_pil_to_numpy,
#                                   _image_ref_to_pil_image)
#         transformed_dict = {key: transform_input(img_ref) for key, img_ref in images_dict.items()}
#         preds = scoring_func(list(transformed_dict.values()))
#         preds = dict(zip(transformed_dict.keys(), preds)) 
#         end = t.default_timer()
#         
#         logger.info("Predictions: {0}".format(preds))
#         logger.info("Predictions took {0} ms".format(round((end-start)*1000, 2)))
#         return (preds, "Computed in {0} ms".format(round((end-start)*1000, 2)))
#     return process_and_score
#
# def init():
#     """ Initialise the model and scoring function
#     """
#     global process_and_score
#     process_and_score = get_model_api()
#
# @rawhttp    
# def run(request):
#     """ Make a prediction based on the data passed in using the preloaded model
#     """
#     return process_and_score(request.files)
# -

# ## Test the driver¶ 
# We test the driver by passing data.

logging.basicConfig(level=logging.DEBUG)

# %run driver.py

# Let's load the workspace.

ws = Workspace.from_config(auth=get_auth())
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep="\n")

model_path = Model.get_model_path('resnet_model', _workspace=ws)

IMAGEURL = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Lynx_lynx_poing.jpg/220px-Lynx_lynx_poing.jpg"

# Always make sure you don't have any lingering notebooks running. Otherwise it may cause GPU memory issue.
process_and_score = get_model_api()

resp = process_and_score({'lynx':open('220px-Lynx_lynx_poing.jpg', 'rb')})

# Clear GPU memory
from keras import backend as K
K.clear_session()

# Next, we will [build a docker image with this modle driver and other supporting files](03_BuildImage.ipynb).
