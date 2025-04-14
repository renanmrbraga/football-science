# app/main.py
import streamlit as st
import logging

st.set_page_config(page_title="Football Analysis BR", page_icon="⚽", layout="wide")

# Importa funções de tema e CSS
from app.constants.theme import init_theme, get_theme_styles
from app.components.css import inject_custom_css
from app.dashboards.clubes_dashboard import dashboard_clubes
from app.dashboards.transferencias_dashboard import dashboard_transferencias

logging.basicConfig(level=logging.INFO)

# Inicializa o seletor de tema (aparece UMA única vez na sidebar)
init_theme()

# Injeta CSS customizado (usando o tema atualmente selecionado)
inject_custom_css()

# Agora obtemos os estilos do tema para eventuais ajustes extras
theme = get_theme_styles()

st.markdown(f"""
    <style>
    section[data-testid="stSidebar"] * {{
        color: {theme['FOREGROUND_COLOR']} !important;
    }}
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] * {{
        color: black !important;
    }}
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {{
        background-color: white !important;
    }}
    </style>
""", unsafe_allow_html=True)

def main() -> None:
    dashboard_options = {
        "Clubes": dashboard_clubes,
        "Transferências": dashboard_transferencias
    }

    st.sidebar.title("📂 Navegação")
    escolha = st.sidebar.radio("Selecione o dashboard:", list(dashboard_options.keys()), key="unique_dashboard_radio")
    dashboard_options[escolha]()

if __name__ == "__main__":
    main()
