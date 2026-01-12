import streamlit as st
import geopandas as gpd
import rasterio
import numpy as np
from rasterio.mask import mask
from shapely.geometry import mapping
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Geospatial CVI App", layout="wide")

st.title("Geospatial CVI Streamlit App")
st.write("Analiza wskaźnika Chlorophyll Vegetation Index (CVI) z trzech rastrów Sentinel-2 i danych wektorowych (GeoJSON)")

# --- Upload plików ---
geojson_file = st.file_uploader("Wgraj plik wektorowy (GeoJSON)", type=["geojson", "json"])
red_file = st.file_uploader("Wgraj pasmo RED (B04.tif)", type=["tif", "tiff"])
nir_file = st.file_uploader("Wgraj pasmo NIR (B08.tif)", type=["tif", "tiff"])
green_file = st.file_uploader("Wgraj pasmo GREEN (B03.tif)", type=["tif", "tiff"])

if geojson_file and red_file and nir_file and green_file:

    # --- wczytanie GeoJSON ---
    gdf = gpd.read_file(geojson_file)

    # --- mapa poligonów ---
    centroid = gdf.geometry.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10)
    folium.GeoJson(gdf).add_to(m)
    st.subheader("Mapa poligonów")
    st_folium(m, width=700, height=500)

    # --- wczytanie rastrów ---
    red_src = rasterio.open(red_file)
    nir_src = rasterio.open(nir_file)
    green_src = rasterio.open(green_file)

    st.subheader("Informacje o rastrach")
    st.write("CRS RED:", red_src.crs)
    st.write("CRS NIR:", nir_src.crs)
    st.write("CRS GREEN:", green_src.crs)

    # --- wyrównanie CRS poligonów do rastra ---
    gdf = gdf.to_crs(red_src.crs)

    # --- odczyt pełnych rastrów ---
    red = red_src.read(1).astype(float) / 10000  # Sentinel-2 odbicie w skali 0-1
    nir = nir_src.read(1).astype(float) / 10000
    green = green_src.read(1).astype(float) / 10000

    # --- CVI ---
    st.subheader("Obliczanie CVI")
    np.seterr(divide='ignore', invalid='ignore')
    cvi = (nir * red) / (green ** 2)
    st.success("CVI obliczone dla całej sceny")

    # --- średnia CVI dla poligonów ---
    st.subheader("Średnia CVI dla obszarów wektorowych")
    mean_results = []

    for _, row in gdf.iterrows():
        geom = [mapping(row.geometry)]

        # maskowanie każdego pasma
        red_crop, _ = mask(red_src, geom, crop=True)
        nir_crop, _ = mask(nir_src, geom, crop=True)
        green_crop, _ = mask(green_src, geom, crop=True)

        # konwersja na float i dzielenie przez 10000
        red_m = red_crop[0].astype(float) / 10000
        nir_m = nir_crop[0].astype(float) / 10000
        green_m = green_crop[0].astype(float) / 10000

        # oblicz CVI dla maskowanego obszaru
        np.seterr(divide='ignore', invalid='ignore')
        cvi_m = (nir_m * red_m) / (green_m ** 2)

        # ignorujemy nan i inf
        cvi_m = np.where(np.isfinite(cvi_m), cvi_m, np.nan)

        # średnia tylko z wartości >0
        mean_val = np.nanmean(cvi_m[cvi_m > 0])
        mean_results.append(mean_val)

    gdf["mean_CVI"] = mean_results
    st.write(gdf[["mean_CVI"]])

else:
    st.info("Wgraj GeoJSON + B04.tif + B08.tif + B03.tif aby rozpocząć analizę.")
