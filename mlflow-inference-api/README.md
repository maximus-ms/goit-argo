# MLflow Inference API

Докер-контейнер з FastAPI сервісом для інференсу моделей з MLflow.

## Локальне збирання та запуск

```bash
# Збірка докер-образу
docker build -t inference-api .

# Запуск контейнеру
docker run -p 8000:8080 \
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
   <your-account-id>.dkr.ecr.us-east-1.amazonaws.com
```

### 3. Збирання, тегування та публікація образу

```bash
# Збірка образу
docker build -t inference-api .

# Тегування образу для ECR
docker tag inference-api:latest \
   <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/inference-api:latest

# Публікація образу в ECR
docker push \
   <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/inference-api:latest
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

### 5. Підключення minikube до ECR репозиторіїв

#### 5.1. Створення секрету для автентифікації в ECR

```bash
# Отримання токену автентифікації для ECR
TOKEN=$(aws ecr get-login-password --region us-east-1 [ --profile your-profile-name ] )

# Створення Kubernetes секрету для автентифікації в ECR
kubectl create secret docker-registry ecr-secret \
  --docker-server=< <your-account-id>>.dkr.ecr.us-east-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$TOKEN \
  --namespace=<default>
```

#### 5.2. Використання секрету в deployment

Додайте в `deployment.yaml` або в Helm-чарт:

```yaml
spec:
  template:
    spec:
      imagePullSecrets:
      - name: ecr-secret
```

#### 5.3. Налаштування автоматичного оновлення токенів (опціонально)

Токени ECR мають обмежений час дії (12 годин). Створіть CronJob для їх оновлення:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: ecr-token-refresh
spec:
  schedule: "0 */8 * * *"  # Кожні 8 годин
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: ecr-token-refresh-sa  # Сервісний акаунт з потрібними правами
          containers:
          - name: ecr-token-refresh
            image: amazon/aws-cli:latest
            command:
            - /bin/sh
            - -c
            - |
              TOKEN=$(aws ecr get-login-password --region us-east-1)
              kubectl delete secret ecr-secret --ignore-not-found
              kubectl create secret docker-registry ecr-secret \
                --docker-server= <your-account-id>.dkr.ecr.us-east-1.amazonaws.com \
                --docker-username=AWS \
                --docker-password=$TOKEN
          restartPolicy: OnFailure
```

#### 5.4. Альтернативний спосіб для minikube

Для тестового середовища можна використати пробкидання образів (потребує ручного "затягування" нової версії іміджа):

```bash
# Спочатку отримайте образ локально
docker pull  <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/inference-api:latest

# Пробкиньте образ в minikube
minikube image load  <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/inference-api:latest
```

Потім у deployment використовуйте imagePullPolicy: IfNotPresent:

```yaml
spec:
  template:
    spec:
      containers:
      - name: inference-api
        image:  <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/inference-api:latest
        imagePullPolicy: IfNotPresent
```