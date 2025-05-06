# app/utils/data_extractor.py
def get_total_participacoes(df_info) -> int:
    return int(df_info["Participacoes_SerieA"])

def get_media_pontos(df_bras_clube) -> float:
    # filtra linhas válidas
    df = df_bras_clube[df_bras_clube["Pontos"].notna()]
    return round(df["Pontos"].mean(), 2) if not df.empty else 0.0

def get_ultimo_ano(df_info) -> int:
    return int(df_info["Ultimo_Ano_SerieA"])

def get_saldo_transferencias(df_info) -> float:
    return float(df_info["Saldo_Transferencias_R$"])

def get_rebaixamentos(df_info) -> int:
    return int(df_info["Rebaixamentos"])

def get_aproveitamento(df_info) -> float:
    return float(df_info["Aproveitamento(%)"])

def get_internacionais(df_info) -> int:
    return int(df_info["Participacoes_Internacionais"])

def get_valor_total_gasto(df_entrada):
    return df_entrada["Valor"].sum()

def get_total_contratacoes(df_entrada):
    return len(df_entrada)

def get_total_emprestimos(df_entrada):
    return len(df_entrada[df_entrada["Empréstimo"].str.lower() == "sim"])

def get_contratacoes_com_custo(df_entrada):
    return len(df_entrada[df_entrada["Valor"] > 0])

def get_contratacoes_gratuitas(df_entrada):
    return len(df_entrada[df_entrada["Valor"] == 0])

def get_ticket_medio(df_entrada):
    total = len(df_entrada)
    return df_entrada["Valor"].sum() / total if total else 0

def get_ticket_medio_com_custo(df_entrada):
    com_custo = df_entrada[df_entrada["Valor"] > 0]
    total = len(com_custo)
    return com_custo["Valor"].sum() / total if total else 0

def get_classificacao_media(df_bras_clube) -> float:
    df = df_bras_clube[df_bras_clube["Posição"].notna()]
    return round(df["Posição"].mean(), 2) if not df.empty else 0

def get_saldo_gols(df_bras_clube) -> int:
    if "SG" in df_bras_clube.columns:
        return int(df_bras_clube["SG"].sum())
    if "GP" in df_bras_clube.columns and "GC" in df_bras_clube.columns:
        diff = (df_bras_clube["GP"] - df_bras_clube["GC"]).sum()
        return int(diff)
    return 0

def get_gasto_medio(df_transf_clube) -> float:
    if df_transf_clube.empty:
        return 0.0
    return round(df_transf_clube["Valor"].mean(), 2)

def get_titulos_seriea(df_bras, clube):
    df_clube = df_bras[df_bras["Nome Oficial"] == clube]
    if "Posição" in df_clube.columns:
        return int((df_clube["Posição"] == 1).sum())
    return 0

def get_vitorias(df_bras_clube) -> float:
    # média de vitórias por temporada
    return round(df_bras_clube["Vitórias"].mean(), 2) if "Vitórias" in df_bras_clube.columns else 0.0

def get_derrotas(df_bras_clube) -> float:
    # média de derrotas por temporada
    return round(df_bras_clube["Derrotas"].mean(), 2) if "Derrotas" in df_bras_clube.columns else 0.0

def get_empates(df_bras_clube) -> float:
    # média de empates por temporada
    return round(df_bras_clube["Empates"].mean(), 2) if "Empates" in df_bras_clube.columns else 0.0
