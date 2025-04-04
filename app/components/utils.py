# app/components/utils.py
import plotly.graph_objects as go

def format_currency(n: float) -> str:
    """Formata um número como moeda no padrão brasileiro."""
    return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_int(n: int) -> str:
    """Formata um número inteiro com separador de milhares."""
    return f"{n:,}".replace(",", "X").replace(".", ",").replace("X", ".")

def style_plotly(fig: go.Figure) -> None:
    """Aplica estilo padrão aos gráficos Plotly."""
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#000000", size=14, family="Open Sans Bold"),
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(
            tickfont=dict(family="Open Sans Bold", color="#000000", size=14),
            title_font=dict(family="Open Sans Bold", color="#000000", size=16)
        ),
        yaxis=dict(
            tickfont=dict(family="Open Sans Bold", color="#000000", size=14),
            title_font=dict(family="Open Sans Bold", color="#000000", size=16)
        )
    )

def style_map(fig: go.Figure) -> None:
    """Aplica estilo padrão a mapas choropleth Plotly."""
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#000000", size=14, family="Open Sans Bold"),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    fig.update_geos(
        bgcolor="#ffffff",
        fitbounds="locations",
        visible=False
    )

    if hasattr(fig.layout, "coloraxis") and fig.layout.coloraxis:
        coloraxis = fig.layout.coloraxis
        colorbar_title = (
            coloraxis.colorbar.title.text
            if hasattr(coloraxis, "colorbar")
            and hasattr(coloraxis.colorbar, "title")
            and hasattr(coloraxis.colorbar.title, "text")
            else "Total Gasto (R$)"
        )
        fig.update_coloraxes(colorbar=dict(
            title=dict(
                text=colorbar_title,
                font=dict(color="#000000", size=16, family="Open Sans Bold")
            ),
            tickfont=dict(color="#000000", size=14, family="Open Sans Bold")
        ))
