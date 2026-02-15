#!/bin/sh

echo "Esperando o MySQL ficar pronto..."

while ! nc -z dolphin 3306; do
  sleep 1
done

echo "MySQL pronto!"

echo "Adquirindo Migrações..."
python manage.py makemigrations
python manage.py makemigrations blog

echo "Aplicando migrações..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 project.wsgi:application