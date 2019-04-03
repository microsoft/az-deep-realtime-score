# Deploy Deep Learning CNN on IoT Edge - Keras

With the completion of the previous task, we introduce how to deploy an ML module through [Azure IoT Edge](https://docs.microsoft.com/en-us/azure/iot-edge/how-iot-edge-works). 

Azure IoT Edge is an Internet of Things (IoT) service that builds on top of Azure IoT Hub. It is a hybrid solution combining the benefits of the two scenarios: *IoT in the Cloud* and *IoT on the Edge*. This service is meant for customers who want to analyze data on devices, a.k.a. "at the edge", instead of in the cloud. By moving parts of your workload to the edge, your devices can spend less time sending messages to the cloud and react more quickly to changes in status. On the other hand, Azure IoT Hub provides centralized way to manage Azure IoT Edge devices, and make it easy to train ML models in the Cloud and deploy the trained models on the Edge devices.  

In this example, we deploy a trained Keras (tensorflow) CNN model to the edge device. When the image data is generated from a process pipeline and fed into the edge device, the deployed model can make predictions right on the edge device without accessing to the cloud. Following diagram shows the major components of an Azure IoT edge device. Source code and full documentation are linked below.

<p align="center">
<img src="azureiotedgeruntime.png" alt="logo" width="90%"/>
</p>

We perform following steps for the deployment.

- Step 1: Build the trained ML model into docker image. This image will be used to create a docker container running on the edge device. 
- Step 2: Provision and Configure IoT Edge Device
- Step 3: Deploy ML Module on IoT Edge Device
- Step 4: Test ML Module

<a id='prerequisites'></a>
## Prerequisites
Please follow instructions described in the repo README page. 

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
