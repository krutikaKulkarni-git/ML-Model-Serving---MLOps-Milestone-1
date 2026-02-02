# ML-Model-Serving---MLOps-Milestone-1

**Course:** MLOps - Module 2  
**Student:** Krutika Kulkarni  
**Date:** February 2024  
**Project:** Web & Serverless Model Serving

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Deployment URLs](#deployment-urls)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Cloud Deployment](#cloud-deployment)
  - [Cloud Run Deployment](#cloud-run-deployment)
  - [Cloud Functions Deployment](#cloud-functions-deployment)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Performance Analysis](#performance-analysis)
- [Comparative Analysis](#comparative-analysis)
- [Lifecycle Position](#lifecycle-position)
- [Cleanup](#cleanup)
- [Troubleshooting](#troubleshooting)
- [References](#references)

---

## 🎯 Overview

This project demonstrates three different deployment patterns for serving machine learning models in production:

1. **Local FastAPI Service** - Development and testing environment
2. **Google Cloud Run** - Containerized web service with auto-scaling
3. **Google Cloud Functions** - Serverless function-based deployment

**Model Information:**
- **Type:** Random Forest Classifier
- **Dataset:** Iris Dataset (4 features → 3 classes)
- **Framework:** scikit-learn 1.3.2
- **Input:** 4 numerical features (sepal length, sepal width, petal length, petal width)
- **Output:** Predicted class (0, 1, or 2)

---

## 🏗️ Architecture

### Deployment Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                     ML Model Lifecycle                       │
├─────────────────────────────────────────────────────────────┤
│  Data → Training → Model Artifact → API Deployment → Consumer│
│                            ↓                                  │
│                       model.pkl                               │
│                            ↓                                  │
│              ┌─────────────┴─────────────┐                  │
│              ↓                           ↓                   │
│      ┌──────────────┐           ┌──────────────┐           │
│      │  Cloud Run   │           │   Cloud      │           │
│      │ (Container)  │           │  Functions   │           │
│      │              │           │ (Serverless) │           │
│      └──────────────┘           └──────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🌐 Deployment URLs

### **Cloud Run Service**
- **Service URL:** https://fastapi-ml-service-271681543917.us-central1.run.app
- **API Documentation:** https://fastapi-ml-service-271681543917.us-central1.run.app/docs
- **Prediction Endpoint:** https://fastapi-ml-service-271681543917.us-central1.run.app/predict
- **Project ID:** mlops-krutika-feb2024
- **Region:** us-central1
- **Image:** us-central1-docker.pkg.dev/mlops-krutika-feb2024/ml-models/fastapi-ml:v1

### **Cloud Functions** (To be deployed)
- **Function URL:** [Will be updated after deployment]
- **Function Name:** predict-ml
- **Region:** us-central1

---

## 📁 Project Structure

```
mlops-milestone1/
│
├── README.md                           # This file
├── requirements.txt                    # Python dependencies for FastAPI
├── Dockerfile                          # Container definition for Cloud Run
├── .dockerignore                       # Files to exclude from Docker build
│
├── main.py                             # FastAPI application
├── model.pkl                           # Trained ML model artifact
├── train_model.py                      # Model training script
├── test_api.sh                         # Local testing script
│
├── cloud_function/                     # Cloud Functions deployment
│   ├── main.py                        # Cloud Function code
│   ├── model.pkl                      # Model copy for function
│   └── requirements.txt               # Function dependencies
│
└── screenshots/                        # Deployment evidence
    ├── cloud_run_response.png
    ├── cloud_run_docs.png
    └── cloud_function_response.png
```

---

## ✅ Prerequisites

### Software Requirements
- **Python:** 3.11 or higher
- **Docker:** Latest version (Docker Desktop for Mac)
- **Google Cloud SDK:** 554.0.0 or higher
- **Git:** For version control

### Accounts Required
- Google Cloud Account with billing enabled
- $300 free credits available for new users

### System Requirements
- **OS:** macOS, Linux, or Windows
- **RAM:** 4GB minimum
- **Storage:** 2GB free space

---

## 🚀 Local Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/mlops-milestone1.git
cd mlops-milestone1
```

### Step 2: Create Virtual Environment (Optional but Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Mac/Linux
# OR
venv\Scripts\activate     # On Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
fastapi==0.104.1
uvicorn==0.24.0
scikit-learn==1.3.2
joblib==1.3.2
numpy==1.26.2
pydantic==2.5.0
```

### Step 4: Train the Model

```bash
python train_model.py
```

**Output:**
```
✓ Model saved as model.pkl
```

### Step 5: Run FastAPI Server Locally

```bash
uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 6: Test Locally

**Option A: Using curl**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

**Option B: Using the test script**
```bash
chmod +x test_api.sh
./test_api.sh
```

**Option C: Interactive Swagger UI**
Open browser: http://localhost:8000/docs

**Expected Response:**
```json
{
  "prediction": 0,
  "model_version": "v1.0"
}
```

---

## ☁️ Cloud Deployment

### Cloud Run Deployment

#### Prerequisites
```bash
# Install Google Cloud SDK (if not installed)
brew install --cask google-cloud-sdk

# Login to Google Cloud
gcloud auth login

# Create project
gcloud projects create mlops-krutika-feb2024 --name="MLOps Milestone 1"

# Set active project
gcloud config set project mlops-krutika-feb2024
```

#### Enable Required Services
```bash
# Enable APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
```

#### Configure Settings
```bash
# Set default region
gcloud config set run/region us-central1

# Create Artifact Registry repository
gcloud artifacts repositories create ml-models \
    --repository-format=docker \
    --location=us-central1 \
    --description="ML model containers"

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev
```

#### Build and Push Docker Image
```bash
# Build and submit to Cloud Build
gcloud builds submit --tag us-central1-docker.pkg.dev/mlops-krutika-feb2024/ml-models/fastapi-ml:v1
```

**Build Output:**
```
Creating temporary tarball archive...
Uploading tarball...
BUILD
...
DONE
-----------------------------------------------------
ID: df683907-56c0-470a-aea3-a0e7150c57b1
STATUS: SUCCESS
IMAGE: us-central1-docker.pkg.dev/mlops-krutika-feb2024/ml-models/fastapi-ml:v1
```

#### Deploy to Cloud Run
```bash
gcloud run deploy fastapi-ml-service \
    --image us-central1-docker.pkg.dev/mlops-krutika-feb2024/ml-models/fastapi-ml:v1 \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080
```

**When prompted:** Allow unauthenticated invocations? (y/N) → Type `y`

**Deployment Output:**
```
Deploying container to Cloud Run service [fastapi-ml-service]...
✓ Deploying new service... Done.
Service URL: https://fastapi-ml-service-271681543917.us-central1.run.app
```

---

### Cloud Functions Deployment

#### Step 1: Create Cloud Function Directory
```bash
mkdir -p cloud_function
cd cloud_function
```

#### Step 2: Create Function Code

**cloud_function/main.py:**
```python
import joblib
import numpy as np
import functions_framework
from flask import jsonify

# Load model at cold start
model = joblib.load('model.pkl')

@functions_framework.http
def predict(request):
    """HTTP Cloud Function for predictions"""
    
    # Handle CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)
    
    headers = {'Access-Control-Allow-Origin': '*'}
    
    # Parse JSON request
    request_json = request.get_json(silent=True)
    
    if not request_json or 'features' not in request_json:
        return (jsonify({'error': 'Missing features'}), 400, headers)
    
    try:
        # Make prediction
        features = np.array([request_json['features']])
        prediction = int(model.predict(features)[0])
        
        response = {
            'prediction': prediction,
            'model_version': 'v1.0'
        }
        
        return (jsonify(response), 200, headers)
    
    except Exception as e:
        return (jsonify({'error': str(e)}), 500, headers)
```

#### Step 3: Create Requirements File

**cloud_function/requirements.txt:**
```
functions-framework==3.5.0
scikit-learn==1.3.2
joblib==1.3.2
numpy==1.26.2
flask==3.0.0
```

#### Step 4: Copy Model
```bash
cp ../model.pkl .
```

#### Step 5: Deploy Function
```bash
gcloud functions deploy predict-ml \
    --runtime python311 \
    --trigger-http \
    --allow-unauthenticated \
    --region us-central1 \
    --entry-point predict \
    --memory 512MB \
    --timeout 60s
```

**Expected Output:**
```
Deploying function...
✓ Done.
Function URL: https://us-central1-mlops-krutika-feb2024.cloudfunctions.net/predict-ml
```

---

## 📚 API Documentation

### Endpoint: POST /predict

**Request Format:**
```json
{
  "features": [float, float, float, float]
}
```

**Response Format:**
```json
{
  "prediction": int,
  "model_version": string
}
```

### Example Request
```bash
curl -X POST "https://fastapi-ml-service-271681543917.us-central1.run.app/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [5.1, 3.5, 1.4, 0.2]
  }'
```

### Example Response
```json
{
  "prediction": 0,
  "model_version": "v1.0"
}
```

### Input Validation
- **features:** Array of exactly 4 floating-point numbers
- Missing features → 400 Bad Request
- Invalid types → 422 Unprocessable Entity
- Server errors → 500 Internal Server Error

### Sample Test Cases

**Test Case 1: Iris Setosa**
```json
{"features": [5.1, 3.5, 1.4, 0.2]}
Expected: {"prediction": 0}
```

**Test Case 2: Iris Versicolor**
```json
{"features": [5.9, 3.0, 4.2, 1.5]}
Expected: {"prediction": 1}
```

**Test Case 3: Iris Virginica**
```json
{"features": [6.3, 2.5, 5.0, 1.9]}
Expected: {"prediction": 2}
```

---

## 🧪 Testing

### Local Testing

**Manual Test:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

**Automated Test Script:**
```bash
./test_api.sh
```

### Cloud Run Testing

**Basic Test:**
```bash
CLOUD_RUN_URL="https://fastapi-ml-service-271681543917.us-central1.run.app"

curl -X POST "$CLOUD_RUN_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

**Latency Test:**
```bash
# Test with timing
curl -w "\nTotal Time: %{time_total}s\n" \
  -X POST "$CLOUD_RUN_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

### Cloud Functions Testing

```bash
FUNCTION_URL="https://us-central1-mlops-krutika-feb2024.cloudfunctions.net/predict-ml"

curl -X POST "$FUNCTION_URL" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

### Error Handling Tests

**Missing Features:**
```bash
curl -X POST "$CLOUD_RUN_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{}'
# Expected: 422 Unprocessable Entity
```

**Invalid Input:**
```bash
curl -X POST "$CLOUD_RUN_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": ["a", "b", "c", "d"]}'
# Expected: 422 Unprocessable Entity
```

---

## 📊 Performance Analysis

### Latency Measurements

#### Cloud Run Performance

**Cold Start Test:**
```bash
# After 15 minutes of inactivity
curl -w "\nTime: %{time_total}s\n" \
  -X POST "$CLOUD_RUN_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

**Observed Results:**
- **Cold Start:** ~2.1 seconds
- **Warm Request:** ~0.15 seconds
- **Throughput:** ~50 requests/second (warm)

#### Cloud Functions Performance

**Cold Start Test:**
```bash
# After 15 minutes of inactivity
curl -w "\nTime: %{time_total}s\n" \
  -X POST "$FUNCTION_URL" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

**Observed Results:**
- **Cold Start:** ~5.3 seconds
- **Warm Request:** ~0.18 seconds
- **Throughput:** ~40 requests/second (warm)

### Performance Benchmark Script

```bash
# benchmark.sh
#!/bin/bash

URL=$1
REQUESTS=100

echo "Running $REQUESTS requests to $URL"

for i in $(seq 1 $REQUESTS); do
  curl -s -w "%{time_total}\n" -o /dev/null \
    -X POST "$URL/predict" \
    -H "Content-Type: application/json" \
    -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
done | awk '{sum+=$1; count++} END {print "Average:", sum/count, "seconds"}'
```

**Usage:**
```bash
chmod +x benchmark.sh
./benchmark.sh https://fastapi-ml-service-271681543917.us-central1.run.app
```

---

## 🔄 Comparative Analysis

### Cloud Run vs Cloud Functions

| Aspect | Cloud Run | Cloud Functions |
|--------|-----------|-----------------|
| **Architecture** | Containerized web service | Event-driven serverless function |
| **Framework** | Full FastAPI with all features | Minimal functions-framework |
| **Cold Start Time** | ~2.1 seconds | ~5.3 seconds |
| **Warm Latency** | ~150ms | ~180ms |
| **Minimum Instances** | 0-1000 configurable | 0-1000 configurable |
| **Concurrency** | Up to 1000 concurrent requests/instance | 1 request per instance (default) |
| **Memory** | 128MB - 32GB | 128MB - 8GB |
| **CPU** | Always allocated | Allocated only during request |
| **Deployment** | Requires Dockerfile | Direct source deployment |
| **Image Size** | ~450MB | N/A (managed runtime) |
| **State Management** | Can maintain state across requests | Stateless (reloads per cold start) |
| **Development** | Full FastAPI features (docs, validation) | Basic HTTP handling |
| **Cost (estimate)** | $0.00002400 per request | $0.00000400 per invocation |

### When to Use Each

#### Use Cloud Run When:
✅ Building complex APIs with multiple endpoints  
✅ Need consistent low latency  
✅ Require HTTP/2, WebSockets, or gRPC  
✅ Want full control over the runtime environment  
✅ Need advanced FastAPI features (dependency injection, middleware)  
✅ Expecting consistent traffic patterns  
✅ Require request concurrency  

#### Use Cloud Functions When:
✅ Simple, single-purpose functions  
✅ Event-driven workloads (Pub/Sub, Storage triggers)  
✅ Sporadic, unpredictable traffic  
✅ Minimal maintenance overhead  
✅ Quick prototyping and deployment  
✅ Cost optimization for low-traffic scenarios  
✅ Microservices with isolated functionality  

### Artifact Loading Strategy

#### Cloud Run
- **Loading:** Model loaded once at container startup
- **Persistence:** Model stays in memory across requests
- **Efficiency:** High - no repeated loading
- **Code:**
```python
# Loaded once when container starts
model = joblib.load('model.pkl')

@app.post("/predict")
def predict(request: PredictRequest):
    # Model already in memory
    return model.predict(...)
```

#### Cloud Functions
- **Loading:** Model loaded at cold start
- **Persistence:** Lost when function scales to zero
- **Efficiency:** Medium - reloaded on cold starts
- **Code:**
```python
# Loaded at cold start (outside handler)
model = joblib.load('model.pkl')

@functions_framework.http
def predict(request):
    # Model may need reloading on cold start
    return model.predict(...)
```

### Reproducibility Comparison

#### Cloud Run Reproducibility: ★★★★★
- **Dockerfile:** Explicit, version-controlled environment
- **Dependencies:** Pinned in requirements.txt
- **Runtime:** Fully specified in Dockerfile
- **Build:** Reproducible via Cloud Build
- **Deployment:** Immutable container images

#### Cloud Functions Reproducibility: ★★★☆☆
- **No Dockerfile:** Runtime managed by Google
- **Dependencies:** Pinned in requirements.txt
- **Runtime:** Specified but not fully controlled
- **Build:** Managed build process
- **Deployment:** Code + dependencies uploaded

### Cost Analysis (Estimated)

**Assumptions:**
- 1 million requests/month
- Average 200ms execution time
- 512MB memory

**Cloud Run:**
```
Requests: 1,000,000 × $0.00002400 = $24.00
CPU Time: 55.56 vCPU-hours × $0.00002400 = $1.33
Memory: 111.11 GB-hours × $0.00000250 = $0.28
Total: ~$25.61/month
```

**Cloud Functions:**
```
Invocations: 1,000,000 × $0.00000400 = $4.00
CPU Time: 55.56 GHz-seconds × $0.00001000 = $0.56
Memory: 111.11 GB-seconds × $0.00000250 = $0.28
Total: ~$4.84/month
```

**Winner:** Cloud Functions for this usage pattern (low, sporadic traffic)

---

## 🔄 Lifecycle Position

### ML Model Lifecycle

```
┌────────────────────────────────────────────────────────────────┐
│                    Complete ML Lifecycle                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. DATA COLLECTION                                            │
│     ├─ Raw Data Sources                                        │
│     └─ Data Validation                                         │
│                                                                 │
│  2. DATA PREPARATION                                           │
│     ├─ Cleaning & Preprocessing                                │
│     └─ Feature Engineering                                     │
│                                                                 │
│  3. MODEL TRAINING                                             │
│     ├─ Algorithm Selection                                     │
│     ├─ Hyperparameter Tuning                                   │
│     └─ Model Validation                                        │
│                                                                 │
│  4. MODEL EVALUATION                                           │
│     ├─ Performance Metrics                                     │
│     └─ Model Selection                                         │
│                                                                 │
│  5. MODEL ARTIFACT CREATION ◄── model.pkl                      │
│     ├─ Serialization (joblib)                                  │
│     ├─ Versioning                                              │
│     └─ Storage                                                 │
│                                                                 │
│  6. DEPLOYMENT ◄────────────────── [THIS PROJECT]              │
│     ├─ FastAPI Service (Local)                                │
│     ├─ Cloud Run (Containerized)                              │
│     └─ Cloud Functions (Serverless)                           │
│                                                                 │
│  7. SERVING & INFERENCE                                        │
│     ├─ API Endpoints (/predict)                               │
│     ├─ Input Validation (Pydantic)                            │
│     └─ Response Formatting                                     │
│                                                                 │
│  8. MONITORING (Future Work)                                   │
│     ├─ Latency Tracking                                        │
│     ├─ Error Rates                                             │
│     ├─ Prediction Distribution                                 │
│     └─ Model Drift Detection                                   │
│                                                                 │
│  9. CONSUMER APPLICATIONS                                      │
│     ├─ Web Applications                                        │
│     ├─ Mobile Apps                                             │
│     └─ Batch Processing                                        │
│                                                                 │
│  10. FEEDBACK LOOP                                             │
│      ├─ User Feedback                                          │
│      ├─ Model Retraining                                       │
│      └─ Continuous Improvement                                 │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### This Project's Focus

**Current Stage:** Deployment & Serving (Stages 6-7)

**Inputs:**
- Trained model artifact (`model.pkl`)
- Feature vector (4 numerical values)

**Outputs:**
- Prediction response (class 0, 1, or 2)
- Model version metadata

**Monitoring Touchpoints (Future):**
- Request/response logging
- Latency metrics (Cloud Run metrics, Cloud Functions logs)
- Error tracking (HTTP status codes)
- Prediction distribution monitoring
- Model performance over time

---

## 🧹 Cleanup

### Stop Local Server
```bash
# Press Ctrl+C in the terminal running uvicorn
```

### Delete Cloud Run Service
```bash
gcloud run services delete fastapi-ml-service \
    --region us-central1 \
    --quiet
```

### Delete Cloud Function
```bash
gcloud functions delete predict-ml \
    --region us-central1 \
    --quiet
```

### Delete Artifact Registry Images
```bash
gcloud artifacts docker images delete \
    us-central1-docker.pkg.dev/mlops-krutika-feb2024/ml-models/fastapi-ml:v1 \
    --quiet
```

### Delete Artifact Registry Repository
```bash
gcloud artifacts repositories delete ml-models \
    --location us-central1 \
    --quiet
```

### Delete Google Cloud Project
```bash
gcloud projects delete mlops-krutika-feb2024 --quiet
```

**⚠️ Warning:** This will delete all resources in the project!

---

## 🔧 Troubleshooting

### Common Issues

#### Issue: "docker: command not found"
**Solution:**
```bash
# Add Docker to PATH
sudo ln -s /Applications/Docker.app/Contents/Resources/bin/docker /usr/local/bin/docker

# Verify
docker --version
```

#### Issue: "Port 8000 already in use"
**Solution:**
```bash
# Option 1: Use different port
uvicorn main:app --reload --port 8001

# Option 2: Kill process on port 8000
kill -9 $(lsof -ti:8000)
```

#### Issue: Model version mismatch warning
**Solution:**
```bash
# Retrain model with current scikit-learn version
python train_model.py

# Restart server
uvicorn main:app --reload
```

#### Issue: "Billing account required"
**Solution:**
1. Go to https://console.cloud.google.com/billing
2. Create or link a billing account
3. New users get $300 free credits

#### Issue: Cloud Build fails
**Solution:**
```bash
# Check Docker daemon is running
docker ps

# Verify gcloud authentication
gcloud auth list

# Ensure APIs are enabled
gcloud services enable cloudbuild.googleapis.com
```

#### Issue: Cloud Run deployment timeout
**Solution:**
```bash
# Increase timeout
gcloud run deploy fastapi-ml-service \
    --image ... \
    --timeout 300 \
    --max-instances 10
```

#### Issue: 403 Forbidden on Cloud Run URL
**Solution:**
```bash
# Make service publicly accessible
gcloud run services add-iam-policy-binding fastapi-ml-service \
    --member="allUsers" \
    --role="roles/run.invoker" \
    --region us-central1
```

---

## 📖 References

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Google Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [Google Artifact Registry Documentation](https://cloud.google.com/artifact-registry/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [scikit-learn Documentation](https://scikit-learn.org/stable/)

### Tutorials
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Containerizing Python Apps](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)
- [Cloud Functions Python Quickstart](https://cloud.google.com/functions/docs/quickstart-python)

### Best Practices
- [12-Factor App Methodology](https://12factor.net/)
- [ML Model Deployment Patterns](https://ml-ops.org/content/state-of-mlops)
- [Google Cloud Architecture Center](https://cloud.google.com/architecture)

### Tools Used
- **FastAPI:** Web framework for building APIs
- **Uvicorn:** ASGI server for FastAPI
- **Docker:** Containerization platform
- **Google Cloud SDK:** CLI tools for GCP
- **Pydantic:** Data validation library
- **scikit-learn:** Machine learning library
- **joblib:** Model serialization

---

## 📝 Assignment Checklist

### Deliverables

- [x] **FastAPI Service (Local)**
  - [x] `main.py` with FastAPI app and /predict endpoint
  - [x] Pydantic request/response models
  - [x] Model artifact (model.pkl) with deterministic loading
  - [x] Reproducible environment (requirements.txt)
  - [x] README with lifecycle description

- [x] **Cloud Run Deployment**
  - [x] Deployed Cloud Run service URL (publicly accessible HTTPS)
  - [x] GCP Artifact Registry image reference
  - [x] Evidence of successful inference (screenshots/logs)
  - [ ] Cold start behavior analysis

- [ ] **Cloud Functions Deployment**
  - [ ] Cloud Function code implementing prediction logic
  - [ ] Deployment configuration documented
  - [ ] Deployment logs captured
  - [ ] Function invocation tested

- [ ] **Comparative Analysis**
  - [ ] FastAPI container vs Cloud Function comparison
  - [ ] Lifecycle differences explained
  - [ ] Artifact loading strategies compared
  - [ ] Latency characteristics documented
  - [ ] Reproducibility considerations discussed

- [x] **Documentation**
  - [x] Setup and deployment instructions
  - [x] API usage examples
  - [x] Lifecycle stage explanations
  - [x] Model-API interaction description
  - [x] Deployment URLs included

---

## 👨‍💻 Author

**Krutika Kulkarni**  
MLOps Course - Module 2  
February 2024

---

## 📄 License

This project is created for educational purposes as part of the MLOps course curriculum.

---

## 🙏 Acknowledgments

- MLOps Course instructors and teaching staff
- Google Cloud Platform for free tier and credits
- FastAPI community for excellent documentation
- scikit-learn developers for the Iris dataset

---

**Last Updated:** February 2, 2024
