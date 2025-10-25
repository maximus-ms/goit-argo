import os
from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.pyfunc
from dotenv import load_dotenv
import subprocess
import uvicorn

load_dotenv()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
MODEL_NAME = os.getenv("MODEL_NAME")
MODEL_STAGE = os.getenv("MODEL_STAGE")

# -------------------------------
# 3. Завантаження моделі з MLflow Registry
MODEL_URI = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
model = mlflow.pyfunc.load_model(MODEL_URI)

# -------------------------------
# 4. FastAPI
app = FastAPI()

class InputData(BaseModel):
    features: list

@app.post("/predict")
def predict(data: InputData):
    preds = model.predict([data.features])
    print(f"Predictions: {preds}")
    return {"predictions": preds.tolist()}

if __name__ == "__main__":
    print(f"start inference-api")
    print(f"ENV: {os.getenv('MLFLOW_TRACKING_URI')}")
    print(f"ENV: {os.getenv('MODEL_NAME')}")
    print(f"ENV: {os.getenv('MODEL_STAGE')}")
    print(f"ENV: {MODEL_URI}")
    print(f"Model: {model}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
