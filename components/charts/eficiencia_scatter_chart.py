    # app/components/charts/eficiencia_scatter_chart.py
from streamlit_echarts import st_echarts, JsCode
import streamlit as st
from constants.theme import get_theme_styles

def render_eficiencia_scatter_chart(df_transf, df_bras, clube_1: str, clube_2: str | None = None):
    theme = get_theme_styles()

    def calcular_pontos_medio(clube):
        df_clube = df_bras[df_bras["Nome Oficial"] == clube]
        return df_clube["Pontos"].mean()

    def calcular_gasto_medio(clube):
        df_clube = df_transf[df_transf["Nome Oficial"] == clube]
        return df_clube["Valor"].mean()

    pontos_1 = round(calcular_pontos_medio(clube_1), 2)
    gastos_1 = round(calcular_gasto_medio(clube_1), 2)

    pontos_2, gastos_2 = None, None
    if clube_2:
        pontos_2 = round(calcular_pontos_medio(clube_2), 2)
        gastos_2 = round(calcular_gasto_medio(clube_2), 2)

    data = [
        {
            "name": clube_1,
            "value": [gastos_1, pontos_1],
            "symbolSize": 20,
            "itemStyle": {"color": theme["CHART_PRIMARY_COLOR"]},
        }
    ]

    if clube_2:
        data.append({
            "name": clube_2,
            "value": [gastos_2, pontos_2],
            "symbolSize": 20,
            "itemStyle": {"color": theme["CHART_SECONDARY_COLOR"]},
        })

    options = {
        "title": {
            "text": "Eficiência: Gasto vs Pontuação Média",
            "textStyle": theme["CHART_TEXT_STYLE"],
        },
        "tooltip": {
            "trigger": "item",
            "formatter": JsCode(
                """
                function(params) {
                    return params.name + '<br/>Gasto Médio: R$ ' +
                    params.value[0].toLocaleString('pt-BR', {minimumFractionDigits: 2}) +
                    '<br/>Pontuação Média: ' + params.value[1].toFixed(2);
                }
                """
            ).js_code,
            "backgroundColor": theme["CHART_TOOLTIP_STYLE"]["backgroundColor"],
            "borderColor": theme["CHART_TOOLTIP_STYLE"]["borderColor"],
            "textStyle": theme["CHART_TOOLTIP_STYLE"]["textStyle"],
        },
        "xAxis": {
            "name": "Gasto Médio (R$)",
            "nameTextStyle": theme["CHART_AXIS_TITLE_STYLE"],
            "axisLabel": theme["CHART_AXIS_LABEL_STYLE"],
            "axisLine": theme["CHART_AXIS_LINE_STYLE"],
        },
        "yAxis": {
            "name": "Pontuação Média",
            "nameTextStyle": theme["CHART_AXIS_TITLE_STYLE"],
            "axisLabel": theme["CHART_AXIS_LABEL_STYLE"],
            "axisLine": theme["CHART_AXIS_LINE_STYLE"],
        },
        "series": [
            {
                "type": "scatter",
                "symbolSize": 20,
                "data": data,
            }
        ],
    }

    st_echarts(options=options, height="500px")
