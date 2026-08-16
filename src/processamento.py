import re

import numpy as np
import pandas as pd

from src.validacao import validar_registro


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


def mapear_categoria_valor(val: str, configuracao_categorias: dict) -> str:
    """Mapeia uma string de categoria para a versão padronizada do dicionário."""
    if not val or pd.isna(val):
        return ""

    val_clean = str(val).strip()
    val_lower = val_clean.lower()

    dicionario = configuracao_categorias.get("categorias", configuracao_categorias)

    for cat_oficial, sinonimos in dicionario.items():
        if isinstance(sinonimos, str):
            if val_lower == cat_oficial.lower() or val_lower == sinonimos.lower():
                return sinonimos
        elif isinstance(sinonimos, list):
            if val_lower == cat_oficial.lower():
                return cat_oficial
            for sinonimo in sinonimos:
                sinonimo_lower = sinonimo.lower()
                if val_lower == sinonimo_lower or sinonimo_lower in val_lower or val_lower in sinonimo_lower:
                    return cat_oficial

    return val_clean


def padronizar_categorias(
    df: pd.DataFrame,
    configuracao_categorias: dict,
) -> pd.DataFrame:
    """Padroniza as categorias usando categorias.json."""
    df = df.copy()

    if "categoria" in df.columns:
        df["categoria"] = df["categoria"].apply(
            lambda cat: mapear_categoria_valor(cat, configuracao_categorias)
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
            return pd.to_datetime(
                valor,
                format=formato,
            )
        except ValueError:
            continue

    return pd.NaT


def padronizar_datas(df: pd.DataFrame) -> pd.DataFrame:
    """Converte as datas para um formato único."""
    df = df.copy()

    df["data"] = df["data"].apply(
        converter_data
    )

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
    descartar_invalidos: bool = True,
) -> pd.DataFrame:
    """Executa todas as etapas de tratamento e filtragem dos dados."""

    df = padronizar_textos(df)

    df = padronizar_categorias(
        df,
        configuracao_categorias,
    )

    df = padronizar_datas(df)

    df = tratar_tempos(df)

    df = remover_duplicidades(df)

    if descartar_invalidos:
        mascara_validos = []
        for _, reg in df.iterrows():
            valido, _ = validar_registro(reg)
            mascara_validos.append(valido)
        df = df[mascara_validos].reset_index(drop=True)

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

    # ---------------------------------------------------------
    # Indicadores de tempo
    # ---------------------------------------------------------

    tempos = df[
        "tempo_atendimento"
    ].to_numpy(dtype=float)

    if np.isfinite(tempos).any():

        tempo_medio = np.nanmean(
            tempos
        )

        tempo_mediano = np.nanmedian(
            tempos
        )

        tempo_minimo = np.nanmin(
            tempos
        )

        tempo_maximo = np.nanmax(
            tempos
        )

        # Normalização do tempo médio em relação
        # ao limite máximo permitido de 480 minutos.
        tempo_medio_normalizado = (
            np.nanmean(tempos) / 480
        ) * 100

    else:

        tempo_medio = 0.0
        tempo_mediano = 0.0
        tempo_minimo = 0.0
        tempo_maximo = 0.0
        tempo_medio_normalizado = 0.0

    # ---------------------------------------------------------
    # Categoria mais frequente
    # ---------------------------------------------------------

    if quantidade_por_categoria:

        categoria_mais_frequente = max(
            quantidade_por_categoria,
            key=quantidade_por_categoria.get,
        )

    else:

        categoria_mais_frequente = None

    # ---------------------------------------------------------
    # Registros incompletos
    # ---------------------------------------------------------

    registros_incompletos = df[
        df["email"].eq("")
        | df["data"].isna()
        | df["tempo_atendimento"].isna()
    ]

    quantidade_incompletos = len(
        registros_incompletos
    )

    # ---------------------------------------------------------
    # Duplicidades
    # ---------------------------------------------------------

    duplicidades_removidas = (
        total_original
        - total_processado
    )

    # ---------------------------------------------------------
    # Percentual de incompletos
    # ---------------------------------------------------------

    if total_original > 0:

        percentual_incompletos = (
            quantidade_incompletos
            / total_original
        ) * 100

    else:

        percentual_incompletos = 0.0

    # ---------------------------------------------------------
    # Resultado
    # ---------------------------------------------------------

    return {
        "resumo": {
            "total_original": total_original,
            "total_processado": total_processado,
            "duplicidades_removidas": (
                duplicidades_removidas
            ),
        },
        "indicadores": {
            "tempo_medio_atendimento": (
                float(tempo_medio)
            ),
            "tempo_mediano_atendimento": (
                float(tempo_mediano)
            ),
            "tempo_minimo_atendimento": (
                float(tempo_minimo)
            ),
            "tempo_maximo_atendimento": (
                float(tempo_maximo)
            ),
            "tempo_medio_normalizado_percentual": (
                float(tempo_medio_normalizado)
            ),
            "categoria_mais_frequente": (
                categoria_mais_frequente
            ),
        },
        "distribuicao": {
            "por_categoria": (
                quantidade_por_categoria
            ),
            "por_status": (
                quantidade_por_status
            ),
        },
        "qualidade_dados": {
            "registros_incompletos": (
                quantidade_incompletos
            ),
            "percentual_incompletos": (
                percentual_incompletos
            ),
        },
    }