# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np


# Load model ONCE when the app starts (not on every request!)
model = joblib.load('model.pkl')


app = FastAPI()


# Define what the input should look like
class PredictRequest(BaseModel):
    features: list[float]


# Define what the output should look like
class PredictResponse(BaseModel):
    prediction: int
    model_version: str


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    # Convert input to numpy array
    features = np.array([request.features])
    
    # Make prediction
    prediction = int(model.predict(features)[0])
    
    return PredictResponse(
        prediction=prediction,
        model_version="v1.0"
    )



