import requests
import pandas as pd

def extraer_datos():
    """Extrae datos de terremotos de la API de USGS"""
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
    response = requests.get(url)
    data = response.json()
    return data["features"]

def transformar_datos(features):
    """Transforma los datos en un DataFrame estructurado"""
    df = pd.json_normalize(features)
    
    # Selección y transformación de columnas
    df_min = df[[
        "id",
        "properties.mag",
        "properties.place",
        "properties.time",
        "geometry.coordinates"
    ]].copy()
    
    df_min.columns = ["id", "magnitud", "lugar", "timestamp", "coordenadas"]
    df_min["fecha"] = pd.to_datetime(df_min["timestamp"], unit="ms")
    df_min[["longitud", "latitud", "profundidad"]] = pd.DataFrame(
        df_min["coordenadas"].to_list(), 
        index=df_min.index
    )
    
    # Filtrar sismos mayores a 4.0
    df_final = df_min[df_min["magnitud"] > 4.0].reset_index(drop=True)
    
    return df_final
import requests
import pandas as pd

def extraer_datos():
    """Extrae datos de terremotos de la API de USGS"""
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        features = data.get("features", [])
        if not features:
            raise ValueError("No se encontraron datos en la API.")
        return features
    except Exception as e:
        raise RuntimeError(f"Error al extraer datos de USGS: {e}")

def transformar_datos(features):
    """Transforma los datos en un DataFrame estructurado"""
    df = pd.json_normalize(features)
    
    df_min = df[[
        "id",
        "properties.mag",
        "properties.place",
        "properties.time",
        "geometry.coordinates"
    ]].copy()
    
    df_min.columns = ["id", "magnitud", "lugar", "timestamp", "coordenadas"]
    df_min["fecha"] = pd.to_datetime(df_min["timestamp"], unit="ms")
    df_min[["longitud", "latitud", "profundidad"]] = pd.DataFrame(
        df_min["coordenadas"].to_list(),
        index=df_min.index
    )
    
    df_final = df_min[df_min["magnitud"] > 4.0].reset_index(drop=True)
    return df_final
