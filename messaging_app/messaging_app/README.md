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