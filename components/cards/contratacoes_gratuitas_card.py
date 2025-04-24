# app/components/cards/contratacoes_gratuitas_card.py
import streamlit as st
from utils.formatters import format_int
from constants.theme import get_theme_styles

def render_contratacoes_gratuitas_card(valor: int) -> None:
    theme = get_theme_styles()
    valor_formatado = format_int(valor)

    card_style = (
        f"background-color: {theme['CARD_BACKGROUND']};"
        "padding: 1.2rem;"
        "border-radius: 1rem;"
        f"box-shadow: 0 0 15px {theme['HIGHLIGHT_COLOR']}55;"
        "text-align: center;"
        "min-width: 180px;"
        "transition: all 0.3s ease;"
    )

    title_style = (
        f"color: {theme['FOREGROUND_COLOR']};"
        "margin-bottom: 0.5rem;"
        "font-size: 1.05rem;"
        "font-weight: 500;"
    )

    value_style = (
        f"color: {theme['HIGHLIGHT_COLOR']};"
        "margin: 0;"
        "font-size: 1.6rem;"
        "font-weight: bold;"
    )

    st.markdown(
        f"""
        <div style="{card_style}">
            <h4 style="{title_style}">Contratações - Gratuitas</h4>
            <h2 style="{value_style}">{valor_formatado}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
