import os
import json
import logging
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv, find_dotenv

# Configuração do logging
logging.basicConfig(level=logging.INFO)

# Carregar variáveis de ambiente
load_dotenv(find_dotenv())

# Configuração geral da página
st.set_page_config(page_title="Dashboards de Análise", layout="wide")

@st.cache_data(show_spinner=False)
def load_data(csv_path: str) -> pd.DataFrame:
    """Carrega dados de um CSV. Retorna DataFrame vazio em caso de erro."""
    if not csv_path or not os.path.isfile(csv_path):
        st.error(f"Arquivo não encontrado: {csv_path}")
        return pd.DataFrame()
    try:
        df = pd.read_csv(csv_path, sep=";", encoding="utf-8")
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo {csv_path}: {e}")
        return pd.DataFrame()

def format_currency(n: float) -> str:
    """Formata um número como moeda no padrão brasileiro."""
    return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_int(n: int) -> str:
    """Formata um número inteiro com separador de milhares."""
    return f"{n:,}".replace(",", "X").replace(".", ",").replace("X", ".")

def style_plotly(fig: go.Figure) -> None:
    """Aplica estilo padrão aos gráficos Plotly."""
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

def style_map(fig: go.Figure) -> None:
    """Aplica estilo específico para mapas Plotly."""
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
    if fig.layout.get("coloraxis"):
        fig.update_coloraxes(colorbar=dict(
            title=dict(
                text=fig.layout.coloraxis.colorbar.title.text if (fig.layout.coloraxis and 
                      fig.layout.coloraxis.colorbar and fig.layout.coloraxis.colorbar.title.text) 
                     else "Total Gasto (R$)",
                font=dict(color="#000000", size=16, family="Open Sans Bold")
            ),
            tickfont=dict(color="#000000", size=14, family="Open Sans Bold")
        ))

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
/* Texto em preto, negrito e com fonte Open Sans Bold */
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

def dashboard_brasileirao() -> None:
    """Dashboard de análise do Brasileirão com dados de clubes, transferências e desempenho."""
    # Carregar caminhos dos arquivos das variáveis de ambiente
    clubes_path = os.getenv("ARQUIVO_CLUBES_PROCESSED")
    transf_path = os.getenv("ARQUIVO_TRANSFERENCIAS_PROCESSED")
    brasileirao_path = os.getenv("ARQUIVO_BRASILEIRAO_PROCESSED")
    geojson_path = os.getenv("ARQUIVO_GEOJSON")
    
    # Carregar datasets
    df_clubes = load_data(clubes_path)
    df_transferencias = load_data(transf_path)
    df_brasileirao = load_data(brasileirao_path)
    
    if df_clubes.empty or df_transferencias.empty or df_brasileirao.empty:
        st.error("Um ou mais datasets não foram carregados corretamente.")
        st.stop()
    
    # Relacionar tabelas
    df_transferencias = df_transferencias.merge(
        df_clubes[['ID', 'Nome Oficial']], left_on="Clube_ID", right_on="ID", how="left"
    )
    df_brasileirao = df_brasileirao.merge(
        df_clubes[['ID', 'Nome Oficial']], left_on="Clube", right_on="Nome Oficial", how="left"
    )
    
    # Seleção de clube
    clubes_disponiveis = sorted(df_clubes["Nome Oficial"].unique())
    clube_selecionado = st.sidebar.selectbox("Selecione um Clube", clubes_disponiveis)
    
    # Filtrar dados do clube
    df_clube_brasileirao = df_brasileirao[df_brasileirao["Nome Oficial"] == clube_selecionado]
    df_clube_transferencias = df_transferencias[df_transferencias["Nome Oficial"] == clube_selecionado].copy()
    df_clube_info = df_clubes[df_clubes["Nome Oficial"] == clube_selecionado].iloc[0]
    
    st.title(f"Análise do {clube_selecionado}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Participações Série A", df_clube_info["Participacoes_SerieA"])
        st.metric("Rebaixamentos", df_clube_info["Rebaixamentos"])
    with col2:
        st.metric("Média de Pontos", round(df_clube_info["Media_Pontos"], 2))
        st.metric("Aproveitamento (%)", round(df_clube_info["Aproveitamento(%)"], 2))
    with col3:
        st.metric("Último Ano na Série A", int(df_clube_info["Ultimo_Ano_SerieA"]))
        st.metric("Participações Internacionais", df_clube_info["Participacoes_Internacionais"])
    with col4:
        st.metric("Saldo de Transferências (R$)", f"{df_clube_info['Saldo_Transferencias_R$']:,.2f}")
    
    st.subheader("Evolução da Posição no Brasileirão")
    fig_posicao = px.line(
        df_clube_brasileirao, x="Ano", y="Posição",
        title=f"Posição do {clube_selecionado} no Brasileirão",
        markers=True
    )
    fig_posicao.update_yaxes(autorange="reversed")
    style_plotly(fig_posicao)
    st.plotly_chart(fig_posicao, use_container_width=True)
    
    st.subheader("Transferências")
    if "Valor" in df_clube_transferencias.columns:
        df_clube_transferencias.loc[:, "Valor"] = df_clube_transferencias["Valor"].apply(lambda x: f"R$ {x:,.2f}")
    
    tab_entradas, tab_saidas = st.tabs(["Entradas", "Saídas"])
    with tab_entradas:
        df_entradas = df_clube_transferencias[df_clube_transferencias["Tipo"].str.lower() == "entrada"]
        st.dataframe(df_entradas[["Ano", "Origem_Destino", "Valor", "Empréstimo"]])
    with tab_saidas:
        df_saidas = df_clube_transferencias[df_clube_transferencias["Tipo"].str.lower() == "saída"]
        st.dataframe(df_saidas[["Ano", "Origem_Destino", "Valor", "Empréstimo"]])
    
    st.subheader("Gastos e Vendas ao Longo dos Anos")
    df_transf_grouped = df_clube_transferencias.groupby(["Ano", "Tipo"])["Valor"].sum().reset_index()
    fig_transf = px.bar(
        df_transf_grouped,
        x="Ano", y="Valor", color="Tipo",
        title="Investimentos e Vendas ao longo dos Anos",
        barmode="group"
    )
    style_plotly(fig_transf)
    st.plotly_chart(fig_transf, use_container_width=True)
    
    if geojson_path and os.path.isfile(geojson_path):
        try:
            with open(geojson_path, "r", encoding="utf-8") as f:
                states_geojson = json.load(f)
            df_transferencias_map = df_transferencias.groupby("UF")["Valor"].sum().reset_index()
            df_transferencias_map.columns = ["UF", "Total_Gasto"]
            st.subheader("Mapa de Transferências")
            fig_mapa = px.choropleth(
                df_transferencias_map,
                geojson=states_geojson, locations="UF", featureidkey="properties.SIGLA",
                color="Total_Gasto", hover_data=["Total_Gasto"],
                title="Distribuição Geográfica de Transferências"
            )
            fig_mapa.update_geos(fitbounds="locations", visible=False)
            style_map(fig_mapa)
            st.plotly_chart(fig_mapa, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao carregar o mapa: {e}")
    else:
        st.warning("GeoJSON não encontrado. Mapa não exibido.")

def dashboard_transferencias() -> None:
    """Dashboard de transferências com análise de entradas, métricas e gráficos."""
    transf_path = os.getenv("ARQUIVO_TRANSFERENCIAS_PROCESSED")
    geojson_path = os.getenv("ARQUIVO_GEOJSON")
    
    # Carregar o dataset de transferências
    df = load_data(transf_path)
    if df.empty:
        st.error("Dataset de transferências não carregado.")
        st.stop()
    
    # Realizar merge para adicionar a coluna "Nome Oficial"
    df_clubes = load_data(os.getenv("ARQUIVO_CLUBES_PROCESSED"))
    if df_clubes.empty:
        st.error("Dataset de clubes não carregado.")
        st.stop()
    df = df.merge(
        df_clubes[['ID', 'Nome Oficial']],
        left_on="Clube_ID",
        right_on="ID",
        how="left"
    )
    
    st.title("Transferências de Todos Clubes da Série A dos Últimos 10 Anos")
    
    df_entrada = df[df["Tipo"].str.lower() == "entrada"]
    if df_entrada.empty:
        st.warning("Não há dados de transferências de entrada disponíveis.")
        st.stop()
    
    valor_total_gasto = df_entrada["Valor"].sum()
    total_contratacoes = len(df_entrada)
    total_emprestimos = len(df_entrada[df_entrada["Empréstimo"].str.lower() == "sim"])
    contratacoes_com_custo = len(df_entrada[df_entrada["Valor"] > 0])
    contratacoes_gratuitas = len(df_entrada[df_entrada["Valor"] == 0])
    ticket_medio = valor_total_gasto / total_contratacoes if total_contratacoes else 0
    ticket_medio_com_custo = valor_total_gasto / contratacoes_com_custo if contratacoes_com_custo else 0
    
    # Verificar se a coluna 'UF' existe
    if "UF" in df_entrada.columns:
        df_map = df_entrada.groupby("UF").agg({
            "Valor": "sum",
            "Nome Oficial": "count"
        }).reset_index().rename(columns={"Nome Oficial": "Total_Contratacoes"})
    else:
        st.warning("Coluna 'UF' não encontrada. Mapa não será exibido.")
        df_map = pd.DataFrame()
    
    if geojson_path and os.path.isfile(geojson_path) and not df_map.empty:
        try:
            with open(geojson_path, "r", encoding="utf-8") as f:
                states_geojson = json.load(f)
        except Exception as e:
            st.warning(f"Erro ao carregar geojson: {e}")
            states_geojson = None
    else:
        states_geojson = None
        if df_map.empty:
            st.warning("Mapa não será exibido devido à ausência da coluna 'UF'.")
    
    if states_geojson is not None:
        siglas = [feat["properties"]["SIGLA"] for feat in states_geojson["features"]]
        df_all_states = pd.DataFrame({"UF": siglas})
        df_map_full = df_all_states.merge(df_map, on="UF", how="left").fillna(0)
    else:
        df_map_full = df_map
    
    col1 = st.columns(1)[0]
    col1.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Valor Total Gasto</div>
            <div class="metric-value">R$ {format_currency(valor_total_gasto)}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Total de Contratações</div>
            <div class="metric-value">{format_int(total_contratacoes)}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Ticket Médio - Total</div>
            <div class="metric-value">R$ {format_currency(ticket_medio)}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Contratações - Com Custo</div>
            <div class="metric-value">{format_int(contratacoes_com_custo)}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Ticket Médio - Com Custo</div>
            <div class="metric-value">R$ {format_currency(ticket_medio_com_custo)}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Contratações - Gratuitas</div>
            <div class="metric-value">{format_int(contratacoes_gratuitas)}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Total de Empréstimos</div>
            <div class="metric-value">{format_int(total_emprestimos)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    top_10_gastos = df_entrada.groupby("Nome Oficial")["Valor"].sum().nlargest(10).reset_index().sort_values(by="Valor", ascending=True)
    top_10_gastos["formatted"] = top_10_gastos["Valor"].apply(format_currency)
    grafico_top_gastos = px.bar(
        top_10_gastos,
        x="Valor",
        y="Nome Oficial",
        title="Top 10 Clubes que Mais Gastaram",
        orientation="h",
        text="formatted",
        color_discrete_sequence=["#003366"]
    )
    style_plotly(grafico_top_gastos)
    
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
        text="formatted",
        color_discrete_sequence=["#003366"]
    )
    style_plotly(grafico_top_contratacoes)
    
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
    
    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_a:
        st.plotly_chart(grafico_top_gastos, use_container_width=True)
        st.plotly_chart(grafico_gastos, use_container_width=True)
    with col_b:
        st.plotly_chart(grafico_top_contratacoes, use_container_width=True)
        st.plotly_chart(grafico_contratacoes, use_container_width=True)
    with col_c:
        if states_geojson is not None and not df_map_full.empty:
            blue_scale = [
                "#e6f2ff", "#b3cde0", "#80a9d0", "#4d85bf", "#1a60af", "#003366"
            ]
            grafico_mapa = px.choropleth(
                df_map_full,
                geojson=states_geojson,
                locations="UF",
                featureidkey="properties.SIGLA",
                color="Valor",
                hover_data=["Valor", "Total_Contratacoes"],
                color_continuous_scale=blue_scale,
                scope="south america",
                title="Mapa de Gasto",
                labels={"Valor": "Total Gasto (R$)", "Total_Contratacoes": "Contratações"}
            )
            grafico_mapa.update_layout(height=1000)
            style_map(grafico_mapa)
            st.plotly_chart(grafico_mapa, use_container_width=True)
        else:
            st.warning("Mapa não exibido devido à ausência de dados ou geojson.")
    
def main() -> None:
    """Função principal para seleção e exibição do dashboard."""
    dashboard_options = {
        "Brasileirão": dashboard_brasileirao,
        "Transferências": dashboard_transferencias
    }
    
    st.sidebar.title("Selecione o Dashboard")
    escolha = st.sidebar.radio("Opções", list(dashboard_options.keys()))
    
    dashboard_options[escolha]()

if __name__ == "__main__":
    main()
