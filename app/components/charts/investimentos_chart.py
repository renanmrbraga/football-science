# app/components/charts/investimentos_chart.py
from streamlit_echarts import st_echarts
from app.constants.theme import get_theme_styles  # Atualização para usar a função

# Obtendo os estilos do tema
theme = get_theme_styles()
CHART_TEXT_STYLE = theme["CHART_TEXT_STYLE"]
CHART_AXIS_LABEL_STYLE = theme["CHART_AXIS_LABEL_STYLE"]
CHART_TOOLTIP_STYLE = theme["CHART_TOOLTIP_STYLE"]

def render_investimentos_chart(df_transf_clube, chart_title: str) -> None:
    df_grouped = (
        df_transf_clube.groupby(["Ano", "Tipo"])["Valor"]
        .sum()
        .reset_index()
    )

    anos = sorted(df_grouped["Ano"].unique())
    tipos = df_grouped["Tipo"].unique()

    GRADIENT_ENTRADA = {
        "type": "linear",
        "x": 0, "y": 0, "x2": 1, "y2": 0,
        "colorStops": [
            {"offset": 0, "color": "#00c6ff"},
            {"offset": 1, "color": "#003366"}
        ]
    }

    GRADIENT_SAIDA = {
        "type": "linear",
        "x": 0, "y": 0, "x2": 1, "y2": 0,
        "colorStops": [
            {"offset": 0, "color": "#b14cff"},
            {"offset": 1, "color": "#3e0099"}
        ]
    }

    series_data = []
    for tipo in tipos:
        valores = [
            float(df_grouped[(df_grouped["Ano"] == ano) & (df_grouped["Tipo"] == tipo)]["Valor"].sum())
            for ano in anos
        ]
        gradient = GRADIENT_ENTRADA if tipo.lower() == "entrada" else GRADIENT_SAIDA

        series_data.append({
            "name": tipo,
            "type": "bar",
            "barGap": "10%",
            "data": valores,
            "itemStyle": {
                "color": gradient,
                "opacity": 0.95
            }
        })

    options = {
        "title": {
            "text": chart_title,
            "textStyle": CHART_TEXT_STYLE
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "backgroundColor": CHART_TOOLTIP_STYLE["backgroundColor"],
            "borderColor": CHART_TOOLTIP_STYLE["borderColor"],
            "textStyle": CHART_TOOLTIP_STYLE["textStyle"],
            "formatter": "{b}<br/>{a0}: {c0}<br/>{a1}: {c1}"
        },
        "legend": {
            "textStyle": {"color": CHART_TEXT_STYLE["color"]}
        },
        "xAxis": {
            "type": "category",
            "data": [str(ano) for ano in anos],
            "axisLabel": CHART_AXIS_LABEL_STYLE,
            "axisLine": {"lineStyle": {"color": CHART_AXIS_LABEL_STYLE["color"]}}
        },
        "yAxis": {
            "type": "value",
            "axisLabel": CHART_AXIS_LABEL_STYLE,
            "axisLine": {"lineStyle": {"color": CHART_AXIS_LABEL_STYLE["color"]}},
            "splitLine": {"lineStyle": {"color": "#333"}}
        },
        "series": series_data
    }

    st_echarts(options=options, height="500px")
