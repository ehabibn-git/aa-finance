"""Ferramenta Determinística de Coleta e Análise Técnica Financeira (B3).

Esta ferramenta conecta-se ao Yahoo Finance (yfinance) para coletar dados históricos
de ações brasileiras e calcula indicadores matemáticos (médias móveis e RSI) via pandas.

PONTO PARA A BANCA:
LLMs não realizam cálculos aritméticos com confiabilidade estrita. O uso desta
ferramenta garante determinismo matemático: os números são calculados em Python
e a LLM é responsável apenas pela interpretação analítica dos resultados.
"""

from typing import Dict, Any, Optional
import pandas as pd
import yfinance as yf


def formatar_ticker_b3(ticker: str) -> str:
    """Padroniza o ticker da B3 adicionando o sufixo '.SA' se necessário.
    
    Exemplo:
        'PETR4' -> 'PETR4.SA'
        'VALE3.SA' -> 'VALE3.SA'
    """
    ticker_limpo = ticker.strip().upper()
    if not ticker_limpo.endswith(".SA"):
        ticker_limpo = f"{ticker_limpo}.SA"
    return ticker_limpo


def calcular_rsi(series_precos: pd.Series, periodos: int = 14) -> pd.Series:
    """Calcula o Índice de Força Relativa (RSI / IFR) de 14 períodos.
    
    Fórmula clássica de J. Welles Wilder:
        RSI = 100 - (100 / (1 + RS))
        onde RS = Média dos Ganhos / Média das Perdas
    """
    delta = series_precos.diff()
    ganhos = delta.clip(lower=0)
    perdas = -1 * delta.clip(upper=0)
    
    # Médias exponenciais (Wilder smoothing)
    media_ganhos = ganhos.ewm(alpha=1/periodos, min_periods=periodos, adjust=False).mean()
    media_perdas = perdas.ewm(alpha=1/periodos, min_periods=periodos, adjust=False).mean()
    
    rs = media_ganhos / media_perdas.replace(0, 0.00001)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def obter_indicadores_tecnicos(ticker: str, dias_historico: int = 60) -> Dict[str, Any]:
    """Coleta o histórico de cotações da B3 e calcula os indicadores técnicos determinísticos.
    
    Args:
        ticker: Código da ação (ex: 'PETR4', 'VALE3', 'ITUB4').
        dias_historico: Quantidade de dias de histórico a buscar (padrão: 60).
        
    Returns:
        Dicionário estruturado com as cotações e os indicadores calculados.
    """
    simbolo = formatar_ticker_b3(ticker)
    
    # Baixar cotações via yfinance
    ativo = yf.Ticker(simbolo)
    historico = ativo.history(period=f"{dias_historico}d", interval="1d")
    
    if historico.empty or len(historico) < 20:
        return {
            "status": "erro",
            "mensagem": f"Dados insuficientes para o ticker '{ticker}'. Verifique se o código existe na B3."
        }
        
    precos_fechamento = historico["Close"]
    
    # Cálculos matemáticos determinísticos
    ultimo_preco = float(precos_fechamento.iloc[-1])
    preco_anterior = float(precos_fechamento.iloc[-2])
    preco_30d_atras = float(precos_fechamento.iloc[-min(30, len(precos_fechamento))])
    
    variacao_1d = float(((ultimo_preco - preco_anterior) / preco_anterior) * 100)
    variacao_30d = float(((ultimo_preco - preco_30d_atras) / preco_30d_atras) * 100)
    
    # Médias Móveis
    sma_14 = float(precos_fechamento.rolling(window=14).mean().iloc[-1])
    ema_20 = float(precos_fechamento.ewm(span=20, adjust=False).mean().iloc[-1])
    
    # RSI (14 períodos)
    serie_rsi = calcular_rsi(precos_fechamento, periodos=14)
    rsi_14 = float(serie_rsi.iloc[-1])
    
    # Classificação técnica objetiva (para guiar a LLM)
    if rsi_14 > 70:
        diagnostico_rsi = "Sobrecomprado (RSI > 70: Pressão compradora excessiva, risco de correção de curto prazo)"
    elif rsi_14 < 30:
        diagnostico_rsi = "Sobrevendido (RSI < 30: Pressão vendedora excessiva, potencial repique técnico de alta)"
    else:
        diagnostico_rsi = f"Neutro (RSI={rsi_14:.1f}: Zona de equilíbrio entre compradores e vendedores)"
        
    if ultimo_preco > ema_20:
        diagnostico_tendencia = "Alta (Preço atual acima da Média Móvel Exponencial de 20 períodos)"
    else:
        diagnostico_tendencia = "Baixa (Preço atual abaixo da Média Móvel Exponencial de 20 períodos)"
        
    volume_medio_20d = float(historico["Volume"].tail(20).mean())
    
    resultado = {
        "status": "sucesso",
        "ticker": simbolo,
        "ultimo_preco": round(ultimo_preco, 2),
        "variacao_1d_pct": round(variacao_1d, 2),
        "variacao_30d_pct": round(variacao_30d, 2),
        "media_movel_sma_14": round(sma_14, 2),
        "media_movel_ema_20": round(ema_20, 2),
        "rsi_14": round(rsi_14, 2),
        "diagnostico_rsi": diagnostico_rsi,
        "diagnostico_tendencia": diagnostico_tendencia,
        "volume_medio_20d": int(volume_medio_20d),
        "resumo_texto": (
            f"Relatório Técnico Quantitativo para {simbolo}:\n"
            f"- Último Preço: R$ {ultimo_preco:.2f} (Variação no dia: {variacao_1d:+.2f}%, 30 dias: {variacao_30d:+.2f}%)\n"
            f"- Média Móvel SMA (14 períodos): R$ {sma_14:.2f}\n"
            f"- Média Móvel EMA (20 períodos): R$ {ema_20:.2f}\n"
            f"- Tendência de Preço: {diagnostico_tendencia}\n"
            f"- RSI (14 períodos): {rsi_14:.1f} -> {diagnostico_rsi}\n"
            f"- Volume Médio Negociado (20 dias): {volume_medio_20d:,.0f} ações."
        )
    }
    
    return resultado


if __name__ == "__main__":
    import sys
    ticker_teste = sys.argv[1] if len(sys.argv) > 1 else "PETR4"
    print(f"Testando coleta e cálculo técnico para: {ticker_teste}...")
    dados = obter_indicadores_tecnicos(ticker_teste)
    if dados["status"] == "sucesso":
        print("\n" + dados["resumo_texto"])
    else:
        print(f"Erro: {dados['mensagem']}")
