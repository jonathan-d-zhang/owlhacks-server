FROM python:3.10.7-slim-bullseye

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py main.py
COPY redis.conf redis.conf
COPY .env .env

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80
