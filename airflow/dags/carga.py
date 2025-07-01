from sqlalchemy import create_engine, text
import pandas as pd

def crear_conexion(db_url):
    return create_engine(db_url)

def crear_esquema_si_no_existe(engine, schema="sismos"):
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))

def crear_tabla_si_no_existe(engine, schema='sismos'):
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {schema}.terremotos (
        id VARCHAR(50) PRIMARY KEY,
        magnitud FLOAT,
        lugar TEXT,
        timestamp BIGINT,
        fecha TIMESTAMP,
        longitud FLOAT,
        latitud FLOAT,
        profundidad FLOAT
    )
    """
    with engine.connect() as conn:
        conn.execute(text(create_table_sql))

def cargar_datos(engine, df, schema='sismos'):
    insert_sql = f"""
    INSERT INTO {schema}.terremotos (
        id, magnitud, lugar, timestamp, fecha, longitud, latitud, profundidad
    ) VALUES (
        :id, :magnitud, :lugar, :timestamp, :fecha, :longitud, :latitud, :profundidad
    )
    ON CONFLICT (id) DO NOTHING;
    """

    records = df.to_dict(orient="records")

    with engine.begin() as conn:
        for row in records:
            conn.execute(text(insert_sql), row)






