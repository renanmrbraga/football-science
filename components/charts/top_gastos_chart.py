# app/components/charts/top_gastos_chart.py
from streamlit_echarts import st_echarts, JsCode
from constants.theme import get_theme_styles

def render_top_gastos_chart(df_entrada, chart_title: str) -> None:
    import streamlit as st

    if df_entrada.empty or "Nome Oficial" not in df_entrada or "Valor" not in df_entrada:
        st.warning("Dados insuficientes para exibir o gráfico de maiores gastos.")
        return

    theme = get_theme_styles()

    df_top = (
        df_entrada.groupby("Nome Oficial")["Valor"]
        .sum()
        .nlargest(10)
        .reset_index()
        .sort_values("Valor", ascending=True)
    )

    clubes = df_top["Nome Oficial"].tolist()
    valores = df_top["Valor"].astype(float).tolist()

    series_data = [
        {
            "value": valor,
            "itemStyle": {
                "color": {
                    **theme["GRADIENT_HORIZONTAL_ECHARTS"],
                    "opacity": 0.9
                }
            }
        }
        for valor in valores
    ]

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
        "grid": {
            "left": "160px",
        },
        "xAxis": {
            "type": "value",
            "name": "Valor (R$)",
            "nameLocation": "middle",
            "nameGap": 40,
            "nameTextStyle": theme["CHART_AXIS_TITLE_STYLE"],
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
        "yAxis": {
            "type": "category",
            "data": clubes,
            "axisLabel": {
                "color": theme["CHART_AXIS_LABEL_STYLE"]["color"],
                "interval": 0,
                "fontSize": 12,
                "overflow": "break",
                "width": 120
            },
            "axisLine": theme["CHART_AXIS_LINE_STYLE"]
        },
        "series": [{
            "type": "bar",
            "name": "Gastos",
            "data": series_data,
            "barWidth": "60%"
        }]
    }

    st_echarts(options=options, height="500px")
