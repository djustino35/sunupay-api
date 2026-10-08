# Volontairement perfectible : image ancienne, execution en root (lab 4)
FROM python:3.9-slim-buster
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
EXPOSE 5000
CMD ["python", "app/app.py"]
