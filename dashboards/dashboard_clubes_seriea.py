# app/dashboards/dashboard_clubes_seriea.py
import streamlit as st
from constants.paths import CLUBES_CSV, TRANSFERENCIAS_CSV, BRASILEIRAO_CSV
from constants.texts import TITLE_CLUBES
from constants.css import inject_custom_css
from utils.data import load_data, enrich_with_uf
from components.charts.radar_indicadores_seriea_chart import render_kpi_radar_chart
from components.charts.aproveitamento_temporada_chart import (
    render_aproveitamento_temporada_chart,
)
from components.charts.gastos_transferencias_chart import (
    render_gastos_transferencias_chart,
)
from components.charts.evolucao_eficiencia_chart import render_evolucao_eficiencia_chart
from components.charts.titulos_seriea_chart import render_titulos_seriea_chart
from components.charts.rebaixamentos_seriea_chart import (
    render_rebaixamentos_seriea_chart,
)
from components.charts.participacoes_seriea_chart import (
    render_participacoes_seriea_chart,
)


def dashboard_clubes_seriea():
    # === injeta CSS dinâmico ===
    inject_custom_css()

    # === Título ===
    st.markdown(
        """
    <div class="dashboard-header">
    <h1>Análise Estratégica dos Clubes na Série A</h1>
    <p>Compare clubes com base em desempenho, eficiência e investimento</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # === Carrega dados =======================================================
    df_clubes = load_data(CLUBES_CSV)  # tem ID e Nome Oficial
    df_transf = load_data(TRANSFERENCIAS_CSV)  # tem Clube_ID, falta Nome Oficial
    df_bras = load_data(BRASILEIRAO_CSV)  # tem Clube, Pontos, Ano

    if df_clubes.empty or df_transf.empty or df_bras.empty:
        st.error("Erro ao carregar os dados. Verifique os arquivos.")
        return

    # === Enriquecimento CONSISTENTE ==========================================
    ## 1) TRANSFERÊNCIAS → adiciona Nome Oficial via Clube_ID
    id2nome = df_clubes.set_index("ID")["Nome Oficial"]
    df_transf["Nome Oficial"] = df_transf["Clube_ID"].map(id2nome)  # NaN se não achar
    df_transf = enrich_with_uf(df_transf, df_clubes)  # UF p/ mapas, etc.

    ## 2) BRASILEIRÃO → garante Nome Oficial sem perder colunas
    if "Nome Oficial" not in df_bras.columns:
        if "Clube" in df_bras.columns:
            df_bras["Nome Oficial"] = df_bras["Clube"]
        else:
            st.error("CSV do Brasileirão não contém 'Clube' nem 'Nome Oficial'.")
            return

    # (opcional) sanity‑check rápido
    cols_needed = {"Ano", "Pontos", "Nome Oficial"}
    missing = cols_needed - set(df_bras.columns)
    if missing:
        st.error(f"df_bras está sem colunas essenciais: {sorted(missing)}")
        return

    # === selects dentro de um wrapper para CSS específico ===
    st.markdown("#### Comparar clubes")
    comparar = st.checkbox("Comparar com outro clube")
    clube_base = st.selectbox("Clube 1", sorted(df_clubes["Nome Oficial"].unique()))
    clube_comp = None
    if comparar:
        clube_comp = st.selectbox("Clube 2", sorted(df_clubes["Nome Oficial"].unique()))

    # === Desempenho ===
    st.markdown("#### Desempenho")
    col_radar, col_linha = st.columns([1, 1])
    with col_radar:
        render_kpi_radar_chart(df_clubes, df_bras, df_transf, clube_base, clube_comp)
    with col_linha:
        render_aproveitamento_temporada_chart(df_bras, clube_base, clube_comp)

    # === Gastos e eficiência ===
    st.subheader("Gastos e eficiência")
    col3, col4 = st.columns([1, 1])
    with col3:
        render_gastos_transferencias_chart(df_transf, clube_base, clube_comp)
    with col4:
        render_evolucao_eficiencia_chart(df_bras, df_transf, clube_base, clube_comp)

    # === Histórico Competitivo ===
    st.subheader("Histórico Competitivo")
    col5, col6, col7 = st.columns([1, 1, 1])
    with col5:
        render_titulos_seriea_chart(df_bras, clube_base, clube_comp)
    with col6:
        render_rebaixamentos_seriea_chart(df_clubes, clube_base, clube_comp)
    with col7:
        render_participacoes_seriea_chart(df_clubes, clube_base, clube_comp)
