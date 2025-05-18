# Imagen base: Python 3.12 slim, liviano pero suficiente para la mayoría de apps
FROM python:3.12-slim

# Evitar prompts de debconf y mejorar logging
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo (por buenas prácticas, no usar root)
WORKDIR /app

# Copiar los archivos de requirements primero para aprovechar el cache de Docker
COPY requirements.txt .

# Instalar dependencias del sistema (si usás base de datos local tipo sqlite, podés necesitar libsqlite3)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libsqlite3-0 \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar el resto del código, assets, db, etc (usa .dockerignore para excluir archivos grandes no necesarios)
COPY . .

# (Opcional) crear un usuario no root por seguridad
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Exponer el puerto que usa streamlit (8501 por default)
EXPOSE 2000

# Comando de entrada: levanta streamlit (puede tomar config si hace falta)
CMD ["streamlit", "run", "app.py", "--server.port=2000", "--server.address=0.0.0.0"]
