from pandas import DataFrame


def get_total_participacoes(df_info: DataFrame) -> int:
    return int(df_info.get("Participacoes_SerieA", 0))


def get_media_pontos(df_bras_clube: DataFrame) -> float:
    if "Pontos" not in df_bras_clube.columns:
        return 0.0
    df = df_bras_clube[df_bras_clube["Pontos"].notna()]
    return round(df["Pontos"].mean(), 2) if not df.empty else 0.0


def get_ultimo_ano(df_info: DataFrame) -> int:
    return int(df_info.get("Ultimo_Ano_SerieA", 0))


def get_saldo_transferencias(df_info: DataFrame) -> float:
    return float(df_info.get("Saldo_Transferencias_R$", 0.0))


def get_rebaixamentos(df_info: DataFrame) -> int:
    return int(df_info.get("Rebaixamentos", 0))


def get_aproveitamento(df_info: DataFrame) -> float:
    return float(df_info.get("Aproveitamento(%)", 0.0))


def get_internacionais(df_info: DataFrame) -> int:
    return int(df_info.get("Participacoes_Internacionais", 0))


def get_valor_total_gasto(df_entrada: DataFrame) -> float:
    return float(df_entrada["Valor"].sum()) if "Valor" in df_entrada.columns else 0.0


def get_total_contratacoes(df_entrada: DataFrame) -> int:
    return len(df_entrada)


def get_total_emprestimos(df_entrada: DataFrame) -> int:
    if "Empréstimo" not in df_entrada.columns:
        return 0
    return len(df_entrada[df_entrada["Empréstimo"].str.lower() == "sim"])


def get_contratacoes_com_custo(df_entrada: DataFrame) -> int:
    if "Valor" not in df_entrada.columns:
        return 0
    return len(df_entrada[df_entrada["Valor"] > 0])


def get_contratacoes_gratuitas(df_entrada: DataFrame) -> int:
    if "Valor" not in df_entrada.columns:
        return 0
    return len(df_entrada[df_entrada["Valor"] == 0])


def get_ticket_medio(df_entrada: DataFrame) -> float:
    if "Valor" not in df_entrada.columns:
        return 0.0
    total = len(df_entrada)
    return df_entrada["Valor"].sum() / total if total else 0.0


def get_ticket_medio_com_custo(df_entrada: DataFrame) -> float:
    if "Valor" not in df_entrada.columns:
        return 0.0
    com_custo = df_entrada[df_entrada["Valor"] > 0]
    total = len(com_custo)
    return com_custo["Valor"].sum() / total if total else 0.0


def get_classificacao_media(df_bras_clube: DataFrame) -> float:
    if "Posição" not in df_bras_clube.columns:
        return 0.0
    df = df_bras_clube[df_bras_clube["Posição"].notna()]
    return round(df["Posição"].mean(), 2) if not df.empty else 0.0


def get_saldo_gols(df_bras_clube: DataFrame) -> int:
    if "SG" in df_bras_clube.columns:
        return int(df_bras_clube["SG"].sum())
    elif "GP" in df_bras_clube.columns and "GC" in df_bras_clube.columns:
        return int((df_bras_clube["GP"] - df_bras_clube["GC"]).sum())
    return 0


def get_gasto_medio(df_transf_clube: DataFrame) -> float:
    if "Valor" not in df_transf_clube.columns or df_transf_clube.empty:
        return 0.0
    return round(df_transf_clube["Valor"].mean(), 2)


def get_titulos_seriea(df_bras: DataFrame, clube: str) -> int:
    if "Nome Oficial" not in df_bras.columns or "Posição" not in df_bras.columns:
        return 0
    df_clube = df_bras[df_bras["Nome Oficial"] == clube]
    return int((df_clube["Posição"] == 1).sum())


def get_vitorias(df_bras_clube: DataFrame) -> float:
    return (
        round(df_bras_clube["Vitórias"].mean(), 2)
        if "Vitórias" in df_bras_clube.columns
        else 0.0
    )


def get_derrotas(df_bras_clube: DataFrame) -> float:
    return (
        round(df_bras_clube["Derrotas"].mean(), 2)
        if "Derrotas" in df_bras_clube.columns
        else 0.0
    )


def get_empates(df_bras_clube: DataFrame) -> float:
    return (
        round(df_bras_clube["Empates"].mean(), 2)
        if "Empates" in df_bras_clube.columns
        else 0.0
    )
