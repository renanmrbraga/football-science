# app/constants/css.py
import streamlit as st
from app.constants.theme import get_theme_styles

def inject_custom_css() -> None:
    """Injeta CSS customizado com base no tema atual (claro/escuro)."""
    styles = get_theme_styles()

    is_light_theme = styles["BACKGROUND_COLOR"].strip().lower() == "#ffffff"

    selectbox_bg = "#ffffff" if is_light_theme else "var(--card-bg)"
    selectbox_text = "#000000" if is_light_theme else "var(--text-color)"
    dropdown_bg = "#ffffff" if is_light_theme else "var(--card-bg)"
    dropdown_text = "#000000" if is_light_theme else "var(--text-color)"
    border_color = styles["HIGHLIGHT_COLOR"] if is_light_theme else "var(--primary-color)"

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&display=swap');

    /* === VARIÁVEIS DE TEMA === */
    :root {{
        --primary-color: {styles['HIGHLIGHT_COLOR']};
        --secondary-color: {styles['PRIMARY_BLUE']};
        --bg-color: {styles['BACKGROUND_COLOR']};
        --text-color: {styles['FOREGROUND_COLOR']};
        --card-bg: {styles['CARD_BACKGROUND']};
    }}

    /* === ESTILOS GLOBAIS === */
    html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {{
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
        font-family: 'Orbitron', sans-serif;
    }}

    [data-testid="stHeader"], [data-testid="stToolbar"] {{
        background: none !important;
    }}

    .block-container {{
        padding: 2rem 3rem;
    }}

    h1, h2, h3, h4, h5, h6,
    .markdown-text-container p,
    .stMarkdown p,
    .stMarkdown span,
    .stText,
    .stTitle,
    .stSubheader,
    .stCaption {{
        color: var(--text-color) !important;
    }}

    /* === BOTÕES === */
    .stButton > button {{
        background-color: var(--secondary-color);
        color: white;
        border-radius: 0.5rem;
        font-weight: bold;
        padding: 0.5rem 1.25rem;
        transition: all 0.3s ease-in-out;
    }}

    .stButton > button:hover {{
        background-color: var(--primary-color);
        transform: scale(1.05);
    }}

    /* === TABELAS E MÉTRICAS === */
    .stDataFrame, .stTable, .stMetric {{
        background-color: var(--card-bg) !important;
        border-radius: 0.75rem;
        padding: 1rem;
        box-shadow: 0 0 6px rgba(0,198,255,0.08);
    }}

    /* === SIDEBAR === */
    section[data-testid="stSidebar"] {{
        background-color: var(--card-bg) !important;
    }}

    section[data-testid="stSidebar"] * {{
        color: var(--text-color) !important;
    }}

    /* === SELECTBOX (tema adaptável) === */
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {{
        background: {selectbox_bg} !important;
        color: {selectbox_text} !important;
        border: 1px solid {border_color} !important;
        border-radius: 0.5rem !important;
        font-weight: bold !important;
        -webkit-text-fill-color: {selectbox_text} !important;
    }}

    section[data-testid="stSidebar"] .stSelectbox input[type="text"] {{
        background: {selectbox_bg} !important;
        color: {selectbox_text} !important;
        caret-color: {selectbox_text} !important;
        font-weight: bold !important;
        -webkit-text-fill-color: {selectbox_text} !important;
    }}

    ul[role="listbox"] {{
        background: {dropdown_bg} !important;
    }}

    ul[role="listbox"] > li {{
        color: {dropdown_text} !important;
        background: {dropdown_bg} !important;
    }}

    ul[role="listbox"] > li:hover {{
        background: {styles['HIGHLIGHT_COLOR']} !important;
        color: #ffffff !important;
    }}

    /* === CORRIGE CONTAINER TRANSPARENTE === */
    div.block-container > div > div > div {{
        background-color: transparent !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
