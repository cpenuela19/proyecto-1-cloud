FROM python:3.10-slim

# Instalar dependencias básicas
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto (puedes sobreescribirlo desde docker-compose)
CMD ["python", "app.py"]
