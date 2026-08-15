import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def salvar_csv(df: pd.DataFrame, caminho: Path) -> None:
    """Salva o DataFrame processado em CSV."""
    caminho.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        caminho,
        index=False,
        encoding="utf-8",
    )


def salvar_json(dados: dict, caminho: Path) -> None:
    """Salva os indicadores em JSON."""
    caminho.parent.mkdir(parents=True, exist_ok=True)

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
    caminho.parent.mkdir(parents=True, exist_ok=True)

    with caminho.open(
        "w",
        encoding="utf-8",
    ) as arquivo:
        for mensagem in mensagens:
            arquivo.write(mensagem + "\n")


def gerar_resumo(indicadores: dict) -> str:
    """Gera um resumo textual dos indicadores."""

    resumo = indicadores["resumo"]
    dados_indicadores = indicadores["indicadores"]
    distribuicao = indicadores["distribuicao"]
    qualidade = indicadores["qualidade_dados"]

    tempo_medio = dados_indicadores[
        "tempo_medio_atendimento"
    ]

    if pd.isna(tempo_medio):
        tempo_medio = 0.0

    linhas = [
        "=" * 60,
        "RELATÓRIO DE ATENDIMENTOS",
        "=" * 60,
        f"Registros originais: {resumo['total_original']}",
        f"Registros processados: {resumo['total_processado']}",
        (
            "Duplicidades removidas: "
            f"{resumo['duplicidades_removidas']}"
        ),
        "",
        "Atendimentos por categoria:",
    ]

    for categoria, quantidade in distribuicao[
        "por_categoria"
    ].items():
        linhas.append(
            f"- {categoria}: {quantidade}"
        )

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

    linhas.extend(
        [
            "",
            f"Tempo médio: {tempo_medio:.2f} minutos",
            (
                "Categoria mais frequente: "
                f"{dados_indicadores['categoria_mais_frequente']}"
            ),
            "",
            "Qualidade dos dados:",
            (
                "Registros incompletos: "
                f"{qualidade['registros_incompletos']}"
            ),
            (
                "Percentual de incompletos: "
                f"{qualidade['percentual_incompletos']:.2f}%"
            ),
            "=" * 60,
        ]
    )

    return "\n".join(linhas)


def gerar_grafico_categorias(
    df: pd.DataFrame,
    caminho: Path,
) -> None:
    """Gera gráfico de atendimentos por categoria."""

    contagem = df["categoria"].value_counts()

    caminho.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.figure(figsize=(10, 6))

    contagem.plot(kind="bar")

    plt.title("Atendimentos por categoria")
    plt.xlabel("Categoria")
    plt.ylabel("Quantidade de atendimentos")
    plt.xticks(rotation=20)

    plt.tight_layout()
    plt.savefig(caminho)
    plt.close()


def gerar_grafico_tempos(
    df: pd.DataFrame,
    caminho: Path,
) -> None:
    """Gera gráfico da distribuição dos tempos."""

    tempos = df["tempo_atendimento"].dropna()

    caminho.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.figure(figsize=(10, 6))

    plt.hist(tempos, bins=6)

    plt.title("Distribuição dos tempos de atendimento")
    plt.xlabel("Tempo de atendimento (minutos)")
    plt.ylabel("Quantidade de atendimentos")

    plt.tight_layout()
    plt.savefig(caminho)
    plt.close()