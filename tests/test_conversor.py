import unittest
from decimal import Decimal
from unittest.mock import Mock, patch

from conversor import ErroConversao, converter, formatar_numero, ler_valor


class ConversorTest(unittest.TestCase):
    def test_ler_valor_aceita_virgula(self):
        self.assertEqual(ler_valor("10,50"), Decimal("10.50"))

    def test_formatacao_brasileira(self):
        self.assertEqual(formatar_numero(Decimal("1234.5")), "1.234,50")

    def test_mesma_moeda_nao_chama_api(self):
        resultado, cotacao = converter(Decimal("12.30"), "brl", "BRL")
        self.assertEqual(resultado, Decimal("12.30"))
        self.assertEqual(cotacao, Decimal("1"))

    @patch("conversor.json.load", return_value={"USDBRL": {"bid": "5.25"}})
    @patch("conversor.urlopen")
    def test_conversao(self, abrir, _json_load):
        abrir.return_value.__enter__.return_value = Mock()

        resultado, cotacao = converter(Decimal("10"), "usd", "brl")

        self.assertEqual(resultado, Decimal("52.50"))
        self.assertEqual(cotacao, Decimal("5.25"))
        abrir.assert_called_once_with(
            "https://economia.awesomeapi.com.br/last/USD-BRL", timeout=10
        )

    @patch("conversor.urlopen", side_effect=TimeoutError)
    def test_timeout_tem_mensagem_amigavel(self, _abrir):
        with self.assertRaisesRegex(ErroConversao, "demorou demais"):
            converter(Decimal("10"), "USD", "BRL")

    def test_rejeita_codigo_invalido(self):
        with self.assertRaises(ValueError):
            converter(Decimal("10"), "dolar", "BRL")

    def test_rejeita_valor_negativo(self):
        with self.assertRaises(ValueError):
            converter(Decimal("-1"), "USD", "BRL")


if __name__ == "__main__":
    unittest.main()
