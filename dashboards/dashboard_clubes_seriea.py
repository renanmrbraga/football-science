# app/dashboards/dashboard_clubes_seriea.py
import streamlit as st
from constants.paths import CLUBES_CSV, TRANSFERENCIAS_CSV, BRASILEIRAO_CSV
from constants.texts import TITLE_CLUBES
from utils.data import load_data, enrich_with_uf
from components.charts.radar_indicadores_seriea_chart import render_kpi_radar_chart
from components.charts.aproveitamento_temporada_chart import render_aproveitamento_temporada_chart
from components.charts.gastos_transferencias_chart import render_gastos_transferencias_chart
from components.charts.eficiencia_scatter_chart import render_eficiencia_scatter_chart
from components.charts.titulos_seriea_chart import render_titulos_seriea_chart
from components.charts.rebaixamentos_seriea_chart import render_rebaixamentos_seriea_chart
from components.charts.participacoes_seriea_chart import render_participacoes_seriea_chart


def dashboard_clubes_seriea():
    st.title("Análise Estratégica dos Clubes da Série A")

    # === Carregamento de dados ===
    df_clubes = load_data(CLUBES_CSV)
    df_transf = load_data(TRANSFERENCIAS_CSV)
    df_bras = load_data(BRASILEIRAO_CSV)

    if df_clubes.empty or df_transf.empty or df_bras.empty:
        st.error("Erro ao carregar os dados. Verifique os arquivos.")
        return

    df_transf = df_transf.merge(df_clubes[["ID", "Nome Oficial"]], left_on="Clube_ID", right_on="ID", how="left")
    df_transf = enrich_with_uf(df_transf, df_clubes)
    df_bras = df_bras.merge(df_clubes[["ID", "Nome Oficial"]], left_on="Clube", right_on="Nome Oficial", how="left")

    clubes = sorted(df_clubes["Nome Oficial"].unique())

    # === Seletor de clubes ===
    st.subheader("Análise Estratégica dos Clubes da Série A")

    st.markdown("#### Comparar clubes")
    comparar = st.checkbox("Comparar com outro clube")

    clube_base = st.selectbox("Clube 1", sorted(df_clubes["Nome Oficial"].unique()))

    clube_comp = None
    if comparar:
        clube_comp = st.selectbox("Clube 2", sorted(df_clubes["Nome Oficial"].unique()))

    # === Seção do Radar + Aproveitamento ===
    st.markdown("#### Desempenho")
    col_radar, col_linha = st.columns([1.2, 2])
    with col_radar:
        render_kpi_radar_chart(df_clubes, df_bras, df_transf, clube_base, clube_comp)
    with col_linha:
        render_aproveitamento_temporada_chart(df_bras, clube_base, clube_comp)

    # === Gastos + Eficiência ===
    st.subheader("Gastos e eficiência")
    col3, col4 = st.columns(2)
    with col3:
        render_gastos_transferencias_chart(df_transf, clube_base, clube_comp)
    with col4:
        render_eficiencia_scatter_chart(df_transf, df_bras, clube_base, clube_comp)

    # === Linha de indicadores históricos ===
    st.subheader("Histórico Competitivo")
    col5, col6, col7 = st.columns(3)
    with col5:
        render_titulos_seriea_chart(df_bras, clube_base, clube_comp)
    with col6:
        render_rebaixamentos_seriea_chart(df_clubes, clube_base, clube_comp)
    with col7:
        render_participacoes_seriea_chart(df_clubes, clube_base, clube_comp)
