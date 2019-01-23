### Authors: Yan Zhang, Mathew Salvaris, and Fidan Boylu Uz

# Deploy Deep Learning CNN on Kubernetes Cluster with GPUs - AML version
## Overview
In this repository there are a number of tutorials in Jupyter notebooks that have step-by-step instructions on how to deploy a pretrained deep learning model on a GPU enabled Kubernetes cluster throught Azure Machine Learning (AML). The tutorials cover how to deploy models from the following deep learning frameworks:

* [Keras (TensorFlow backend)](Keras_Tensorflow)
* [Pytorch](Pytorch)

![alt text](static/example.png "Example Classification")
 
 For each framework, we go through the following steps:
 * Create an AML Workspace
 * Model development where we load the pretrained model and test it by using it to score images
 * Develop the API that will call our model 
 * Building the Docker Image with our REST API and model and testing the image
 * Creating our Kubernetes cluster and deploying our application to it
 * Testing the deployed model
 * Testing the throughput of our model
 * Cleaning up resources
 
## Design
![alt text](static/Design.png "Design")

### Below content need to be modified after adding the architecture diagram.
The application we will develop is a simple image classification service, where we will submit an image and get back what class the image belongs to. The application flow for the deep learning model is as follows:
1)	The client sends a HTTP POST request with the encoded image data.
2)	The Flask app extracts the image from the request.
3)	The image is then appropriately preprocessed and sent to the model for scoring.
4)	The scoring result is then piped into a JSON object and returned to the client.

If you already have a Docker image that you would like to deploy you can skip the first four notebooks.

**NOTE**: The tutorial goes through step by step how to deploy a deep learning model on Azure; it **does** **not** include enterprise best practices such as securing the endpoints and setting up remote logging etc. 

**Deploying with GPUS:** For a detailed comparison of the deployments of various deep learning models, see the blog post [here](https://azure.microsoft.com/en-us/blog/gpus-vs-cpus-for-deployment-of-deep-learning-models/) which provides evidence that, at least in the scenarios tested, GPUs provide better throughput and stability at a lower cost.



## Setup
Please find out the Prerequisites and Setup procedures for different networks:

* [Keras (TensorFlow backend)](Keras_Tensorflow)
* [Pytorch](Pytorch)



# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

