FROM python:3.10

# Instalar dependencias del sistema y Ollama
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Instalar Ollama
RUN curl -fsSL https://ollama.com/install.sh | bash

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Definir comando de inicio
CMD ["python", "app.py"]
