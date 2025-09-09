#!/usr/bin/env python
# coding: utf-8

# In[58]:


import boto3
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, IsolationForest


# In[59]:


# DynamoDB setup
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Anomalies')


# In[82]:


import os
import boto3
import pandas as pd

# Define S3 bucket name and file key
bucket_name = 'aws-cloudtrail-logs-258283632626-e2888416'  # Replace with your actual bucket name
test_file_key = 'AWS_LOGS/CIC_UNSW_NB15_testing-set.csv'  # S3 path to the file

# Initialize the boto3 S3 client
s3 = boto3.client('s3')

# Define the local file path where the file will be saved
local_file_path = 'CIC_UNSW_NB15_testing-set.csv'  # Local file name to save the data

# Download the file from S3 to the local path
s3.download_file(bucket_name, test_file_key, local_file_path)

# Read the downloaded file into a pandas DataFrame
test_data_total = pd.read_csv(local_file_path)
test_data = test_data_total.head(1500)
original_data = test_data.copy()  # Keep original string columns

# Verify the data has been loaded correctly
print(test_data.head())  # Print first few rows to verify


# In[61]:


# Step 3: Load models from S3
def load_model_from_s3(model_key):
    model_file = '/tmp/' + model_key.split('/')[-1]  # Saving temporarily in /tmp
    s3.download_file(bucket_name, model_key, model_file)
    return joblib.load(model_file)

# Load the models
rf_model = load_model_from_s3('models/rf_model.joblib')
iso_model = load_model_from_s3('models/iso_model.joblib')
scaler = load_model_from_s3('models/scaler.joblib')
label_encoders = joblib.load('/tmp/label_encoders.joblib')  # Load label encoders


# In[62]:


def preprocess_data(test_data):
    # Drop the 'id' column if it exists in the test data
    test_data = test_data.drop(columns=['id'], errors='ignore')
    
    # Preprocess categorical columns the same way as during training
    categorical_columns = test_data.select_dtypes(include=['object']).columns

    for col in categorical_columns:
        encoder = label_encoders[col]  # Get the trained encoder for this column
        
        # Add 'unknown' to the encoder's classes if not already present
        if 'unknown' not in encoder.classes_:
            encoder.classes_ = np.append(encoder.classes_, 'unknown')
        
        # Apply 'unknown' label for unseen categories in the test data
        test_data[col] = test_data[col].apply(lambda x: x if x in encoder.classes_ else 'unknown')

        # Transform the column using the trained encoder
        test_data[col] = encoder.transform(test_data[col])
    
    # Align the features by making sure the test data has the same columns as the training data
    # Remove the label column and other unnecessary columns before scaling
    X_test = test_data.drop(columns=['label'], errors='ignore')  # Drop the label column if it exists
    
    # Ensure the columns are in the same order as during training
    X_test = X_test[scaler.feature_names_in_]
    
    # Scale features (assuming you used StandardScaler during training)
    X_test_scaled = scaler.transform(X_test)  # Use the same scaler from training
    
    return X_test_scaled


# In[63]:


# Step 5: Make predictions
def make_predictions(X_test_scaled):
    # Run predictions using Random Forest model
    rf_pred = rf_model.predict(X_test_scaled)
    
    # Run predictions using Isolation Forest model
    iso_pred = iso_model.predict(X_test_scaled)
    iso_pred = [1 if pred == -1 else 0 for pred in iso_pred]  # Convert anomalies to 1, normal to 0

    # Hybrid model: Majority vote (use RF if different)
    hybrid_prediction = np.array([
        rf_pred if rf_pred == iso_pred else rf_pred
        for rf_pred, iso_pred in zip(rf_pred, iso_pred)
    ])
    
    return hybrid_prediction


# In[78]:


import boto3
import pandas as pd
from decimal import Decimal
from botocore.exceptions import ClientError

# Initialize DynamoDB resource and table (do this once, not inside the function)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # change region if needed
table = dynamodb.Table('Anomalies')  # make sure this matches your table name

# Store results with all columns + prediction
def store_results_in_dynamodb(test_data, hybrid_prediction):
    for i in range(len(test_data)):
        try:
            anomaly_id = str(test_data['id'][i])  # Assuming 'id' exists
            prediction = int(hybrid_prediction[i])
            timestamp = int(pd.to_datetime('now').timestamp())

            # Start with required keys
            item = {
                'AnomalyID': anomaly_id,
                'Timestamp': timestamp,
                'Prediction': prediction
            }

            # Add all test_data columns
            for col in test_data.columns:
                value = test_data.iloc[i][col]
                if isinstance(value, float):
                    item[col] = Decimal(str(value))
                elif isinstance(value, (int, str, bool)):
                    item[col] = value
                elif pd.isnull(value):
                    continue  # skip nulls
                else:
                    item[col] = str(value)  # fallback to string

            # Put item into DynamoDB
            table.put_item(Item=item)
            print(f"✅ Stored AnomalyID {anomaly_id} with Prediction: {prediction}")
        
        except ClientError as e:
            print(f"❌ Failed to store AnomalyID {anomaly_id}: {e.response['Error']['Message']}")


# In[83]:


# Main function
def main():
    X_test_scaled = preprocess_data(test_data.copy())
    hybrid_prediction = make_predictions(X_test_scaled)
    store_results_in_dynamodb(test_data.copy(), hybrid_prediction)

# Run the main function
if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:





# In[ ]:




