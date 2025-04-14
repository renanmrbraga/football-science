# app/utils/data.py
import os
import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def load_data(csv_path: str, sep: str = ";") -> pd.DataFrame:
    """
    Carrega um arquivo CSV para um DataFrame com cache e tratamento de erro.
    """
    if not csv_path or not os.path.isfile(csv_path):
        st.error(f"Arquivo não encontrado: {csv_path}")
        return pd.DataFrame()

    try:
        return pd.read_csv(csv_path, sep=sep, encoding="utf-8")
    except Exception as e:
        st.error(f"Erro ao carregar {csv_path}: {e}")
        return pd.DataFrame()


def enrich_with_uf(df_transf: pd.DataFrame, df_clubes: pd.DataFrame) -> pd.DataFrame:
    """
    Garante que a coluna 'UF' esteja presente no dataframe de transferências.
    Faz merge com df_clubes se necessário.
    """
    if "UF" not in df_transf.columns:
        df_transf = df_transf.merge(
            df_clubes[["ID", "UF"]],
            left_on="Clube_ID",
            right_on="ID",
            how="left"
        )
    return df_transf


def ensure_all_ufs(df: pd.DataFrame, geojson: dict) -> pd.DataFrame:
    """
    Garante que todas as UFs do GeoJSON estejam no DataFrame com valor 0 caso ausentes.
    """
    ufs_geojson = [f["properties"]["SIGLA"] for f in geojson["features"]]
    df = df.set_index("UF").reindex(ufs_geojson, fill_value=0).reset_index()
    return df
