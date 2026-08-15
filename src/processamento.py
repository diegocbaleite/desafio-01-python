import re

import numpy as np
import pandas as pd


def limpar_texto(valor) -> str:
    """Remove espaços extras e padroniza o texto."""
    if pd.isna(valor):
        return ""

    return re.sub(r"\s+", " ", str(valor)).strip()


def padronizar_textos(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa os campos textuais do DataFrame."""
    df = df.copy()

    colunas_texto = [
        "protocolo",
        "nome",
        "email",
        "categoria",
        "status",
    ]

    for coluna in colunas_texto:
        df[coluna] = df[coluna].apply(limpar_texto)

    df["email"] = df["email"].str.lower()
    df["status"] = df["status"].str.title()

    return df


def padronizar_categorias(
    df: pd.DataFrame,
    configuracao_categorias: dict,
) -> pd.DataFrame:
    """Padroniza as categorias usando categorias.json."""
    df = df.copy()

    mapa = configuracao_categorias.get("categorias", {})

    df["categoria"] = (
        df["categoria"]
        .str.lower()
        .map(mapa)
        .fillna(df["categoria"])
    )

    return df


def converter_data(valor):
    """Converte datas em formatos diferentes para uma data única."""
    if pd.isna(valor):
        return pd.NaT

    valor = str(valor).strip()

    formatos = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%d-%m-%Y",
    ]

    for formato in formatos:
        try:
            return pd.to_datetime(valor, format=formato)
        except ValueError:
            continue

    return pd.NaT


def padronizar_datas(df: pd.DataFrame) -> pd.DataFrame:
    """Converte as datas para um formato único."""
    df = df.copy()

    df["data"] = df["data"].apply(converter_data)

    return df


def tratar_tempos(df: pd.DataFrame) -> pd.DataFrame:
    """Converte e trata os tempos de atendimento."""
    df = df.copy()

    df["tempo_atendimento"] = pd.to_numeric(
        df["tempo_atendimento"],
        errors="coerce",
    )

    # Tempos fora do intervalo permitido tornam-se ausentes.
    df.loc[
        (df["tempo_atendimento"] <= 0)
        | (df["tempo_atendimento"] > 480),
        "tempo_atendimento",
    ] = np.nan

    return df


def remover_duplicidades(df: pd.DataFrame) -> pd.DataFrame:
    """Remove registros duplicados pelo protocolo."""
    df = df.copy()

    return df.drop_duplicates(
        subset="protocolo",
        keep="first",
    ).reset_index(drop=True)


def processar_dados(
    df: pd.DataFrame,
    configuracao_categorias: dict,
) -> pd.DataFrame:
    """Executa todas as etapas de tratamento dos dados."""
    df = padronizar_textos(df)
    df = padronizar_categorias(df, configuracao_categorias)
    df = padronizar_datas(df)
    df = tratar_tempos(df)
    df = remover_duplicidades(df)

    return df