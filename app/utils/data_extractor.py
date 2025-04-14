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
