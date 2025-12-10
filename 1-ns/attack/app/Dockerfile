FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY static/ static/
COPY templates/ templates/
COPY GeoLite2-Country.mmdb . 

EXPOSE 5000
CMD ["python", "app.py"]
