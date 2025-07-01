FROM apache/airflow:2.5.1

USER root

# Instalar librerías necesarias para compilar psycopg2 (usado por airflow-providers-postgres)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

USER airflow

# Instalación de dependencias compatibles con Python 3.7 y Airflow 2.5.1
RUN pip install --no-cache-dir \
    pandas==1.3.5 \
    requests==2.28.1 \
    psycopg2-binary==2.9.5 \
    sqlalchemy==1.4.46 \
    apache-airflow-providers-postgres==5.3.1 \
    python-dotenv==0.21.1

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1





    