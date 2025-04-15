# app/main.py
import streamlit as st
import logging

from app.constants.css import inject_custom_css
from app.dashboards.clubes_dashboard import dashboard_clubes
from app.dashboards.transferencias_dashboard import dashboard_transferencias


def main():
    # Configuração global da página
    st.set_page_config(
        page_title="Football Analysis BR",
        page_icon="⚽",
        layout="wide"
    )
    logging.basicConfig(level=logging.INFO)

    # === SIDEBAR: Tema e Navegação ===
    with st.sidebar:
        st.title("⚙️ Personalização")

        # Detecta ou inicializa o tema do navegador
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

        # Navegação entre dashboards
        st.title("📂 Navegação")
        if "dashboard" not in st.session_state:
            st.session_state["dashboard"] = "Clubes"

        st.session_state["dashboard"] = st.radio(
            "Selecione o dashboard:",
            ["Clubes", "Transferências"],
            index=["Clubes", "Transferências"].index(st.session_state["dashboard"])
        )

    # === CSS customizado global ===
    inject_custom_css()

    # === Renderiza o dashboard selecionado ===
    dashboards = {
        "Clubes": dashboard_clubes,
        "Transferências": dashboard_transferencias
    }
    dashboards[st.session_state["dashboard"]]()


if __name__ == "__main__":
    main()
