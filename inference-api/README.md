# Інференс Моделі

## Запуск API для інференсу

1. Переконайтесь, що змінні середовища налаштовані правильно:
   ```
   MLFLOW_TRACKING_URI=http://localhost:5000
   MODEL_NAME=iris_rf_model
   MODEL_STAGE=@champion  # Новий формат з аліасами
   # або 
   # MODEL_STAGE=Production  # Старий формат зі стадіями
   ```

2. Встановіть необхідні залежності:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустіть API сервіс:
   ```bash
   python -m app.main
   #or
   python app.main.py
   ```

4. API буде доступне за адресою: http://localhost:8000

## Виконання ручного інференсу

### Через curl

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

### Через Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={"features": [5.1, 3.5, 1.4, 0.2]}
)

print(response.json())
```

### Через Swagger UI

1. Відкрийте у браузері: http://localhost:8000/docs
2. Розгорніть ендпоінт POST /predict
3. Натисніть "Try it out"
4. Введіть дані у форматі JSON:
   ```json
   {
     "features": [5.1, 3.5, 1.4, 0.2]
   }
   ```
5. Натисніть "Execute"

## Формат даних

- **Вхідні дані:** JSON об'єкт з полем "features", яке містить список числових значень (4 характеристики квітки Iris)
- **Вихідні дані:** JSON об'єкт з полем "predictions", яке містить передбачений клас (0, 1 або 2 - відповідає видам Iris)

Приклад відповіді:
```json
{
  "predictions": [0]
}
```
