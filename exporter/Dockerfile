FROM python:3.11-slim

LABEL maintainer="Data Engineering Course"
LABEL description="Prometheus exporter that reads CSV sales data"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV CSV_PATH=/data/sales_data.csv
ENV EXPORTER_PORT=8000
ENV REFRESH_INTERVAL=30

EXPOSE 8000

CMD ["python", "-u", "app.py"]
