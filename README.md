# Selenium Test on Kubernetes

## Overview
This repository contains Selenium tests running on a Kubernetes cluster managed by Amazon EKS. 

## How the Test Controller Pod Works
The Test Controller Pod collects test cases and sends them to the Chrome Node Pods for execution. It communicates with the Chrome Node Pods through the defined service endpoints.

## Deploying the System to Kubernetes
### Deploying on AWS EKS
1. Create an EKS cluster.
2. Configure kubectl.
3. Apply the YAML files to deploy resources:
   ```bash
   kubectl apply -f test-controller-service.yaml
   kubectl apply -f test-controller.yaml
   kubectl apply -f chrome-node.yaml
   kubectl apply -f chrome-node-service.yaml

## Docker Hub 
https://hub.docker.com/r/yagmurefe/test-insider

