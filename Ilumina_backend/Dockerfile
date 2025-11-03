# Imagen base oficial de Python
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y fuerza salida sin buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crea y define el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para compilar algunas libs
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements.txt e instala dependencias Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el proyecto dentro del contenedor
COPY . /app/

# Expone el puerto 8000 para Django
EXPOSE 8000

# Ejecuta Django usando runserver (para desarrollo)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
