FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "calculate_distance.wsgi", "--bind", "0.0.0.0:8000"]
