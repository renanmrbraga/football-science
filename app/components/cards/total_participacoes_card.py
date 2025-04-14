# app/components/cards/total_participacoes_card.py
import streamlit as st
from app.utils.formatters import format_int
from app.constants.theme import get_theme_styles  # Importando a função

# Acessando os estilos do tema
theme = get_theme_styles()
CARD_STYLE = theme["CARD_STYLE"]
CARD_TITLE_STYLE = theme["CARD_TITLE_STYLE"]
CARD_VALUE_STYLE = theme["CARD_VALUE_STYLE"]

def render_total_participacoes_card(valor: int) -> None:
    st.markdown(
        f"""
        <div style="{CARD_STYLE}">
            <h4 style="{CARD_TITLE_STYLE}">Participações</h4>
            <h2 style="{CARD_VALUE_STYLE}">{valor}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
