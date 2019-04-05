### Authors: Yan Zhang, Mathew Salvaris, and Fidan Boylu Uz
[![Build Status](https://dev.azure.com/customai/AKSDeploymentTutorialAML/_apis/build/status/Microsoft.AKSDeploymentTutorialAML?branchName=master)](https://dev.azure.com/customai/AKSDeploymentTutorialAML/_build/latest?definitionId=11&branchName=master)
# Deploy Deep Learning CNN using Azure Machine Learning
## Overview
In this repository there are a number of tutorials in Jupyter notebooks that have step-by-step instructions on how to deploy a pretrained deep learning model on a GPU enabled Kubernetes cluster throught Azure Machine Learning (AML). The tutorials cover how to deploy models from the following deep learning frameworks on specific deployment target:

* Keras (TensorFlow backend)
  - [Azure Kubernetes Service (AKS) Cluster with GPUs](./{{cookiecutter.project_name}}/Keras_Tensorflow/aks)
  - [Azure IoT Edge](./{{cookiecutter.project_name}}/Keras_Tensorflow/iotedge)
* [Pytorch](./{{cookiecutter.project_name}}/Pytorch) (coming soon)

![alt text](static/example.png "Example Classification")
 
 For each framework, we go through the following steps:
 * Create an AML Workspace
 * Model development where we load the pretrained model and test it by using it to score images
 * Develop the API that will call our model 
 * Building the Docker Image with our REST API and model and testing the image
 * AKS option
     * Creating our Kubernetes cluster and deploying our application to it
     * Testing the deployed model
     * Testing the throughput of our model
     * Cleaning up resources
 * IOT Edge option
     * Creating IoT hub and IoT Edge device identity, configuring the phisical IOT Edge device, and deploying our application to it
     * Cleaning up resources
 
## Design

The application we will develop is a simple image classification service, where we will submit an image and get back what class the image belongs to. The application flow for the deep learning model is as follows:
1)	Deep learning model is registered to AML model registry.
2)	AML creates a docker image including the model and scoring script.
3)	AML deploys the scoring image on the chosen deployment compute target (AKS or IoT Edge) as a web service.
4)	The client sends a HTTP POST request with the encoded image data.
5)	The web service created by AML preprocesses the image data and sends it to the model for scoring.
6)	The predicted categories with their scores are then returned to the client.


**NOTE**: The tutorial goes through step by step how to deploy a deep learning model on Azure; it **does** **not** include enterprise best practices such as securing the endpoints and setting up remote logging etc. 

**Deploying with GPUS:** For a detailed comparison of the deployments of various deep learning models, see the blog post [here](https://azure.microsoft.com/en-us/blog/gpus-vs-cpus-for-deployment-of-deep-learning-models/) which provides evidence that, at least in the scenarios tested, GPUs provide better throughput and stability at a lower cost.



# Getting Started
This repository is arranged as submodules and threfore you can either pull all the tutorials or simply the ones you want.

To get started with the tutorial, please proceed with following steps **in sequential order**.

 * [Prerequisites](#prerequisites)
 * [Setup](#setup)
 * [Steps](#steps)
 * [Cleaning up](#cleanup)

<a id='prerequisites'></a>
## Prerequisites
1. Linux (Ubuntu) with GPU enabled.
2. [Anaconda Python](https://www.anaconda.com/download)
3. [Docker](https://docs.docker.com/v17.12/install/linux/docker-ee/ubuntu) installed.
4. [Azure account](https://azure.microsoft.com).

The tutorial was developed on an [Azure Ubuntu
DSVM](https://docs.microsoft.com/en-us/azure/machine-learning/data-science-virtual-machine/dsvm-ubuntu-intro),
which addresses the first three prerequisites.

<a id='setup'></a>
## Setup
To set up your environment to run these notebooks, please follow these steps.  They setup the notebooks to use Docker and Azure seamlessly.
1. Create a _Linux_ Ubuntu DSVM (NC6 or above to use GPU).

2. Install [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html), a tool creates projects from project templates.
```bash
pip install cookiecutter
```

3. Clone and choose a specific framework and deployment option for this repository. You will obtain a repository tailored to your choice of framework and deployment compute target.
   ```bash
   cookiecutter https://github.com/Microsoft/AKSDeploymentTutorialAML.git --checkout yzhang_cc
   ```
4. Add your user to the docker group (after executing this command, exit and start a new bash shell): 
   ```bash
   sudo usermod -aG docker $USER
   ```
   To verify whether you have correct configuration, try executing `docker ps` command. You should not get `permission denied` errors.

5. Navigate to the framework directory (either Keras_Tensorflow or Pytorch based on your selection)

6. Create the Python virtual environment using the environment.yml:
   ```bash
   conda env create -f environment.yml
   ```
7. Activate the virtual environment:
   ```bash
   source activate deployment_aml
   ```
8. Login to Azure:
   ```bash
   az login
   ```
9. If you have more than one Azure subscription, select it:
   ```bash
   az account set --subscription <Your Azure Subscription>
   ```
10. Start the Jupyter notebook server in the virtual environment:
   ``` bash
   jupyter notebook
   ```
11. Select correct kernel: set the kernel to be `Python [conda env: deployment_aml]`(or `Python 3` if that option does not show).

<a id='steps'></a>

## Steps
After following the setup instructions above, run the Jupyter notebooks in order starting with the first notebook `00_AMLSetup.ipynb`.

<a id='cleanup'></a>
## Cleaning up
To remove the conda environment created see [here](https://conda.io/projects/continuumio-conda/en/latest/commands/remove.html). The last Jupyter notebook in each framework directory  also gives details on deleting Azure resources associated with this repository.




# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

