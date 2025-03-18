# Football Analysis

## Descrição

Este projeto avançado de Análise de Dados busca compreender a relação entre os gastos financeiros, dívidas e sucesso esportivo de todos os clubes da Série A do Campeonato Brasileiro nos últimos 10 anos. Utilizando dashboards interativos e ferramentas de visualização, o objetivo é responder questões críticas sobre a gestão financeira e o desempenho esportivo dos clubes.

As principais tecnologias utilizadas serão:
- **Power BI**
- **Streamlit + Python**
- **Pandas e NumPy para manipulação de dados**
- **Matplotlib e Seaborn para visualização**
- **PostgreSQL para armazenamento dos dados estruturados**
- **APIs e Web Scraping para coleta de dados**

## Objetivos
- Analisar os investimentos dos clubes e seu impacto nos resultados esportivos.
- Estudar o endividamento dos clubes e como isso afeta sua sustentabilidade financeira.
- Construir dashboards interativos para visualizar os padrões e tendências financeiras e esportivas.

## Coleta de Dados

### Fontes de Dados:
Os dados serão coletados a partir de diversas fontes, incluindo:
- **APIs esportivas** para estatísticas de partidas e desempenho dos clubes.
- **Web Scraping** em sites de finanças e relatórios contábeis dos clubes.
- **Banco de dados históricos** de campeonatos e resultados.

### Web Scraping e APIs
Serão utilizadas ferramentas como **BeautifulSoup** e **Selenium** para coletar dados financeiros de relatórios anuais e balanços dos clubes. APIs esportivas fornecerão estatísticas sobre partidas, jogadores e classificação ao longo dos anos. Ambos serão feitos no meu projeto [Football Science](https://github.com/renanmrbraga/footballscience).

## Estrutura do Projeto
```
footballanalysis/
|-- data/                # Conjunto de dados
|-- notebooks/           # Jupyter Notebooks para exploração dos dados
|-- dashboards/          # Dashboards interativos
|-- src/                 # Código-fonte principal do projeto
|   |-- preprocessing/   # Scripts de pré-processamento
|   |-- analysis/        # Análises exploratórias e estatísticas
|   |-- visualization/   # Dashboards e relatórios
|-- requirements.txt     # Dependências do projeto
|-- README.md            # Documentação do projeto
```

## Instalação e Configuração

### 1. Clonar o repositório
```bash
git clone https://github.com/renanmrbraga/footballanalysis.git
cd footballanalysis
```

### 2. Criar e ativar um ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Para Linux/macOS
venv\Scripts\activate     # Para Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar o banco de dados
- Certifique-se de que o banco de dados (PostgreSQL) esteja rodando.
- Configurar as credenciais no arquivo `.env`.

### 5. Executar a coleta de dados
```bash
python src/coletar_dados.py
```

### 6. Iniciar o Dashboard
```bash
streamlit run dashboards/dashboard.py  # Para visualização dos dados
```

## Contribuição
Se quiser contribuir para este projeto, siga os passos:
1. **Fork** o repositório
2. Crie uma **branch** para sua funcionalidade (`git checkout -b minha-feature`)
3. Commit suas mudanças (`git commit -m 'Adicionando nova feature'`)
4. Faça **push** para a branch (`git push origin minha-feature`)
5. Abra um **Pull Request**

## Licença
Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
