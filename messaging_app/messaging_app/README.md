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