FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY analyze_sensor_data.py .
COPY data/capteur_temp.csv .

CMD ["python", "analyze_sensor_data.py", "capteur_temp.csv"]