# app/dashboards/transferencias.py
import streamlit as st
import plotly.express as px
import pandas as pd
from app.utils.data import load_data, enrich_with_uf, ensure_all_ufs
from app.utils.geo import load_geojson
from app.components.utils import format_currency, format_int, style_plotly, style_map
from app.constants.paths import CLUBES_CSV, TRANSFERENCIAS_CSV, GEOJSON_PATH
from app.constants.texts import TITLE_TRANSFERENCIAS, WARNING_EMPTY_ENTRADAS, METRICS, CHARTS, WARNING_NO_UF_COLUMN


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

    valor_total_gasto = df_entrada["Valor"].sum()
    total_contratacoes = len(df_entrada)
    total_emprestimos = len(df_entrada[df_entrada["Empréstimo"].str.lower() == "sim"])
    contratacoes_com_custo = len(df_entrada[df_entrada["Valor"] > 0])
    contratacoes_gratuitas = len(df_entrada[df_entrada["Valor"] == 0])
    ticket_medio = valor_total_gasto / total_contratacoes if total_contratacoes else 0
    ticket_medio_com_custo = valor_total_gasto / contratacoes_com_custo if contratacoes_com_custo else 0

    st.subheader("Indicadores Gerais")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Valor Total Gasto**")
        st.markdown(f"#### R$ {format_currency(valor_total_gasto)}")
        st.markdown("**Ticket Médio - Total**")
        st.markdown(f"#### R$ {format_currency(ticket_medio)}")
        st.markdown("**Contratações - Com Custo**")
        st.markdown(f"#### {format_int(contratacoes_com_custo)}")
        st.markdown("**Total de Empréstimos**")
        st.markdown(f"#### {format_int(total_emprestimos)}")

    with col2:
        st.markdown("**Total de Contratações**")
        st.markdown(f"#### {format_int(total_contratacoes)}")
        st.markdown("**Ticket Médio - Com Custo**")
        st.markdown(f"#### R$ {format_currency(ticket_medio_com_custo)}")
        st.markdown("**Contratações - Gratuitas**")
        st.markdown(f"#### {format_int(contratacoes_gratuitas)}")

    # Gráficos
    top_10_gastos = df_entrada.groupby("Nome Oficial")["Valor"].sum().nlargest(10).reset_index()
    top_10_gastos["formatted"] = top_10_gastos["Valor"].apply(format_currency)
    grafico_top_gastos = px.bar(
        top_10_gastos.sort_values("Valor"),
        x="Valor", y="Nome Oficial", orientation="h",
        text="formatted", title=CHARTS["top_gastos"],
        color_discrete_sequence=["#003366"]
    )
    style_plotly(grafico_top_gastos)

    gastos_por_ano = df_entrada.groupby("Ano")["Valor"].sum().reset_index()
    gastos_por_ano["formatted"] = gastos_por_ano["Valor"].apply(format_currency)
    grafico_gastos = px.line(
        gastos_por_ano, x="Ano", y="Valor", markers=True,
        text="formatted", title=CHARTS["gastos_ano"],
        color_discrete_sequence=["#003366"]
    )
    style_plotly(grafico_gastos)

    st.plotly_chart(grafico_top_gastos, use_container_width=True)
    st.plotly_chart(grafico_gastos, use_container_width=True)

    # Mapa
    geojson = load_geojson(GEOJSON_PATH)
    if geojson and "UF" in df_entrada.columns:
        df_map = df_entrada.groupby("UF")["Valor"].sum().reset_index()
        df_map.columns = ["UF", "Total_Gasto"]
        df_map = ensure_all_ufs(df_map, geojson)

        st.subheader(CHARTS["mapa_transferencias"])
        fig_mapa = px.choropleth(
            df_map,
            geojson=geojson,
            locations="UF",
            featureidkey="properties.SIGLA",
            color="Total_Gasto",
            hover_data=["Total_Gasto"]
        )
        style_map(fig_mapa)
        st.plotly_chart(fig_mapa, use_container_width=True)
    else:
        st.warning(WARNING_NO_UF_COLUMN)
