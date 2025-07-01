import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pydeck as pdk
import altair as alt
import plotly.express as px
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------
# CONFIGURACIÓN DE CONEXIÓN
# ------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

# ------------------------
# CARGA DE DATOS
# ------------------------
def cargar_datos():
    engine = create_engine(DATABASE_URL)
    query = "SELECT * FROM sismos.terremotos ORDER BY fecha DESC LIMIT 1000"
    conn = engine.raw_connection()
    try:
        df = pd.read_sql_query(query, conn)
    finally:
        conn.close()
    return df

# ------------------------
# APP STREAMLIT
# ------------------------
st.set_page_config(page_title="Sismos en Tiempo Real", layout="wide")
st.title("🌍 Dashboard de Sismos - Datos desde USGS")

try:
    df = cargar_datos()
    df = df.rename(columns={"latitud": "latitude", "longitud": "longitude"})
    df["fecha"] = pd.to_datetime(df["fecha"])

    # ------------------------
    # 🧹 LIMPIEZA Y NORMALIZACIÓN
    # ------------------------
    df = df.dropna(subset=["latitude", "longitude", "magnitud", "profundidad"])
    df = df[df["magnitud"].between(0, 10)]
    df = df[df["latitude"].between(-75, 75)]  # evitar distorsión polar

    # Escalado logarítmico de magnitud para tamaño visual
    df["radio_visual"] = np.log1p(df["magnitud"]) * 30000  # ajustado

    # ------------------------
    # 🎚️ FILTROS
    # ------------------------
    st.sidebar.header("🎛️ Filtros")

    # Rango de fechas
    fecha_min = df["fecha"].min().date()
    fecha_max = df["fecha"].max().date()
    rango_fecha = st.sidebar.date_input(
        "📅 Rango de fechas",
        [fecha_min, fecha_max],
        min_value=fecha_min,
        max_value=fecha_max
    )
    if len(rango_fecha) == 2:
        df = df[
            (df["fecha"] >= pd.to_datetime(rango_fecha[0])) &
            (df["fecha"] <= pd.to_datetime(rango_fecha[1]))
        ]

    # Rango de magnitudes
    magn_min = float(df["magnitud"].min())
    magn_max = float(df["magnitud"].max())
    magn_range = st.sidebar.slider(
        "📊 Rango de magnitudes",
        min_value=0.0,
        max_value=10.0,
        value=(magn_min, magn_max),
        step=0.1
    )
    df = df[df["magnitud"].between(*magn_range)]

    st.write(f"📅 Mostrando datos entre {rango_fecha[0]} y {rango_fecha[1]} - {len(df)} registros")

    # ------------------------
    # 📋 TABLA DE DATOS
    # ------------------------
    with st.expander("🗃️ Ver tabla de datos"):
        st.dataframe(df)

    # ------------------------
    # 🗺️ MAPA INTERACTIVO DE SISMOS
    # ------------------------
    st.subheader("🌐 Mapa interactivo de sismos")

    neon_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[longitude, latitude]',
        get_color='[0, 255, 255, 160]',
        get_radius='radio_visual',
        pickable=True,
    )

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=df["latitude"].mean(),
            longitude=df["longitude"].mean(),
            zoom=2,
            pitch=0,
        ),
        layers=[neon_layer],
        tooltip={"text": "Lugar: {lugar}\nMagnitud: {magnitud}\nProfundidad: {profundidad} km"},
    ))

    # ------------------------
    # 📈 EVOLUCIÓN TEMPORAL DE MAGNITUDES
    # ------------------------
    st.subheader("📈 Evolución temporal de magnitudes")

    chart_temporal = alt.Chart(df).mark_line(point=True, color="#39ff14").encode(
        x=alt.X('fecha:T', title='Fecha'),
        y=alt.Y('magnitud:Q', title='Magnitud'),
        tooltip=['fecha:T', 'magnitud:Q', 'lugar:N']
    ).properties(width=700, height=300).configure_axis(
        labelColor='white',
        titleColor='white'
    )

    st.altair_chart(chart_temporal, use_container_width=True)

    # ------------------------
    # 📊 MAGNITUD VS PROFUNDIDAD
    # ------------------------
    st.subheader("📊 Magnitud vs Profundidad")

    fig = px.scatter(
        df,
        x="profundidad",
        y="magnitud",
        color="magnitud",
        size="magnitud",
        hover_data=["lugar", "fecha"],
        color_continuous_scale="Turbo",
        template="plotly_dark"
    )
    fig.update_traces(marker=dict(line=dict(width=0.5, color='white')))
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"❌ Error al cargar los datos: {e}")


