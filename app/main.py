# app/main.py
import streamlit as st
from app.dashboards.clubes import dashboard_clubes
from app.dashboards.transferencias import dashboard_transferencias
from app.components.styles import inject_custom_css
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO)

# Configuração da página
st.set_page_config(page_title="Dashboards de Análise", layout="wide")

# Injetar estilo customizado
inject_custom_css()

def main() -> None:
    """Função principal para seleção e exibição dos dashboards."""
    dashboard_options = {
        "Clubes": dashboard_clubes,
        "Transferências": dashboard_transferencias
    }

    st.sidebar.title("Selecione o Dashboard")
    escolha = st.sidebar.radio("Opções", list(dashboard_options.keys()))

    dashboard_options[escolha]()

if __name__ == "__main__":
    main()
