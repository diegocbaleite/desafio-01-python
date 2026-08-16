import numpy as np
import pandas as pd

from src.processamento import (
    limpar_texto,
    padronizar_textos,
    padronizar_categorias,
    converter_data,
    padronizar_datas,
    tratar_tempos,
    remover_duplicidades,
    processar_dados,
    calcular_indicadores,
)


def criar_dataframe():
    """Cria um DataFrame pequeno para os testes."""

    return pd.DataFrame(
        {
            "protocolo": [
                "ATD001",
                "ATD002",
                "ATD002",
            ],
            "nome": [
                " Ana Silva ",
                "Bruno Costa",
                "Bruno Costa",
            ],
            "email": [
                "ANA@EMAIL.COM",
                "bruno@email.com",
                "bruno@email.com",
            ],
            "categoria": [
                "acesso ao ava",
                "INSTALAÇÃO DE PROGRAMAS",
                "INSTALAÇÃO DE PROGRAMAS",
            ],
            "data": [
                "2026-08-01",
                "01/08/2026",
                "2026/08/02",
            ],
            "tempo_atendimento": [
                25,
                40,
                30,
            ],
            "status": [
                "resolvido",
                "pendente",
                "pendente",
            ],
        }
    )


def test_limpar_texto():
    assert limpar_texto("  Ana   Silva  ") == "Ana Silva"


def test_limpar_texto_vazio():
    assert limpar_texto(np.nan) == ""


def test_padronizar_textos():
    df = criar_dataframe()

    resultado = padronizar_textos(df)

    assert resultado.loc[0, "nome"] == "Ana Silva"
    assert resultado.loc[0, "email"] == "ana@email.com"
    assert resultado.loc[0, "status"] == "Resolvido"


def test_padronizar_categorias():
    df = criar_dataframe()

    configuracao = {
        "Acesso ao AVA": ["acesso ao ava", "ava"],
        "Instalação de programas": ["instalação de programas", "instalacao"],
    }

    resultado = padronizar_textos(df)
    resultado = padronizar_categorias(
        resultado,
        configuracao,
    )

    assert resultado.loc[0, "categoria"] == "Acesso ao AVA"
    assert (
        resultado.loc[1, "categoria"]
        == "Instalação de programas"
    )



def test_converter_data_iso():
    resultado = converter_data("2026-08-01")

    assert resultado == pd.Timestamp("2026-08-01")


def test_converter_data_brasileira():
    resultado = converter_data("01/08/2026")

    assert resultado == pd.Timestamp("2026-08-01")


def test_converter_data_invalida():
    resultado = converter_data("data-invalida")

    assert pd.isna(resultado)


def test_padronizar_datas():
    df = criar_dataframe()

    resultado = padronizar_datas(df)

    assert resultado.loc[0, "data"] == pd.Timestamp(
        "2026-08-01"
    )

    assert resultado.loc[1, "data"] == pd.Timestamp(
        "2026-08-01"
    )


def test_tratar_tempos():
    df = pd.DataFrame(
        {
            "tempo_atendimento": [
                30,
                -10,
                0,
                481,
                None,
            ]
        }
    )

    resultado = tratar_tempos(df)

    assert resultado.loc[0, "tempo_atendimento"] == 30

    assert pd.isna(
        resultado.loc[1, "tempo_atendimento"]
    )

    assert pd.isna(
        resultado.loc[2, "tempo_atendimento"]
    )

    assert pd.isna(
        resultado.loc[3, "tempo_atendimento"]
    )

    assert pd.isna(
        resultado.loc[4, "tempo_atendimento"]
    )


def test_remover_duplicidades():
    df = criar_dataframe()

    resultado = remover_duplicidades(df)

    assert len(resultado) == 2
    assert resultado["protocolo"].tolist() == [
        "ATD001",
        "ATD002",
    ]


def test_processar_dados():
    df = criar_dataframe()

    configuracao = {
        "categorias": {
            "acesso ao ava": "Acesso ao AVA",
            "instalação de programas": (
                "Instalação de Programas"
            ),
        }
    }

    resultado = processar_dados(
        df,
        configuracao,
    )

    assert len(resultado) == 2

    assert (
        resultado.loc[0, "categoria"]
        == "Acesso ao AVA"
    )

    assert (
        resultado.loc[1, "categoria"]
        == "Instalação de Programas"
    )

    assert (
        resultado.loc[0, "email"]
        == "ana@email.com"
    )

    assert (
        resultado.loc[0, "status"]
        == "Resolvido"
    )


def test_calcular_indicadores():
    df = pd.DataFrame(
        {
            "protocolo": [
                "ATD001",
                "ATD002",
                "ATD003",
            ],
            "nome": [
                "Ana",
                "Bruno",
                "Carla",
            ],
            "email": [
                "ana@email.com",
                "bruno@email.com",
                "",
            ],
            "categoria": [
                "Acesso ao AVA",
                "Acesso ao AVA",
                "Configuração Python",
            ],
            "data": [
                pd.Timestamp("2026-08-01"),
                pd.Timestamp("2026-08-01"),
                pd.Timestamp("2026-08-02"),
            ],
            "tempo_atendimento": [
                20,
                40,
                np.nan,
            ],
            "status": [
                "Resolvido",
                "Resolvido",
                "Pendente",
            ],
        }
    )

    indicadores = calcular_indicadores(
        df,
        total_original=3,
    )

    assert (
        indicadores["resumo"]["total_original"]
        == 3
    )

    assert (
        indicadores["resumo"]["total_processado"]
        == 3
    )

    assert (
        indicadores["indicadores"][
            "tempo_medio_atendimento"
        ]
        == 30.0
    )

    assert (
        indicadores["indicadores"][
            "categoria_mais_frequente"
        ]
        == "Acesso ao AVA"
    )

    assert (
        indicadores["distribuicao"]["por_categoria"][
            "Acesso ao AVA"
        ]
        == 2
    )

    assert (
        indicadores["distribuicao"]["por_status"][
            "Resolvido"
        ]
        == 2
    )

    assert (
        indicadores["qualidade_dados"][
            "registros_incompletos"
        ]
        == 1
    )