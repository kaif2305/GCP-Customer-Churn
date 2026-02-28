#!/usr/bin/env python
# coding: utf-8

# In[83]:


import pandas as pd
import joblib
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from google.cloud import storage


# In[84]:


# Configure logging
logging.basicConfig(level=logging.INFO)

# 1. Load Data
# Note: In a container, we don't need !gsutil. We can read directly from GCS 
# because we included 'gcsfs' in our requirements.txt earlier.
storage_client = storage.Client()
bucket_name = "telco-customer-dataset"
file_name = "WA_Fn-UseC_-Telco-Customer-Churn.csv"

logging.info(f"Downloading data from gs://{bucket_name}/{file_name}")
df = pd.read_csv(f"gs://{bucket_name}/{file_name}")


# In[85]:


# type(df)
# df


# In[86]:


# 2. Preprocessing
df = df.drop("customerID", axis=1)


# In[87]:


# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna()


# In[88]:


from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# Encode categorical columns
for col in df.select_dtypes(include="object").columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])

# Split
X = df.drop("Churn", axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# In[89]:


# 3. Train Model with Scaling (to fix ConvergenceWarning)
logging.info("Starting model training...")
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression(max_iter=1000))
])

pipeline.fit(X_train, y_train)


# In[90]:


# 4. Evaluate
preds = pipeline.predict(X_test)
acc = accuracy_score(y_test, preds)
logging.info(f"Accuracy: {acc}")
print("Acuuracay: ",acc)


# In[91]:


# 5. Save and Export
model_filename = "model.joblib"
joblib.dump(pipeline, model_filename)
logging.info(f"Model saved locally as {model_filename}")


# In[92]:


import logging
from google.cloud import storage
storage_path = "gs://telco-customer-dataset/model.joblib"
blob = storage.blob.Blob.from_string(storage_path, client = storage.Client())
blob.upload_from_filename('model.joblib')
logging.info("model exported to : {}".format(storage_path))


# In[ ]:




