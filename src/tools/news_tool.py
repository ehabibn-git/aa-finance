"""Ferramenta Determinística de Coleta de Notícias em Tempo Real (B3).

Esta ferramenta busca as manchetes e resumos mais recentes em língua portuguesa
relacionados à empresa pesquisada, utilizando o DuckDuckGo Search com fallback
para o RSS público do Google News Brasil.

PONTO PARA A BANCA:
LLMs possuem corte temporal de conhecimento (cutoff date) e não têm acesso à internet
por padrão. Esta ferramenta alimenta o Agente de Sentimento com dados frescos do dia,
permitindo a captura de riscos regulatórios, balanços trimestrais e crises corporativas.
"""

from typing import List, Dict, Any, Optional
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
from duckduckgo_search import DDGS


# Mapeamento auxiliar de tickers populares da B3 para nomes corporativos
# para maximizar a relevância das notícias retornadas
MAPEAMENTO_EMPRESAS_B3: Dict[str, str] = {
    "PETR4": "Petrobras",
    "PETR3": "Petrobras",
    "VALE3": "Vale",
    "ITUB4": "Itaú Unibanco",
    "BBDC4": "Bradesco",
    "BBAS3": "Banco do Brasil",
    "MGLU3": "Magazine Luiza",
    "WEGE3": "WEG",
    "ABEV3": "Ambev",
    "RENT3": "Localiza",
    "PRIO3": "PRIO PetroRio",
    "SUZB3": "Suzano",
    "JBSS3": "JBS",
    "ELET3": "Eletrobras",
    "B3SA3": "B3 Bolsa",
}


def resolver_termo_busca(ticker: str) -> str:
    """Retorna o termo de busca otimizado combinando nome da empresa e ações."""
    codigo_limpo = ticker.replace(".SA", "").strip().upper()
    nome_empresa = MAPEAMENTO_EMPRESAS_B3.get(codigo_limpo, codigo_limpo)
    return f"{nome_empresa} acoes B3"


def buscar_noticias_duckduckgo(termo: str, max_noticias: int = 5) -> List[Dict[str, str]]:
    """Busca notícias recentes via DuckDuckGo News em português."""
    noticias = []
    try:
        with DDGS() as ddgs:
            resultados = ddgs.news(
                keywords=termo,
                region="br-pt",
                safesearch="moderate",
                max_results=max_noticias
            )
            for item in resultados:
                noticias.append({
                    "titulo": item.get("title", ""),
                    "resumo": item.get("body", ""),
                    "data": item.get("date", ""),
                    "fonte": item.get("source", "DuckDuckGo News"),
                    "url": item.get("url", "")
                })
    except Exception as erro:
        # Silencia erro pontual para tentar o fallback do Google News
        pass
    return noticias


def buscar_noticias_google_rss(termo: str, max_noticias: int = 5) -> List[Dict[str, str]]:
    """Fallback: busca notícias via RSS público do Google News Brasil."""
    noticias = []
    try:
        url_rss = f"https://news.google.com/rss/search?q={quote_plus(termo)}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
        req = urllib.request.Request(
            url_rss,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=8) as resposta:
            xml_data = resposta.read()
            root = ET.fromstring(xml_data)
            
            for item in root.findall(".//channel/item")[:max_noticias]:
                titulo = item.findtext("title", "")
                data_pub = item.findtext("pubDate", "")
                link = item.findtext("link", "")
                fonte = item.findtext("source", "Google News")
                
                noticias.append({
                    "titulo": titulo,
                    "resumo": titulo,
                    "data": data_pub,
                    "fonte": fonte,
                    "url": link
                })
    except Exception:
        pass
    return noticias


def obter_noticias_mercado(ticker: str, max_noticias: int = 5) -> Dict[str, Any]:
    """Coleta notícias recentes sobre a empresa listada na B3.
    
    Args:
        ticker: Código da ação (ex: 'PETR4', 'VALE3').
        max_noticias: Limite de notícias a retornar (padrão: 5).
        
    Returns:
        Dicionário estruturado com as notícias e resumo em texto para o agente.
    """
    termo = resolver_termo_busca(ticker)
    
    # 1. Tentar busca via DuckDuckGo
    noticias = buscar_noticias_duckduckgo(termo, max_noticias=max_noticias)
    
    # 2. Se falhar ou vier vazio, aplicar Fallback via Google News RSS
    if not noticias:
        noticias = buscar_noticias_google_rss(termo, max_noticias=max_noticias)
        
    if not noticias:
        return {
            "status": "aviso",
            "ticker": ticker,
            "total_noticias": 0,
            "noticias": [],
            "resumo_texto": f"Nenhuma notícia recente encontrada nos últimos dias para o termo '{termo}'."
        }
        
    linhas_resumo = [f"Notícias recentes de mercado para {ticker} (Termo de busca: '{termo}'):"]
    for i, notic in enumerate(noticias, 1):
        linhas_resumo.append(
            f"{i}. [{notic['fonte']}] {notic['titulo']}\n"
            f"   Resumo: {notic['resumo']}\n"
            f"   Data: {notic['data']}"
        )
        
    resumo_completo = "\n\n".join(linhas_resumo)
    
    return {
        "status": "sucesso",
        "ticker": ticker,
        "total_noticias": len(noticias),
        "noticias": noticias,
        "resumo_texto": resumo_completo
    }


if __name__ == "__main__":
    import sys
    ticker_teste = sys.argv[1] if len(sys.argv) > 1 else "PETR4"
    print(f"Buscando notícias recentes para {ticker_teste}...")
    resultado = obter_noticias_mercado(ticker_teste)
    print("\n" + resultado["resumo_texto"])
