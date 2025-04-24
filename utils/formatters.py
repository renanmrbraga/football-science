# app/components/formatters.py
def format_currency(n: float) -> str:
    """Formata um número como moeda no padrão brasileiro."""
    return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_currency_symbol(n: float) -> str:
    """Formata número como moeda com símbolo R$."""
    return f"R$ {format_currency(n)}"

def format_int(n: int) -> str:
    """Formata um número inteiro com separador de milhares."""
    return f"{n:,}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percent(n: float, decimals: int = 2) -> str:
    """Formata um número como porcentagem no padrão brasileiro."""
    return f"{n:.{decimals}f}".replace(".", ",") + " %"

def abreviar_valor(valor):
    if valor >= 1e9:
        return f"{valor / 1e9:.1f} bi"
    elif valor >= 1e6:
        return f"{valor / 1e6:.1f} mi"
    elif valor >= 1e3:
        return f"{valor / 1e3:.1f} mil"
    else:
        return str(valor)
