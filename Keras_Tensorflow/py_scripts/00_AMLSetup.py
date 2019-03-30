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

# ## Installation and configuration¶
#
# This notebook configures the notebooks in this tutorial to connect to an Azure Machine Learning (AML) Workspace. You can use an existing workspace or create a new one.

import azureml.core
from azureml.core import Workspace
from dotenv import set_key, get_key, find_dotenv
from pathlib import Path
from testing_utilities import get_auth

# ## Prerequisites
#
#

# If you have already completed the prerequisites, you can execute following command to ensure you are using correct conda environment. The output of this command should contain "tutorial_env" in the path, e.g. `/anaconda/envs/tutorial_env/bin/python`

# The AML Python SDK is already installed. Let's check the AML SDK version.

print("SDK Version:", azureml.core.VERSION)

# ## Set up your Azure Machine Learning workspace

# To create or access an Azure ML Workspace, you will need the following information:
#
# * An Azure subscription id
# * A resource group name
# * A name for your workspace
# * A region for your workspace
#
# We also require you to provide variable names that will be used to create images, deployment computes, etc. in later notebooks.
#
# **Note**: As with other Azure services, there are limits on certain resources like cluster size associated with the Azure Machine Learning service. Please read [this article](https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-manage-quotas) on the default limits and how to request more quota.

# Replace the values in the following cell with your information. If you would like to use service principal authentication as described [here](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/manage-azureml-service/authentication-in-azureml/authentication-in-azure-ml.ipynb) make sure you provide the optional values as well.

# + {"tags": ["parameters"]}
# Azure resources
subscription_id = "<YOUR_SUBSCRIPTION_ID>"
resource_group = "<YOUR_RESOURCE_GROUP>"  # e.g. resource_group = 'myamlrg'
workspace_name = "<YOUR_WORKSPACE_NAME>"  # e.g. workspace_name = 'myamlworkspace'
workspace_region = "<YOUR_WORKSPACE_REGION>"  # e.g. workspace_region =  'eastus2'

# Docker image and Azure Kubernetes Service (AKS) Cluster - deployment compute
image_name = (
    "<YOUR_IMAGE_NAME>"
)  # e.g. image_name = "image1 (avoid underscore in names)"
aks_name = "<YOUR_AKS_NAME>"  # e.g. aks_name = "my-aks-gpu1"
aks_location = "<YOUR_AKS_LOCATION>"  # e.g. aks_location = "eastus"
aks_service_name = (
    "<YOUR_AKS_SERVICE_NAME>"
)  # e.g. aks_service_name ="my-aks-service-1"
# -

# Create and initialize a dotenv file for storing parameters used in multiple notebooks.

env_path = find_dotenv()
if env_path == "":
    Path(".env").touch()
    env_path = find_dotenv()

# +
set_key(env_path, "subscription_id", subscription_id)
set_key(env_path, "resource_group", resource_group)
set_key(env_path, "workspace_name", workspace_name)
set_key(env_path, "workspace_region", workspace_region)

set_key(env_path, "image_name", image_name)
set_key(env_path, "aks_name", aks_name)
set_key(env_path, "aks_location", aks_location)
set_key(env_path, "aks_service_name", aks_service_name)
# -

# ## Create the workspace
# This cell will create an AML workspace for you in a subscription, provided you have the correct permissions.
# This will fail when:
#
# 1. You do not have permission to create a workspace in the resource group
# 2. You do not have permission to create a resource group if it's non-existing.
# 3. You are not a subscription owner or contributor and no Azure ML workspaces have ever been created in this subscription
#
# If workspace creation fails, please work with your IT admin to provide you with the appropriate permissions or to provision the required resources. If this cell succeeds, you're done configuring AML!

# +
# import the Workspace class and check the azureml SDK version
# from azureml.core import Workspace

ws = Workspace.create(
    name=workspace_name,
    subscription_id=subscription_id,
    resource_group=resource_group,
    location=workspace_region,
    create_resource_group=True,
    auth=get_auth(),
    exist_ok=True,
)
# persist the subscription id, resource group name, and workspace name in aml_config/config.json.
ws.write_config()
# -

# Below we will reload it just to make sure that everything is working.

# load workspace configuratio from ./aml_config/config.json file.
ws = Workspace.from_config(auth=get_auth())
ws.get_details()

# In this notebook, we created a ".env" file to save and reuse the variables needed cross all the notebooks. We also created a new Azure resource group with name <YOUR\_RESOURCE\_GROUP>, where an AML workspace and a few other Azure resources are created. We can now move on to the next notebook [developing the model](01_DevelopModel.ipynb).
