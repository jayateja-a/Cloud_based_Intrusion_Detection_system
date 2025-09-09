from flask import Flask, render_template, jsonify, request
import boto3
import os
from collections import Counter
from decimal import Decimal
 
app = Flask(__name__, template_folder='templates', static_folder='static')
 
# DynamoDB initialization with AWS credentials (ensure your keys are set in your environment variables or passed securely)
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',  # Adjust your region
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
 
# DynamoDB table reference
table = dynamodb.Table('Anomalies')
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/api/anomalies', methods=['GET'])
def get_anomalies():
    # Fetch the data from DynamoDB
    response = table.scan()
    items = response['Items']
 
    # Function to convert Decimal to float
    def convert_decimals(item):
        for key, value in item.items():
            if isinstance(value, Decimal):
                item[key] = float(value)
        return item
 
    # Apply Decimal conversion to all items
    items = [convert_decimals(item) for item in items]
 
    # Filter the relevant columns
    filtered_items = [{
        'AnomalyID': item.get('AnomalyID', ''),
        'Timestamp': item.get('Timestamp', ''),
        'Prediction': item.get('Prediction', ''),
        'proto': item.get('proto', ''),
        'service': item.get('service', ''),
        'dur': item.get('dur', ''),
        'dbytes': item.get('dbytes', '')
    } for item in items]
 
    # Count the number of each unique Prediction
    prediction_counts = dict(Counter(item['Prediction'] for item in filtered_items if 'Prediction' in item))
 
    # Return the filtered anomalies and prediction counts for the chart
    return jsonify({
        'anomalies': filtered_items,
        'prediction_counts': prediction_counts
    })
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)