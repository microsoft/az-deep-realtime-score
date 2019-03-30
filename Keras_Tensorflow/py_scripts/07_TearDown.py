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
#     display_name: Python [default]
#     language: python
#     name: python3
# ---

# # Tear it all down
# Once you are done with your cluster you can use the following two commands to destroy it all.

from azureml.core import Workspace
from azureml.core.compute import AksCompute, ComputeTarget
from dotenv import set_key, get_key, find_dotenv
from testing_utilities import get_auth

ws = Workspace.from_config(auth=get_auth())
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep="\n")

env_path = find_dotenv(raise_error_if_not_found=True)
resource_group = get_key(env_path, 'resource_group')
aks_name = get_key(env_path, 'aks_name')

# Once you are done with your cluster you can use the following command to delete the AKS cluster. This step may take a few minutes.

aks_target = AksCompute(name=aks_name,workspace=ws)
aks_aml_name = aks_target.cluster_resource_id.rsplit("/")[-1]

# !az aks delete -n $aks_aml_name -g $resource_group -y

# Finally, you should delete the resource group. This also deletes the AKS cluster and can be used instead of the above command if the resource group is only used for this purpose.

# !az group delete --name $resource_group -y
