FROM python:3.10-slim

WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY app/main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
