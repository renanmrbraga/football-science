# app/components/transferencias_dashboard.py
import streamlit as st
from utils.data import load_data, enrich_with_uf
from utils.data_extractor import (
    get_valor_total_gasto, get_total_contratacoes, get_contratacoes_com_custo,
    get_ticket_medio_com_custo
)
from constants.paths import CLUBES_CSV, TRANSFERENCIAS_CSV
from constants.texts import TITLE_TRANSFERENCIAS, WARNING_EMPTY_ENTRADAS, CHARTS
from components.cards.valor_total_gasto_card import render_valor_total_gasto_card
from components.cards.contratacoes_com_custo_card import render_contratacoes_com_custo_card
from components.cards.total_contratacoes_card import render_total_contratacoes_card
from components.cards.ticket_medio_com_custo_card import render_ticket_medio_com_custo_card
from components.charts.top_gastos_chart import render_top_gastos_chart
from components.charts.gastos_por_ano_chart import render_gastos_por_ano_chart
from components.maps.transferencias_map import render_mapa_transferencias_chart

def dashboard_transferencias():
    st.title(TITLE_TRANSFERENCIAS)

    df = load_data(TRANSFERENCIAS_CSV)
    df_clubes = load_data(CLUBES_CSV)

    if df.empty or df_clubes.empty:
        st.error("Erro ao carregar os dados.")
        st.stop()

    df = df.merge(df_clubes[['ID', 'Nome Oficial']], left_on="Clube_ID", right_on="ID", how="left")
    df = enrich_with_uf(df, df_clubes)

    df_entrada = df[df["Tipo"].str.lower() == "entrada"]
    if df_entrada.empty:
        st.warning(WARNING_EMPTY_ENTRADAS)
        st.stop()

    valor_total_gasto = get_valor_total_gasto(df_entrada)
    total_contratacoes = get_total_contratacoes(df_entrada)
    contratacoes_com_custo = get_contratacoes_com_custo(df_entrada)
    ticket_medio_com_custo = get_ticket_medio_com_custo(df_entrada)

    st.subheader("Indicadores Gerais")
    cols = st.columns(2 if st.session_state.get("is_mobile") else 4)

    with cols[0]: render_total_contratacoes_card(total_contratacoes)
    with cols[1]: render_valor_total_gasto_card(valor_total_gasto)
    if len(cols) > 2:
        with cols[2]: render_contratacoes_com_custo_card(contratacoes_com_custo)
        with cols[3]: render_ticket_medio_com_custo_card(ticket_medio_com_custo)
    else:
        render_contratacoes_com_custo_card(contratacoes_com_custo)
        render_ticket_medio_com_custo_card(ticket_medio_com_custo)

    st.subheader("Gráficos")

    col1, col2 = st.columns(1 if st.session_state.get("is_mobile") else 2)
    with col1: render_top_gastos_chart(df_entrada, CHARTS["top_gastos"])
    with col2: render_gastos_por_ano_chart(df_entrada, CHARTS["gastos_ano"])

    render_mapa_transferencias_chart(df_entrada, CHARTS["mapa_transferencias"])
