# Deploy Deep Learning CNN on Kubernetes Cluster with GPUs - Keras


## Prerequisites
1. Linux(Ubuntu) with GPU enabled.
2. [Anaconda Python](https://www.anaconda.com/download)
3. [Docker](https://docs.docker.com/v17.12/install/linux/docker-ee/ubuntu) installed.
4. [Azure account](https://azure.microsoft.com).

The tutorial was developed on an [Azure Ubuntu
DSVM](https://docs.microsoft.com/en-us/azure/machine-learning/data-science-virtual-machine/dsvm-ubuntu-intro),
which addresses the first three prerequisites.

## Setup
To set up your environment to run these notebooks, please follow these steps.  They setup the notebooks to use Docker and Azure seamlessly.
1. Create a _Linux_ DSVM (NC6 or above to use GPU).
2. Clone, fork, or download the zip file for this repository:
   ```
   git clone https://github.com/Microsoft/AKSDeploymentTutorial_AML.git
   ```
3. Add your user to the docker group: 
   ```
   sudo usermod -aG docker $USER
   ```
4. Navigate to _./AKSDeploymentTutorial\_AML/Keras\_Tensorflow_ directory

5. Create the Python virtual environment using the tutorial_env.yml:
   ```
   conda env create -f tutorial_env.yml
   ```
6. Activate the virtual environment:
   ```
   source activate tutorial_env
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
After following the setup instructions above, run the Jupyter notebooks in order starting with the first notebook.

## Cleaning up
To remove the conda environment created see [here](https://conda.io/docs/commands/env/conda-env-remove.html). The last Jupyter notebook also gives details on deleting Azure resources associated with this repository.

# Contributing
This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repositories using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
