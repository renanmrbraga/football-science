# app/constants/texts.py

# === TÍTULOS DAS PÁGINAS ===
TITLE_CLUBES = "Análise dos Clubes na Série A"
TITLE_TRANSFERENCIAS = "Transferências dos Clubes"
TITLE_DASHBOARD_APP = "Dashboards de Análise"

# === BARRA LATERAL ===
SIDEBAR_TITLE = "Selecione o Dashboard"
SIDEBAR_OPTIONS = ["Brasileirão", "Transferências"]

# === ERROS ===
ERROR_LOAD_DATA = "Erro ao carregar os dados."
ERROR_EMPTY_DATASET = "Dataset não carregado."
WARNING_EMPTY_ENTRADAS = "Não há dados de transferências de entrada disponíveis."
WARNING_GEOJSON_MISSING = "GeoJSON não encontrado. Mapa não exibido."
WARNING_NO_UF_COLUMN = "Coluna 'UF' não encontrada. Mapa não será exibido."
WARNING_GEO_LOAD_FAIL = "Erro ao carregar geojson:"

# === MÉTRICAS ===
METRICS = {
    "participacoes": "Participações",
    "rebaixamentos": "Rebaixamentos",
    "media_pontos": "Média de Pontos",
    "aproveitamento": "Aproveitamento (%)",
    "ultimo_ano": "Último Ano",
    "internacionais": "Internacionais",
    "saldo_transferencias": "Saldo Transf. (R$)",
    "valor_total": "Valor Total Gasto",
    "total_contratacoes": "Total de Contratações",
    "ticket_medio": "Ticket Médio - Total",
    "com_custo": "Contratações - Com Custo",
    "ticket_custo": "Ticket Médio - Com Custo",
    "gratuitas": "Contratações - Gratuitas",
    "emprestimos": "Total de Empréstimos"
}

# === TÍTULOS DE GRÁFICOS ===
CHARTS = {
    "evolucao_brasileirao": "Evolução no Brasileirão",
    "posicao_ano": lambda clube: f"{clube} no Brasileirão",
    "transferencias": "Transferências",
    "investimentos": "Investimentos e Vendas",
    "gastos_ano": "Evolução do Gasto por Ano",
    "mapa_transferencias": "Distribuição Geográfica de Transferências",
    "top_gastos": "Top 10 Clubes que Mais Gastaram"
}
