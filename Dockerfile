# Imagen base con Python
FROM python:3.10-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de tu proyecto
COPY requirements.txt requirements.txt
COPY app.py app.py

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 5000 (el que usa Flask)
EXPOSE 5000

# Comando para ejecutar la app
CMD ["python", "app.py"]
