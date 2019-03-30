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

# # Test deployed web application

# This notebook pulls some images and tests them against the deployed web application on AKS.

import matplotlib.pyplot as plt
import numpy as np
import requests
from testing_utilities import to_img, img_url_to_json, plot_predictions, get_auth, read_image_from
from azureml.core.workspace import Workspace
from azureml.core.webservice import AksWebservice
from dotenv import set_key, get_key, find_dotenv

env_path = find_dotenv(raise_error_if_not_found=True)

# Get the external url for the web application running on AKS cluster.

ws = Workspace.from_config(auth=get_auth())
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep="\n")

# Let's retrieve web service.

aks_service_name = get_key(env_path, 'aks_service_name')
aks_service = AksWebservice(ws, name=aks_service_name)

aks_service.state

scoring_url = aks_service.scoring_uri
api_key = aks_service.get_keys()[0]

# Pull an image of a Lynx to test it with.

IMAGEURL = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Lynx_lynx_poing.jpg/220px-Lynx_lynx_poing.jpg"

plt.imshow(to_img(IMAGEURL))

# +

headers = {'Authorization':('Bearer '+ api_key)}
img_data = read_image_from(IMAGEURL).read()
r = requests.post(scoring_url, files={'image':img_data}, headers=headers) # Run the request twice since the first time takes a 
                                                              # little longer due to the loading of the model
# %time r = requests.post(scoring_url, files={'image':img_data}, headers=headers)
r.json()
# -

# From the results above we can see that the model correctly classifies this as an Lynx. 

# Let's try a few more images.

images = ('https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Lynx_lynx_poing.jpg/220px-Lynx_lynx_poing.jpg',
          'https://upload.wikimedia.org/wikipedia/commons/3/3a/Roadster_2.5_windmills_trimmed.jpg',
          'http://www.worldshipsociety.org/wp-content/themes/construct/lib/scripts/timthumb/thumb.php?src=http://www.worldshipsociety.org/wp-content/uploads/2013/04/stock-photo-5495905-cruise-ship.jpg&w=570&h=370&zc=1&q=100',
          'http://yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-FwsgxpiZv_E9ZfPsNV5B0ER8-bOdruvNfMD5EbP4SznWz4PYn/',
          'https://cdn.arstechnica.net/wp-content/uploads/2012/04/bohol_tarsier_wiki-4f88309-intro.jpg',
          'http://i.telegraph.co.uk/multimedia/archive/03233/BIRDS-ROBIN_3233998b.jpg')


results = [requests.post(scoring_url, files={'image': read_image_from(img).read()}, headers=headers) for img in images]

plot_predictions(images, results)

# The labels predicted by our model seem to be consistent with the images supplied.

# Next let's quickly check what the request response performance is for the deployed model on AKS cluster.

image_data = list(map(lambda img: read_image_from(img).read(), images)) # Retrieve the images and data

timer_results = list()
for img in image_data:
    res=%timeit -r 1 -o -q requests.post(scoring_url, files={'image': img}, headers=headers)
    timer_results.append(res.best)

timer_results

print('Average time taken: {0:4.2f} ms'.format(10**3 * np.mean(timer_results)))

# We have tested that the model works and we can now move on to the [next notebook to get a sense of its throughput](06_SpeedTestWebApp.ipynb).
