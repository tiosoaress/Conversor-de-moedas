from decimal import Decimal, InvalidOperation
import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


API_URL = "https://economia.awesomeapi.com.br/last/{origem}-{destino}"
MOEDAS_SUGERIDAS = ("BRL", "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "BTC", "ETH")


class ErroConversao(Exception):
    pass


def normalizar_moeda(codigo: str) -> str:
    codigo = codigo.strip().upper()
    if len(codigo) != 3 or not codigo.isalpha():
        raise ValueError("use um código de moeda com 3 letras, como USD ou BRL")
    return codigo


def converter(valor: Decimal, origem: str, destino: str) -> tuple[Decimal, Decimal]:
    origem = normalizar_moeda(origem)
    destino = normalizar_moeda(destino)

    if valor < 0:
        raise ValueError("o valor não pode ser negativo")
    if origem == destino:
        return valor, Decimal("1")

    try:
        with urlopen(API_URL.format(origem=origem, destino=destino), timeout=10) as resposta:
            dados = json.load(resposta)
        cotacao = Decimal(str(dados[f"{origem}{destino}"]["bid"]))
    except TimeoutError as erro:
        raise ErroConversao("a consulta demorou demais; tente novamente") from erro
    except (HTTPError, URLError, OSError, json.JSONDecodeError) as erro:
        raise ErroConversao("não foi possível consultar a cotação") from erro
    except (KeyError, TypeError, ValueError, InvalidOperation) as erro:
        raise ErroConversao("par de moedas inválido ou indisponível") from erro

    return valor * cotacao, cotacao


def ler_valor(texto: str) -> Decimal:
    try:
        valor = Decimal(texto.strip().replace(",", "."))
    except InvalidOperation as erro:
        raise ValueError("digite um valor numérico válido") from erro
    if not valor.is_finite():
        raise ValueError("digite um valor numérico finito")
    return valor


def formatar_numero(valor: Decimal, casas: int = 2) -> str:
    texto = f"{valor:,.{casas}f}"
    return texto.translate(str.maketrans({",": ".", ".": ","}))


def main() -> None:
    print("=== Conversor de moedas ===")
    print(f"Sugestões: {', '.join(MOEDAS_SUGERIDAS)}\n")

    try:
        valor = ler_valor(input("Valor: "))
        origem = normalizar_moeda(input("Converter de (código): "))
        destino = normalizar_moeda(input("Converter para (código): "))
        resultado, cotacao = converter(valor, origem, destino)
    except (ValueError, ErroConversao) as erro:
        print(f"Erro: {erro}.")
        return
    except (EOFError, KeyboardInterrupt):
        print("\nConversão cancelada.")
        return

    casas = 8 if destino in {"BTC", "ETH"} else 2
    print(
        f"\n{formatar_numero(valor)} {origem} = "
        f"{formatar_numero(resultado, casas)} {destino}"
    )
    print(f"Cotação: 1 {origem} = {formatar_numero(cotacao, 6)} {destino}")


if __name__ == "__main__":
    main()
