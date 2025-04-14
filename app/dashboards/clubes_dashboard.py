# app/components/clubes_dashboard.py
import streamlit as st

from app.utils.data import load_data, enrich_with_uf
from app.constants.paths import CLUBES_CSV, TRANSFERENCIAS_CSV, BRASILEIRAO_CSV
from app.constants.texts import TITLE_BRASILEIRAO, METRICS, CHARTS, ERROR_LOAD_DATA
from app.utils.data_extractor import (
    get_total_participacoes, get_media_pontos, get_ultimo_ano,
    get_saldo_transferencias, get_rebaixamentos, get_aproveitamento,
    get_internacionais
)
from app.components.cards.total_participacoes_card import render_total_participacoes_card
from app.components.cards.media_pontos_card import render_media_pontos_card
from app.components.cards.ultimo_ano_card import render_ultimo_ano_card
from app.components.cards.saldo_transferencias_card import render_saldo_transferencias_card
from app.components.cards.rebaixamentos_card import render_rebaixamentos_card
from app.components.cards.aproveitamento_card import render_aproveitamento_card
from app.components.charts.evolucao_brasileirao_chart import render_evolucao_brasileirao_chart
from app.components.charts.investimentos_chart import render_investimentos_chart


def dashboard_clubes():
    st.title(TITLE_BRASILEIRAO)

    # === Carga dos dados ===
    df_clubes = load_data(CLUBES_CSV)
    df_transf = load_data(TRANSFERENCIAS_CSV)
    df_bras = load_data(BRASILEIRAO_CSV)

    if df_clubes.empty or df_transf.empty or df_bras.empty:
        st.error(ERROR_LOAD_DATA)
        return

    # === Enriquecimento ===
    df_transf = df_transf.merge(df_clubes[["ID", "Nome Oficial"]], left_on="Clube_ID", right_on="ID", how="left")
    df_transf = enrich_with_uf(df_transf, df_clubes)
    df_bras = df_bras.merge(df_clubes[["ID", "Nome Oficial"]], left_on="Clube", right_on="Nome Oficial", how="left")

    clubes = sorted(df_clubes["Nome Oficial"].unique())
    clube = st.sidebar.selectbox("Clube", clubes)

    df_bras_clube = df_bras[df_bras["Nome Oficial"] == clube]
    df_transf_clube = df_transf[df_transf["Nome Oficial"] == clube].copy()
    df_info = df_clubes[df_clubes["Nome Oficial"] == clube].iloc[0]

    # === Indicadores ===
    st.subheader("Indicadores Gerais")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        render_total_participacoes_card(get_total_participacoes(df_info))

    with col2:
        render_rebaixamentos_card(get_rebaixamentos(df_info))

    with col3:
        render_ultimo_ano_card(get_ultimo_ano(df_info))

    with col4:
        render_media_pontos_card(get_media_pontos(df_info))

    with col5:
        render_aproveitamento_card(get_aproveitamento(df_info))

    # === Gráficos ===
    st.subheader("Gráficos")

    col1, col2 = st.columns(2)

    with col1:
        render_evolucao_brasileirao_chart(df_bras_clube, CHARTS["posicao_ano"](clube))

    with col2:
        render_investimentos_chart(df_transf_clube, CHARTS["investimentos"])
