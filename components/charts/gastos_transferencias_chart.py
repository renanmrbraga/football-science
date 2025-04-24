
# app/components/charts/gastos_transferencias_chart.py
from streamlit_echarts import st_echarts, JsCode
import streamlit as st
from constants.theme import get_theme_styles


def render_gastos_transferencias_chart(df_transf, clube_1: str, clube_2: str | None = None, chart_title: str = "Gastos em Transferências por Temporada"):
    if df_transf.empty or "Nome Oficial" not in df_transf or "Valor" not in df_transf:
        st.warning("Dados insuficientes para exibir o gráfico.")
        return

    theme = get_theme_styles()

    def get_serie(clube):
        df_clube = df_transf[df_transf["Nome Oficial"] == clube]
        df_ano = df_clube.groupby("Ano")["Valor"].sum().reset_index().sort_values("Ano")
        return df_ano["Ano"].astype(str).tolist(), df_ano["Valor"].astype(float).tolist()

    anos1, valores1 = get_serie(clube_1)
    anos = anos1  # Assume anos1 como base

    series = [{
        "name": clube_1,
        "type": "bar",
        "data": valores1,
        "itemStyle": {"color": theme["CHART_PRIMARY_COLOR"]},
        "barGap": "10%"
    }]

    if clube_2:
        _, valores2 = get_serie(clube_2)
        series.append({
            "name": clube_2,
            "type": "bar",
            "data": valores2,
            "itemStyle": {"color": theme["CHART_SECONDARY_COLOR"]},
            "barGap": "10%"
        })

    options = {
        "title": {
            "text": chart_title,
            "textStyle": theme["CHART_TEXT_STYLE"]
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "backgroundColor": theme["CHART_TOOLTIP_STYLE"]["backgroundColor"],
            "borderColor": theme["CHART_TOOLTIP_STYLE"]["borderColor"],
            "textStyle": theme["CHART_TOOLTIP_STYLE"]["textStyle"],
            "formatter": JsCode(
                "function(params) {"
                "  return params[0].name + '<br/>' + "
                "    params.map(p => p.marker + ' ' + p.seriesName + ': R$ ' + "
                "    p.value.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})"
                "  ).join('<br/>');"
                "}"
            ).js_code
        },
        "legend": {
            "data": [clube_1] + ([clube_2] if clube_2 else []),
            "textStyle": {"color": theme["CHART_TEXT_STYLE"]["color"]}
        },
        "xAxis": {
            "type": "category",
            "name": "Ano",
            "data": anos,
            "nameTextStyle": theme["CHART_AXIS_TITLE_STYLE"],
            "axisLabel": theme["CHART_AXIS_LABEL_STYLE"],
            "axisLine": theme["CHART_AXIS_LINE_STYLE"]
        },
        "yAxis": {
            "type": "value",
            "axisLabel": {
                "color": theme["CHART_AXIS_LABEL_STYLE"]["color"],
                "formatter": JsCode(
                    "function(value) { return 'R$ ' + value.toLocaleString('pt-BR', {minimumFractionDigits: 2}); }"
                ).js_code
            },
            "axisLine": theme["CHART_AXIS_LINE_STYLE"],
            "splitLine": {
                "show": True,
                "lineStyle": {"color": theme["CHART_GRIDLINE_COLOR"]}
            }
        },
        "series": series
    }

    st_echarts(options=options, height="500px")
