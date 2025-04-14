# app/components/cards/media_pontos_card.py
import streamlit as st
from app.constants.theme import get_theme_styles  # Importando a função
from app.utils.formatters import format_int

# Acessando os estilos do tema
theme = get_theme_styles()
CARD_STYLE = theme["CARD_STYLE"]
CARD_TITLE_STYLE = theme["CARD_TITLE_STYLE"]
CARD_VALUE_STYLE = theme["CARD_VALUE_STYLE"]

def render_media_pontos_card(valor: float) -> None:
    st.markdown(
        f"""
        <div style="{CARD_STYLE}">
            <h4 style="{CARD_TITLE_STYLE}">Média de Pontos</h4>
            <h2 style="{CARD_VALUE_STYLE}">{valor:.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
