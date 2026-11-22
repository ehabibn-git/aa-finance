"""Ponto de Entrada Principal (CLI) do Projeto AA-FINANCE.

Permite executar o sistema multiagente diretamente via linha de comando:
Exemplo:
    python src/main.py --ticker PETR4
    python src/main.py --ticker VALE3 --modelo gemini/gemini-3.8-flash
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Garantir que a pasta raiz do projeto esteja no sys.path ao executar via 'python src/main.py'
RAIZ_PROJETO = str(Path(__file__).resolve().parent.parent)
if RAIZ_PROJETO not in sys.path:
    sys.path.insert(0, RAIZ_PROJETO)

# Carregar variáveis do arquivo .env (caso exista)
load_dotenv()

from src.agents.crew_orchestrator import executar_comite_analise


def main():
    parser = argparse.ArgumentParser(
        description="AA-FINANCE: Sistema Multiagente de Apoio à Decisão na B3 (TCC PUC-Rio)"
    )
    parser.add_argument(
        "--ticker",
        type=str,
        default="PETR4",
        help="Código da ação da B3 a ser analisada (ex: PETR4, VALE3, ITUB4). Padrão: PETR4"
    )
    parser.add_argument(
        "--modelo",
        type=str,
        default="gemini/gemini-3.5-flash-lite",
        help="Modelo LLM a utilizar via CrewAI (padrão: gemini/gemini-3.5-flash-lite)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("AA-FINANCE: SISTEMA MULTIAGENTE DE APOIO À DECISÃO NA B3")
    print("=" * 70)
    print(f"Data e Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Ativo Alvo: {args.ticker.upper()}")
    print(f"Modelo LLM: {args.modelo}")
    print("-" * 70)
    print("Iniciando deliberação do comitê de investimentos...")
    print("-" * 70 + "\n")
    
    try:
        relatorio_final = executar_comite_analise(
            ticker=args.ticker,
            modelo=args.modelo
        )
        
        print("\n" + "=" * 70)
        print("RELATÓRIO FINAL DO COMITÊ DE INVESTIMENTOS")
        print("=" * 70 + "\n")
        print(relatorio_final)
        print("\n" + "=" * 70)
        print("Análise concluída com sucesso.")
        print("=" * 70 + "\n")
        
    except Exception as erro:
        print(f"\n[ERRO NA EXECUÇÃO]: {erro}", file=sys.stderr)
        print("\nDica: Certifique-se de que a variável GEMINI_API_KEY está configurada no seu arquivo .env", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
