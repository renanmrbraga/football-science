# app/main.py
import streamlit as st
import logging

from app.constants.css import inject_custom_css
from app.dashboards.clubes_dashboard import dashboard_clubes
from app.dashboards.transferencias_dashboard import dashboard_transferencias


def main():
    # === Configuração da página ===
    st.set_page_config(
        page_title="Football Analysis BR",
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
        st.title("📂 Navegação")
        if "dashboard" not in st.session_state:
            st.session_state["dashboard"] = "Clubes"

        st.session_state["dashboard"] = st.radio(
            "Selecione o dashboard:",
            ["Clubes", "Transferências"],
            index=["Clubes", "Transferências"].index(st.session_state["dashboard"])
        )

    # === CSS global ===
    inject_custom_css()

    # === Renderiza ===
    dashboards = {
        "Clubes": dashboard_clubes,
        "Transferências": dashboard_transferencias
    }
    dashboards[st.session_state["dashboard"]]()


if __name__ == "__main__":
    main()
