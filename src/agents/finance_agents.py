"""Definição dos Agentes Especialistas no CrewAI para o Mercado da B3.

Este módulo define as 3 personas do comitê de investimentos:
1. Analista Técnico / Quantitativo (opera com a ferramenta financeira yfinance)
2. Analista de Sentimento / Notícias (opera com a ferramenta de busca de notícias)
3. Diretor de Investimentos / Decisor Crítico (pondera e resolve conflitos)
"""

from typing import Tuple, Any
from crewai import Agent
from crewai.tools import tool
from src.tools.financial_tool import obter_indicadores_tecnicos
from src.tools.news_tool import obter_noticias_mercado


# ---------------------------------------------------------------------------
# Envelopamento das Ferramentas no padrão CrewAI (@tool)
# ---------------------------------------------------------------------------

@tool("Ferramenta de Indicadores Técnicos da B3")
def tool_indicadores_tecnicos(ticker: str) -> str:
    """Coleta o histórico de cotações da B3 e calcula deterministamente indicadores:
    Último Preço, Variação em 1d/30d, Médias Móveis (SMA 14, EMA 20) e RSI (14 períodos).
    """
    resultado = obter_indicadores_tecnicos(ticker)
    return resultado.get("resumo_texto", str(resultado))


@tool("Ferramenta de Notícias e Fatos Relevantes da B3")
def tool_noticias_mercado(ticker: str) -> str:
    """Busca as manchetes e resumos mais recentes em língua portuguesa sobre a empresa,
    capturando fatos relevantes, balanços e riscos regulatórios na imprensa brasileira.
    """
    resultado = obter_noticias_mercado(ticker)
    return resultado.get("resumo_texto", str(resultado))


# ---------------------------------------------------------------------------
# Fábrica de Agentes Especialistas
# ---------------------------------------------------------------------------

def criar_agente_tecnico(llm: Any) -> Agent:
    """Cria o Analista Técnico / Quantitativo."""
    return Agent(
        role="Analista Técnico e Quantitativo Sênior da B3",
        goal="Analisar deterministamente os preços históricos, médias móveis e RSI do ativo {ticker} "
             "para diagnosticar com precisão a tendência de preço e zonas de sobrecompra ou sobrevenda.",
        backstory=(
            "Você é um renomado analista quantitativo credenciado pela APIMEC/CNPI com mais de 15 anos "
            "de atuação na bolsa brasileira (B3). Você não confia em achismos ou previsões místicas. "
            "Sua análise é estritamente pautada na interpretação fria de dados numéricos calculados: "
            "Médias Móveis (SMA 14 e EMA 20) e Índice de Força Relativa (RSI 14). "
            "Você sempre destaca se o ativo está em momento de exaustão compradora (RSI > 70) ou "
            "desconto técnico excessivo (RSI < 30)."
        ),
        tools=[tool_indicadores_tecnicos],
        llm=llm,
        verbose=True,
        memory=False
    )


def criar_agente_sentimento(llm: Any) -> Agent:
    """Cria o Analista Macroeconômico e de Sentimento de Notícias."""
    return Agent(
        role="Analista de Inteligência de Mercado e Sentimento de Notícias",
        goal="Rastrear e sintetizar o noticiário recente sobre {ticker}, identificando o sentimento "
             "predominante (Positivo, Neutro ou Negativo) e destacando catalisadores de alta ou riscos corporativos.",
        backstory=(
            "Você é um experiente jornalista investigativo e analista de inteligência de mercado do Valor Econômico. "
            "Sua especialidade é ler nas entrelinhas de notícias econômicas, separando mero ruído de mercado "
            "de sinais reais que impactam os fundamentos de uma companhia: investigações, decisões governamentais, "
            "resultados trimestrais, troca de comando e oscilação de commodities. "
            "Você resume os fatos de maneira clara e pontua os riscos mais críticos."
        ),
        tools=[tool_noticias_mercado],
        llm=llm,
        verbose=True,
        memory=False
    )


def criar_agente_diretor(llm: Any) -> Agent:
    """Cria o Diretor de Investimentos e Gestor de Portfólio (Decisor Final)."""
    return Agent(
        role="Diretor de Investimentos e Gestor de Portfólio (Chief Investment Officer)",
        goal="Confrontar o relatório técnico com o relatório de notícias do ativo {ticker}, "
             "resolver qualquer contradição entre eles e deliberar a recomendação final de investimento: "
             "COMPRAR, VENDER ou MANTER, com justificativa executiva estruturada.",
        backstory=(
            "Você é o sócio-gestor e Diretor de Investimentos (CIO) de um dos fundos de ações mais respeitados "
            "do Brasil. A decisão final sobre a alocação de milhões de reais dos cotistas depende da sua caneta. "
            "Você é conhecido por seu ceticismo pragmático: não compra apenas porque o gráfico subiu, nem entra "
            "em pânico se o noticiário for passageiro. Você confronta os dois analistas sob seu comando, "
            "pesa a relação risco-retorno e define uma recomendação definitiva (COMPRAR, VENDER ou MANTER) "
            "com argumentos cristalinos e sem respostas evasivas."
        ),
        tools=[],  # O Diretor não busca dados brutos; ele delibera sobre as análises dos especialistas
        llm=llm,
        verbose=True,
        memory=False
    )


def criar_comite_investimento(llm: Any) -> Tuple[Agent, Agent, Agent]:
    """Instancia os três agentes do comitê."""
    agente_tecnico = criar_agente_tecnico(llm)
    agente_sentimento = criar_agente_sentimento(llm)
    agente_diretor = criar_agente_diretor(llm)
    return agente_tecnico, agente_sentimento, agente_diretor
