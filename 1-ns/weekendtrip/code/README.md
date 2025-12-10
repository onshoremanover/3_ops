# 🗺️ Weekend Spots Map (Streamlit + Folium)

An ultra-simple web app that shows clickable pins for your 8 candidate stays. Click a pin → click **Open listing ↗** to jump to the original page.

## Run locally (Python 3.10+)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app starts on http://localhost:8501

## Run with Docker

```bash
docker build -t weekend-map-app .
docker run --rm -p 8501:8501 weekend-map-app
```

Then open http://localhost:8501

## Edit locations

Open `app.py` and edit the `PLACES` list (title, url, lat, lon, note). You can add/remove items and the map will update automatically.

> **Accuracy note:** some pins use village/park center coordinates when exact GPS wasn’t published on the listing pages. You can swap in exact lat/lon any time.