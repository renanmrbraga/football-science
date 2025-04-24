# app/utils/geo.py
import json
import os
import streamlit as st
from typing import Optional

def load_geojson(path: str) -> Optional[dict]:
    """Carrega e ajusta o GeoJSON adicionando a chave 'name' com valor da 'SIGLA' dentro de 'properties'."""
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            geojson = json.load(f)

        for feature in geojson.get("features", []):
            sigla = feature.get("properties", {}).get("SIGLA")
            if sigla:
                feature["properties"]["name"] = sigla

        return geojson
    except Exception as e:
        st.error(f"Erro ao carregar geojson: {e}")
        return None
