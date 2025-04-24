# app/constants/css.py
import streamlit as st
from constants.theme import get_theme_styles

def inject_custom_css() -> None:
    styles = get_theme_styles()

    is_light_theme = styles["BACKGROUND_COLOR"].strip().lower() in ["#ffffff", "#fff", "white"]
    selectbox_bg = "#ffffff" if is_light_theme else "var(--card-bg)"
    selectbox_text = "#000000" if is_light_theme else "var(--text-color)"
    dropdown_bg = "#ffffff" if is_light_theme else "var(--card-bg)"
    dropdown_text = "#000000" if is_light_theme else "var(--text-color)"
    border_color = styles["HIGHLIGHT_COLOR"] if is_light_theme else "var(--primary-color)"

    css = f"""
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
        width: auto;
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

    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {{
        background-color: {selectbox_bg} !important;
        color: {selectbox_text} !important;
        border: 1px solid {border_color} !important;
        border-radius: 0.5rem !important;
        font-weight: bold !important;
    }}

    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] * {{
        color: {selectbox_text} !important;
        background-color: {selectbox_bg} !important;
        -webkit-text-fill-color: {selectbox_text} !important;
        border-color: {border_color} !important;
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
        border-radius: 0.5rem !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.15) !important;
        padding: 0.5rem !important;
    }}

    ul[role="listbox"] > li {{
        color: {dropdown_text} !important;
        background: {dropdown_bg} !important;
        padding: 0.5rem 1rem !important;
        border-radius: 0.4rem !important;
    }}

    ul[role="listbox"] > li:hover {{
        background: {styles['HIGHLIGHT_COLOR']} !important;
        color: #ffffff !important;
    }}

    div.block-container > div > div > div {{
        background-color: transparent !important;
    }}

    /* ========== MOBILE RESPONSIVE ========== */
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
