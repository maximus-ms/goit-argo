# MLflow Training та Управління Моделями

## Тренування моделі

1. Переконайтесь, що змінні середовища налаштовані правильно:
   ```
   MLFLOW_TRACKING_URI=http://localhost:5000
   ```

2. Встановіть необхідні залежності:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустіть скрипт тренування:
   ```bash
   python train.py
   ```

4. Після успішного виконання, модель буде зареєстрована в MLflow Registry з назвою "iris_rf_model".

## Просування моделі (Promote)

### Використання Аліасів (Рекомендовано з MLflow 2.0+)

Аліаси замінюють стару систему "stages" (Production, Staging, тощо).

1. Щоб позначити версію моделі як "champion" (аналог Production):
   ```bash
   python promote.py
   ```

2. Код для встановлення аліасу:
   ```python
   client.set_registered_model_alias(
       name="iris_rf_model",
       alias="champion",  # аналог "Production"
       version=2  # номер версії моделі
   )
   ```

3. Звернення до моделі через аліас:
   ```python
   MODEL_URI = f"models:/{MODEL_NAME}@champion"
   ```

### Застарілий підхід (Stages)

Для сумісності зі старими версіями MLflow:

```python
client.transition_model_version_stage(
    name="iris_rf_model",
    version=2,
    stage="Production"
)
```

## Важливі примітки

- Рекомендується використовувати аліаси замість stages для нових проектів
- Для інференсу моделі використовуйте URI формату `models:/iris_rf_model@champion`
- При оновленні моделі, лише змініть версію аліасу, без необхідності оновлення коду інференсу
