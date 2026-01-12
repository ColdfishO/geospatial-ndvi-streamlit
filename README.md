# Geospatial CVI Streamlit App

Aplikacja umożliwia:

- wczytywanie danych wektorowych (GeoJSON)  
- wczytywanie trzech rastrów Sentinel-2:  
  - B03 (GREEN)  
  - B04 (RED)  
  - B08 (NIR)  
- obliczanie wskaźnika **Chlorophyll Vegetation Index (CVI)**  
- wyznaczanie średniej CVI dla obiektów wektorowych  

## Wymagania

- Python 3.10+  
- biblioteki: `streamlit`, `geopandas`, `rasterio`, `numpy`, `shapely`, `folium`, `streamlit-folium`  

Przykładowy `requirements.txt`:

