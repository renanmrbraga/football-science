# app/components/cards/ticket_medio_com_custo_card.py
import streamlit as st
from app.utils.formatters import format_currency_symbol
from app.constants.theme import get_theme_styles  # Atualização para usar a função

# Obtendo os estilos do tema
theme = get_theme_styles()
CARD_STYLE = theme["CARD_STYLE"]
CARD_TITLE_STYLE = theme["CARD_TITLE_STYLE"]
CARD_VALUE_STYLE = theme["CARD_VALUE_STYLE"]

def render_ticket_medio_com_custo_card(valor: float) -> None:
    valor_formatado = format_currency_symbol(valor)
    st.markdown(
        f"""
        <div style="{CARD_STYLE}">
            <h4 style="{CARD_TITLE_STYLE}">Ticket Médio - Com Custo</h4>
            <h2 style="{CARD_VALUE_STYLE}">{valor_formatado}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
