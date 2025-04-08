# app/dashboards/brasileirao.py
import streamlit as st
import plotly.express as px
from app.utils.data import load_data, enrich_with_uf, ensure_all_ufs
from app.utils.geo import load_geojson
from app.components.utils import format_currency, style_plotly, style_map
from app.constants.paths import CLUBES_CSV, TRANSFERENCIAS_CSV, BRASILEIRAO_CSV, GEOJSON_PATH
from app.constants.texts import TITLE_BRASILEIRAO, METRICS, CHARTS, WARNING_NO_UF_COLUMN, ERROR_LOAD_DATA
from app.constants.colors import PRIMARY_BLUE, BLUE_SCALE

def dashboard_clubes():
    st.title(TITLE_BRASILEIRAO)

    df_clubes = load_data(CLUBES_CSV)
    df_transf = load_data(TRANSFERENCIAS_CSV)
    df_bras = load_data(BRASILEIRAO_CSV)

    if df_clubes.empty or df_transf.empty or df_bras.empty:
        st.error(ERROR_LOAD_DATA)
        return

    df_transf = df_transf.merge(df_clubes[["ID", "Nome Oficial"]], left_on="Clube_ID", right_on="ID", how="left")
    df_transf = enrich_with_uf(df_transf, df_clubes)
    df_bras = df_bras.merge(df_clubes[["ID", "Nome Oficial"]], left_on="Clube", right_on="Nome Oficial", how="left")

    clubes = sorted(df_clubes["Nome Oficial"].unique())
    clube = st.sidebar.selectbox("Clube", clubes)

    df_bras_clube = df_bras[df_bras["Nome Oficial"] == clube]
    df_transf_clube = df_transf[df_transf["Nome Oficial"] == clube].copy()
    df_info = df_clubes[df_clubes["Nome Oficial"] == clube].iloc[0]

    st.subheader("Indicadores Gerais")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**{METRICS['participacoes']}**")
        st.markdown(f"#### {df_info['Participacoes_SerieA']}")
        st.markdown(f"**{METRICS['media_pontos']}**")
        st.markdown(f"#### {round(df_info['Media_Pontos'], 2)}")
        st.markdown(f"**{METRICS['ultimo_ano']}**")
        st.markdown(f"#### {int(df_info['Ultimo_Ano_SerieA'])}")
        st.markdown(f"**{METRICS['saldo_transferencias']}**")
        st.markdown(f"#### R$ {format_currency(df_info['Saldo_Transferencias_R$'])}")

    with col2:
        st.markdown(f"**{METRICS['rebaixamentos']}**")
        st.markdown(f"#### {df_info['Rebaixamentos']}")
        st.markdown(f"**{METRICS['aproveitamento']}**")
        st.markdown(f"#### {round(df_info['Aproveitamento(%)'], 2)}%")
        st.markdown(f"**{METRICS['internacionais']}**")
        st.markdown(f"#### {df_info['Participacoes_Internacionais']}")

    st.subheader(CHARTS["evolucao_brasileirao"])
    fig_pos = px.line(
        df_bras_clube, x="Ano", y="Posição",
        title=CHARTS["posicao_ano"](clube), markers=True,
        color_discrete_sequence=[PRIMARY_BLUE]
    )
    fig_pos.update_yaxes(autorange="reversed")
    style_plotly(fig_pos)
    st.plotly_chart(fig_pos, use_container_width=True)

    st.subheader(CHARTS["transferencias"])
    df_transf_clube["Valor"] = df_transf_clube["Valor"].apply(lambda x: f"R$ {x:,.2f}")

    st.subheader(CHARTS["investimentos"])
    df_grouped = df_transf_clube.groupby(["Ano", "Tipo"])["Valor"].count().reset_index()
    fig_bar = px.bar(
        df_grouped, x="Ano", y="Valor", color="Tipo", barmode="group",
        title=CHARTS["investimentos"], color_discrete_sequence=BLUE_SCALE
    )
    style_plotly(fig_bar)
    st.plotly_chart(fig_bar, use_container_width=True)
