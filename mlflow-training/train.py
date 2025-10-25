import os
import time
import subprocess
from dotenv import load_dotenv
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# -------------------------------
# 1. Автоматично встановлюємо залежності
# (щоб можна було запустити скрипт навіть без попереднього pip install)
# subprocess.run(["pip", "install", "-r", "requirements.txt"])

# Завантажуємо .env
load_dotenv()

# 1. Дані
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 2. Модель
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

experiment_name = f"Iris Classification [{time.strftime('%Y-%m-%d %H:%M:%S')}]"
mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
experiment_id = mlflow.create_experiment(experiment_name)

# 3. Логування в MLflow
with mlflow.start_run(experiment_id=experiment_id) as run:
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("random_state", 42)
    mlflow.log_metric("train_accuracy", clf.score(X_train, y_train))
    mlflow.log_metric("test_accuracy", clf.score(X_test, y_test))

    mlflow.sklearn.log_model(
        clf,
        name="model",
        registered_model_name="iris_rf_model"
    )

print("✅ Модель iris_rf_model зареєстрована в MLflow")
