# Sistema Multiagente Autônomo com LLMs para Análise Técnica e de Sentimento no Mercado Acionário Brasileiro (B3)

#### Aluno: [Nome do Aluno](https://github.com/link_do_github)
#### Orientadora: [Nome da Orientadora](https://github.com/link_do_github) <!-- ou Prof. Manoela Kohler -->
#### Co-orientador(/a/es/as): [Nome Sobrenome](https://github.com/link_do_github) <!-- caso não aplicável, remover esta linha -->

---

Trabalho apresentado ao curso [GenAI e LLM MASTER](https://ica.ele.puc-rio.br/cursos/ia-generativa-large-language-models/) como pré-requisito para conclusão de curso e obtenção de crédito na disciplina "Projetos de Sistemas Inteligentes de Apoio à Decisão".

- [Link para o código](https://github.com/link_do_repositorio).
- [Link para o Google Colab](https://colab.research.google.com/). <!-- Adicionar link direto do notebook -->
- [Link para a monografia](https://link_da_monografia.com). <!-- caso aplicável -->

---

### Resumo

Este trabalho apresenta uma Prova de Conceito (PoC) de um Sistema Multiagente Autônomo de apoio à tomada de decisão de investimentos em ações negociadas na B3 (Brasil, Bolsa, Balcão). Modelos de linguagem de grande porte (LLMs) isolados sofrem com a falta de dados atualizados em tempo real, incapacidade de realizar cálculos numéricos precisos e propensão a alucinações. Para superar essas barreiras, propõe-se uma arquitetura baseada no framework CrewAI, orquestrando três agentes inteligentes especializados: (i) um Agente Analista Técnico/Quantitativo, que utiliza ferramentas determinísticas em Python para calcular indicadores matemáticos como RSI e médias móveis a partir de cotações históricas do Yahoo Finance; (ii) um Agente Analista de Sentimento, responsável por rastrear e sintetizar notícias em língua portuguesa sobre a empresa; e (iii) um Agente Diretor de Investimentos, que pondera os sinais quantitativos e qualitativos, resolve eventuais divergências e emite uma recomendação fundamentada de investimento (Comprar, Vender ou Manter). O projeto é disponibilizado em formato modular e executável interativamente via Google Colab.

---

### 1. Introdução

*(Esta seção será complementada com o embasamento do mercado de capitais brasileiro, a volatilidade dos ativos na B3 e a necessidade de sistemas de apoio à decisão orientados a IA generativa).*

---

### 2. Modelagem

*(Esta seção conterá o diagrama arquitetural do sistema multiagente, o detalhamento das ferramentas desenvolvidas em Python (Tools), a engenharia de prompts dos agentes e a justificativa da escolha dos modelos de fundação).*

---

### 3. Resultados

*(Esta seção apresentará os estudos de caso práticos realizados com ações reais da B3, tais como PETR4, VALE3 e ITUB4, demonstrando os outputs de cada agente e a resolução de conflitos pelo agente decisor).*

---

### 4. Conclusões

*(Esta seção discutirá as vantagens da abordagem determinística combinada a sistemas multiagentes, as limitações identificadas durante os testes e propostas para trabalhos futuros).*

---

### 5. Referências

1. Wu, Q., et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*.
2. Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR.
3. CrewAI Documentation. *Multi-agent orchestration platform for engineering intelligence*. Disponível em: https://docs.crewai.com.
4. Yahoo Finance API (`yfinance`). *Open-source financial data collection tool*.

---

### 6. Instalação

#### 6.1 Pré-requisitos
- Python 3.10 ou superior (caso execute localmente).
- Conta no [Google AI Studio](https://aistudio.google.com/) para obter uma chave de API gratuita do Google Gemini (`GEMINI_API_KEY`).

#### 6.2 Clonando o Repositório
```bash
git clone https://github.com/link_do_repositorio.git
cd aa-finance
```

#### 6.3 Configurando o Ambiente Virtual (Local)
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Ativar ambiente virtual (Linux/macOS)
source .venv/bin/activate
```

#### 6.4 Instalando as Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Nota:** Conforme novas ferramentas e bibliotecas forem incorporadas ao projeto durante o desenvolvimento, todos os pacotes e comandos de instalação serão mantidos rigorosamente atualizados nesta seção e no arquivo `requirements.txt`.

---

### 7. Como executar

#### 7.1 Execução no Google Colab (Recomendada)
1. Acesse o notebook do projeto no Google Colab através do link disponibilizado no topo deste documento.
2. Adicione sua chave de API nos **Secrets** (ícone de chave no menu lateral do Colab) com o nome `GEMINI_API_KEY`.
3. Execute a primeira célula para instalar as dependências necessárias:
   ```python
   !pip install -r requirements.txt
   ```
4. Defina o código do ativo da B3 que deseja analisar:
   ```python
   ticker = "PETR4"  # Exemplo: PETR4, VALE3, ITUB4
   ```
5. Execute as células sequenciais para acompanhar a análise de cada agente em tempo real e visualizar o relatório final de recomendação.

#### 7.2 Execução Local
1. Configure suas variáveis de ambiente copiando o arquivo de exemplo:
   ```bash
   cp .env.example .env
   ```
2. Adicione sua chave de API no arquivo `.env`:
   ```env
   GEMINI_API_KEY=sua_chave_aqui
   ```
3. Execute o script principal informando o ticker desejado:
   ```bash
   python src/main.py --ticker PETR4
   ```

---

Matrícula: [Número de Matrícula]

Pontifícia Universidade Católica do Rio de Janeiro

Curso de Pós Graduação *Inteligência Artificial Generativa & Large Language Models*
