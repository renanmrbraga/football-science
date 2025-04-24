import streamlit as st
from streamlit_javascript import st_javascript

def validar_contraste(modo_dev=False):
    js_code = r"""
    async function checkContrast() {
        function luminancia(cor) {
            let c = cor.replace(/[^\d,]/g, '').split(',').map(Number);
            let [r, g, b] = c.map(v => {
                v /= 255;
                return v <= 0.03928
                    ? v / 12.92
                    : Math.pow((v + 0.055) / 1.055, 2.4);
            });
            return 0.2126 * r + 0.7152 * g + 0.0722 * b;
        }

        function contraste(bg, fg) {
            const L1 = luminancia(bg) + 0.05;
            const L2 = luminancia(fg) + 0.05;
            return L1 > L2 ? L1 / L2 : L2 / L1;
        }

        function pegarCor(selector, prop) {
            const el = document.querySelector(selector);
            if (!el) return null;
            return getComputedStyle(el).getPropertyValue(prop);
        }

        const elementos = [
            { selector: ".stSelectbox > div", nome: "Selectbox" },
            { selector: ".stButton > button", nome: "Botão" },
            { selector: "ul[role='listbox']", nome: "Dropdown" },
        ];

        let resultado = [];

        for (let el of elementos) {
            const bg = pegarCor(el.selector, "background-color");
            const fg = pegarCor(el.selector, "color");

            if (!bg || !fg) continue;

            const c = contraste(bg, fg);
            if (c < 4.5) resultado.push({ nome: el.nome, contraste: c.toFixed(2) });
        }

        return resultado;
    }

    return await checkContrast();
    """

    resultado = st_javascript(js_code, key="contraste-silencioso")

    # Só exibe resultado se estiver em modo_dev
    if modo_dev and resultado:
        if len(resultado) > 0:
            for problema in resultado:
                st.warning(f"⚠️ Contraste insuficiente em **{problema['nome']}**: {problema['contraste']} (mínimo: 4.5)")
        else:
            st.success("✅ Todos os elementos principais possuem contraste adequado.")
