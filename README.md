![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-dark?style=for-the-badge&logo=streamlit&logoColor=white)
![ECharts](https://img.shields.io/badge/ECharts-000000?style=for-the-badge&logo=apacheecharts&logoColor=white)

# Football Science

Sistema completo de **ciência de dados futebolísticos**, com ETL automatizado, scraping de fontes abertas, armazenamento em banco PostgreSQL e visualização interativa via Streamlit + ECharts. Focado em clubes da elite do futebol brasileiro, oferece insights sobre desempenho, eficiência e histórico competitivo.

---

## 📌 Índice

- [✨ Funcionalidades](#-funcionalidades)
- [📊 Fontes de Dados](#-fontes-de-dados)
- [⚖️ Arquitetura](#-arquitetura)
- [🛠️ Tecnologias](#-tecnologias)
- [🚀 Setup Rápido](#-setup-rápido)
- [🔖 Licença](#-licença)
- [📢 Aviso](#-aviso)

---

## ✨ Funcionalidades

### Pipeline completo e automatizado:

1. **Coleta de dados** via scraping com `Selenium` e `BeautifulSoup`
2. **Tratamento, limpeza e padronização** com `Pandas`
3. **Armazenamento estruturado** em banco de dados `PostgreSQL`
4. **Visualização interativa** com `Streamlit` + `ECharts`

---

### Dashboard: **Análise dos Clubes na Série A**

- **Radar Multimétrico**: Aproveitamento, Pontuação média, Classificação média, Saldo de gols, Gasto médio
- **Aproveitamento por Temporada** (linha)
- **Gasto em Transferências por Temporada** (barra vertical)
- **Eficiência: Gasto vs Pontuação Média** (scatter)
- **Títulos conquistados** (barra vertical)
- **Rebaixamentos** (barra vertical)
- **Participações na Série A** (barra vertical)

> Todos os gráficos suportam comparação entre dois clubes selecionados.

---

### Dashboard: **Análise das Transferências**

- **Evolução de investimento por temporada** (barra)
- **Balanço de compras e vendas** (linha ou barra empilhada)
- **Top clubes compradores e vendedores** (ranking)
- **Distribuição de tipos de transferência** (empréstimo x definitiva)
- **Rede de transferências (futuro)**

> Gráficos focados na movimentação financeira e comportamento de mercado.

## 📊 Fontes de Dados

- Dados coletados automaticamente para uso educacional a partir de portais públicos como a Wikipedia e sites especializados de futebol
- Os dados são utilizados apenas para análise e visualização, não sendo redistribuídos nem revendidos

---

## ⚖️ Arquitetura

```
📁 football-science/
├── components/        # Componentes visuais reutilizáveis (gráficos, KPIs, etc)
├── constants/         # Temas, textos fixos e configurações globais
├── dashboards/        # Dashboards principais (clubes, transferências, etc)
├── notebooks/         # Análises exploratórias, validações e testes
├── scraping/          # Scripts de scraping (Selenium + BeautifulSoup)
├── utils/             # Funções auxiliares e formatações reutilizáveis
│
├── .gitignore         # Arquivos ignorados pelo Git
├── LICENSE            # Licença de uso do projeto
├── main.py            # Entrypoint da aplicação Streamlit
├── README.md          # Documentação do repositório
└── requirements.txt   # Lista de dependências Python
```

---

## 🛠️ Tecnologias

| Camada             | Tecnologias                                 |
|--------------------|---------------------------------------------|
| Web App            | **Python**, Streamlit, ECharts        |
| Scraping/ETL       | Selenium, BeautifulSoup, Pandas             |
| Banco de Dados     | **PostgreSQL**                                  |
| Visualização       | streamlit-echarts, HTML/CSS, temas custom   |
| Infra (futuro)     | Docker + Deploy 24/7                        |

---

## 🚀 Setup Rápido

```bash
# Clone o projeto
git clone https://github.com/renanmrbraga/football-science.git
cd football-science

# Instale as dependências
pip install -r requirements.txt

# Rode o dashboard
streamlit run main.py
```

---

## 🔖 Licença

Este projeto está licenciado sob os termos da [Licença MIT](./LICENSE).

---

## 📢 Aviso

Este projeto utiliza dados de fontes abertas com finalidades analíticas e educacionais. Para decisões oficiais, consulte os sites originais. Os dados podem conter inconsistências ou atualizações não refletidas em tempo real.
