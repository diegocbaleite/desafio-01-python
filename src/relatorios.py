import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def salvar_csv(
    df: pd.DataFrame,
    caminho: Path,
) -> None:
    """Salva o DataFrame processado em CSV."""

    caminho.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        caminho,
        index=False,
        encoding="utf-8",
    )


def salvar_json(
    dados: dict,
    caminho: Path,
) -> None:
    """Salva os indicadores em JSON."""

    caminho.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with caminho.open(
        "w",
        encoding="utf-8",
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4,
        )


def salvar_log(
    mensagens: list[str],
    caminho: Path,
) -> None:
    """Salva mensagens de processamento em um arquivo de log."""

    caminho.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with caminho.open(
        "w",
        encoding="utf-8",
    ) as arquivo:

        for mensagem in mensagens:
            arquivo.write(
                mensagem + "\n"
            )


def gerar_resumo(
    indicadores: dict,
) -> str:
    """Gera um resumo textual dos indicadores."""

    resumo = indicadores[
        "resumo"
    ]

    dados_indicadores = indicadores[
        "indicadores"
    ]

    distribuicao = indicadores[
        "distribuicao"
    ]

    qualidade = indicadores[
        "qualidade_dados"
    ]

    # ---------------------------------------------------------
    # Indicadores de tempo
    # ---------------------------------------------------------

    tempo_medio = dados_indicadores[
        "tempo_medio_atendimento"
    ]

    tempo_mediano = dados_indicadores[
        "tempo_mediano_atendimento"
    ]

    tempo_minimo = dados_indicadores[
        "tempo_minimo_atendimento"
    ]

    tempo_maximo = dados_indicadores[
        "tempo_maximo_atendimento"
    ]

    tempo_medio_normalizado = dados_indicadores.get(
        "tempo_medio_normalizado_percentual",
        0.0,
    )

    # ---------------------------------------------------------
    # Tratamento de valores ausentes
    # ---------------------------------------------------------

    if pd.isna(tempo_medio):
        tempo_medio = 0.0

    if pd.isna(tempo_mediano):
        tempo_mediano = 0.0

    if pd.isna(tempo_minimo):
        tempo_minimo = 0.0

    if pd.isna(tempo_maximo):
        tempo_maximo = 0.0

    if pd.isna(tempo_medio_normalizado):
        tempo_medio_normalizado = 0.0

    # ---------------------------------------------------------
    # Cabeçalho
    # ---------------------------------------------------------

    linhas = [
        "=" * 60,
        "RELATÓRIO DE ATENDIMENTOS",
        "=" * 60,

        (
            "Registros originais: "
            f"{resumo['total_original']}"
        ),

        (
            "Registros processados: "
            f"{resumo['total_processado']}"
        ),

        (
            "Duplicidades removidas: "
            f"{resumo['duplicidades_removidas']}"
        ),

        "",
        "Atendimentos por categoria:",
    ]

    # ---------------------------------------------------------
    # Distribuição por categoria
    # ---------------------------------------------------------

    for categoria, quantidade in distribuicao[
        "por_categoria"
    ].items():

        linhas.append(
            f"- {categoria}: {quantidade}"
        )

    # ---------------------------------------------------------
    # Distribuição por status
    # ---------------------------------------------------------

    linhas.extend(
        [
            "",
            "Atendimentos por status:",
        ]
    )

    for status, quantidade in distribuicao[
        "por_status"
    ].items():

        linhas.append(
            f"- {status}: {quantidade}"
        )

    # ---------------------------------------------------------
    # Indicadores de tempo
    # ---------------------------------------------------------

    linhas.extend(
        [
            "",
            "Indicadores de tempo:",

            (
                "- Tempo médio: "
                f"{tempo_medio:.2f} minutos"
            ),

            (
                "- Tempo mediano: "
                f"{tempo_mediano:.2f} minutos"
            ),

            (
                "- Tempo mínimo: "
                f"{tempo_minimo:.2f} minutos"
            ),

            (
                "- Tempo máximo: "
                f"{tempo_maximo:.2f} minutos"
            ),

            (
                "- Tempo médio normalizado: "
                f"{tempo_medio_normalizado:.2f}%"
            ),

            "",
            (
                "Categoria mais frequente: "
                f"{dados_indicadores['categoria_mais_frequente']}"
            ),

            "",
            "Qualidade dos dados:",
        ]
    )

    # ---------------------------------------------------------
    # Qualidade dos dados
    # ---------------------------------------------------------

    linhas.extend(
        [
            (
                "Registros incompletos: "
                f"{qualidade['registros_incompletos']}"
            ),

            (
                "Percentual de incompletos: "
                f"{qualidade['percentual_incompletos']:.2f}%"
            ),
        ]
    )

    # ---------------------------------------------------------
    # Registros com problemas
    # ---------------------------------------------------------

    if "registros_com_problemas" in qualidade:

        linhas.append(
            (
                "Registros com problemas: "
                f"{qualidade['registros_com_problemas']}"
            )
        )

    if "percentual_com_problemas" in qualidade:

        linhas.append(
            (
                "Percentual com problemas: "
                f"{qualidade['percentual_com_problemas']:.2f}%"
            )
        )

    # ---------------------------------------------------------
    # Dados extraídos do TXT
    # ---------------------------------------------------------

    dados_txt = indicadores.get(
        "dados_extraidos_txt"
    )

    if dados_txt:

        linhas.extend(
            [
                "",
                "Informações extraídas das observações:",

                (
                    "- Protocolos encontrados: "
                    f"{dados_txt.get('total_protocolos', 0)}"
                ),

                (
                    "- Telefones encontrados: "
                    f"{dados_txt.get('total_telefones', 0)}"
                ),

                (
                    "- E-mails encontrados: "
                    f"{dados_txt.get('total_emails', 0)}"
                ),
            ]
        )

    linhas.append("=" * 60)

    return "\n".join(linhas)


def gerar_grafico_categorias(
    df: pd.DataFrame,
    caminho: Path,
) -> None:
    """Gera gráfico de atendimentos por categoria."""

    contagem = df[
        "categoria"
    ].value_counts()

    caminho.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.figure(
        figsize=(10, 6)
    )

    contagem.plot(
        kind="bar"
    )

    plt.title(
        "Atendimentos por categoria"
    )

    plt.xlabel(
        "Categoria"
    )

    plt.ylabel(
        "Quantidade de atendimentos"
    )

    plt.xticks(
        rotation=20
    )

    plt.tight_layout()

    plt.savefig(
        caminho
    )

    plt.close()


def gerar_grafico_tempos(
    df: pd.DataFrame,
    caminho: Path,
) -> None:
    """Gera gráfico da distribuição dos tempos."""

    tempos = df[
        "tempo_atendimento"
    ].dropna()

    caminho.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.figure(
        figsize=(10, 6)
    )

    plt.hist(
        tempos,
        bins=6,
    )

    plt.title(
        "Distribuição dos tempos de atendimento"
    )

    plt.xlabel(
        "Tempo de atendimento (minutos)"
    )

    plt.ylabel(
        "Quantidade de atendimentos"
    )

    plt.tight_layout()

    plt.savefig(
        caminho
    )

    plt.close()