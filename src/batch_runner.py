"""Execução em Lote de Estudos de Caso (Batch Runner) para o Projeto AA-FINANCE.

Permite analisar múltiplos ativos da B3 sequencialmente e salvar os relatórios
executivos na pasta 'reports/' para compor as evidências acadêmicas do TCC.

Exemplo de uso:
    python src/batch_runner.py --tickers PETR4 VALE3 ITUB4
"""

import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from src.agents.crew_orchestrator import executar_comite_analise


def executar_estudos_em_lote(tickers: list, pasta_saida: str = "reports") -> None:
    """Executa a análise multiagente para uma lista de ativos e salva os relatórios."""
    os.makedirs(pasta_saida, exist_ok=True)
    
    print("\n" + "=" * 75)
    print("AA-FINANCE: EXECUÇÃO EM LOTE DE ESTUDOS DE CASO (B3)")
    print("=" * 75)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Total de Ativos: {len(tickers)} ({', '.join(tickers)})")
    print(f"Diretório de Destino: {pasta_saida}/")
    print("=" * 75 + "\n")
    
    for i, ticker in enumerate(tickers, 1):
        ticker_limpo = ticker.strip().upper()
        print(f"[{i}/{len(tickers)}] Iniciando deliberação para {ticker_limpo}...")
        
        try:
            relatorio = executar_comite_analise(ticker=ticker_limpo)
            
            nome_arquivo = os.path.join(pasta_saida, f"estudo_caso_{ticker_limpo}.md")
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write(f"# Estudo de Caso de Apoio à Decisão: {ticker_limpo}\n\n")
                f.write(f"**Data da Execução:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  \n")
                f.write(f"**Ambiente:** Sistema Multiagente CrewAI + Google Gemini  \n")
                f.write(f"**Projeto:** AA-FINANCE (TCC GenAI e LLM Master - PUC-Rio)\n\n")
                f.write("---\n\n")
                f.write(relatorio)
                f.write("\n")
                
            print(f" -> Relatório gerado com sucesso: {nome_arquivo}\n")
            
        except Exception as e:
            print(f" -> [ERRO] Falha ao processar {ticker_limpo}: {e}\n", file=sys.stderr)
            
    print("=" * 75)
    print("Execução em lote concluída com sucesso!")
    print("=" * 75 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Executa múltiplos estudos de caso na B3")
    parser.add_argument(
        "--tickers",
        nargs="+",
        default=["PETR4", "VALE3", "ITUB4"],
        help="Lista de códigos de ações a analisar (padrão: PETR4 VALE3 ITUB4)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="reports",
        help="Diretório onde os relatórios Markdown serão salvos (padrão: reports)"
    )
    
    args = parser.parse_args()
    executar_estudos_em_lote(tickers=args.tickers, pasta_saida=args.output_dir)


if __name__ == "__main__":
    main()
