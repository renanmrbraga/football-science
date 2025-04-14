# app/components/charts/top_gastos_chart.py
from streamlit_echarts import st_echarts
from app.constants.echarts import GRADIENT_HORIZONTAL
from app.constants.theme import get_theme_styles

# Obter os estilos do tema
theme = get_theme_styles()

def render_top_gastos_chart(df_entrada, chart_title: str) -> None:
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
                    **GRADIENT_HORIZONTAL,
                    "opacity": 0.9
                }
            }
        }
        for valor in valores
    ]

    options = {
        "title": {
            "text": chart_title,
            "textStyle": {
                "color": theme["FOREGROUND_COLOR"],
                "fontWeight": "bold",
                "fontSize": 14
            }
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "backgroundColor": theme["TOOLTIP_BG"],
            "borderColor": theme["PRIMARY_BLUE"],
            "textStyle": {"color": theme["TOOLTIP_TEXT"]},
        },
        "grid": {
            "left": "160px",
            "right": "40px",
            "top": "60px",
            "bottom": "40px"
        },
        "xAxis": {
            "type": "value",
            "axisLabel": {
                "color": theme["FOREGROUND_COLOR"],
                "formatter": "{value}"
            },
            "axisLine": {"lineStyle": {"color": theme["FOREGROUND_COLOR"]}},
            "splitLine": {"lineStyle": {"color": "#333"}}
        },
        "yAxis": {
            "type": "category",
            "data": clubes,
            "axisLabel": {
                "color": theme["FOREGROUND_COLOR"],
                "interval": 0,
                "fontSize": 12,
                "overflow": "break",
                "width": 120
            },
            "axisLine": {"lineStyle": {"color": theme["FOREGROUND_COLOR"]}}
        },
        "series": [{
            "type": "bar",
            "name": "Gastos",
            "data": series_data,
            "barWidth": "60%",
        }]
    }

    st_echarts(options=options, height="500px")
