# app/components/charts/radar_indicadores_chart.py
from streamlit_echarts import st_echarts
import streamlit as st
from constants.theme import get_theme_styles
from utils.data_extractor import (
    get_aproveitamento,
    get_classificacao_media,
    get_media_pontos,
    get_saldo_gols,
    get_gasto_medio,
)

def render_kpi_radar_chart(df_clubes, df_bras, df_transf, clube_1: str, clube_2: str | None = None):
    theme = get_theme_styles()

    def get_dados(clube):
        df_info = df_clubes[df_clubes["Nome Oficial"] == clube].iloc[0]
        df_bras_clube = df_bras[df_bras["Nome Oficial"] == clube]
        df_transf_clube = df_transf[df_transf["Nome Oficial"] == clube]

        return [
            round(get_aproveitamento(df_info), 2),
            round(get_media_pontos(df_info), 2),
            round(get_classificacao_media(df_bras_clube), 2),
            get_saldo_gols(df_bras_clube),
            get_gasto_medio(df_transf_clube),
        ]

    labels = [
        {"name": "Aproveitamento (%)", "max": 100},
        {"name": "Pontuação Média", "max": 90},
        {"name": "Classificação Média", "max": 20},
        {"name": "Saldo de Gols", "max": 100},
        {"name": "Gasto Médio (R$)", "max": 6_500_000},
    ]

    data = [
        {
            "value": get_dados(clube_1),
            "name": clube_1,
            "lineStyle": {"color": theme["CHART_PRIMARY_COLOR"]},
            "itemStyle": {"color": theme["CHART_PRIMARY_COLOR"]},
            "areaStyle": {"color": theme["CHART_PRIMARY_COLOR"], "opacity": 0.1},
            "label": {
                "show": True,
                "color": theme["CHART_PRIMARY_COLOR"],
                "fontWeight": "bold"
            }
        }
    ]

    if clube_2:
        data.append({
            "value": get_dados(clube_2),
            "name": clube_2,
            "lineStyle": {"color": theme["CHART_SECONDARY_COLOR"]},
            "itemStyle": {"color": theme["CHART_SECONDARY_COLOR"]},
            "areaStyle": {"color": theme["CHART_SECONDARY_COLOR"], "opacity": 0.1},
            "label": {
                "show": True,
                "color": theme["CHART_SECONDARY_COLOR"],
                "fontWeight": "bold"
            }
        })

    options = {
        "title": {"text": "Indicadores Estratégicos", "left": "center", "textStyle": theme["CHART_TEXT_STYLE"]},
        "tooltip": {"trigger": "item"},
        "legend": {
            "data": [clube_1] + ([clube_2] if clube_2 else []),
            "top": "top",
            "textStyle": {"color": theme["CHART_TEXT_STYLE"]["color"]}
        },
        "radar": {
            "indicator": labels,
            "splitArea": {"areaStyle": {"color": theme["CHART_RADAR_BG"]}},
            "axisName": theme["CHART_AXIS_LABEL_STYLE"],
            "axisLine": theme["CHART_AXIS_LINE_STYLE"],
            "splitLine": {"lineStyle": {"color": theme["CHART_GRIDLINE_COLOR"]}},
        },
        "series": [{
            "type": "radar",
            "data": data
        }]
    }

    st_echarts(options=options, height="500px")
