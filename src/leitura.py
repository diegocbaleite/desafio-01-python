from pathlib import Path
import json
import re

import pandas as pd


# =========================================================
# Expressões regulares
# =========================================================

PADRAO_PROTOCOLO = re.compile(
    r"\bATD\d{3}\b",
    re.IGNORECASE,
)

PADRAO_TELEFONE = re.compile(
    r"\(?\d{2}\)?\s?9?\d{4,5}[-\s]?\d{4}"
)

PADRAO_EMAIL = re.compile(
    r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+",
    re.IGNORECASE,
)


# =========================================================
# Verificação de arquivos
# =========================================================

def verificar_arquivo(caminho: Path) -> bool:
    """Verifica se um arquivo existe."""

    return caminho.exists() and caminho.is_file()


# =========================================================
# Leitura de arquivos
# =========================================================

def ler_csv(caminho: Path) -> pd.DataFrame:
    """Lê os atendimentos do arquivo CSV."""

    return pd.read_csv(
        caminho,
        encoding="utf-8",
    )


def ler_json(caminho: Path) -> dict:
    """Lê um arquivo JSON."""

    with caminho.open(
        "r",
        encoding="utf-8",
    ) as arquivo:

        return json.load(arquivo)


def ler_txt(caminho: Path) -> str:
    """Lê o conteúdo de um arquivo TXT."""

    with caminho.open(
        "r",
        encoding="utf-8",
    ) as arquivo:

        return arquivo.read()


# =========================================================
# Extração com Regex
# =========================================================

def extrair_protocolos(texto: str) -> list[str]:
    """
    Extrai protocolos no formato ATD### do texto.

    Exemplo:
        ATD001
        ATD002
        ATD012
    """

    if not texto:
        return []

    return PADRAO_PROTOCOLO.findall(
        texto
    )


def extrair_telefones(texto: str) -> list[str]:
    """
    Extrai números de telefone do texto.

    Aceita formatos como:

        (65) 99999-1111
        (65) 98888-2222
        65 99999-3333
    """

    if not texto:
        return []

    return PADRAO_TELEFONE.findall(
        texto
    )


def extrair_emails(texto: str) -> list[str]:
    """
    Extrai endereços de e-mail do texto.

    Exemplo:

        suporte@ficdevia.com.br
        atendimento@ficdevia.com.br
    """

    if not texto:
        return []

    return PADRAO_EMAIL.findall(
        texto
    )