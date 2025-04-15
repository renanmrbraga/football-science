# ⚽ Football Analysis BR

Dashboard interativo para análise dos clubes da Série A do Campeonato Brasileiro. Este projeto une dados financeiros, desempenho esportivo e transferência de atletas em uma plataforma moderna e responsiva desenvolvida com **Python + Streamlit**.

## ✨ Destaques

- 🎨 **Tema claro/escuro com detecção automática**
- 📊 **Gráficos interativos usando Streamlit ECharts**
- 🧱 **Arquitetura modular, escalável e fácil de manter**

## 📌 Tecnologias Utilizadas

- **Python 3.13+**
- **Streamlit + ECharts**
- **Pandas, NumPy, Plotly**
- **PostgreSQL (opcional para futura expansão)**
- **CSS customizado via injeção direta**
- **Fontes tipográficas com Google Fonts**

## 📁 Estrutura do Projeto

```
📁 app/
│   ├── dashboards/           # Dashboards interativos (Clubes, Transferências)
│   ├── components/           # Componentes visuais reutilizáveis (gráficos, mapas, etc.)
│   ├── constants/            # Cores, temas, paths, textos
│   └── utils/                # Funções auxiliares e carregamento de dados
📁 data/
│   ├── external/             # Dados brutos obtidos via scraping ou APIs
│   ├── processed/            # Dados tratados e prontos para uso
│   └── images/               # Recursos visuais
📄 run.py                     # Entrypoint da aplicação
```

## 🚀 Como Rodar Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/renanmrbraga/football-analysis.git
cd football-analysis
```

### 2. Crie e ative um ambiente virtual
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/Mac
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute o app
```bash
streamlit run run.py
```

## 📈 Funcionalidades Atuais

- 📌 **Dashboard de Clubes**: evolução de participações na Série A, desempenho, aproveitamento e top clubes com maiores gastos.
- 📌 **Dashboard de Transferências**: comparação por tipo de transferência, mapa interativo por estado e série histórica de gastos.
- 🔄 **Switch dinâmico entre temas** com consistência visual garantida.

## 🧩 Próximas Etapas

- Integração com base de dados PostgreSQL para persistência
- Painel de filtros avançados por temporada, posição, e região
- Deploy via Streamlit Cloud com URL pública

## 🤝 Contribuições

Contribuições são bem-vindas!

1. Faça um **fork**
2. Crie sua branch: `git checkout -b minha-feature`
3. Commit: `git commit -m 'feat: nova funcionalidade'`
4. Push: `git push origin minha-feature`
5. Abra um Pull Request

## 🪪 Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais informações.
