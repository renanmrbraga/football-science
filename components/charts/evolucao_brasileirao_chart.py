# app/components/charts/evolucao_brasileirao_chart.py
from streamlit_echarts import st_echarts, JsCode
from constants.theme import get_theme_styles

def render_evolucao_brasileirao_chart(df_brasileirao_clube, chart_title: str) -> None:
    import streamlit as st

    if df_brasileirao_clube.empty or "Ano" not in df_brasileirao_clube or "Posição" not in df_brasileirao_clube:
        st.warning("Dados insuficientes para exibir o gráfico de evolução no Brasileirão.")
        return

    theme = get_theme_styles()
    anos = df_brasileirao_clube.sort_values("Ano")["Ano"].astype(str).tolist()
    posicoes = df_brasileirao_clube.sort_values("Ano")["Posição"].fillna(0).astype(int).tolist()

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
            "textStyle": theme["CHART_TOOLTIP_STYLE"]["textStyle"]
        },
        "xAxis": {
            "type": "category",
            "name": "Ano",
            "nameLocation": "center",
            "nameGap": 25,
            "nameTextStyle": theme["CHART_AXIS_TITLE_STYLE"],
            "data": anos,
            "boundaryGap": False,
            "axisLabel": theme["CHART_AXIS_LABEL_STYLE"],
            "axisLine": theme["CHART_AXIS_LINE_STYLE"],
            "splitLine": {
                "show": True,
                "lineStyle": {"color": theme["CHART_GRIDLINE_COLOR"]}
            }
        },
        "yAxis": {
            "type": "value",
            "name": "Posição",
            "nameLocation": "middle",
            "nameGap": 35,
            "nameTextStyle": theme["CHART_AXIS_TITLE_STYLE"],
            "inverse": True,
            "min": 1,
            "max": 20,
            "interval": 1,
            "axisLabel": {
                "color": theme["CHART_AXIS_LABEL_STYLE"]["color"],
                "formatter": JsCode("function (value) { return [1,5,10,15,20].includes(value) ? value : ''; }").js_code
            },
            "axisLine": theme["CHART_AXIS_LINE_STYLE"],
            "splitLine": {
                "show": True,
                "lineStyle": {"color": theme["CHART_GRIDLINE_COLOR"]}
            }
        },
        "series": [{
            "name": "Posição",
            "data": posicoes,
            "type": "line",
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 10,
            "lineStyle": {
                "width": 3,
                "color": theme["CHART_PRIMARY_COLOR"]
            },
            "itemStyle": {
                "color": theme["CHART_POINT_COLOR"]
            },
            "areaStyle": {
                "origin": "end",
                "color": theme["CHART_AREA_GRADIENT"]
            }
        }]
    }

    st_echarts(options=options, height="500px")
