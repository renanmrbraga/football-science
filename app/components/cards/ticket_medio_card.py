# app/components/cards/ticket_medio_card.py
import streamlit as st
from app.utils.formatters import format_currency_symbol
from app.constants.theme import CARD_STYLE, CARD_TITLE_STYLE, CARD_VALUE_STYLE

def render_ticket_medio_card(valor: float) -> None:
    valor_formatado = format_currency_symbol(valor)
    st.markdown(
        f"""
        <div style="{CARD_STYLE}">
            <h4 style="{CARD_TITLE_STYLE}">Ticket Médio - Total</h4>
            <h2 style="{CARD_VALUE_STYLE}">{valor_formatado}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
