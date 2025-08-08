# Django Messaging App (Containerized)

This project is a robust, containerized Django-based messaging application. It leverages Docker to ensure a consistent development, testing, and production environment.

## Project Overview

This application provides API endpoints for a simple messaging system. It is built with Django and Django REST Framework. The entire application is containerized with Docker, making it easy to set up and run on any machine with Docker installed.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

* [Docker](https://docs.docker.com/get-docker/)
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

---

## Getting Started

Follow these instructions to get the application up and running on your local machine.

### 1. Clone the Repository

First, clone the project repository to your local machine.

```bash
git clone <your-repository-url>
cd messaging_app
```

### 2. Build the Docker Image

Build the Docker image using the provided `Dockerfile`. This command packages the application and all its dependencies into a single image named `messaging-app`.

```bash
docker build -t messaging-app .
```

### 3. Run the Docker Container

Once the image is built, you can run it as a container. This will start the Django development server inside the container.

```bash
docker run -p 8000:8000 messaging-app
```

**Explanation:**
* `-p 8000:8000`: This maps port 8000 on your local machine to port 8000 inside the container.

### 4. Access the Application

With the container running, you can access the application by navigating to the following URL in your web browser:

[http://localhost:8000](http://localhost:8000)

---

## Project Structure

```
messaging_app/
├── messaging_app/     
├── messaging_app/     # Django project settings
├── manage.py          # Django's command-line utility
├── requirements.txt   # Python package dependencies
├── Dockerfile         # Recipe for building the Docker image
└── README.md          # This file
```