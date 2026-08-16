from pathlib import Path
import json
import re

import pandas as pd


# =========================================================
# Expressões regulares
# =========================================================

PADRAO_PROTOCOLO = re.compile(
    r"\b(?:[A-Z]+-)?\d{4}-\d{4}\b|\bATD\d{3,4}\b",
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

def ler_csv(caminho: Path, separador: str = ";") -> pd.DataFrame:
    """Lê os atendimentos do arquivo CSV utilizando o separador configurado."""
    df = pd.read_csv(
        caminho,
        sep=separador,
        encoding="utf-8",
    )
    # Se o separador informado não encontrou múltiplas colunas, faz fallback para vírgula
    if len(df.columns) == 1 and separador != ",":
        df_alt = pd.read_csv(
            caminho,
            sep=",",
            encoding="utf-8",
        )
        if len(df_alt.columns) > 1:
            return df_alt
    return df


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
    Extrai protocolos no formato SUP-2026-XXXX, 2026-XXXX ou ATDXXX do texto.
    """
    if not texto:
        return []

    return PADRAO_PROTOCOLO.findall(texto)


def extrair_telefones(texto: str) -> list[str]:
    """
    Extrai números de telefone do texto.
    """
    if not texto:
        return []

    return PADRAO_TELEFONE.findall(texto)


def extrair_emails(texto: str) -> list[str]:
    """
    Extrai endereços de e-mail do texto.
    """
    if not texto:
        return []

    return PADRAO_EMAIL.findall(texto)