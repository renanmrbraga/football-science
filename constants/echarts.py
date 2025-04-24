# app/constants/echarts.py
from constants.theme import get_theme_styles

# Obter os estilos do tema
theme = get_theme_styles()

# Gradiente horizontal (para gráficos de barras horizontais)
GRADIENT_HORIZONTAL = {
    "type": "linear",
    "x": 0, "y": 0, "x2": 1, "y2": 0,
    "colorStops": [
        {"offset": 0, "color": theme["GRADIENT_HORIZONTAL"][0]},
        {"offset": 1, "color": theme["GRADIENT_HORIZONTAL"][1]},
    ]
}

# Gradiente vertical (para gráficos de área)
GRADIENT_VERTICAL = {
    "type": "linear",
    "x": 0, "y": 0, "x2": 0, "y2": 1,
    "colorStops": [
        {"offset": 0, "color": theme["GRADIENT_VERTICAL"][0]},
        {"offset": 1, "color": theme["GRADIENT_VERTICAL"][1]},
    ]
}

# Estilo do título dos gráficos
ECHARTS_TITLE_STYLE = {
    "textStyle": {
        "color": theme["FOREGROUND_COLOR"]
    }
}

# Estilo dos eixos dos gráficos
AXIS_LABEL_STYLE = {
    "axisLabel": {
        "color": theme["FOREGROUND_COLOR"]
    },
    "axisLine": {
        "lineStyle": {
            "color": theme["FOREGROUND_COLOR"]
        }
    },
    "splitLine": {
        "lineStyle": {
            "color": "#444"
        }
    }
}

# Estilo dos tooltips
TOOLTIP_STYLE = {
    "trigger": "axis",
    "axisPointer": {"type": "shadow"},
    "backgroundColor": theme["TOOLTIP_BG"],
    "borderColor": theme["PRIMARY_BLUE"],
    "textStyle": {"color": theme["TOOLTIP_TEXT"]}
}
