# Conversor de Moedas

Aplicação de linha de comando para converter moedas usando cotações atualizadas da [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas).

O projeto foi construído em Python, não exige dependências externas e aceita valores no formato brasileiro.

## Funcionalidades

- Consulta de cotações em tempo real
- Conversão entre moedas fiduciárias e criptomoedas
- Valores com vírgula ou ponto decimal
- Precisão monetária com `Decimal`
- Formatação numérica brasileira
- Tratamento de erros de conexão e entradas inválidas
- Suporte a códigos de moeda em letras maiúsculas ou minúsculas

## Tecnologias

- Python 3.10+
- Biblioteca padrão do Python
- AwesomeAPI
- Unittest

## Como usar

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/tiosoaress/Conversor-de-moedas.git
cd Conversor-de-moedas
```

Execute a aplicação:

```bash
python conversor.py
```

Informe o valor e os códigos das moedas solicitados:

```text
=== Conversor de moedas ===
Sugestões: BRL, USD, EUR, GBP, JPY, CAD, AUD, BTC, ETH

Valor: 100,50
Converter de (código): USD
Converter para (código): BRL

100,50 USD = 515,28 BRL
Cotação: 1 USD = 5,127200 BRL
```

O resultado do exemplo varia conforme a cotação atual.

## Testes

Execute toda a suíte com:

```bash
python -m unittest discover -s tests -v
```

## Estrutura

```text
conversor-de-moedas/
├── conversor.py
├── tests/
│   └── test_conversor.py
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Como contribuir

Contribuições são bem-vindas. Consulte o [guia de contribuição](CONTRIBUTING.md) para começar.

## Licença

Distribuído sob a licença MIT. Consulte [LICENSE](LICENSE) para mais informações.
