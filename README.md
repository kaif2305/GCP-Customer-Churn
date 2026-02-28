# 📡 Telco Customer Churn Prediction on Google Cloud Vertex AI

This repository contains an end-to-end Machine Learning pipeline for predicting customer churn using the **Telco Customer Churn dataset**. The project leverages **Vertex AI** for scalable training, model registry, and real-time serving.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [System Architecture](#-system-architecture)
- [Technical Stack](#-technical-stack)
- [Installation & Setup](#-installation--setup)
- [Training Workflow](#-training-workflow)
- [Deployment](#-deployment)
- [Inference & API Usage](#-inference--api-usage)
- [Known Issues & Fixes](#-known-issues--fixes)

---

## 🔍 Project Overview

The goal of this project is to predict whether a telecom customer is likely to churn.

This is a **binary classification problem** where:

- `1` → Customer will churn  
- `0` → Customer will stay  

### Features Used

- **Demographics**
  - Gender
  - SeniorCitizen
  - Partner
  - Dependents

- **Services**
  - PhoneService
  - InternetService
  - OnlineSecurity
  - StreamingTV
  - TechSupport
  - etc.

- **Account Information**
  - Tenure
  - Contract type
  - Payment method
  - MonthlyCharges
  - TotalCharges

---

## 🏗 System Architecture

This project follows a **Custom Container Training + Prebuilt Prediction Container** architecture on Vertex AI.

### Flow

1. **Data Source**
   - Dataset stored in Google Cloud Storage (GCS)

2. **Training**
   - Dockerized Python script (`train.py`)
   - Scikit-learn `Pipeline`:
     - `StandardScaler`
     - `LogisticRegression`

3. **Model Export**
   - Model saved as `model.joblib`
   - Uploaded to GCS
   - Registered in Vertex AI Model Registry

4. **Deployment**
   - Deployed to a Vertex AI Endpoint
   - Uses prebuilt Scikit-learn serving container

5. **Prediction**
   - Real-time REST API predictions via Vertex AI Endpoint

---

## 🛠 Technical Stack

- **Language:** Python 3.10
- **ML Framework:** Scikit-learn 1.2.2
- **Cloud Platform:** Google Cloud Platform (GCP)
- **Vertex AI Services:**
  - Custom Training Jobs
  - Model Registry
  - Endpoints
- **Storage:** Google Cloud Storage (GCS)
- **Container Registry:** Artifact Registry
- **Containerization:** Docker (Slim Debian images)

---

## 🚀 Installation & Setup

### 1️⃣ Install Required Packages

```bash
pip install pandas scikit-learn==1.2.2 google-cloud-storage gcsfs joblib