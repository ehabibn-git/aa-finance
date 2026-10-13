"""Testes unitários e de integração para as ferramentas determinísticas.
"""

import unittest
from src.tools.financial_tool import formatar_ticker_b3, calcular_rsi
from src.tools.news_tool import resolver_termo_busca
import pandas as pd


class TestFerramentas(unittest.TestCase):

    def test_formatar_ticker_b3(self):
        """Testa a padronização do sufixo .SA da B3."""
        self.assertEqual(formatar_ticker_b3("petr4"), "PETR4.SA")
        self.assertEqual(formatar_ticker_b3("VALE3.SA"), "VALE3.SA")
        self.assertEqual(formatar_ticker_b3(" itub4 "), "ITUB4.SA")

    def test_resolver_termo_busca(self):
        """Testa o mapeamento de ticker para nome corporativo."""
        self.assertEqual(resolver_termo_busca("PETR4"), "Petrobras acoes B3")
        self.assertEqual(resolver_termo_busca("VALE3.SA"), "Vale acoes B3")
        self.assertEqual(resolver_termo_busca("XYZW3"), "XYZW3 acoes B3")

    def test_calcular_rsi_deterministico(self):
        """Valida que o cálculo do RSI retorna valores entre 0 e 100."""
        # Série fictícia de 20 preços
        precos = pd.Series([
            10.0, 10.5, 11.0, 10.8, 11.2, 11.5, 12.0, 12.5, 12.2, 12.8,
            13.0, 13.5, 13.2, 13.8, 14.0, 14.5, 14.2, 14.8, 15.0, 15.5
        ])
        rsi = calcular_rsi(precos, periodos=14)
        ultimo_rsi = rsi.iloc[-1]
        
        self.assertFalse(pd.isna(ultimo_rsi))
        self.assertTrue(0 <= ultimo_rsi <= 100)
        # Como a série foi de forte alta, o RSI deve ser elevado (> 70)
        self.assertGreater(ultimo_rsi, 70)


if __name__ == "__main__":
    unittest.main()
