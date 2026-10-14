"""Orquestrador do Fluxo Multiagente (CrewAI) para Análise de Ações da B3.

Este módulo define as tarefas (Tasks), estabelece o pipeline sequencial
e conecta os agentes ao modelo de linguagem (Google Gemini).

PONTO PARA A BANCA:
A orquestração utiliza o padrão de 'Process.sequential' do CrewAI:
1. O Agente Técnico gera a base quantitativa;
2. O Agente de Sentimento gera a base qualitativa;
3. O Diretor de Investimentos recebe os dois contextos encadeados e resolve
   qualquer divergência antes de emitir a recomendação final.
"""

import os
from typing import Dict, Any, Optional
from crewai import Task, Crew, Process, LLM
from src.agents.finance_agents import criar_comite_investimento


def inicializar_modelo_llm(
    nome_modelo: str = "gemini/gemini-1.5-flash",
    temperatura: float = 0.2,
    api_key: Optional[str] = None
) -> LLM:
    """Inicializa o modelo de linguagem no CrewAI.
    
    Por padrão utiliza o Google Gemini (gemini-1.5-flash) que alia
    alta velocidade, grande janela de contexto e custo acessível.
    """
    chave = api_key or os.getenv("GEMINI_API_KEY")
    if not chave:
        raise ValueError(
            "Chave de API do Gemini não encontrada! "
            "Configure a variável de ambiente GEMINI_API_KEY ou informe-a nos Secrets do Colab."
        )
        
    return LLM(
        model=nome_modelo,
        temperature=temperatura,
        api_key=chave
    )


def criar_tarefas(agente_tecnico, agente_sentimento, agente_diretor, ticker: str):
    """Cria e encadeia as tarefas sequenciais do comitê."""
    
    tarefa_tecnica = Task(
        description=(
            f"1. Use a ferramenta de indicadores técnicos para coletar as métricas da ação {ticker}.\n"
            f"2. Analise os valores calculados: Último Preço, Média SMA 14, Média EMA 20 e RSI 14.\n"
            f"3. Produza um parecer técnico objetivo explicando se o ativo está em tendência de alta "
            f"ou baixa e se o RSI indica sobrevenda (desconto excessivo) ou sobrecompra (risco de correção)."
        ),
        expected_output=(
            f"Relatório Técnico Quantitativo para {ticker} contendo cotação atual, médias móveis, "
            f"valor exato do RSI (14) e o diagnóstico fundamentado de tendência."
        ),
        agent=agente_tecnico
    )
    
    tarefa_sentimento = Task(
        description=(
            f"1. Use a ferramenta de notícias para coletar as manchetes e fatos recentes sobre a empresa {ticker}.\n"
            f"2. Sintetize os principais tópicos noticiados na imprensa brasileira.\n"
            f"3. Identifique riscos regulatórios, balanços, decisões judiciais ou fatores macroeconômicos.\n"
            f"4. Classifique o sentimento geral de mercado como POSITIVO, NEUTRO ou NEGATIVO."
        ),
        expected_output=(
            f"Relatório de Sentimento e Notícias para {ticker} contendo resumo das manchetes, "
            f"classificação clara do sentimento e lista dos 3 principais fatores de risco ou catalisadores."
        ),
        agent=agente_sentimento
    )
    
    tarefa_deliberacao = Task(
        description=(
            f"1. Analise criticamente o Relatório Técnico e o Relatório de Sentimento gerados sobre {ticker}.\n"
            f"2. Resolva qualquer aparente conflito entre os dois lados. "
            f"(Exemplo: Se o técnico indicar compra pelo RSI sobrevendido, mas o noticiário indicar "
            f"uma crise de governança grave, pese o risco do negócio contra o desconto no preço).\n"
            f"3. Emita uma deliberação inequívoca: **COMPRAR**, **VENDER** ou **MANTER**.\n"
            f"4. Forneça uma justificativa executiva formal, sintetizando os números e os fatos."
        ),
        expected_output=(
            f"Relatório Executivo Final de Recomendação para {ticker} formatado em Markdown:\n"
            f"- **RECOMENDAÇÃO FINAL:** [COMPRAR | VENDER | MANTER]\n"
            f"- **Pilar Quantitativo:** Resumo dos dados técnicos e RSI.\n"
            f"- **Pilar Qualitativo:** Resumo do sentimento das notícias e riscos.\n"
            f"- **Conclusão e Justificativa:** Síntese decisória clara explicando por que a decisão foi tomada."
        ),
        agent=agente_diretor,
        context=[tarefa_tecnica, tarefa_sentimento]
    )
    
    return [tarefa_tecnica, tarefa_sentimento, tarefa_deliberacao]


def executar_comite_analise(ticker: str, api_key: Optional[str] = None, modelo: str = "gemini/gemini-1.5-flash") -> str:
    """Executa o pipeline multiagente completo para o ticker informado.
    
    Args:
        ticker: Código da ação (ex: 'PETR4', 'VALE3', 'ITUB4').
        api_key: Chave do Google Gemini (opcional se estiver no .env).
        modelo: Nome do modelo do Gemini no formato litellm (padrão: 'gemini/gemini-1.5-flash').
        
    Returns:
        Texto em Markdown contendo a deliberação final do comitê.
    """
    ticker_padronizado = ticker.strip().upper()
    llm = inicializar_modelo_llm(nome_modelo=modelo, api_key=api_key)
    
    # 1. Instanciar Agentes
    agente_tecnico, agente_sentimento, agente_diretor = criar_comite_investimento(llm)
    
    # 2. Criar Tarefas
    tarefas = criar_tarefas(agente_tecnico, agente_sentimento, agente_diretor, ticker_padronizado)
    
    # 3. Criar Equipe (Crew) com Processamento Sequencial
    equipe = Crew(
        agents=[agente_tecnico, agente_sentimento, agente_diretor],
        tasks=tarefas,
        process=Process.sequential,
        verbose=True
    )
    
    # 4. Executar e Coletar Resultado
    resultado = equipe.kickoff(inputs={"ticker": ticker_padronizado})
    return str(resultado)
