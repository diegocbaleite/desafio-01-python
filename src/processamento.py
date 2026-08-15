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


def calcular_indicadores(
    df: pd.DataFrame,
    total_original: int | None = None,
) -> dict:
    """Calcula os principais indicadores dos atendimentos."""

    if total_original is None:
        total_original = len(df)

    total_processado = len(df)

    quantidade_por_categoria = (
        df["categoria"]
        .value_counts()
        .to_dict()
    )

    quantidade_por_status = (
        df["status"]
        .value_counts()
        .to_dict()
    )

    tempo_medio = df["tempo_atendimento"].mean()

    if quantidade_por_categoria:
        categoria_mais_frequente = max(
            quantidade_por_categoria,
            key=quantidade_por_categoria.get,
        )
    else:
        categoria_mais_frequente = None

    registros_incompletos = df[
        df["email"].eq("")
        | df["data"].isna()
        | df["tempo_atendimento"].isna()
    ]

    quantidade_incompletos = len(registros_incompletos)

    duplicidades_removidas = (
        total_original - total_processado
    )

    if total_original > 0:
        percentual_incompletos = (
            quantidade_incompletos / total_original
        ) * 100
    else:
        percentual_incompletos = 0.0

    return {
        "resumo": {
            "total_original": total_original,
            "total_processado": total_processado,
            "duplicidades_removidas": duplicidades_removidas,
        },
        "indicadores": {
            "tempo_medio_atendimento": (
                float(tempo_medio)
                if not pd.isna(tempo_medio)
                else 0.0
            ),
            "categoria_mais_frequente": categoria_mais_frequente,
        },
        "distribuicao": {
            "por_categoria": quantidade_por_categoria,
            "por_status": quantidade_por_status,
        },
        "qualidade_dados": {
            "registros_incompletos": quantidade_incompletos,
            "percentual_incompletos": percentual_incompletos,
        },
    }