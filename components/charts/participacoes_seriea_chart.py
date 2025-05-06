# app/components/charts/participacoes_seriea_chart.py
from streamlit_echarts import st_echarts, JsCode
import streamlit as st
from constants.theme import get_theme_styles
from utils.data_extractor import get_total_participacoes


def render_participacoes_seriea_chart(df_clubes, clube_1: str, clube_2: str | None = None):
    theme = get_theme_styles()

    nomes = [clube_1]
    valores = [get_total_participacoes(df_clubes[df_clubes["Nome Oficial"] == clube_1].iloc[0])]

    if clube_2:
        nomes.append(clube_2)
        valores.append(get_total_participacoes(df_clubes[df_clubes["Nome Oficial"] == clube_2].iloc[0]))

    series_data = [
        {
            "value": valor,
            "itemStyle": {
                "color": theme["CHART_PRIMARY_COLOR"] if nome == clube_1 else theme["CHART_SECONDARY_COLOR"]
            }
        }
        for nome, valor in zip(nomes, valores)
    ]

    options = {
        "title": {"text": "Participações na Série A", "textStyle": theme["CHART_TEXT_STYLE"]},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "backgroundColor": theme["CHART_TOOLTIP_STYLE"]["backgroundColor"],
            "borderColor": theme["CHART_TOOLTIP_STYLE"]["borderColor"],
            "textStyle": theme["CHART_TOOLTIP_STYLE"]["textStyle"]
        },
        "xAxis": {
            "type": "category",
            "data": nomes,
            "axisLabel": theme["CHART_AXIS_LABEL_STYLE"],
            "axisLine": theme["CHART_AXIS_LINE_STYLE"]
        },
        "yAxis": {
            "type": "value",
            "axisLabel": theme["CHART_AXIS_LABEL_STYLE"],
            "axisLine": theme["CHART_AXIS_LINE_STYLE"],
            "splitLine": {"lineStyle": {"color": theme["CHART_GRIDLINE_COLOR"]}}
        },
        "series": [{
            "name": "Participações",
            "type": "bar",
            "data": series_data,
            "barWidth": "60%"
        }]
    }

    st_echarts(options=options, height="350px")
