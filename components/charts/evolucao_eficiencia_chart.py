# components/charts/evolucao_eficiencia_chart.py
from streamlit_echarts import st_echarts
from constants.theme import get_theme_styles
import streamlit as st


def render_evolucao_eficiencia_chart(
    df_bras,
    df_transf,
    clube1: str,
    clube2: str | None = None,
) -> None:
    """
    Evolução anual da eficiência (pontos / R$).

    • Considera apenas temporadas em que o clube disputou a Série A
      (coluna Pontos/Pts presente).
    • Eficiência = soma de pontos ÷ soma de gastos em transferências
      no mesmo ano.
    • Se o gasto da temporada for 0, devolve `None`
      (deixa buraco em vez de 0 para não distorcer o gráfico).

    Detecta automaticamente cabeçalhos:
      –  Nome do clube:  'Nome Oficial'  ou 'Clube'
      –  Pontos:         'Pontos'        ou 'Pts'
      –  Ano:            'Ano'           ou 'Temporada'
    """
    theme = get_theme_styles()

    # ---------- detectar colunas -----------------------------------------
    col_nome = (
        "Nome Oficial"
        if "Nome Oficial" in df_bras.columns
        else "Clube" if "Clube" in df_bras.columns else None
    )
    col_pts = (
        "Pontos"
        if "Pontos" in df_bras.columns
        else "Pts" if "Pts" in df_bras.columns else None
    )
    col_ano = (
        "Ano"
        if "Ano" in df_bras.columns
        else "Temporada" if "Temporada" in df_bras.columns else None
    )

    faltando = [
        lab
        for lab, c in [
            ("Nome/Clube", col_nome),
            ("Pontos/Pts", col_pts),
            ("Ano/Temporada", col_ano),
        ]
        if c is None
    ]
    if faltando:
        st.error("❌ df_bras não contém: " + ", ".join(faltando))
        st.write(df_bras.columns.tolist())
        return
    if "Valor" not in df_transf.columns:
        st.error("❌ df_transf precisa da coluna 'Valor'.")
        return
    # ---------------------------------------------------------------------

    # ▼ mantém apenas temporadas de Série A (onde há pontos)
    df_bras = df_bras[df_bras[col_pts].notna()]

    anos = [int(a) for a in sorted(df_bras[col_ano].unique())]

    def eficiencia_ano(df_bras_tmp, df_transf_tmp):
        pts = float(df_bras_tmp[col_pts].sum())
        gasto = float(df_transf_tmp["Valor"].sum())
        return round(pts, 4) if gasto == 0 else round(pts / gasto, 4)

    def gerar_serie(clube_nome):
        pts_tmp = df_bras[df_bras[col_nome] == clube_nome]
        transf_tmp = df_transf[df_transf["Nome Oficial"] == clube_nome]
        return [
            eficiencia_ano(
                pts_tmp[pts_tmp[col_ano] == ano],
                transf_tmp[transf_tmp["Ano"] == ano],
            )
            for ano in anos
        ]

    serie1 = gerar_serie(clube1)
    serie2 = gerar_serie(clube2) if clube2 else None

    # Se todas as eficiências forem None → nada para mostrar
    if all(v is None for v in serie1) and (
        not serie2 or all(v is None for v in serie2)
    ):
        st.info("Sem dados de Série A + gastos para calcular eficiência.")
        return

    # Converter para tipos nativos
    serie1 = [float(v) if v is not None else None for v in serie1]
    if serie2:
        serie2 = [float(v) if v is not None else None for v in serie2]

    legend = [clube1] + ([clube2] if clube2 else [])
    series = [
        {
            "name": clube1,
            "type": "line",
            "data": serie1,
            "itemStyle": {"color": theme["CHART_PRIMARY_COLOR"]},
            "smooth": True,
        }
    ]
    if clube2:
        series.append(
            {
                "name": clube2,
                "type": "line",
                "data": serie2,
                "itemStyle": {"color": theme["CHART_SECONDARY_COLOR"]},
                "smooth": True,
            }
        )

    options = {
        "title": {
            "text": "Evolução de Eficiência (pts/R$)",
            "textStyle": theme["CHART_TEXT_STYLE"],
        },
        "tooltip": {"trigger": "axis"},
        "legend": {"data": legend, "textStyle": theme["CHART_TEXT_STYLE"]},
        "xAxis": {
            "type": "category",
            "data": anos,
            "axisLabel": theme["CHART_AXIS_LABEL_STYLE"],
            "axisLine": theme["CHART_AXIS_LINE_STYLE"],
        },
        "yAxis": {
            "type": "value",
            "name": "Eficiência (pts/R$)",
            "axisLabel": theme["CHART_AXIS_LABEL_STYLE"],
            "axisLine": theme["CHART_AXIS_LINE_STYLE"],
        },
        "series": series,
    }

    st_echarts(options=options, height="500px")
