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

# # Develop Model
# In this noteook, we will go through the steps to load the ResNet152 model, pre-process the images to the required format and call the model to find the top predictions.
#
#     Note: Always make sure you don't have any lingering notebooks running (Shutdown previous notebooks). Otherwise it may cause GPU memory issue.

# +
import numpy as np
from PIL import Image, ImageOps
import wget
from resnet152 import ResNet152
from keras.applications.imagenet_utils import preprocess_input, decode_predictions

from dotenv import set_key, find_dotenv
from testing_utilities import get_auth

# -

env_path = find_dotenv(raise_error_if_not_found=True)

# ## Create the model

# If you see error msg "InternalError: Dst tensor is not initialized.", it indicates there are not enough memory.
model = ResNet152(weights="imagenet")
print("model loaded")

wget.download(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Lynx_lynx_poing.jpg/220px-Lynx_lynx_poing.jpg"
)

img_path = "220px-Lynx_lynx_poing.jpg"
print(Image.open(img_path).size)
Image.open(img_path)

# Below, we load the image by resizing to (224, 224) and then preprocessing using the methods from keras preprocessing and imagenet utilities.

# Evaluate the model using the input data
img = Image.open(img_path).convert("RGB")
img = ImageOps.fit(img, (224, 224), Image.ANTIALIAS)
img = np.array(img)  # shape: (224, 224, 3)
img = np.expand_dims(img, axis=0)
img = preprocess_input(img)

# Now, let's call the model on our image to predict the top 3 labels. This will take a few seconds.

# %%time
preds = model.predict(img)
decoded_predictions = decode_predictions(preds, top=3)
print("Predicted:", decoded_predictions)
resp = {img_path: str(decoded_predictions)}

# ## Register the model
# Register an existing trained model, add descirption and tags.

# +
# Get workspace
# Load existing workspace from the config file info.
from azureml.core.workspace import Workspace

ws = Workspace.from_config(auth=get_auth())
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep="\n")
# -

model.save_weights("model_resnet_weights.h5")

# Register the model
from azureml.core.model import Model

model = Model.register(
    model_path="model_resnet_weights.h5",  # this points to a local file
    model_name="resnet_model",  # this is the name the model is registered as
    tags={"model": "dl", "framework": "resnet"},
    description="resnet 152 model",
    workspace=ws,
)

print(model.name, model.description, model.version)

set_key(env_path, "model_version", str(model.version))

# Clear GPU memory
from keras import backend as K

K.clear_session()

# We have registred the trained ResNet152 model in Azure ML. We can now move on to [developing the model api for our model](02_DevelopModelDriver.ipynb).
