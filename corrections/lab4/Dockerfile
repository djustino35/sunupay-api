FROM python:3.13-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
RUN useradd --no-create-home --uid 10001 sunupay && chown -R sunupay /srv
USER sunupay
ENV BIND=0.0.0.0
EXPOSE 5000
HEALTHCHECK CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:5000/')"
CMD ["python", "app/app.py"]
