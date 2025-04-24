# app/utils/data_extractor.py
def get_total_participacoes(df_info) -> int:
    return int(df_info["Participacoes_SerieA"])

def get_media_pontos(df_info) -> float:
    return round(df_info["Media_Pontos"], 2)

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
    df = df_bras_clube.copy()
    if "Gols Pró" in df.columns and "Gols Contra" in df.columns:
        df["Saldo"] = df["Gols Pró"] - df["Gols Contra"]
        return int(df["Saldo"].sum())
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
