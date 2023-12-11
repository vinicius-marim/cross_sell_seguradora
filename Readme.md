
## Cross-Sell de Seguro de Saúde

**Sobre**

Este projeto visa otimizar as vendas de planos de saúde para clientes de uma seguradora já estabelecida no ramo de seguros automotivos.

Contexto: A seguradora iniciou uma campanha de oferta de planos de saúde para sua base de clientes automotivos(Cross-Sell), mas a taxa média de conversão estava abaixo de 12.2%. Diante dos custos associados à oferta, a seguradora buscou nossa equipe de analistas de dados para desenvolver soluções inteligentes visando melhorar a taxa de conversão.

Nossa abordagem incluiu a Análise Exploratória dos Dados para melhor entender os dados e fornecer insights relevantes por meio de análises de correlação e cohort's. Posteriormente, desenvolvemos um modelo de machine learning para identificar padrões em clientes mais propensos a adquirir o plano de saúde oferecido pela seguradora. E, por fim, desenvolver uma API para facilitar a integração do output do modelo preditivo aos demais setores da seguradora.

**Principais Insights da EDA:**

- Clientes entre 33 e 48 anos estão mais propensos à compra do novo seguro, superior a 20%, contrastando com a média geral de 12.2% (Veja EDA 4.1)
- Diferentes Canais de Vendas possuem diferentes eficiência. Os Top 5 canais conseguem converter de 25-30%, porém (Veja EDA 9.0).
- **Urgência: Problema Grave de Fidelização -** Clientes que adquiriram o seguro de saúde previamente, possuem nível de conversão abaixo de 0.1%. A base de dados não nos forneceu informações para encontrar a causa-raiz deste fenômeno. Contuto, levantamos duas hipóteses, 1- O serviço oferecido no passado possuia qualidade deficiente, ou 2- O cliente encontrou serviço com melhor custo-benefício em outra seguradora.

**Resultado do modelo preditivo:**

Realizado stacking de LightGBM com GradientBoostingClassifier, utilizando a técnica de ranqueamento. O modelo obteve ótimos resultados na base de testes de 95k clientes.

Dos 95k clientes totais, os primeiros 25k clientes rankeados pelo algorítmo apresentou precisão de 33.4%, conversão de 8,350 clientes do total de 11,600, ou seja, o modelo foi capaz de capturar 71.8% de todos os clientes "conversíveis" (Vide Model 4.0)

Com base na mediana do prêmio anual de Rp$ 33,000.00 (Mais detalhes EDA 9.0), a conversão dos 8,350 clientes representaria Rp 275,550,000.00 de faturamento. Equivalente a 162.574.450,00 reais.

**Notebooks Jupyter:**

* Três notebooks fazem parte do projeto: "EDA", "Model" e "Deploy_config", cada um dedicado a diferentes fases do desenvolvimento.

**Requisitos:**

* Um arquivo requirements.txt lista todas as ferramentas necessárias para reproduzir o projeto.

**Estrutura do Projeto:**

* Dois subdiretórios compõem o projeto: "api", que armazena os arquivos necessários a sua execução, e o diretório de dados fonte, chamado "data".
