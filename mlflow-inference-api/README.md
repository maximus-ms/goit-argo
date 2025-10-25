# MLflow Inference API

Докер-контейнер з FastAPI сервісом для інференсу моделей з MLflow.

## Локальне збирання та запуск

```bash
# Збірка докер-образу
docker build -t inference-api .

# Запуск контейнеру
docker run -p 8080:8080 \
  -e MLFLOW_TRACKING_URI=http://your-mlflow-server:5000 \
  -e MODEL_NAME=iris_rf_model \
  -e MODEL_STAGE=@champion \
  inference-api
```

## Публікація в Amazon ECR

### 1. Створення репозиторія в ECR (якщо його ще немає, але ми його вже створили через terraform)

```bash
aws ecr create-repository \
  --repository-name inference-api \
  --region us-east-1 \
  --profile your-profile-name
```

### 2. Автентифікація в ECR

```bash
# Отримання токену для автентифікації в ECR
aws ecr get-login-password \
  --region us-east-1 \
  --profile your-profile-name | \
docker login --username AWS --password-stdin \
  your-account-id.dkr.ecr.us-east-1.amazonaws.com
```

### 3. Збирання, тегування та публікація образу

```bash
# Збірка образу
docker build -t inference-api .

# Тегування образу для ECR
docker tag inference-api:latest \
  your-account-id.dkr.ecr.us-east-1.amazonaws.com/inference-api:latest

# Публікація образу в ECR
docker push \
  your-account-id.dkr.ecr.us-east-1.amazonaws.com/inference-api:latest
```

### 4. Перевірка наявності образу в репозиторії

```bash
aws ecr describe-images \
  --repository-name inference-api \
  --region us-east-1 \
  --profile your-profile-name
```

## Використання образу з Helm Chart

Для деплою в Kubernetes з використанням Helm:

```bash
# Перейдіть у директорію з Helm чартом
cd helm

# Встановіть чарт
helm install mlflow-inference ./
```

## Змінні середовища для контейнера

- `MLFLOW_TRACKING_URI` - URI для підключення до MLflow серверу
- `MODEL_NAME` - назва зареєстрованої моделі в MLflow
- `MODEL_STAGE` - аліас (@champion) або стадія (Production) моделі