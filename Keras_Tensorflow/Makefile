.ONESHELL:
SHELL=/bin/bash

define PROJECT_HELP_MSG
Makefile for testing notebooks
Make sure you have edited the dev_env_template files and renamed it to .dev_env
All the variables loaded in this makefile must come from the .dev_env file

Usage:
	make test					run all notebooks
	make clean					delete env and remove files
endef
export PROJECT_HELP_MSG


include .dev_env


help:
	echo "$$PROJECT_HELP_MSG" | less


test: setup test-notebook1 test-notebook2 test-notebook3 test-notebook4 test-notebook5 test-notebook6 test-notebook7 \
	test-notebook8
	@echo All Notebooks Passed

setup:
	conda env create -f environment.yml
ifndef TENANT_ID
	@echo starting interactive login
	az login -o table
else
	@echo using service principal login
	az login -t ${TENANT_ID} --service-principal -u ${SP_USERNAME} --password ${SP_PASSWORD}
endif


test-notebook1:
	source activate aks_deployment_aml
	@echo Testing 00_AMLSetup.ipynb
	papermill 00_AMLSetup.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3 \
		-p subscription_id ${SUBSCRIPTION_ID} \
		-p resource_group ${RESOURCE_GROUP} \
		-p workspace_name ${WORKSPACE_NAME} \
		-p workspace_region ${WORKSPACE_REGION} \
		-p image_name ${IMAGE_NAME} \
		-p aks_name ${AKS_NAME} \
		-p aks_location ${WORKSPACE_REGION} \
		-p aks_service_name ${AKS_SERVICE_NAME}

test-notebook2:
	source activate aks_deployment_aml
	@echo Testing 01_DevelopModel.ipynb
	papermill 01_DevelopModel.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3

test-notebook3:
	source activate aks_deployment_aml
	@echo Testing 02_DevelopModelDriver.ipynb
	papermill 02_DevelopModelDriver.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3

test-notebook4:
	source activate aks_deployment_aml
	@echo Testing 03_BuildImage.ipynb
	papermill 03_BuildImage.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3

test-notebook5:
	source activate aks_deployment_aml
	@echo Testing 04_DeployOnAKS.ipynb
	papermill 04_DeployOnAKS.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3

test-notebook6:
	source activate aks_deployment_aml
	@echo Testing 05_TestWebApp.ipynb
	papermill 05_TestWebApp.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3

test-notebook7:
	source activate aks_deployment_aml
	@echo Testing 06_SpeedTestWebApp.ipynb
	papermill 06_SpeedTestWebApp.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3

test-notebook8:
	source activate aks_deployment_aml
	@echo Testing 07_TearDown.ipynb
	papermill 07_TearDown.ipynb test.ipynb \
		--log-output \
		--no-progress-bar \
		-k python3

remove-notebook:
	rm -f test.ipynb

clean: remove-notebook
	conda remove --name aks_deployment_aml -y --all
	rm -rf aml_config
	rm -rf __pycache__
	rm -rf .ipynb_checkpoints
	rm *.jpg
	rm -rf azureml-models
	rm driver.py img_env.yml model_resnet_weights.h5

notebook:
	source activate aks_deployment_aml
	jupyter notebook --port 9999 --ip 0.0.0.0 --no-browser

install-jupytext:
	source activate aks_deployment_aml
	conda install -c conda-forge jupytext

convert-to-py:
	jupytext --set-formats ipynb,py_scripts//py --sync *.ipynb

sync:
	jupytext --sync *.ipynb

convert-to-ipynb:
	jupytext --set-formats ipynb *.ipynb

remove-py:
	rm -r py_scripts

.PHONY: help test setup clean remove-notebook test-notebook1 test-notebook2 test-notebook3 test-notebook4 \
		test-notebook5 test-notebook6 test-notebook7 test-notebook8