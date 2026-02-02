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
