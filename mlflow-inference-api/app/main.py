from fastapi import FastAPI, Request
from pydantic import BaseModel
# import mlflow.pyfunc
# import pandas as pd
import os

app = FastAPI()

MODEL_NAME = os.getenv("MODEL_NAME")
MODEL_STAGE = os.getenv("MODEL_STAGE")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
MODEL_URI = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0.2")

print(f"MLFLOW_TRACKING_URI: {MLFLOW_TRACKING_URI}")
print(f"MODEL_NAME: {MODEL_NAME}")
print(f"MODEL_STAGE: {MODEL_STAGE}")
print(f"MODEL_URI: {MODEL_URI}")
print(f"MODEL_VERSION: {MODEL_VERSION}")

# model = mlflow.pyfunc.load_model(model_uri=MODEL_URI)
# print(f"Model: {model}")

class InputData(BaseModel):
    features: list

@app.post("/predict")
def predict(data: InputData):
    # df = pd.DataFrame(body["instances"])
    # prediction = model.predict(df)
    # return {"predictions": prediction.tolist()}
    return {"predictions": data.features + [42]}

@app.post("/version")
def version():
    return {"version": MODEL_VERSION}
