![Build Status](https://dev.azure.com/customai/HyperdriveDeepLearning/_apis/build/status/microsoft.HyperdriveDeepLearning?branchName=master)

### Author: Fidan Boylu Uz

# Training of Python Deep Learning Models on Azure 

## Overview

This scenario shows how to tune an object detection Mask RCNN model that can be deployed as a web service to provide predictions for empty spaces on store shelves. For this scenario, "Input Data" in the architecture diagram refers to images of retailer store shelves filled with products and empty spaces to be predicted by the model. The scenario is designed for Pytorch's torchvision library but can be generalized to any scenario to tune the hyperparameters of the models that use pytorch deep learning libraries. 

## Design

![alt text](Design.png "Design")
The scenario uses a dataset which includes images of 4 and 8 ft retail store shelves filled with grocery products and bounding box annotations for empty spaces on the shelves in xml format (This dataset is distributed under the [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.) It tunes a torchvision Mask RCNN model to predict the bounding box coordinates and probabilities of empty spaces on the shelves. The application flow of this architecture is as follows:

1. Configure Azure Machine Learning (Azure ML) service.
2. Create an Azure ML Compute cluster.
3. Upload training and test data to Azure Storage.
4. Configure a HyperDrive random parameter search.
5. Submit the search and monitor until complete.
6. Retrieve the best set of hyperparameters.
7. Register the best model.

## Prerequisites

1. Linux (x64) with GPU enabled.
2. [Anaconda Python](https://www.anaconda.com/download) installed.
3. [Azure account](https://azure.microsoft.com).

The tutorial was developed on an NC series [Azure Ubuntu
DSVM](https://docs.microsoft.com/en-us/azure/machine-learning/data-science-virtual-machine/dsvm-ubuntu-intro),
which addresses the first three prerequisites.

## Setup

To set up your environment to run these notebooks, please follow these steps.  They setup the notebooks to use Azure seamlessly.

1. Create a _Linux_ _Ubuntu_ DSVM.
2. Add your user to the docker group:
    ```
    sudo usermod -aG docker $USER
    newgrp docker
    ```
2. Clone, fork, or download the zip file for this repository:
   ```
   git clone https://github.com/microsoft/HyperdriveDeepLearning.git
   ```
3. Enter the local repository:
   ```
   cd HyperdriveDeepLearning
   ```
4. Create the Python virtual environment using the environment.yml:
   ```
   conda env create -f environment.yml
   ```
5. Activate the TorchDetectAML virtual environment:
   ```
   conda activate TorchDetectAML
   ```
6. Clone COCO API under scripts folder and install:
    ```
    cd scripts
    git clone https://github.com/cocodataset/cocoapi.git
    cd cocoapi/PythonAPI
    make
    cd ../../..
    ```
   
7. Login to Azure:
   ```
   az login
   ```
8. If you have more than one Azure subscription, select it:
   ```
   az account set --subscription <Your Azure Subscription>
   ```
9. Start the Jupyter notebook server in the virtual environment:
   ```
   jupyter notebook
   ```

## Steps

After following the setup instructions above, run the Jupyter notebooks in order starting with [first notebook](https://github.com/Microsoft/MLHyperparameterTuning/blob/master/00_.ipynb).

## Cleaning up

The [last Jupyter notebook](05_Tear_Down.ipynb) describes how to delete the Azure resources created for running the tutorial. Consult the [conda documentation](https://docs.conda.io) for information on how to remove the conda environment created during the setup.

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Related projects

[Microsoft AI Github](https://github.com/microsoft/ai) Find other Best Practice projects, and Azure AI Designed patterns in our central repository. 
