import mlflow

import os
from dotenv import load_dotenv
load_dotenv()

mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
client = mlflow.tracking.MlflowClient()

# Версія 1 → Production
client.transition_model_version_stage(
    name="iris_rf_model",
    version=2,
    stage="Production"
)

# Версія 1 → champion (replacing Production stage)
client.set_registered_model_alias(
    name="iris_rf_model",
    alias="champion",
    version=2
)