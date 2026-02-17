#!/bin/sh
set -e

echo "Applying migrations..."
# Tenta rodar as migrações. Se falhar, o container para e você vê o erro nos logs.
python manage.py migrate --noinput

echo "Collecting static files..."
# Essencial para o WhiteNoise servir os arquivos CSS/JS corretamente
python manage.py collectstatic --noinput

echo "Starting server..."
exec gunicorn project.wsgi:application \
    --bind 0.0.0.0:${PORT:-8080} \
    --workers 1 \
    --threads 8 \
    --timeout 0