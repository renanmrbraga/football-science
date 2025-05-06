# app/main.py
import streamlit as st
import logging

from constants.css import inject_custom_css
from dashboards.dashboard_clubes_seriea import dashboard_clubes_seriea
from dashboards.transferencias_dashboard import dashboard_transferencias
from utils.theme_tester import validar_contraste

def main():
    # === Configuração da página ===
    st.set_page_config(
        page_title="Football Science",
        page_icon="⚽",
        layout="wide"
    )
    logging.basicConfig(level=logging.INFO)

    # Detecta mobile via query params
    query_params = st.query_params
    is_mobile_flag = query_params.get("isMobile", ["false"])[0].lower() == "true"
    st.session_state["is_mobile"] = is_mobile_flag

    # === SIDEBAR ===
    with st.sidebar:
        st.title("⚙️ Personalização")

        # Detecta ou inicializa o tema
        if "chosen_theme" not in st.session_state:
            st.session_state["chosen_theme"] = st.get_option("theme.base") or "dark"
            st.session_state["theme_changed"] = False

        selected_theme = st.selectbox(
            "Tema",
            ["dark", "light"],
            index=0 if st.session_state["chosen_theme"] == "dark" else 1
        )

        if selected_theme != st.session_state["chosen_theme"]:
            st.session_state["chosen_theme"] = selected_theme
            st.session_state["theme_changed"] = True
        else:
            st.session_state["theme_changed"] = False

        # Navegação
        pagina = st.radio(
            "Selecione o dashboard:",
            ["Clubes - Série A", "Transferências"]
        )

    # === CSS global ===
    inject_custom_css()

    # === Validador de contraste ===
    validar_contraste()

    # === Renderiza o dashboard ===
    dashboards = {
        "Clubes - Série A": dashboard_clubes_seriea,
        "Transferências": dashboard_transferencias
    }
    dashboards[pagina]()

if __name__ == "__main__":
    main()
