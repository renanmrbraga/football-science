# app/utils/geo.py
import json
import os
from typing import Optional

def load_geojson(path: str) -> Optional[dict]:
    """Carrega um arquivo GeoJSON."""
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return None

def get_uf_list_from_geojson(geojson: dict) -> list[str]:
    """Extrai as siglas de UF do GeoJSON."""
    try:
        return [feat["properties"]["SIGLA"] for feat in geojson.get("features", [])]
    except Exception:
        return []
