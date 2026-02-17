#!/bin/sh
set -e

# Define 8080 caso a variável PORT esteja vazia (fallback)
export PORT=${PORT:-8080}

echo "Running on port: $PORT"

echo "Starting server with Gunicorn..."
# O 'exec' é vital para que o Gunicorn receba os sinais de encerramento do Cloud Run
exec gunicorn project.wsgi:application \
    --bind 0.0.0.0:${PORT} \
    --workers 1 \
    --threads 8 \
    --timeout 0 \
    --log-level debug


O que ajustar no seu Docke