import streamlit as st
import geopandas as gpd
import rasterio
import numpy as np
from rasterio.mask import mask
from shapely.geometry import mapping

st.set_page_config(page_title="Geospatial App", layout="wide")

st.title("Geospatial Streamlit App")
st.write("Obsługa danych wektorowych (GeoJSON) + dwa rastry (B04 i B08), "
         "wspólne przetwarzanie i analiza NDVI")

# --- Upload plików ---
geojson_file = st.file_uploader("Wgraj plik wektorowy (GeoJSON)", type=["geojson", "json"])
red_file = st.file_uploader("Wgraj pasmo RED (B04.tif)", type=["tif", "tiff"])
nir_file = st.file_uploader("Wgraj pasmo NIR (B08.tif)", type=["tif", "tiff"])

if geojson_file and red_file and nir_file:

    # --- dane wektorowe ---
    gdf = gpd.read_file(geojson_file)
    st.subheader("Podgląd danych wektorowych")
    st.map(gdf)

    # --- otwarcie rastrów ---
    red_src = rasterio.open(red_file)
    nir_src = rasterio.open(nir_file)

    # --- sprawdzenie zgodności CRS/rozmiaru ---
    st.subheader("Informacje o rastrach")
    st.write("CRS RED:", red_src.crs)
    st.write("CRS NIR:", nir_src.crs)

    if red_src.crs != nir_src.crs:
        st.error("Różne układy współrzędnych (CRS). Przereprojektuj jeden raster.")
    else:
        # --- odczyt pełnych rastrów ---
        red = red_src.read(1).astype(float)
        nir = nir_src.read(1).astype(float)

        # --- NDVI ---
        st.subheader("Obliczanie NDVI z B04 i B08")
        np.seterr(divide='ignore', invalid='ignore')
        ndvi = (nir - red) / (nir + red)

        st.success("NDVI obliczone dla całej sceny")

        # --- średnia NDVI dla poligonów ---
        st.subheader("Średnia NDVI dla obszarów wektorowych")

        mean_results = []

        for idx, row in gdf.iterrows():
            geom = [mapping(row.geometry)]

            # maskowanie osobno RED i NIR
            red_crop, _ = mask(red_src, geom, crop=True)
            nir_crop, _ = mask(nir_src, geom, crop=True)

            red_m = red_crop[0].astype(float)
            nir_m = nir_crop[0].astype(float)

            ndvi_m = (nir_m - red_m) / (nir_m + red_m)

            mean_val = np.nanmean(ndvi_m)
            mean_results.append(mean_val)

        gdf["mean_NDVI"] = mean_results

        st.write(gdf[["mean_NDVI"]])

else:
    st.info("Wgraj: GeoJSON + B04.tif + B08.tif aby rozpocząć analizę.")
