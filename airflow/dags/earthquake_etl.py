from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from extracción_transformacion import extraer_datos, transformar_datos
from carga import crear_conexion, crear_esquema_si_no_existe, crear_tabla_si_no_existe, cargar_datos
import pandas as pd
import os

AZURE_DB_URL = "postgresql+psycopg2://innovacion_2025:Fer_13462169@innovacion-2025-server.postgres.database.azure.com:5432/postgres"
SCHEMA = "sismos"

TMP_PATH = "/opt/airflow/tmp"
CSV_FILENAME = "earthquake_data.csv"
CSV_PATH = os.path.join(TMP_PATH, CSV_FILENAME)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def etl_extract_transform():
    features = extraer_datos()
    df = transformar_datos(features)

    if df.empty:
        raise ValueError("No hay datos válidos para cargar. Verifica la magnitud mínima o la estructura de los datos.")

    # Crear carpeta temporal si no existe
    os.makedirs(TMP_PATH, exist_ok=True)

    # Guardar DataFrame a CSV temporal
    df.to_csv(CSV_PATH, index=False)
    print(f"📂 Datos guardados en archivo temporal: {CSV_PATH}")

def etl_load():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Archivo CSV no encontrado en: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    print(f"📊 Datos leídos del CSV, filas: {len(df)}")

    engine = crear_conexion(AZURE_DB_URL)
    crear_esquema_si_no_existe(engine, schema=SCHEMA)
    crear_tabla_si_no_existe(engine, schema=SCHEMA)
    cargar_datos(engine, df, schema=SCHEMA)

    # Opcional: borrar archivo tras cargar
    os.remove(CSV_PATH)
    print(f"🗑️ Archivo temporal eliminado: {CSV_PATH}")

with DAG(
    'earthquake_etl',
    default_args=default_args,
    description='ETL de datos de terremotos desde USGS a PostgreSQL en Azure',
    schedule_interval=timedelta(hours=1),
    catchup=False,
) as dag:

    extract_transform_task = PythonOperator(
        task_id='etl_extract_transform',
        python_callable=etl_extract_transform,
    )

    load_task = PythonOperator(
        task_id='etl_load',
        python_callable=etl_load,
    )

    extract_transform_task >> load_task



