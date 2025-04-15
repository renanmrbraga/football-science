# app/components/charts/investimentos_chart.py
from streamlit_echarts import st_echarts, JsCode
from app.constants.theme import get_theme_styles

def render_investimentos_chart(df_transf_clube, chart_title: str) -> None:
    import streamlit as st

    if df_transf_clube.empty or "Ano" not in df_transf_clube or "Tipo" not in df_transf_clube or "Valor" not in df_transf_clube:
        st.warning("Dados insuficientes para exibir o gráfico.")
        return

    theme = get_theme_styles()

    df_grouped = (
        df_transf_clube.groupby(["Ano", "Tipo"])["Valor"]
        .sum()
        .reset_index()
    )

    anos = sorted(df_grouped["Ano"].unique())
    tipos = df_grouped["Tipo"].unique()

    series_data = []
    for tipo in tipos:
        valores = [
            float(df_grouped[(df_grouped["Ano"] == ano) & (df_grouped["Tipo"] == tipo)]["Valor"].sum())
            for ano in anos
        ]
        gradient = theme["BAR_GRADIENT_ENTRADA"] if tipo.lower() == "entrada" else theme["BAR_GRADIENT_SAIDA"]

        series_data.append({
            "name": tipo,
            "type": "bar",
            "barGap": "10%",
            "data": valores,
            "itemStyle": {
                "color": gradient,
                "opacity": 0.9
            }
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
                "function(params){"
                "  return params[0].name + '<br/>' + "
                "    params.map(p => p.marker + ' ' + p.seriesName + ': R$ ' + "
                "    p.value.toLocaleString('pt-BR', {minimumFractionDigits: 2})"
                "  ).join('<br/>');"
                "}"
            ).js_code
        },
        "legend": {
            "textStyle": {"color": theme["CHART_TEXT_STYLE"]["color"]}
        },
        "grid": {
            "left": "120px"
        },
        "xAxis": {
            "type": "category",
            "name": "Ano",
            "nameLocation": "center",
            "nameGap": 30,
            "nameTextStyle": theme["CHART_AXIS_TITLE_STYLE"],
            "data": [str(ano) for ano in anos],
            "axisLabel": theme["CHART_AXIS_LABEL_STYLE"],
            "axisLine": theme["CHART_AXIS_LINE_STYLE"],
            "splitLine": {
                "show": True,
                "lineStyle": {"color": theme["CHART_GRIDLINE_COLOR"]}
            }
        },
        "yAxis": {
            "type": "value",
            # Título do eixo Y removido
            "axisLabel": {
                "color": theme["CHART_AXIS_LABEL_STYLE"]["color"],
                "formatter": JsCode(
                    "function(value){return 'R$ ' + value.toLocaleString('pt-BR', {minimumFractionDigits: 2});}"
                ).js_code
            },
            "axisLine": theme["CHART_AXIS_LINE_STYLE"],
            "splitLine": {
                "show": True,
                "lineStyle": {"color": theme["CHART_GRIDLINE_COLOR"]}
            }
        },
        "series": series_data
    }

    st_echarts(options=options, height="500px")
