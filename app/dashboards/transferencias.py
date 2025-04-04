# app/dashboards/transferencias.py
import json
import pandas as pd
import plotly.express as px
import streamlit as st
from app.utils.data import load_data, enrich_with_uf, ensure_all_ufs
from app.utils.geo import load_geojson
from app.components.utils import format_currency, format_int, style_plotly, style_map
from app.constants.paths import CLUBES_CSV, TRANSFERENCIAS_CSV, GEOJSON_PATH
from app.constants.texts import TITLE_TRANSFERENCIAS, WARNING_EMPTY_ENTRADAS


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
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Valor Total Gasto", f"R$ {format_currency(valor_total_gasto)}")
    col1.metric("Total de Contratações", format_int(total_contratacoes))

    col2.metric("Ticket Médio (Total)", f"R$ {format_currency(ticket_medio)}")
    col2.metric("Ticket Médio (Com Custo)", f"R$ {format_currency(ticket_medio_com_custo)}")

    col3.metric("Com Custo", format_int(contratacoes_com_custo))
    col3.metric("Gratuitas", format_int(contratacoes_gratuitas))

    col4.metric("Empréstimos", format_int(total_emprestimos))

    top_10_gastos = df_entrada.groupby("Nome Oficial")["Valor"].sum().nlargest(10).reset_index()
    top_10_gastos["formatted"] = top_10_gastos["Valor"].apply(format_currency)
    grafico_top_gastos = px.bar(
        top_10_gastos.sort_values("Valor"),
        x="Valor",
        y="Nome Oficial",
        title="Top 10 Clubes que Mais Gastaram",
        orientation="h",
        text="formatted",
        color_discrete_sequence=["#003366"]
    )
    style_plotly(grafico_top_gastos)

    gastos_por_ano = df_entrada.groupby("Ano")["Valor"].sum().reset_index()
    gastos_por_ano["formatted"] = gastos_por_ano["Valor"].apply(format_currency)
    grafico_gastos = px.line(
        gastos_por_ano,
        x="Ano",
        y="Valor",
        title="Evolução do Gasto por Ano",
        markers=True,
        text="formatted",
        color_discrete_sequence=["#003366"]
    )
    style_plotly(grafico_gastos)

    st.plotly_chart(grafico_top_gastos, use_container_width=True)
    st.plotly_chart(grafico_gastos, use_container_width=True)

    geojson = load_geojson(GEOJSON_PATH)
    if geojson and "UF" in df_entrada.columns:
        df_map = df_entrada.groupby("UF")["Valor"].sum().reset_index()
        df_map.columns = ["UF", "Total_Gasto"]
        df_map = ensure_all_ufs(df_map, geojson)
        fig_mapa = px.choropleth(
            df_map,
            geojson=geojson,
            locations="UF",
            featureidkey="properties.SIGLA",
            color="Total_Gasto",
            title="Distribuição Geográfica de Transferências"
        )
        style_map(fig_mapa)
        st.plotly_chart(fig_mapa, use_container_width=True)
    else:
        st.warning("Coluna 'UF' não encontrada. Mapa não será exibido.")
