# app/constants/theme.py
import streamlit as st

# === DEFINIÇÃO DOS TEMAS ===
LIGHT_THEME = {
    "mode": "light",
    "PRIMARY_BLUE": "#003366",
    "HIGHLIGHT_COLOR": "#1a60af",
    "FOREGROUND_COLOR": "#000000",
    "BACKGROUND_COLOR": "#ffffff",
    "CARD_BACKGROUND": "#f0f2f6",
    "GRADIENT": {
        "horizontal": ["#80a9d0", "#003366"],
        "vertical": ["#003366", "#e6f2ff"]
    },
    "TOOLTIP_BG": "#ffffff",
    "TOOLTIP_TEXT": "#000000",
    "RADIO_COLOR": "#1a60af",
    # Nova cor terciária para linhas de gráfico
    "CHART_TERTIARY_COLOR": "#FF77AA"
}

DARK_THEME = {
    "mode": "dark",
    "PRIMARY_BLUE": "#003366",
    "HIGHLIGHT_COLOR": "#00c6ff",
    "FOREGROUND_COLOR": "#ffffff",
    "BACKGROUND_COLOR": "#0d1117",
    "CARD_BACKGROUND": "#161b22",
    "GRADIENT": {
        "horizontal": ["#0072ff", "#00c6ff"],
        "vertical": ["#00c6ff", "#161b22"]
    },
    "TOOLTIP_BG": "#222222",
    "TOOLTIP_TEXT": "#ffffff",
    "RADIO_COLOR": "#00c6ff",
    # Nova cor terciária para linhas de gráfico
    "CHART_TERTIARY_COLOR": "#FF4F79"
}

THEMES = {
    "light": LIGHT_THEME,
    "dark": DARK_THEME
}

# === INICIALIZAÇÃO DO TEMA COM BASE NO NAVEGADOR E SELEÇÃO MANUAL ===
def init_theme():
    browser_theme = st.get_option("theme.base")
    if "chosen_theme" not in st.session_state:
        st.session_state["chosen_theme"] = browser_theme if browser_theme in ["light", "dark"] else "dark"
        st.session_state["theme_changed"] = False

    selected_theme = st.sidebar.selectbox(
        "Tema",
        ["dark", "light"],
        index=0 if st.session_state["chosen_theme"] == "dark" else 1
    )

    if selected_theme != st.session_state["chosen_theme"]:
        st.session_state["chosen_theme"] = selected_theme
        st.session_state["theme_changed"] = True
    else:
        st.session_state["theme_changed"] = False


def theme_changed():
    return st.session_state.get("theme_changed", False)

# === ESTILOS COMPLETOS PARA COMPONENTES VISUAIS ===
def get_theme_styles():
    chosen = st.session_state.get("chosen_theme", "dark")
    theme = THEMES[chosen]

    # Estilos extras para gráficos
    if chosen == "dark":
        primary_color = theme["HIGHLIGHT_COLOR"]
        secondary_color = "#a7ff00"
        gridline_color = "#333"
        axis_line_color = "#ccc"
        bar_gradient_entrada = {
            "type": "linear", "x": 0, "y": 0, "x2": 1, "y2": 0,
            "colorStops": [
                {"offset": 0, "color": "rgba(0,198,255,0.8)"},
                {"offset": 1, "color": "rgba(0,51,102,0.2)"}
            ]
        }
        bar_gradient_saida = {
            "type": "linear", "x": 0, "y": 0, "x2": 1, "y2": 0,
            "colorStops": [
                {"offset": 0, "color": "rgba(177,76,255,0.8)"},
                {"offset": 1, "color": "rgba(62,0,153,0.2)"}
            ]
        }
        area_gradient = {
            "type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
            "colorStops": [
                {"offset": 0, "color": "rgba(0,198,255,0.35)"},
                {"offset": 1, "color": "rgba(0,114,255,0.05)"}
            ]
        }
    else:
        primary_color = theme["PRIMARY_BLUE"]
        secondary_color = theme["HIGHLIGHT_COLOR"]
        gridline_color = "#aaa"
        axis_line_color = "#333"
        bar_gradient_entrada = {
            "type": "linear", "x": 0, "y": 0, "x2": 1, "y2": 0,
            "colorStops": [
                {"offset": 0, "color": "rgba(26,96,175,0.8)"},
                {"offset": 1, "color": "rgba(128,169,208,0.2)"}
            ]
        }
        bar_gradient_saida = {
            "type": "linear", "x": 0, "y": 0, "x2": 1, "y2": 0,
            "colorStops": [
                {"offset": 0, "color": "rgba(230,126,34,0.9)"},
                {"offset": 1, "color": "rgba(230,126,34,0.3)"}
            ]
        }
        area_gradient = {
            "type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
            "colorStops": [
                {"offset": 0, "color": "rgba(26,96,175,0.35)"},
                {"offset": 1, "color": "rgba(26,96,175,0.05)"}
            ]
        }

    return {
        "mode": theme["mode"],
        "PRIMARY_BLUE": theme["PRIMARY_BLUE"],
        "HIGHLIGHT_COLOR": theme["HIGHLIGHT_COLOR"],
        "FOREGROUND_COLOR": theme["FOREGROUND_COLOR"],
        "BACKGROUND_COLOR": theme["BACKGROUND_COLOR"],
        "CARD_BACKGROUND": theme["CARD_BACKGROUND"],
        "RADIO_COLOR": theme.get("RADIO_COLOR", None),
        "TOOLTIP_BG": theme["TOOLTIP_BG"],
        "TOOLTIP_TEXT": theme["TOOLTIP_TEXT"],
        "SELECTBOX_BG": "#ffffff" if theme["BACKGROUND_COLOR"].lower() in ["#ffffff", "#fff", "white"] else theme["CARD_BACKGROUND"],
        "SELECTBOX_TEXT": "#000000" if theme["BACKGROUND_COLOR"].lower() in ["#ffffff", "#fff", "white"] else theme["FOREGROUND_COLOR"],
        "DROPDOWN_BG": "#ffffff" if theme["BACKGROUND_COLOR"].lower() in ["#ffffff", "#fff", "white"] else theme["CARD_BACKGROUND"],
        "DROPDOWN_TEXT": "#000000" if theme["BACKGROUND_COLOR"].lower() in ["#ffffff", "#fff", "white"] else theme["FOREGROUND_COLOR"],
        "BORDER_COLOR": theme["HIGHLIGHT_COLOR"],

        # Gradientes
        "GRADIENT_HORIZONTAL": theme["GRADIENT"]["horizontal"],
        "GRADIENT_VERTICAL": theme["GRADIENT"]["vertical"],
        "GRADIENT_VERTICAL_ECHARTS": {
            "type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
            "colorStops": [
                {"offset": 0, "color": theme["GRADIENT"]["vertical"][0]},
                {"offset": 1, "color": theme["GRADIENT"]["vertical"][1]}
            ]
        },
        "GRADIENT_HORIZONTAL_ECHARTS": {
            "type": "linear", "x": 0, "y": 0, "x2": 1, "y2": 0,
            "colorStops": [
                {"offset": 0, "color": theme["GRADIENT"]["horizontal"][0]},
                {"offset": 1, "color": theme["GRADIENT"]["horizontal"][1]}
            ]
        },

        # Cards
        "CARD_STYLE": (
            f"background-color: {theme['CARD_BACKGROUND']};"
            "padding: 1.2rem;"
            "border-radius: 1rem;"
            f"box-shadow: 0 0 15px {theme['HIGHLIGHT_COLOR']}55;"
            "text-align: center;"
            "min-width: 180px;"
            "transition: all 0.3s ease;"
        ),
        "CARD_TITLE_STYLE": (
            f"color: {theme['FOREGROUND_COLOR']};"
            "margin-bottom: 0.5rem;"
            "font-size: 1.05rem;"
            "font-weight: 500;"
        ),
        "CARD_VALUE_STYLE": (
            f"color: {theme['HIGHLIGHT_COLOR']};"
            "margin: 0;"
            "font-size: 1.6rem;"
            "font-weight: bold;"
        ),

        # Gráficos
        "CHART_TEXT_STYLE": {
            "color": theme["FOREGROUND_COLOR"],
            "fontWeight": "bold",
            "fontSize": 20
        },
        "CHART_AXIS_LABEL_STYLE": {
            "color": theme["FOREGROUND_COLOR"],
            "fontSize": 12
        },
        "CHART_AXIS_LINE_STYLE": {
            "lineStyle": {"color": axis_line_color}
        },
        "CHART_AXIS_TITLE_STYLE": {
            "color": theme["FOREGROUND_COLOR"],
            "fontSize": 12,
            "fontWeight": "bold"
        },
        "CHART_GRIDLINE_COLOR": gridline_color,
        "CHART_TOOLTIP_STYLE": {
            "backgroundColor": theme["TOOLTIP_BG"],
            "borderColor": theme["PRIMARY_BLUE"],
            "textStyle": {"color": theme["TOOLTIP_TEXT"]}
        },
        "CHART_PRIMARY_COLOR": primary_color,
        "CHART_SECONDARY_COLOR": secondary_color,
        # Nova cor terciária para linhas de gráfico
        "CHART_TERTIARY_COLOR": theme["CHART_TERTIARY_COLOR"],
        "CHART_AREA_GRADIENT": area_gradient,
        "BAR_GRADIENT_ENTRADA": bar_gradient_entrada,
        "BAR_GRADIENT_SAIDA": bar_gradient_saida,
        "CHART_RADAR_BG": ["#1d1d1d", "#121212", "transparent"] if chosen == "dark" else ["#ffffff", "#f0f2f6", "transparent"],
    }
