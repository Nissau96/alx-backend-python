# Basics of Container Orchestration with Kubernetes 🚀

This project serves as a hands-on guide to understanding the fundamentals of container orchestration using Kubernetes. It covers setting up a local cluster, deploying applications, and managing Kubernetes resources according to modern DevOps best practices.

## Project Structure

- **/messaging_app**: Contains all the scripts and Kubernetes configuration files (YAML) for the project.
  - `kurbeScript`: A shell script to initialize and verify the local Minikube cluster.

## Getting Started

### Prerequisites

- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- A container or virtual machine manager, such as [Docker](https://docs.docker.com/engine/install/).

### Task 0: Setting Up the Local Cluster

To start and verify your local Kubernetes cluster, run the setup script:

```sh
# Make the script executable (only need to do this once)
chmod +x messaging_app/kurbeScript

# Run the script
./messaging_app/kurbeScript
```

## Task 1: Deploying the Application

This section describes how to deploy the containerized Django application to the Kubernetes cluster.

### 1. Load the Docker Image
Before deploying, you must load your locally built Docker image into the Minikube cluster's internal registry.

```bash
minikube image load messaging_app-web
```

### 2. Apply the Configuration
Deploy the application using the `deployment.yaml` file. This will create the Deployment and Service objects in Kubernetes.

```bash
kubectl apply -f messaging_app/deployment.yaml
```

### 3. Verify the Deployment
Check that the application Pods are running correctly.

```bash
# List the running pods
kubectl get pods

# Check the logs of one of the pods to ensure the app started
# (replace <pod-name> with a real pod name from the command above)
kubectl logs <pod-name>
```
---

## Task 2: Scaling the Application

This task demonstrates how to scale the application and perform a simple load test to observe its behavior under load.

### Prerequisites
You must install the `wrk` HTTP benchmarking tool.
- **On Debian/Ubuntu:** `sudo apt-get update && sudo apt-get install wrk`
- **On macOS (with Homebrew):** `brew install wrk`

### Running the Script
The `kubctl-0x01` script automates the entire process. It will:
1.  Enable the Kubernetes Metrics Server.
2.  Scale the deployment to 3 replicas.
3.  Run a 30-second load test.
4.  Display the resource usage of the pods and node.

```bash
# Make the script executable (only need to do this once)
chmod +x messaging_app/kubctl-0x01

# Run the script
./messaging_app/kubctl-0x01
```

---

## Task 3: Exposing the Application with Ingress

This task explains how to expose the application to external traffic using a Kubernetes Ingress.

### 1. Enable the Ingress Addon
First, enable the Nginx Ingress controller addon in your Minikube cluster. This only needs to be done once.

```bash
minikube addons enable ingress
```
### 2. Apply the Ingress Configuration
Apply the `ingress.yaml` file to create the routing rules.

```bash
kubectl apply -f messaging_app/ingress.yaml
```

### 3. Access the Application
Find your cluster's IP address and construct the URL to access your application.

```bash
# 1. Get the cluster IP address
minikube ip

# 2. Use the output from the above command to build your URL.
#    Open this URL in your web browser:
#    http://<YOUR-MINIKUBE-IP>/messaging
```

---

## Task 4: Blue-Green Deployment for Zero Downtime

This task implements a blue-green deployment strategy. This allows you to deploy a new version of the application without any user-facing downtime by switching traffic instantly after the new version is confirmed to be healthy.

### Running the Orchestration Script

The `kubctl-0x02` script automates the entire process. Before running, ensure the old service is deleted with `kubectl delete service messaging-app-service`.

```bash
# Make the script executable (only need to do this once)
chmod +x messaging_app/kubctl-0x02

# Run the script
./messaging_app/kubctl-0x02
```
