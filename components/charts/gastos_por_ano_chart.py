# app/components/charts/gastos_por_ano_chart.py
from streamlit_echarts import st_echarts, JsCode
from constants.theme import get_theme_styles

def render_gastos_por_ano_chart(df_entrada, chart_title: str) -> None:
    import streamlit as st

    if df_entrada.empty or "Ano" not in df_entrada or "Valor" not in df_entrada:
        st.warning("Dados insuficientes para exibir o gráfico de gastos.")
        return

    theme = get_theme_styles()
    df_ano = df_entrada.groupby("Ano")["Valor"].sum().reset_index().sort_values("Ano")
    anos = df_ano["Ano"].astype(str).tolist()
    valores = df_ano["Valor"].astype(float).tolist()

    options = {
        "title": {
            "text": chart_title,
            "textStyle": theme["CHART_TEXT_STYLE"]
        },
        "grid": {
            "left": "130px",
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "line"},
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
        "xAxis": {
            "type": "category",
            "name": "Ano",
            "nameLocation": "center",
            "nameGap": 30,
            "nameTextStyle": theme["CHART_AXIS_TITLE_STYLE"],
            "data": anos,
            "axisLabel": theme["CHART_AXIS_LABEL_STYLE"],
            "axisLine": theme["CHART_AXIS_LINE_STYLE"],
            "splitLine": {
                "show": True,
                "lineStyle": {"color": theme["CHART_GRIDLINE_COLOR"]}
            }
        },
        "yAxis": {
            "type": "value",
            # Título removido
            "axisLabel": {
                "color": theme["CHART_AXIS_LABEL_STYLE"]["color"],
                "formatter": JsCode(
                    "function(value){return 'R$ ' + value.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2});}"
                ).js_code
            },
            "axisLine": theme["CHART_AXIS_LINE_STYLE"],
            "splitLine": {
                "show": True,
                "lineStyle": {"color": theme["CHART_GRIDLINE_COLOR"]}
            }
        },
        "series": [{
            "name": "Gastos",
            "data": valores,
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
                "origin": "auto",
                "color": theme["CHART_AREA_GRADIENT"]
            }
        }]
    }

    st_echarts(options=options, height="500px")
