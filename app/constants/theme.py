# app/constants/theme.py
import streamlit as st
from app.constants.theme_config import THEMES

def init_theme():
    """
    Exibe UM ÚNICO seletor de tema na sidebar e armazena a escolha em st.session_state["chosen_theme"].
    Essa função deve ser chamada no início (por exemplo, no main.py) para evitar duplicações.
    """
    if "chosen_theme" not in st.session_state:
        st.session_state["chosen_theme"] = "dark"  # valor padrão

    # Selectbox com chave única (único seletor global)
    selected_theme = st.sidebar.selectbox(
        "Tema",
        ["dark", "light"],
        index=0 if st.session_state["chosen_theme"] == "dark" else 1,
        key="unique_theme_selector"
    )
    st.session_state["chosen_theme"] = selected_theme

def get_theme_styles():
    """
    Retorna um dicionário com os estilos baseados na escolha do tema (light ou dark).
    """
    # Lê a escolha do usuário (padrão dark se não existir)
    chosen = st.session_state.get("chosen_theme", "dark")
    theme = THEMES[chosen]

    return {
        "PRIMARY_BLUE": theme["PRIMARY_BLUE"],
        "HIGHLIGHT_COLOR": theme["HIGHLIGHT_COLOR"],
        "FOREGROUND_COLOR": theme["FOREGROUND_COLOR"],
        "BACKGROUND_COLOR": theme["BACKGROUND_COLOR"],
        "CARD_BACKGROUND": theme["CARD_BACKGROUND"],
        "GRADIENT_HORIZONTAL": theme["GRADIENT"]["horizontal"],
        "GRADIENT_VERTICAL": theme["GRADIENT"]["vertical"],
        "TOOLTIP_BG": theme["TOOLTIP_BG"],
        "TOOLTIP_TEXT": theme["TOOLTIP_TEXT"],
        # Gradientes prontos para ECharts
        "GRADIENT_VERTICAL_ECHARTS": {
            "type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
            "colorStops": [
                {"offset": 0, "color": theme["GRADIENT"]["vertical"][0]},
                {"offset": 1, "color": theme["GRADIENT"]["vertical"][1]},
            ]
        },
        "GRADIENT_HORIZONTAL_ECHARTS": {
            "type": "linear", "x": 0, "y": 0, "x2": 1, "y2": 0,
            "colorStops": [
                {"offset": 0, "color": theme["GRADIENT"]["horizontal"][0]},
                {"offset": 1, "color": theme["GRADIENT"]["horizontal"][1]},
            ]
        },
        # Estilos para Cards
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
        # Estilos ECharts globais
        "CHART_TEXT_STYLE": {
            "color": theme["FOREGROUND_COLOR"],
            "fontWeight": "bold",
            "fontSize": 14
        },
        "CHART_AXIS_LABEL_STYLE": {
            "color": theme["FOREGROUND_COLOR"]
        },
        "CHART_TOOLTIP_STYLE": {
            "backgroundColor": theme["TOOLTIP_BG"],
            "borderColor": theme["PRIMARY_BLUE"],
            "textStyle": {"color": theme["TOOLTIP_TEXT"]}
        }
    }
