# app/constants/theme_config.py
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
    "TOOLTIP_TEXT": "#000000"
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
    "TOOLTIP_TEXT": "#ffffff"
}

THEMES = {
    "light": LIGHT_THEME,
    "dark": DARK_THEME
}
