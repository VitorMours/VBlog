# 1. Imagem base (Python leve)
FROM python:3.11-slim

# 2. Impede que o Python gere ficheiros .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Define a pasta de trabalho dentro do container
WORKDIR /app

# 4. Instala dependências do sistema necessárias para algumas bibliotecas Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Instala as dependências do projeto
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# 6. Copia o resto do código para o container
COPY . /app/

# 7. Coleta ficheiros estáticos para o Nginx poder servir depois
RUN python manage.py collectstatic --noinput
RUN pip install gunicorn
# 8. Comando para iniciar o servidor Gunicorn
# Nota: Substitua 'core' pelo nome da pasta onde está o seu ficheiro wsgi.py
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]