# app/components/charts/aproveitamento_temporada_chart.py
from streamlit_echarts import st_echarts
import streamlit as st
from constants.theme import get_theme_styles


def render_aproveitamento_temporada_chart(df_bras, clube_1: str, clube_2: str | None = None):
    theme = get_theme_styles()

    def calcular_aproveitamento(df):
        df = df.copy()
        df = df[df["Jogos"] > 0]  # evita divisões por zero
        df["Aproveitamento"] = ((df["Pontos"] / (df["Jogos"] * 3)) * 100).round(2)
        df = df.sort_values("Ano")
        return df[["Ano", "Aproveitamento"]]

    df_1 = calcular_aproveitamento(df_bras[df_bras["Nome Oficial"] == clube_1])
    df_2 = calcular_aproveitamento(df_bras[df_bras["Nome Oficial"] == clube_2]) if clube_2 else None

    anos = df_1["Ano"].astype(str).tolist()
    valores1 = df_1["Aproveitamento"].tolist()

    valores2 = []
    if clube_2:
        # Alinha os anos entre os dois clubes para garantir consistência no eixo X
        df_2 = df_2.set_index("Ano").reindex(df_1["Ano"]).fillna(0).reset_index()
        valores2 = df_2["Aproveitamento"].tolist()

    series = [
        {
            "name": clube_1,
            "type": "line",
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 10,
            "data": valores1,
            "lineStyle": {"width": 3, "color": theme["CHART_PRIMARY_COLOR"]},
            "itemStyle": {"color": theme["CHART_PRIMARY_COLOR"]},
            "areaStyle": {"origin": "auto", "color": theme["CHART_AREA_GRADIENT"]}
        }
    ]

    if clube_2:
        series.append({
            "name": clube_2,
            "type": "line",
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 10,
            "data": valores2,
            "lineStyle": {"width": 3, "color": theme["CHART_SECONDARY_COLOR"]},
            "itemStyle": {"color": theme["CHART_SECONDARY_COLOR"]},
            "areaStyle": {"origin": "auto", "opacity": 0.1}
        })

    options = {
        "title": {"text": "Aproveitamento por Temporada", "textStyle": theme["CHART_TEXT_STYLE"]},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "line"},
            "backgroundColor": theme["CHART_TOOLTIP_STYLE"]["backgroundColor"],
            "borderColor": theme["CHART_TOOLTIP_STYLE"]["borderColor"],
            "textStyle": theme["CHART_TOOLTIP_STYLE"]["textStyle"]
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
            "name": "Aproveitamento (%)",
            "min": 0,
            "max": 100,
            "nameTextStyle": theme["CHART_AXIS_TITLE_STYLE"],
            "axisLabel": theme["CHART_AXIS_LABEL_STYLE"],
            "axisLine": theme["CHART_AXIS_LINE_STYLE"],
            "splitLine": {"lineStyle": {"color": theme["CHART_GRIDLINE_COLOR"]}}
        },
        "series": series
    }

    st_echarts(options=options, height="500px")
