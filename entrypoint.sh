#!/bin/sh
set -e

# Define 8080 caso a variável PORT esteja vazia (fallback)
export PORT=${PORT:-8080}

echo "Running on port: $PORT"

# Executa as tarefas de setup em BACKGROUND e inicia o servidor
python manage.py collectstatic --noinput &
python manage.py makemigrations &
python manage.py makemigrations blog &
python manage.py migrate &

echo "Starting server with Gunicorn..."
# O 'exec' é vital para que o Gunicorn receba os sinais de encerramento do Cloud Run
exec gunicorn project.wsgi:application \
    --bind 0.0.0.0:${PORT} \
    --workers 1 \
    --threads 8 \
    --timeout 0 \
    --log-level debug