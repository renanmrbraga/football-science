# components/charts/evolucao_eficiencia_chart.py
from streamlit_echarts import st_echarts
from constants.theme import get_theme_styles

def render_evolucao_eficiencia_chart(df_bras, df_transf, clube1: str, clube2: str | None = None):
    """
    Plota a evolução anual da eficiência (pontos por R$) de um ou dois clubes.
    """
    theme = get_theme_styles()
    anos = sorted(df_bras["Ano"].unique())

    # Função para calcular eficiência em um ano
    def eficiencia_ano(df_bras_clube, df_transf_clube):
        p = df_bras_clube["Pontos"].mean() if not df_bras_clube.empty else 0
        c = df_transf_clube["Valor"].mean() if not df_transf_clube.empty else 0
        return round(p / c, 4) if c else None

    # Séries para cada clube
    serie1 = []
    serie2 = []
    for ano in anos:
        df1_b = df_bras[(df_bras["Nome Oficial"] == clube1) & (df_bras["Ano"] == ano)]
        df1_t = df_transf[(df_transf["Nome Oficial"] == clube1) & (df_transf.get("Ano", df_transf["Temporada"]) == ano)]
        serie1.append(eficiencia_ano(df1_b, df1_t))
        if clube2:
            df2_b = df_bras[(df_bras["Nome Oficial"] == clube2) & (df_bras["Ano"] == ano)]
            df2_t = df_transf[(df_transf["Nome Oficial"] == clube2) & (df_transf.get("Ano", df_transf["Temporada"]) == ano)]
            serie2.append(eficiencia_ano(df2_b, df2_t))

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
        series.append({
            "name": clube2,
            "type": "line",
            "data": serie2,
            "itemStyle": {"color": theme["CHART_SECONDARY_COLOR"]},
            "smooth": True,
        })

    options = {
        "title": {"text": "Evolução de Eficiência (pts/R$)", "textStyle": theme["CHART_TEXT_STYLE"]},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": legend, "textStyle": theme["CHART_TEXT_STYLE"]},
        "xAxis": {
            "type": "category",
            "data": anos,
            "axisLabel": theme["CHART_AXIS_LABEL_STYLE"],
            "axisLine": theme["CHART_AXIS_LINE_STYLE"]
        },
        "yAxis": {
            "type": "value",
            "name": "Eficiência (pts/R$)",
            "axisLabel": theme["CHART_AXIS_LABEL_STYLE"],
            "axisLine": theme["CHART_AXIS_LINE_STYLE"]
        },
        "series": series,
    }

    st_echarts(options=options, height="500px")
