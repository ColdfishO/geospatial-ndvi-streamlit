# Geospatial NDVI Streamlit App

Aplikacja umożliwia:
- wczytywanie danych wektorowych (GeoJSON)
- wczytywanie dwóch rastrów (B04 – RED, B08 – NIR)
- obliczanie indeksu NDVI
- wyznaczanie średniej NDVI dla obiektów wektorowych

## Uruchomienie lokalne

pip install -r requirements.txt
streamlit run app.py

## Uruchomienie w Dockerze

docker-compose up --build

Aplikacja dostępna pod:
http://localhost:8501
