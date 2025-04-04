# app/components/styles.py
import streamlit as st

def inject_custom_css() -> None:
    css_code = """
    <style>
    [data-testid="stHeader"] {
        background: none !important;
    }
    main .block-container {
        padding-top: 0 !important;
        background: none !important;
        max-width: 90%;
    }
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background: #ffffff !important;
        margin: 0;
        padding: 0;
        font-family: 'Open Sans', sans-serif !important;
    }
    * {
        color: #1a1a1a;
    }
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)
