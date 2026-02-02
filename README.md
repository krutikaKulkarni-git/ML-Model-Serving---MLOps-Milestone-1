# ML Model Serving - MLOps Milestone 1

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
- [Testing & Results](#testing--results)
- [Performance Analysis](#performance-analysis)
- [Comparative Analysis](#comparative-analysis)
- [Lifecycle Position](#lifecycle-position)
- [Screenshots](#screenshots)
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

### **Cloud Functions**
- **Function URL:** https://us-central1-mlops-krutika-feb2024.cloudfunctions.net/predict-ml
- **Function Name:** predict-ml
- **Region:** us-central1
- **Runtime:** Python 3.11
- **Memory:** 512MB

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
├── compare_deployments.sh              # Performance comparison script
│
├── cloud_function/                     # Cloud Functions deployment
│   ├── main.py                        # Cloud Function code
│   ├── model.pkl                      # Model copy for function
│   └── requirements.txt               # Function dependencies
│
└── screenshots/                        # Deployment evidence
    ├── cloud_run_deployment.png       # Cloud Run deployment success
    ├── cloud_run_test.png             # Cloud Run API test
    ├── cloud_run_warm_test.png        # Warm instance performance
    ├── cloud_function_deployment.png  # Cloud Function deployment
    ├── cloud_function_test.png        # Cloud Function API test
    ├── cloud_function_warm_test.png   # Function warm performance
    └── performance_comparison.png     # Side-by-side comparison
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
✓ Creating Revision...
✓ Routing traffic...
✓ Setting IAM Policy...
Done.
Service [fastapi-ml-service] revision [fastapi-ml-service-00001-n29] has been deployed 
and is serving 100 percent of traffic.
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

# Load model at cold start (outside the function handler)
model = joblib.load('model.pkl')

@functions_framework.http
def predict(request):
    """HTTP Cloud Function for predictions"""
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)
    
    # Set CORS headers for main request
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

#### Step 4: Copy Model and Deploy
```bash
# Copy model from parent directory
cp ../model.pkl .

# Deploy the function
gcloud functions deploy predict-ml \
    --runtime python311 \
    --trigger-http \
    --allow-unauthenticated \
    --region us-central1 \
    --entry-point predict \
    --memory 512MB \
    --timeout 60s
```

**Deployment Output:**
```
Deploying function (may take a while - up to 2 minutes)...
✓ Deploying function... Done.
✓ Setting IAM Policy...
Done.
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

## 🧪 Testing & Results

### Cloud Run Testing

**Test Command:**
```bash
curl -X POST "https://fastapi-ml-service-271681543917.us-central1.run.app/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

**Response:**
```json
{"prediction":0,"model_version":"v1.0"}
```

**Warm Instance Test Results:**
```bash
Time: 0.189154s
```

### Cloud Functions Testing

**Test Command:**
```bash
curl -X POST "https://us-central1-mlops-krutika-feb2024.cloudfunctions.net/predict-ml" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

**Response:**
```json
{"model_version":"v1.0","prediction":0}
```

**Warm Instance Test Results:**
```bash
Time: 0.140968s
```

### Performance Comparison Test Results

**Test Setup:** 5 consecutive requests to each endpoint

#### Cloud Run Performance (Warm):
```
Request 1: 7.999956s  (First request after idle - cold start)
Request 2: 0.133654s
Request 3: 0.124456s
Request 4: 0.122936s
Request 5: 0.121142s

Average (excluding cold start): 0.1255s
Cold Start: ~8.0s
```

#### Cloud Function Performance (Warm):
```
Request 1: 0.185310s
Request 2: 0.120840s
Request 3: 0.143795s
Request 4: 0.139710s
Request 5: 0.125980s

Average: 0.143s
```

---

## 📊 Performance Analysis

### Actual Measured Performance Metrics

#### Cloud Run
| Metric | Value |
|--------|-------|
| **Cold Start Time** | ~8.0 seconds |
| **Warm Latency (avg)** | 0.125 seconds |
| **Fastest Request** | 0.121 seconds |
| **Slowest Warm Request** | 0.189 seconds |
| **Consistency** | High (low variance after warm-up) |

#### Cloud Functions
| Metric | Value |
|--------|-------|
| **Cold Start Time** | Not measured (requires 15+ min idle) |
| **Warm Latency (avg)** | 0.143 seconds |
| **Fastest Request** | 0.120 seconds |
| **Slowest Request** | 0.185 seconds |
| **Consistency** | Moderate (some variance) |

### Key Observations

1. **Cold Start Impact:** Cloud Run's first request after idle took 8 seconds vs. ~0.12s for subsequent requests (67x slower)

2. **Warm Performance:** Cloud Run slightly outperformed Cloud Functions on average
   - Cloud Run: 0.125s average
   - Cloud Functions: 0.143s average
   - Difference: 18ms (~14% slower)

3. **Consistency:** Cloud Run showed more consistent latency after warm-up with requests ranging from 0.121-0.133s

4. **Best Performance:** Both achieved sub-150ms latency when warm, suitable for real-time applications

### Performance Comparison Script

The comparison was run using:
```bash
./compare_deployments.sh
```

Which executes 5 consecutive requests to each endpoint and measures total time.

---

## 🔄 Comparative Analysis

### Cloud Run vs Cloud Functions - Detailed Comparison

| Aspect | Cloud Run | Cloud Functions |
|--------|-----------|-----------------|
| **Architecture** | Containerized web service | Event-driven serverless function |
| **Framework** | Full FastAPI with all features | Minimal functions-framework |
| **Measured Cold Start** | ~8.0 seconds | Not measured |
| **Measured Warm Latency** | 0.125s (average) | 0.143s (average) |
| **Minimum Instances** | 0-1000 configurable | 0-1000 configurable |
| **Concurrency** | Up to 1000 concurrent requests/instance | 1 request per instance (default) |
| **Memory** | 128MB - 32GB | 128MB - 8GB |
| **CPU** | Always allocated | Allocated only during request |
| **Deployment Complexity** | Requires Dockerfile | Direct source deployment |
| **Image Size** | ~450MB | N/A (managed runtime) |
| **State Management** | Can maintain state across requests | Stateless (reloads per cold start) |
| **Development Experience** | Full FastAPI features (auto docs, validation) | Basic HTTP handling |
| **API Documentation** | Auto-generated Swagger UI at /docs | Manual documentation needed |
| **Request Validation** | Automatic via Pydantic | Manual validation required |

### Artifact Loading Strategy

#### Cloud Run
- **Loading:** Model loaded once at container startup
- **Persistence:** Model stays in memory across requests
- **Efficiency:** High - no repeated loading overhead
- **Observed Behavior:** After initial cold start, all requests use cached model
- **Code Location:** Global scope (outside request handler)

**Evidence from logs:**
```
Starting new instance. Reason: AUTOSCALING
Default STARTUP_TCP probe succeeded after 1 attempt for container "worker" on port 8080
```

#### Cloud Functions
- **Loading:** Model loaded at cold start (outside function handler)
- **Persistence:** Lost when function scales to zero
- **Efficiency:** Medium - reloaded on cold starts only
- **Observed Behavior:** Function autoscales based on traffic
- **Code Location:** Global scope (executed once per instance)

**Evidence from logs:**
```
Starting new instance. Reason: DEPLOYMENT_ROLLOUT
InconsistentVersionWarning: Trying to unpickle estimator from version 1.5.1 when using version 1.3.2
```

### When to Use Each - Based on Testing

#### Use Cloud Run When:
✅ You need consistent low latency (<150ms)  
✅ Building complex APIs with multiple endpoints  
✅ Want full FastAPI features (auto docs, validation, dependency injection)  
✅ Expect consistent traffic patterns  
✅ Need request concurrency (multiple requests per instance)  
✅ Require full control over runtime environment  
✅ Cold starts can be mitigated with min-instances setting  

**Real-world scenario:** Production ML API serving a web application with steady traffic

#### Use Cloud Functions When:
✅ Simple, single-purpose prediction endpoints  
✅ Event-driven workloads (Pub/Sub, Storage triggers, etc.)  
✅ Sporadic, unpredictable traffic patterns  
✅ Want minimal deployment complexity (no Dockerfile)  
✅ Cost optimization for low-traffic scenarios  
✅ Quick prototyping and rapid deployment  
✅ Microservices with isolated functionality  

**Real-world scenario:** On-demand predictions triggered by file uploads or database changes

### Reproducibility Comparison

#### Cloud Run Reproducibility: ★★★★★
**Strengths:**
- Dockerfile provides explicit, version-controlled environment definition
- All dependencies pinned in requirements.txt
- Base image version specified (python:3.11-slim)
- Build process is reproducible via Cloud Build
- Immutable container images ensure consistency
- Can be tested locally with Docker before deployment

**Evidence:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

#### Cloud Functions Reproducibility: ★★★☆☆
**Strengths:**
- Dependencies pinned in requirements.txt
- Runtime version specified (python311)
- Simpler deployment (less to go wrong)

**Limitations:**
- No control over base system packages
- Runtime managed by Google (less control)
- Cannot test exact production environment locally
- System-level dependencies may differ

**Evidence:**
```
Runtime: python311
Entry point: predict
```

### Cost Analysis (Estimated)

**Assumptions:**
- 1 million requests/month
- Average 150ms execution time
- 512MB memory allocation
- 1 vCPU (Cloud Run) vs 0.4 GHz-seconds (Functions)

**Cloud Run Monthly Cost:**
```
Requests:        1,000,000 × $0.00002400 = $24.00
CPU Time:        41.67 vCPU-hours × $0.00002400 = $1.00
Memory:          83.33 GB-hours × $0.00000250 = $0.21
Total:           ~$25.21/month
```

**Cloud Functions Monthly Cost:**
```
Invocations:     1,000,000 × $0.00000400 = $4.00
Compute (GHz-s): 150,000 GHz-seconds × $0.00001000 = $1.50
Memory (GB-s):   75,000 GB-seconds × $0.00000250 = $0.19
Total:           ~$5.69/month
```

**Winner for this usage pattern:** Cloud Functions (~$19.52/month savings)

**However:** For high-traffic applications with consistent load, Cloud Run's concurrency model and ability to run min-instances becomes more cost-effective.

### Lifecycle Implications

#### Cloud Run Lifecycle
```
Build → Push to Registry → Deploy → Container Starts → Model Loads (once) 
→ Accepts Requests → Scales Up/Down → Eventually Scales to Zero
```

**Monitoring Points:**
- Container startup logs
- HTTP request/response logs
- Cloud Run metrics (latency, request count, instance count)
- Custom application logs (prediction distribution, errors)

#### Cloud Functions Lifecycle
```
Deploy → Cold Start (on first request) → Model Loads 
→ Accepts Request → Processes → Scales to Zero → Repeat on next trigger
```

**Monitoring Points:**
- Function invocation logs
- Execution time logs
- Error logs
- Cloud Monitoring metrics (invocations, latency, errors)

---

## 🔄 Lifecycle Position

### ML Model Lifecycle

```
┌────────────────────────────────────────────────────────────────┐
│                    Complete ML Lifecycle                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. DATA COLLECTION                                            │
│     ├─ Raw Data Sources (Iris Dataset)                        │
│     └─ Data Validation                                         │
│                                                                 │
│  2. DATA PREPARATION                                           │
│     ├─ Cleaning & Preprocessing                                │
│     └─ Feature Engineering                                     │
│                                                                 │
│  3. MODEL TRAINING (train_model.py)                           │
│     ├─ Algorithm Selection (Random Forest)                    │
│     ├─ Hyperparameter Tuning                                   │
│     └─ Model Validation                                        │
│                                                                 │
│  4. MODEL EVALUATION                                           │
│     ├─ Performance Metrics                                     │
│     └─ Model Selection                                         │
│                                                                 │
│  5. MODEL ARTIFACT CREATION ◄── model.pkl                      │
│     ├─ Serialization (joblib)                                  │
│     ├─ Versioning (v1.0)                                       │
│     └─ Storage (local + cloud deployments)                     │
│                                                                 │
│  6. DEPLOYMENT ◄────────────────── [THIS PROJECT]              │
│     ├─ Local Development (uvicorn)                            │
│     ├─ Cloud Run (containerized FastAPI)                      │
│     └─ Cloud Functions (serverless)                           │
│                                                                 │
│  7. SERVING & INFERENCE ◄────────── [THIS PROJECT]            │
│     ├─ API Endpoints (/predict)                               │
│     ├─ Input Validation (Pydantic for Cloud Run)             │
│     ├─ Prediction Logic (model.predict)                       │
│     └─ Response Formatting (JSON)                              │
│                                                                 │
│  8. MONITORING (Implemented via Cloud Services)                │
│     ├─ Latency Tracking (measured: 0.125s avg)               │
│     ├─ Error Rates (tracked via HTTP status codes)           │
│     ├─ Request Logs (Cloud Run/Functions logging)            │
│     └─ Performance Metrics (documented in this README)         │
│                                                                 │
│  9. CONSUMER APPLICATIONS                                      │
│     ├─ Web Applications (via HTTPS API)                       │
│     ├─ Mobile Apps (REST API integration)                     │
│     └─ Batch Processing (multiple predictions)                │
│                                                                 │
│  10. FEEDBACK LOOP (Future Enhancement)                        │
│      ├─ User Feedback Collection                              │
│      ├─ Model Performance Monitoring                           │
│      ├─ Retraining Pipeline                                    │
│      └─ Continuous Improvement                                 │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### This Project's Focus

**Current Stage:** Deployment & Serving (Stages 6-8)

**Inputs:**
- Trained model artifact (`model.pkl`) - 4.2 KB
- Feature vector: 4 numerical values representing iris flower measurements

**Processing:**
- Model loading at startup (Cloud Run) or cold start (Functions)
- Input validation (Pydantic in Cloud Run, manual in Functions)
- NumPy array conversion
- Random Forest prediction computation
- Response serialization

**Outputs:**
- Prediction response: integer class (0, 1, or 2)
- Model version metadata: "v1.0"
- HTTP status code: 200 (success) or error codes

**Monitoring Touchpoints (Implemented):**
- Request/response logging (automatic via Cloud Logging)
- Latency metrics:
  - Cloud Run: 0.125s average (measured)
  - Cloud Functions: 0.143s average (measured)
- Error tracking via HTTP status codes
- Deployment logs showing model version warnings
- Performance comparison results (documented)

**Production Readiness Considerations:**
- ✅ Deterministic model loading
- ✅ Input validation and error handling
- ✅ Reproducible deployments (especially Cloud Run)
- ✅ Auto-scaling configured
- ✅ HTTPS endpoints with authentication options
- ⚠️ Model version mismatch warning (requires retraining with consistent scikit-learn version)
- 🔄 Future: A/B testing, model versioning, drift detection

---

## 📸 Screenshots

### Cloud Run Deployment

**1. Successful Cloud Run Deployment**
![Cloud Run Deployment Success](screenshots/cloud_run_deployment.png)
*Shows deployment completion with service URL and traffic routing*

**2. Cloud Run API Test**
![Cloud Run Test](screenshots/cloud_run_test.png)
*Demonstrates successful prediction request returning {"prediction":0,"model_version":"v1.0"}*

**3. Cloud Run Warm Instance Performance**
![Cloud Run Warm Test](screenshots/cloud_run_warm_test.png)
*Shows consistent latency of 0.189154s for warm requests*

### Cloud Functions Deployment

**4. Cloud Functions Deployment & Logs**
![Cloud Function Deployment](screenshots/cloud_function_deployment.png)
*Displays function deployment logs with autoscaling events and model loading warnings*

**5. Cloud Function API Test**
![Cloud Function Test](screenshots/cloud_function_test.png)
*Successful invocation with Function URL and prediction response*

**6. Cloud Function Warm Performance**
![Cloud Function Warm Test](screenshots/cloud_function_warm_test.png)
*Warm instance latency measurement of 0.140968s*

### Performance Comparison

**7. Side-by-Side Performance Comparison**
![Performance Comparison](screenshots/performance_comparison.png)
*Benchmark showing Cloud Run vs Cloud Functions across 5 consecutive requests*

**Key Results from Screenshot:**
- Cloud Run Request 1: 7.999956s (cold start)
- Cloud Run Requests 2-5: ~0.12s (warm)
- Cloud Function Requests 1-5: ~0.12-0.18s (warm)

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

### Delete Google Cloud Project (Complete Cleanup)
```bash
gcloud projects delete mlops-krutika-feb2024 --quiet
```

**⚠️ Warning:** This will delete ALL resources in the project and cannot be undone!

---

## 🔧 Troubleshooting

### Common Issues Encountered

#### Issue: Model Version Mismatch Warning
**Observed in Cloud Functions logs:**
```
InconsistentVersionWarning: Trying to unpickle estimator RandomForestClassifier 
from version 1.5.1 when using version 1.3.2
```

**Solution:**
```bash
# Retrain model with matching scikit-learn version
pip install scikit-learn==1.3.2
python train_model.py

# Redeploy function
gcloud functions deploy predict-ml --runtime python311 ...
```

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

#### Issue: Cloud Run Cold Start (8+ seconds)
**Solution:**
```bash
# Configure minimum instances to keep at least 1 warm
gcloud run services update fastapi-ml-service \
    --min-instances 1 \
    --region us-central1

# Note: This increases cost but eliminates cold starts
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

#### Issue: Cloud Function Deployment Timeout
**Solution:**
```bash
# Increase timeout and memory
gcloud functions deploy predict-ml \
    --timeout 300s \
    --memory 1024MB \
    ...
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
- [Model Serving Patterns](https://developers.google.com/machine-learning/guides/rules-of-ml)

### Tools Used
- **FastAPI:** Web framework for building APIs
- **Uvicorn:** ASGI server for FastAPI
- **Docker:** Containerization platform
- **Google Cloud SDK:** CLI tools for GCP (version 554.0.0)
- **Pydantic:** Data validation library
- **scikit-learn:** Machine learning library (1.3.2)
- **joblib:** Model serialization
- **functions-framework:** Cloud Functions Python framework

---

## 📝 Assignment Checklist

### Deliverables Status

- [x] **FastAPI Service (Local)**
  - [x] `main.py` with FastAPI app and /predict endpoint
  - [x] Pydantic request/response models
  - [x] Model artifact (model.pkl) with deterministic loading
  - [x] Reproducible environment (requirements.txt)
  - [x] README with lifecycle description

- [x] **Cloud Run Deployment**
  - [x] Deployed Cloud Run service URL (publicly accessible HTTPS)
  - [x] GCP Artifact Registry image reference
  - [x] Evidence of successful inference (screenshots + curl output)
  - [x] Cold start behavior analysis (8.0s measured)

- [x] **Cloud Functions Deployment**
  - [x] Cloud Function code implementing prediction logic
  - [x] Deployment configuration documented
  - [x] Deployment logs captured (screenshots included)
  - [x] Function invocation tested (0.141s average latency)

- [x] **Comparative Analysis**
  - [x] FastAPI container vs Cloud Function comparison
  - [x] Lifecycle differences explained (stateful vs stateless)
  - [x] Artifact loading strategies compared
  - [x] Latency characteristics documented (actual measurements)
  - [x] Reproducibility considerations discussed

- [x] **Documentation**
  - [x] Setup and deployment instructions
  - [x] API usage examples
  - [x] Lifecycle stage explanations
  - [x] Model-API interaction description
  - [x] Deployment URLs included and tested
  - [x] Screenshots of all deployments
  - [x] Performance metrics documented

### Performance Summary

| Deployment | Cold Start | Warm Avg | Best Time | Worst Time |
|-----------|------------|----------|-----------|------------|
| **Cloud Run** | 8.0s | 0.125s | 0.121s | 7.99s |
| **Cloud Functions** | N/A* | 0.143s | 0.120s | 0.185s |

*Cloud Functions cold start not measured (requires 15+ min idle period not tested)

---

## 👨‍💻 Author

**Krutika Kulkarni**  
MLOps Course - Module 2  
February 2024

**Project Repository:** [GitHub Link - To be added]

---

## 📄 License

This project is created for educational purposes as part of the MLOps course curriculum.

---

## 🙏 Acknowledgments

- MLOps Course instructors and teaching staff
- Google Cloud Platform for free tier and $300 credits
- FastAPI community for excellent documentation
- scikit-learn developers for the Iris dataset
- Anthropic's Claude for development assistance

---

## 🔗 Quick Links

### Live Deployments
- [Cloud Run Service](https://fastapi-ml-service-271681543917.us-central1.run.app/predict)
- [Cloud Run API Docs](https://fastapi-ml-service-271681543917.us-central1.run.app/docs)
- [Cloud Function](https://us-central1-mlops-krutika-feb2024.cloudfunctions.net/predict-ml)

### Test Commands
```bash
# Test Cloud Run
curl -X POST "https://fastapi-ml-service-271681543917.us-central1.run.app/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'

# Test Cloud Function
curl -X POST "https://us-central1-mlops-krutika-feb2024.cloudfunctions.net/predict-ml" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

### Project Stats
- **Total Deployment Time:** ~15 minutes
- **Lines of Code:** ~200 (including both deployments)
- **Docker Image Size:** 450MB
- **Model Size:** 4.2KB
- **Total Requests Tested:** 10+
- **Success Rate:** 100%

---

**Last Updated:** February 2, 2024  
**Version:** 1.0  
**Status:** ✅ All deliverables complete
