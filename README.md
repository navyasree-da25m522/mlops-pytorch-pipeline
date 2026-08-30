# MLOPS Assignment 3 – PyTorch MLOps Pipeline

**Name:** Navya Sree
**Roll Number:** DA25M522
---

## 1. Project Overview

End-to-end CIFAR-10 image classification pipeline using:

- PyTorch and ResNet18
- Docker
- Kubernetes
- FastAPI
- Git and GitHub

The model is trained for **10 epochs** with early stopping configured.

---


## 2. Architecture

```text
                    CIFAR-10 Dataset
                           |
                           v
                   PyTorch Training
                           |
                           v
                       ResNet18
                           |
                           v
                   classifier_v1.pt
                           |
                           v
              Model Checkpoint PVC
                           |
                           v
              Model Serving Deployment
                    (2 Replicas)
                           |
                           v
                    FastAPI Server
                  /health    /predict
                           |
                           v
                  ClusterIP Service
                     Port 80 -> 8080
                           |
                           v
                        Client

Kubernetes components:
    ConfigMap -> Training configuration
    Data PVC -> CIFAR-10 dataset
    Checkpoint PVC -> Trained model
    Training Job -> Model training
    Deployment -> Model serving
    Service -> Internal API access
    HPA -> 2 to 4 replicas, 60% CPU target
---
## 3. Project Structure
mlops-pytorch-pipeline/
│
├── data/
├── checkpoints/
│
├── docker/
│   ├── Dockerfile.train
│   └── Dockerfile.serve
│
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── persistent-volumes.yaml
│   ├── training-job.yaml
│   ├── serving-deployment.yaml
│   ├── serving-service.yaml
│   └── hpa.yaml
│
├── requirements/
│   ├── train.txt
│   └── serve.txt
│
├── src/
│   ├── dataset.py
│   ├── model.py
│   ├── train.py
│   └── serve.py
│
└── README.md
---
##4. Model Configuration

Dataset:	CIFAR-10
Architecture:	ResNet18
Classes:	10
Epochs:	10
Batch size:	64
Learning rate:	0.001
Early stopping patience:3
Model: classifier_v1.pt

##5. Kubernetes Setup
Namespace
ml-training
Persistent Storage
PVC	Purpose
cifar10-data-pvc	CIFAR-10 dataset
model-checkpoints-pvc	Model checkpoint
Training
Kubernetes Job
Training Docker image
ConfigMap mounted at /app/configs
Dataset mounted at /app/data
Checkpoints mounted at /app/checkpoints
CPU request/limit: 2 cores
Memory request: 2Gi
Memory limit: 4Gi
Serving
Deployment: model-serving
Replicas: 2
Container port: 8080
Service type: ClusterIP
Service port: 80
Target port: 8080
Autoscaling
HPA: model-serving-hpa
Minimum replicas: 2
Maximum replicas: 4
CPU target: 60%
---
##6. Kubernetes Setup Instructions

1. Create Namespace: kubectl apply -f k8s/namespace.yaml
2. Create ConfigMap: kubectl apply -f k8s/configmap.yaml
3. Create Persistent Storage: kubectl apply -f k8s/persistent-volumes.yaml
4. Start Training: kubectl apply -f k8s/training-job.yaml

---

##7. Deploy Model Serving
kubectl apply -f k8s/serving-deployment.yaml
kubectl apply -f k8s/serving-service.yaml
kubectl apply -f k8s/hpa.yaml
---
##8. Verify Deployment
kubectl get pods -n ml-training
kubectl describe deployment model-serving -n ml-training
---
##9. Verify Service
kubectl get service,endpoints -n ml-training
---
##10. Verify HPA
kubectl get hpa -n ml-training
---
##11. API Testing
Port Forward: kubectl port-forward svc/model-serving 8080:80 -n ml-training
Health Check: curl http://localhost:8080/health

---
##12. API Endpoints
Method	   Endpoint	     Purpose
GET	        /health	     Health check
POST	    /predict	 CIFAR-10 image prediction

---
##13. Technologies
Python
PyTorch
ResNet18
CIFAR-10
FastAPI
Uvicorn
Docker
Kubernetes
ConfigMap
PersistentVolumeClaim
Job
Deployment
ClusterIP Service
Horizontal Pod Autoscaler
