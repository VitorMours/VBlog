FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn whitenoise

COPY . .

COPY entrypoint.sh /entrypoint.sh
ENV DJANGO_SETTINGS_MODULE=project.settings
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]