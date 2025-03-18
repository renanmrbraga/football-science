import os
import json
import base64
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Transferências - Completo",
    layout="wide"
)

@st.cache_data
def load_data(csv_path: str) -> pd.DataFrame:
    """Carrega dados do CSV e converte a coluna 'Valor' para numérico."""
    if not os.path.isfile(csv_path):
        st.error(f"Arquivo não encontrado: {csv_path}")
        return pd.DataFrame()
    df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
    return df

def format_currency(n):
    """Formata número como moeda: separador de milhares = ponto; decimal = vírgula."""
    return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_int(n):
    """Formata número inteiro: separador de milhares = ponto."""
    return f"{n:,}".replace(",", "X").replace(".", ",").replace("X", ".")

# Caminhos e carregamento dos dados
csv_file_path = os.getenv("ARQUIVO_TRANSFERENCIAS_PROCESSED")
df = load_data(csv_file_path)
if df.empty:
    st.stop()

st.title("Transferências dos Clubes da Série A - Últimos 10 Anos")

# Filtrar entradas
df_entrada = df[df["Tipo"].str.lower() == "entrada"]
if df_entrada.empty:
    st.warning("Não há dados de transferências de entrada disponíveis.")
    st.stop()

# Cálculo das métricas gerais
valor_total_gasto = df_entrada["Valor"].sum()
total_contratacoes = len(df_entrada)
total_emprestimos = len(df_entrada[df_entrada["Empréstimo"].str.lower() == "sim"])

# Agrupamento para o mapa
df_map = df_entrada.groupby("UF").agg({
    "Valor": "sum",
    "Nome Oficial": "count"
}).reset_index()
df_map.columns = ["UF", "Total_Gasto", "Total_Contratacoes"]

# Carregar GeoJSON dos estados
geojson_path = os.getenv("ARQUIVO_GEOJSON")
if os.path.isfile(geojson_path):
    with open(geojson_path, "r", encoding="utf-8") as f:
        states_geojson = json.load(f)
else:
    states_geojson = None
    st.warning("Arquivo geojson não encontrado. O mapa não pode ser exibido.")

# Criar DataFrame com todos os estados
if states_geojson is not None:
    siglas = [feat["properties"]["SIGLA"] for feat in states_geojson["features"]]
    df_all_states = pd.DataFrame({"UF": siglas})
    df_map_full = df_all_states.merge(df_map, on="UF", how="left").fillna(0)
else:
    df_map_full = df_map

# CSS para fundo branco e texto preto negrito com fonte Open Sans
css_code = """
<style>
/* Remover fundo do cabeçalho e ajustar container */
[data-testid="stHeader"] {
    background: none !important;
}
main .block-container {
    padding-top: 0 !important;
    background: none !important;
}

/* Fundo branco para toda a página */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #ffffff !important;
    margin: 0;
    padding: 0;
}

/* Todo o texto em preto, negrito e com fonte Open Sans Bold */
* {
    color: #000000 !important;
    font-weight: bold !important;
    font-family: 'Open Sans Bold', sans-serif !important;
}

/* Cards de métricas com fundo branco */
.metric-card {
    border-radius: 16px;
    background-color: #ffffff;
    padding: 16px;
    margin-bottom: 16px;
    text-align: center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
}
.metric-title {
    font-size: 16px;
    margin-bottom: 4px;
}
.metric-value {
    font-size: 20px;
}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)


def style_plotly(fig):
    """Aplica estilo aos gráficos Plotly com fundo branco e texto preto negrito."""
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#000000", size=14, family="Open Sans Bold"),
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(
            tickfont=dict(family="Open Sans Bold", color="#000000", size=14),
            title_font=dict(family="Open Sans Bold", color="#000000", size=16)
        ),
        yaxis=dict(
            tickfont=dict(family="Open Sans Bold", color="#000000", size=14),
            title_font=dict(family="Open Sans Bold", color="#000000", size=16)
        )
    )


def style_map(fig):
    """Aplica estilo ao mapa Plotly, configurando a legenda em negrito."""
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#000000", size=14, family="Open Sans Bold"),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    fig.update_geos(
        bgcolor="#ffffff",
        fitbounds="locations",
        visible=False
    )
    fig.update_coloraxes(colorbar=dict(
        title=dict(
            text=fig.layout.coloraxis.colorbar.title.text
                 if fig.layout.coloraxis and fig.layout.coloraxis.colorbar and fig.layout.coloraxis.colorbar.title.text
                 else "Total Gasto (R$)",
            font=dict(color="#000000", size=16, family="Open Sans Bold")
        ),
        tickfont=dict(color="#000000", size=14, family="Open Sans Bold")
    ))


# Criar gráficos

# 1) Top 10 Gastos
top_10_gastos = df_entrada.groupby("Nome Oficial")["Valor"].sum().nlargest(10).reset_index()
top_10_gastos = top_10_gastos.sort_values(by="Valor", ascending=True)
top_10_gastos["formatted"] = top_10_gastos["Valor"].apply(format_currency)
grafico_top_gastos = px.bar(
    top_10_gastos,
    x="Valor",
    y="Nome Oficial",
    title="Top 10 Clubes que Mais Gastaram",
    orientation="h",
    text=top_10_gastos["formatted"],
    color_discrete_sequence=["#003366"]
)
style_plotly(grafico_top_gastos)

# 2) Top 10 Contratações
top_10_contratacoes = df_entrada["Nome Oficial"].value_counts().nlargest(10).reset_index()
top_10_contratacoes.columns = ["Nome Oficial", "Quantidade"]
top_10_contratacoes = top_10_contratacoes.sort_values(by="Quantidade", ascending=True)
top_10_contratacoes["formatted"] = top_10_contratacoes["Quantidade"].apply(format_int)
grafico_top_contratacoes = px.bar(
    top_10_contratacoes,
    x="Quantidade",
    y="Nome Oficial",
    title="Top 10 Clubes que Mais Contrataram",
    orientation="h",
    text=top_10_contratacoes["formatted"],
    color_discrete_sequence=["#003366"]
)
style_plotly(grafico_top_contratacoes)

# 3) Gastos por Ano
gastos_por_ano = df_entrada.groupby("Ano")["Valor"].sum().reset_index()
gastos_por_ano = gastos_por_ano[gastos_por_ano["Ano"] <= 2024]
gastos_por_ano["formatted"] = gastos_por_ano["Valor"].apply(format_currency)
grafico_gastos = px.line(
    gastos_por_ano,
    x="Ano",
    y="Valor",
    title="Evolução do Gasto por Ano",
    markers=True,
    color_discrete_sequence=["#003366"]
)
grafico_gastos.update_traces(text=gastos_por_ano["formatted"], textposition="top center")
grafico_gastos.update_layout(xaxis=dict(tickmode="linear"))
style_plotly(grafico_gastos)

# 4) Contratações por Ano
contratacoes_por_ano = df_entrada.groupby("Ano").size().reset_index(name="Quantidade")
contratacoes_por_ano = contratacoes_por_ano[contratacoes_por_ano["Ano"] <= 2024]
contratacoes_por_ano["formatted"] = contratacoes_por_ano["Quantidade"].apply(format_int)
grafico_contratacoes = px.line(
    contratacoes_por_ano,
    x="Ano",
    y="Quantidade",
    title="Evolução das Contratações por Ano",
    markers=True,
    color_discrete_sequence=["#003366"]
)
grafico_contratacoes.update_traces(text=contratacoes_por_ano["formatted"], textposition="top center")
grafico_contratacoes.update_layout(xaxis=dict(tickmode="linear"))
style_plotly(grafico_contratacoes)

# Layout: 4 colunas (métricas, 2 colunas de gráficos e mapa)
col1, col2, col3, col4 = st.columns([0.5, 1, 1, 1.5])

# Coluna 1: Métricas
with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">💰 Valor Total Gasto</div>
            <div class="metric-value">R$ {format_currency(valor_total_gasto)}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">📋 Total de Contratações</div>
            <div class="metric-value">{format_int(total_contratacoes)}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">🔄 Total de Empréstimos</div>
            <div class="metric-value">{format_int(total_emprestimos)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Coluna 2: Dois gráficos (Top 10 Gastos e Gastos por Ano)
with col2:
    st.plotly_chart(grafico_top_gastos, use_container_width=True)
    st.plotly_chart(grafico_gastos, use_container_width=True)

# Coluna 3: Dois gráficos (Top 10 Contratações e Contratações por Ano)
with col3:
    st.plotly_chart(grafico_top_contratacoes, use_container_width=True)
    st.plotly_chart(grafico_contratacoes, use_container_width=True)

# Coluna 4: Mapa
with col4:
    if states_geojson is not None:
        blue_scale = [
            "#e6f2ff",  # muito claro
            "#b3cde0",
            "#80a9d0",
            "#4d85bf",
            "#1a60af",
            "#003366"   # escuro
        ]
        grafico_mapa = px.choropleth(
            df_map_full,
            geojson=states_geojson,
            locations="UF",
            featureidkey="properties.SIGLA",
            color="Total_Gasto",
            hover_data=["Total_Gasto", "Total_Contratacoes"],
            color_continuous_scale=blue_scale,
            scope="south america",
            title="Mapa de Gasto",
            labels={"Total_Gasto": "Total Gasto (R$)", "Total_Contratacoes": "Contratações"}
        )
        grafico_mapa.update_layout(height=1000)
        style_map(grafico_mapa)
        st.plotly_chart(grafico_mapa, use_container_width=True)
    else:
        st.warning("Não foi possível carregar o geojson para o mapa.")
