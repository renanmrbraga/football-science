# app/constants/css.py
import streamlit as st
from constants.theme import get_theme_styles

def inject_custom_css() -> None:
    styles = get_theme_styles()

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&display=swap');

    /* Variáveis de tema dinâmico */
    :root {{
        --primary-color: {styles['HIGHLIGHT_COLOR']};
        --secondary-color: {styles['PRIMARY_BLUE']};
        --bg-color: {styles['BACKGROUND_COLOR']};
        --text-color: {styles['FOREGROUND_COLOR']};
        --card-bg: {styles['CARD_BACKGROUND']};

        /* Específicos para selects e dropdowns */
        --selectbox-bg: {styles['SELECTBOX_BG']};
        --selectbox-text: {styles['SELECTBOX_TEXT']};
        --dropdown-bg: {styles['DROPDOWN_BG']};
        --dropdown-text: {styles['DROPDOWN_TEXT']};
        --border-color: {styles['BORDER_COLOR']};
    }}

    /* Estilo base do app (body e containers) */
    html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {{
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
        font-family: 'Orbitron', sans-serif;
        text-color: var(--text-color) !important;
    }}

    /* Header e toolbar nativos removidos */
    [data-testid="stHeader"], [data-testid="stToolbar"] {{
        background: none !important;
    }}

    /* Padding do container principal */
    .block-container {{
        padding: 2rem 3rem;
    }}

    /* Fundo da sidebar */
    section[data-testid="stSidebar"] {{
        background-color: var(--card-bg) !important;
    }}

    /* Botões */
    .stButton > button {{
        background-color: var(--secondary-color);
        color: white;
        border-radius: 0.5rem;
        font-weight: bold;
        padding: 0.5rem 1.25rem;
        transition: all 0.3s ease-in-out;
        width: auto;
    }}

    /* Hover nos botões */
    .stButton > button:hover {{
        background-color: var(--primary-color);
        transform: scale(1.05);
    }}

    /* Selectboxes */
    div[data-baseweb="select"] > div {{
        min-height: 36px !important;
        font-size: 14px !important;
        background-color: var(--selectbox-bg) !important;
        color: var(--selectbox-text) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 0.5rem !important;
        max-width: 200px !important;
        align-items: center !important;
    }}

    div.stSelectbox > label {{
        color: var(--text-color) !important;
    }}

    /* ==== Checkbox e Radio ==== */
    .stCheckbox label,
    .stCheckbox label *,
    .stRadio label,
    .stRadio label * {{
        color: var(--text-color) !important;
    }}

    /* Dropdown */
    ul[role="listbox"] > li {{
        font-size: 14px !important;
        color: var(--dropdown-text) !important;
        background-color: var(--dropdown-bg) !important;
        border-radius: 0.4rem !important;
    }}
    /* Itens do dropdown */
    ul[role="listbox"] > li {{
        color: var(--dropdown-text) !important;
        background: var(--dropdown-bg) !important;
        padding: 0.5rem 1rem !important;
        border-radius: 0.4rem !important;
    }}

    /* Hover nos itens do dropdown */
    ul[role="listbox"] > li:hover {{
        background: var(--primary-color) !important;
        color: #ffffff !important;
    }}

    /* DataFrame, Table e Metric */
    .stDataFrame, .stTable, .stMetric {{
        background-color: var(--card-bg) !important;
        border-radius: 0.75rem;
        padding: 1rem;
        box-shadow: 0 0 6px rgba(0,198,255,0.08);
    }}

    /* Container do dropdown */
    ul[role="listbox"] {{
        background: var(--border-color) !important;
        border-radius: 0.5rem !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.15) !important;
        padding: 0.5rem !important;
    }}

    /* Remove fundo de blocos aninhados */
    div.block-container > div > div > div {{
        background-color: transparent !important;
    }}

    /* Cor de texto na sidebar */
    section[data-testid="stSidebar"] * {{
        color: var(--text-color) !important;
    }}

    /* Estilo do selectbox na sidebar */
    section[data-testid="stSidebar"] 
    .stSelectbox div[data-baseweb="select"],
    section[data-testid="stSidebar"] 
    .stSelectbox div[data-baseweb="select"] > div {{
        max-width: none !important;   /* remove o limite de 200px do global */
        width: 100% !important;       /* ocupa toda a largura disponível */
        font-weight: bold !important;
    }}

    /* Cores de títulos e texto */
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

    /* Cabeçalhos dos Dashboards */
    .dashboard-header h1 {{
        text-align: center !important;
        margin-bottom: 0 !important;
    }}

    .dashboard-header p {{
        text-align: center !important;
        margin-top: 0 !important;
        font-size: 30px !important;
        color: var(--text-color) !important;
    }}

    /* Mobile */
    @media (max-width: 768px) {{
        .block-container {{
            padding: 1rem 1.5rem !important;
        }}

        .stButton > button {{
            width: 100% !important;
            font-size: 14px !important;
        }}

        .stSelectbox div[data-baseweb="select"],
        ul[role="listbox"] > li {{
            font-size: 14px !important;
        }}

        h1 {{ font-size: 1.6rem !important; }}
        h2 {{ font-size: 1.4rem !important; }}
        h3 {{ font-size: 1.2rem !important; }}

        .stMetric > div {{
            text-align: center;
        }}

        .element-container {{
            margin-bottom: 1rem !important;
        }}

        .stRadio > div {{
            flex-direction: column !important;
        }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
