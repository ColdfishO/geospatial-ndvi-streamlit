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

streamlit==1.30.0
geopandas==0.13.0
rasterio==1.3.7
shapely==2.2.3
folium==0.14.0
streamlit-folium==0.11.0
numpy==1.26.0
pandas==2.1.0


## Uruchomienie lokalne

1. Zainstaluj wymagania:

```bash
pip install -r requirements.txt

    Uruchom aplikację:

streamlit run app.py

Aplikacja uruchomi się w przeglądarce pod adresem:

http://localhost:8501

Uruchomienie w Dockerze

Przykładowy Dockerfile i docker-compose.yml pozwalają uruchomić aplikację w kontenerze:

docker-compose up --build
