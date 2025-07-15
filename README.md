# 🎵 MP3 Video Converter - Microservices Architecture with Kubernetes and RabbitMQ

This project is a complete video-to-audio (MP3) converter built using **microservices architecture** and deployed in a **Kubernetes** environment. It demonstrates the integration of several core technologies such as **RabbitMQ**, **MongoDB**, **MySQL**, and **Minikube**, focusing on service communication and asynchronous processing.

## 🚀 Overview

The application allows users to upload video files, which are then processed and converted into audio format. The process involves multiple microservices communicating through RabbitMQ, and the entire infrastructure is managed using Kubernetes.

Here's a high-level view of the flow:

1. A user uploads a video through the **Gateway Service**.
2. The **Auth Service** verifies the user's credentials using a **MySQL** database.
3. The **Gateway** saves the video to **MongoDB** using GridFS and sends a message to a RabbitMQ queue.
4. The **Converter Service** listens to this queue, retrieves the video, converts it to audio, saves it to MongoDB, and sends a new message indicating that the audio is ready.
5. The **Notification Service** listens for completed audio conversion messages and sends an email to the user with a download link.

## 🧩 Microservices

### 🌐 Gateway Service

- Acts as the main entry point of the system.
- Handles file uploads and user authentication.
- Interacts with the **Auth Service**, **MongoDB**, and **RabbitMQ**.
- Uses `ingress.yaml` to expose the `/upload` and `/download` routes via `mp3converter.com`.
- Authentication is required before allowing uploads.
- Stores uploaded videos in MongoDB (GridFS).
- Publishes messages to RabbitMQ for further processing.

> **Note:** The Ingress configuration requires local setup on Minikube and on your machine to map `mp3converter.com` correctly.

### 🔐 Auth Service

- Validates user credentials against a MySQL database.
- Exposed internally and only accessed by the Gateway.

### 🎧 Converter Service

- A lightweight, non-HTTP service.
- Listens for new video upload messages via RabbitMQ.
- Converts video files to MP3 audio using a media processing tool.
- Stores the audio files back in MongoDB.
- Sends a "conversion completed" message to a new RabbitMQ queue.

### 📬 Notification Service

- Listens for audio conversion messages.
- Sends a download link to the user's email.
- The link leads to the Gateway's `/download` endpoint.

## 📦 RabbitMQ

- Facilitates asynchronous communication between services.
- Managed via Kubernetes manifests only (no Dockerfile or installation script).
- Deployed as a **StatefulSet** for identity persistence.

> **Note:** RabbitMQ is configured purely via Kubernetes manifests in the `manifest/` directory.

## 🛠️ Technologies Used

- **Node.js / TypeScript**
- **MongoDB (GridFS)**
- **MySQL**
- **RabbitMQ**
- **Kubernetes (Minikube)**
- **Ingress Controller**
- **K9s** for cluster monitoring

## 📸 Screenshot

> _(Add a screenshot from K9s here showing the pods/services running)_

## 🧪 How to Run Locally

```bash
# Start Minikube
minikube start

# Enable Ingress
minikube addons enable ingress

# Apply Kubernetes manifests
kubectl apply -f manifest/

# Port-forward or access mp3converter.com locally
```
