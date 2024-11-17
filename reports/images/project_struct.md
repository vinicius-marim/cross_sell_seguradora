### Estrutura do Projeto
```r
project_name/
├── data/
│   ├── raw/              # Dados brutos
│   ├── processed/        # Dados processados
├── notebooks/            # Notebooks Jupyter
├── scripts/              # Scripts para automação (ex.: limpeza, modelagem)
├── reports/              # Relatórios e gráficos
├── models/               # Modelos treinados
├── api/                  # Código da API
│   ├── app.py            # Arquivo principal da API (ex.: Flask/FastAPI)
│   ├── routes/           # Rotas da API
│   ├── services/         # Lógica para manipulação de dados/modelos
│   ├── tests/            # Testes unitários e de integração da API
│   └── environment.yml   # Dependências específicas da API (opcional)
├── environment.yml       # Dependências gerais do projeto
└── README.md             # Explicação do projeto