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

# # Build Image
#
# In this notebook, we show the following steps for deploying a web service using AML:
#
# - Create an image
# - Test image locally
#

# +
import docker
import matplotlib.pyplot as plt
import numpy as np
import requests
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azureml._model_management._util import (get_docker_client, pull_docker_image)
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.image import ContainerImage
from dotenv import get_key, find_dotenv
from testing_utilities import to_img, plot_predictions, get_auth, wait_until_ready

# -

env_path = find_dotenv(raise_error_if_not_found=True)

resource_group = get_key(env_path, 'resource_group')
model_name = 'resnet_model'
image_name = get_key(env_path, 'image_name')

# ## Get workspace
# Load existing workspace from the config file info.

# +
from azureml.core.workspace import Workspace

ws = Workspace.from_config(auth=get_auth())
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep = '\n')
# -

# ## Create Image

# +
# create yml file to be used in the image
conda_pack = ["tensorflow-gpu==1.10.0"]
requirements = ["keras==2.2.0","Pillow==5.2.0", "azureml-defaults", "toolz"]

imgenv = CondaDependencies.create(conda_packages=conda_pack,pip_packages=requirements)
with open("img_env.yml", "w") as f:
    f.write(imgenv.serialize_to_string())

# +

image_config = ContainerImage.image_configuration(execution_script = "driver.py",
                                                  runtime = "python",
                                                  conda_file = "img_env.yml",
                                                  description = "Image for AKS Deployment Tutorial",
                                                  tags = {"name":"AKS","project":"AML"}, 
                                                  dependencies = ["resnet152.py"],
                                                  enable_gpu = True
                                                 )



# +
# create image. It may take upto 15-20 minutes. 
image = ContainerImage.create(name = image_name,
                              # this is the model object
                              models = [ws.models[model_name]],                              
                              image_config = image_config,
                              workspace = ws)

image.wait_for_creation(show_output = True)

# +
# You can find the logs of image creation
# image.image_build_log_uri

# You can get the image object when not creating a new image
# image = ws.images['image1']
# -

# ## Test image locally
# - Pull the image from ACR registry to local host 
# - Start a container
# - Test API call

# +
# Getting your container details
container_reg = ws.get_details()["containerRegistry"]
reg_name=container_reg.split("/")[-1]
container_url = "\"" + image.image_location + "\","
subscription_id = ws.subscription_id

client = ContainerRegistryManagementClient(ws._auth,subscription_id)
result= client.registries.list_credentials(resource_group, reg_name, custom_headers=None, raw=False)
username = result.username
password = result.passwords[0].value
print('ContainerURL:{}'.format(image.image_location))
print('Servername: {}'.format(reg_name))
print('Username: {}'.format(username))
print('Password: {}'.format(password))
# -

dc = get_docker_client(username, 
                       password, 
                       image.image_location.split("/")[0])

pull_docker_image(dc, image.image_location, username, password)

# make sure port 80 is not occupied
container_labels = {'containerName': 'kerasgpu'}
container = dc.containers.run(image.image_location, 
                                         detach=True, 
                                         ports={'5001/tcp': 80},
                                         labels=container_labels,
                                         runtime='nvidia' )

for log_msg in container.logs(stream=True):
    str_msg = log_msg.decode('UTF8')
    print(str_msg)
    if "Model loading time:" in str_msg:
        print('Model loaded and container ready')
        break

client = docker.APIClient()
details = client.inspect_container(container.id)

service_ip = details['NetworkSettings']['Ports']['5001/tcp'][0]['HostIp']
service_port = details['NetworkSettings']['Ports']['5001/tcp'][0]['HostPort']

# Wait a few seconds for the application to spin up and then check that everything works.

print('Checking service on {} port {}'.format(service_ip, service_port))

# +
endpoint="http://__service_ip:__service_port"
endpoint = endpoint.replace('__service_ip', service_ip)
endpoint = endpoint.replace('__service_port', service_port)

max_attempts = 50
output_str = wait_until_ready(endpoint, max_attempts)
print(output_str)
# -

# !curl 'http://{service_ip}:{service_port}/'

IMAGEURL = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Lynx_lynx_poing.jpg/220px-Lynx_lynx_poing.jpg"

plt.imshow(to_img(IMAGEURL))

with open('220px-Lynx_lynx_poing.jpg', 'rb') as f:
    img_data = f.read()

# %time r = requests.post('http://0.0.0.0:80/score', files={'image': img_data})
print(r)
r.json()

images = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Lynx_lynx_poing.jpg/220px-Lynx_lynx_poing.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/3/3a/Roadster_2.5_windmills_trimmed.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Harmony_of_the_Seas_%28ship%2C_2016%29_001.jpg/1920px-Harmony_of_the_Seas_%28ship%2C_2016%29_001.jpg",
    "http://yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-FwsgxpiZv_E9ZfPsNV5B0ER8-bOdruvNfMD5EbP4SznWz4PYn/",
    "https://cdn.arstechnica.net/wp-content/uploads/2012/04/bohol_tarsier_wiki-4f88309-intro.jpg",
    "http://i.telegraph.co.uk/multimedia/archive/03233/BIRDS-ROBIN_3233998b.jpg",
)

from testing_utilities import read_image_from

url = "http://0.0.0.0:80/score"
results = [
    requests.post(url, files={'image': read_image_from(img).read()}) for img in images
]

plot_predictions(images, results)

image_data = list(map(lambda img: read_image_from(img).read(), images)) # Retrieve the images and data

timer_results = list()
for img in image_data:
    res=%timeit -r 1 -o -q requests.post(url, files={'image': img})
    timer_results.append(res.best)

timer_results

print("Average time taken: {0:4.2f} ms".format(10 ** 3 * np.mean(timer_results)))

container.stop()

# remove stopped container
# !docker system prune -f

# We can now move on to [Create kubenetes cluster and deploy web service](04_DeployOnAKS.ipynb) with the image we just built.
