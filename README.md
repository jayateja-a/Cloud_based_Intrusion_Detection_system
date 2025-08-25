# Log-based Intrusion Detection System (Log-based IDS)

## Overview
The **Log-based Intrusion Detection System (IDS)** is a cloud-based security solution that detects potential cyber threats using machine learning. It analyzes **network traffic logs** stored in AWS, processes them using **AWS Lambda**, classifies them with an ML model hosted on **AWS SageMaker**, and visualizes the results through a **web dashboard**.

## Architecture
![Architecture Diagram](https://github.com/user-attachments/assets/2f8ccb7d-1511-4a93-90fc-fb8d410bfc86)

## Features
- **Automated Log Processing**: Uses AWS Lambda to extract and parse network logs.
- **Machine Learning-Based Threat Detection**: Uses an ML model trained on the **CIC-UNSW-NB15 dataset**.
- **Real-Time Monitoring Dashboard**: Displays anomaly detection results via a frontend hosted on AWS CloudFront.
- **Secure API**: Flask-based REST API to fetch and serve intrusion detection logs.
- **Scalable & Cost-Efficient**: Runs on AWS services with optimized resource allocation.

## Dataset
The project utilizes the **CIC-UNSW-NB15 dataset**, which includes multiple attack categories for classification.

[Dataset Link](https://www.unb.ca/cic/datasets/cic-unsw-nb15.html)

### Attack Categories Used
- **Normal** (benign traffic)
- **Exploits**
- **DoS (Denial of Service)**
- **Fuzzers**
- **Generic Attacks**
- **Reconnaissance**
- **Worms**
- **Shellcode**
- **Backdoor**
- **Analysis**

## System Components
### AWS Services Used
- **Amazon S3**: Stores raw network logs.
- **AWS Lambda**: Parses logs and sends structured data to DynamoDB.
- **Amazon SageMaker**: Hosts the ML model for intrusion detection.
- **Amazon DynamoDB**: Stores processed logs and detection results.
- **Amazon EventBridge**: Triggers ML processing every 5 minutes.
- **Amazon EC2 (Public Subnet)**: Hosts the **Flask API Server**.
- **Amazon CloudFront & S3**: Hosts and serves the frontend dashboard.

### Data Flow
1. **Network logs** from AWS **VPC Flow Logs** are stored in **S3**.
2. **Lambda function** extracts, processes, and stores structured logs in **DynamoDB**.
3. **SageMaker Model** classifies logs as **normal or attack** and updates **DynamoDB**.
4. **API Server** retrieves classification results and serves them to the frontend.
5. **Frontend Dashboard** displays logs, threat trends, and a pie chart of attacks vs. normal traffic.

## Project Setup
### Prerequisites
- AWS account with permissions to deploy EC2, S3, DynamoDB, Lambda, SageMaker, and CloudFront.
- Python 3.x installed locally.
- Node.js (for frontend development, optional).

### Deployment Steps
#### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/log-based-ids.git
cd log-based-ids
```

#### 2. Setup API Server
```bash
cd backend
pip install -r requirements.txt
python app.py
```

#### 3. Deploy Lambda Function
- Create a Lambda function in AWS and upload `lambda/parse_vpc_logs.py`.
- Set appropriate **IAM roles** to access S3 and DynamoDB.

#### 4. Train & Deploy ML Model in SageMaker
- Upload dataset to an S3 bucket.
- Train the model using a **Jupyter notebook on SageMaker**.
- Deploy the trained model as a SageMaker endpoint.

#### 5. Deploy Frontend
- Upload `frontend/index.html` to an **S3 bucket**.
- Enable **CloudFront** for hosting the frontend.

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/logs`  | Fetch all stored logs from DynamoDB |
| GET    | `/logs?query=<param>` | Search logs using filters |
| GET    | `/stats` | Get summary statistics for attack distribution |

## Frontend Features
- **Searchable Logs Table**: Allows filtering logs based on multiple columns.
- **Pie Chart**: Displays real-time distribution of **normal vs attack** traffic.
- **Responsive UI**: Hosted on AWS CloudFront with S3.

## Security Considerations
- **IAM Policies**: Configured to enforce least privilege access.
- **API Authentication**: Uses AWS IAM and Cognito (optional).
- **Encryption**: All stored logs and model outputs are encrypted using **AWS KMS**.

## Testing & Validation
### Integration Testing
| Test Case | Expected Outcome |
|-----------|-----------------|
| Log Ingestion | Logs appear in S3 |
| Lambda Processing | Parsed logs stored in DynamoDB |
| SageMaker Classification | Attack/Normal labels assigned correctly |
| API Response | JSON data returned correctly |
| Frontend Updates | Dashboard updates with new logs |

## Log Ingestion
![image](https://github.com/user-attachments/assets/344e0c48-00c7-4793-9b39-982ab2d57666)
## Lambda Processing
![image](https://github.com/user-attachments/assets/e93e066d-4405-4ad4-8b92-cc91862c4fe7)
## SageMaker Classification (DynamoDB Result)
![image](https://github.com/user-attachments/assets/4b8b6a02-8655-4cb0-b544-9b0fa3d860fb)
## API Response
![image](https://github.com/user-attachments/assets/997471c5-10ce-4804-a9d5-0deef7a61796)
## Frontend Updates
![image](https://github.com/user-attachments/assets/93295b0d-b071-4f69-b9e8-0d9b9fbfff63)
![image](https://github.com/user-attachments/assets/9b66f37b-ccbc-4161-b0e9-e833142fa2e2)
![image](https://github.com/user-attachments/assets/466bfee7-6c53-4649-88b8-2bda88e4aa7b)
![image](https://github.com/user-attachments/assets/9c964d57-4418-4fde-9324-26832264ecce)
![image](https://github.com/user-attachments/assets/235e914a-9a75-400b-a307-22244701be57)



### Security Testing
- Unauthorized API requests should return **401 Unauthorized**.
- Logs should not be accessible outside of AWS services.

## Challenges & Solutions
| Issue | Solution |
|-------|----------|
| High cost with NAT Gateway | Switched to **NAT Instance**, then eliminated preprocessing server |
| Lambda timeout issues | Increased memory and execution time |
| Model misclassifications | Improved **feature engineering** and retrained model |

## Future Enhancements
- **Real-Time Stream Processing** using AWS Kinesis.
- **Automated Model Retraining** when new logs are ingested.
- **Anomaly Scoring** for better threat classification.

## Contributor
**Jayateja Alugolu**



