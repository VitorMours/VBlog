#!/bin/sh
set -e

# Define 8080 caso a variável PORT esteja vazia (fallback)
export PORT=${PORT:-8080}

echo "Running on port: $PORT"

# Executa as tarefas de setup (síncronas) antes de iniciar o servidor.
# Rodar colet static e migrações aqui garante que os arquivos estáticos
# existam em `STATIC_ROOT` antes do Gunicorn arrancar no Cloud Run.
python manage.py collectstatic --noinput
# Criar migrações e aplicar (não falhará se não houver mudanças)
python manage.py makemigrations --noinput || true
python manage.py makemigrations blog --noinput || true
python manage.py migrate --noinput

echo "Starting server with Gunicorn..."
# O 'exec' é vital para que o Gunicorn receba os sinais de encerramento do Cloud Run
exec gunicorn project.wsgi:application \
    --bind 0.0.0.0:${PORT} \
    --workers 1 \
    --threads 8 \
    --timeout 0 \
    --log-level debug