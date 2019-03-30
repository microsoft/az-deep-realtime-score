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

# # Deploying a web service to Azure Kubernetes Service (AKS)
#
# In this notebook, we show the following steps for deploying a web service using AML:
#
# - Provision an AKS cluster (one time action)
# - Deploy the service
# - Test the web service

import json
import subprocess

import azureml.core

# +
import matplotlib.pyplot as plt
import requests
from azureml.core.compute import AksCompute, ComputeTarget
from azureml.core.webservice import Webservice, AksWebservice
from dotenv import get_key, find_dotenv
from testing_utilities import read_image_from
from testing_utilities import to_img, get_auth

print(azureml.core.VERSION)
# -

env_path = find_dotenv(raise_error_if_not_found=True)

aks_service_name = get_key(env_path, "aks_service_name")
aks_name = get_key(env_path, "aks_name")

# <a id='get_workspace'></a>
# ## Get workspace
# Load existing workspace from the config file info.

# +
from azureml.core.workspace import Workspace

ws = Workspace.from_config(auth=get_auth())
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep="\n")
# -

# <a id='provision_cluster'></a>
# ## Provision the AKS Cluster¶
# This is a one time setup. You can reuse this cluster for multiple deployments after it has been created. If you delete the cluster or the resource group that contains it, then you would have to recreate it. Let's first check if there are enough cores in the subscription for the cluster.

vm_dict = {"NC": {"size": "Standard_NC6", "cores": 6}}

vm_family = "NC"
node_count = 3  # We need to have a minimum of 3 nodes
requested_cores = node_count * vm_dict[vm_family]["cores"]

results = subprocess.run(
    [
        "az",
        "vm",
        "list-usage",
        "--location",
        get_key(env_path, "aks_location"),
        "--query",
        "[?contains(localName, '%s')].{max:limit, current:currentValue}" % (vm_family),
    ],
    stdout=subprocess.PIPE,
)
quota = json.loads("".join(results.stdout.decode("utf-8")))
diff = int(quota[0]["max"]) - int(quota[0]["current"])

if diff <= requested_cores:
    print(
        "Not enough cores of NC6 in region, asking for {} but have {}".format(
            requested_cores, diff
        )
    )
    raise Exception("Core Limit", "Note enough cores to satisfy request")
print("There are enough cores, you may continue...")

# +
# Provision AKS cluster with GPU machine
prov_config = AksCompute.provisioning_configuration(vm_size="Standard_NC6")

# Create the cluster
aks_target = ComputeTarget.create(
    workspace=ws, name=aks_name, provisioning_configuration=prov_config
)

# -

# %%time
aks_target.wait_for_completion(show_output=True)
print(aks_target.provisioning_state)
print(aks_target.provisioning_errors)

# Optional step: Attach existing AKS cluster
#
# Modify and use below scripts if you have an existing cluster and want to use it as the aks_target. Note that you need to find out the ``cluster_name`` from Azure portal.

# +
# Attach an existing AKS cluster

# attach_config = AksCompute.attach_configuration(resource_group=ws.resource_group,
#                                                cluster_name='deployaks')
# aks_target = ComputeTarget.attach(ws, aks_name, attach_config)
# aks_target.wait_for_completion(True)

# +
# Execute following commands if you want to delete an AKS cluster
# aks_target = AksCompute(name=aks_name,workspace=ws)
# aks_target.delete()
# -

# <a id='deploy_ws'></a>
# ## Deploy web service to AKS¶

# Deploy web service to AKS
# Set the web service configuration (using customized configuration)
aks_config = AksWebservice.deploy_configuration(autoscale_enabled=False, num_replicas=1)

# get the image built in previous notebook
image_name = get_key(env_path, "image_name")
image = ws.images[image_name]

aks_service_name

aks_service = Webservice.deploy_from_image(
    workspace=ws,
    name=aks_service_name,
    image=image,
    deployment_config=aks_config,
    deployment_target=aks_target,
)

# %%time
aks_service.wait_for_deployment(show_output=True)
print(aks_service.state)

# +
### debug
# aks_service.error
# aks_service.get_logs()

# Excute following commands if you want to delete a web service
# s =  Webservice(ws, aks_service_name)
# s.delete()
# -

# <a id='test_ws'></a>
# ## Test Web Service¶
# We test the web sevice by passing data.

IMAGEURL = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Lynx_lynx_poing.jpg/220px-Lynx_lynx_poing.jpg"
plt.imshow(to_img(IMAGEURL))

service_keys = aks_service.get_keys()
headers = {}
headers["Authorization"] = "Bearer " + service_keys[0]

resp = requests.post(
    aks_service.scoring_uri,
    headers=headers,
    files={"image": read_image_from(IMAGEURL).read()},
)

print(resp.json())

# Having deplied web service succesfully, we can now move on to [Test Web app](05_TestWebApp.ipynb).
