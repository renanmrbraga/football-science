# app/components/css.py
import streamlit as st
from app.constants.theme import get_theme_styles

def inject_custom_css() -> None:
    styles = get_theme_styles()
    css_code = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&display=swap');
    :root {{
        --primary-color: {styles['HIGHLIGHT_COLOR']};
        --secondary-color: {styles['PRIMARY_BLUE']};
        --bg-color: {styles['BACKGROUND_COLOR']};
        --text-color: {styles['FOREGROUND_COLOR']};
        --card-bg: {styles['CARD_BACKGROUND']};
    }}

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

    .stDataFrame, .stTable, .stMetric {{
        background-color: var(--card-bg) !important;
        border-radius: 0.75rem;
        padding: 1rem;
        box-shadow: 0 0 6px rgba(0,198,255,0.08);
    }}

    section[data-testid="stSidebar"] {{
        background-color: var(--card-bg) !important;
    }}

    section[data-testid="stSidebar"] * {{
        color: var(--text-color) !important;
    }}

    /* Fix para container transparente */
    div.block-container > div > div > div {{
        background-color: transparent !important;
    }}
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)
