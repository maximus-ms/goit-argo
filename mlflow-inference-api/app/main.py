from fastapi import FastAPI, Request
import mlflow.pyfunc
import pandas as pd
import os

app = FastAPI()

MODEL_NAME = os.getenv("MODEL_NAME")
MODEL_STAGE = os.getenv("MODEL_STAGE")
MODEL_URI = f"models:/{MODEL_NAME}/{MODEL_STAGE}"

model = mlflow.pyfunc.load_model(model_uri=MODEL_URI)

@app.post("/predict")
async def predict(request: Request):
    body = await request.json()
    df = pd.DataFrame(body["instances"])
    prediction = model.predict(df)
    return {"predictions": prediction.tolist()}
