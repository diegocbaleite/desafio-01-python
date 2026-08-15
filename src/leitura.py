from pathlib import Path
import json
import pandas as pd


def verificar_arquivo(caminho: Path) -> bool:
    """Verifica se um arquivo existe."""
    return caminho.exists() and caminho.is_file()


def ler_csv(caminho: Path) -> pd.DataFrame:
    """Lê os atendimentos do arquivo CSV."""
    return pd.read_csv(caminho)


def ler_json(caminho: Path) -> dict:
    """Lê um arquivo JSON."""
    with caminho.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def ler_txt(caminho: Path) -> str:
    """Lê o conteúdo de um arquivo TXT."""
    with caminho.open("r", encoding="utf-8") as arquivo:
        return arquivo.read()