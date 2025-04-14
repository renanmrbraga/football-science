# app/components/charts/gastos_por_ano_chart.py
from streamlit_echarts import st_echarts
from app.constants.echarts import GRADIENT_VERTICAL
from app.constants.theme import get_theme_styles  # Ajuste para acessar os estilos do tema

# Obter os estilos do tema
theme = get_theme_styles()

def render_gastos_por_ano_chart(df_entrada, chart_title: str) -> None:
    df_ano = (
        df_entrada.groupby("Ano")["Valor"]
        .sum()
        .reset_index()
        .sort_values("Ano")
    )

    anos = df_ano["Ano"].astype(str).tolist()
    valores = df_ano["Valor"].astype(float).tolist()

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
            "axisPointer": {"type": "line"},
            "backgroundColor": theme["TOOLTIP_BG"],
            "borderColor": theme["PRIMARY_BLUE"],
            "textStyle": {"color": theme["TOOLTIP_TEXT"]},
            "formatter": "{b}<br/>{a0}: {c0}"
        },
        "xAxis": {
            "type": "category",
            "data": anos,
            "axisLabel": {
                "color": theme["FOREGROUND_COLOR"]
            },
            "axisLine": {
                "lineStyle": {"color": theme["FOREGROUND_COLOR"]}
            }
        },
        "yAxis": {
            "type": "value",
            "axisLabel": {
                "color": theme["FOREGROUND_COLOR"]
            },
            "axisLine": {
                "lineStyle": {"color": theme["FOREGROUND_COLOR"]}
            },
            "splitLine": {
                "lineStyle": {"color": "#333"}
            }
        },
        "series": [{
            "name": "Gastos",  # <--- Isso remove o 'series0' do tooltip
            "data": valores,
            "type": "line",
            "smooth": True,
            "areaStyle": {
                "color": GRADIENT_VERTICAL,
                "opacity": 0.25
            },
            "lineStyle": {"width": 3, "color": theme["FOREGROUND_COLOR"]},
            "symbol": "circle",
            "symbolSize": 10
        }]
    }

    st_echarts(options=options, height="500px")
