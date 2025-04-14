# app/components/cards/contratacoes_gratuitas_card.py
import streamlit as st
from app.utils.formatters import format_int
from app.constants.theme import CARD_STYLE, CARD_TITLE_STYLE, CARD_VALUE_STYLE

def render_contratacoes_gratuitas_card(valor: int) -> None:
    valor_formatado = format_int(valor)
    st.markdown(
        f"""
        <div style="{CARD_STYLE}">
            <h4 style="{CARD_TITLE_STYLE}">Contratações - Gratuitas</h4>
            <h2 style="{CARD_VALUE_STYLE}">{valor_formatado}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
