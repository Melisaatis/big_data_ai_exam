# FROM python:3.12.0-alpine

# WORKDIR /app

FROM python:3.12.0-alpine

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
