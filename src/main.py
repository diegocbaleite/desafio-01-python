from pathlib import Path

from src.leitura import (
    ler_csv,
    ler_json,
    ler_txt,
    verificar_arquivo,
)
from src.processamento import (
    calcular_indicadores,
    processar_dados,
)
from src.relatorios import (
    gerar_grafico_categorias,
    gerar_grafico_tempos,
    gerar_resumo,
    salvar_csv,
    salvar_json,
    salvar_log,
)
from src.validacao import validar_registro


RAIZ = Path(__file__).resolve().parent.parent


def main():
    """Executa todo o pipeline do sistema."""

    print("=" * 60)
    print("SISTEMA DE ANÁLISE DE ATENDIMENTOS")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Ler configuração
    # ---------------------------------------------------------

    caminho_config = RAIZ / "data" / "config.json"

    if not verificar_arquivo(caminho_config):
        print(f"Erro: arquivo não encontrado: {caminho_config}")
        return

    config = ler_json(caminho_config)

    caminho_csv = RAIZ / config["arquivos"]["atendimentos"]
    caminho_categorias = RAIZ / config["arquivos"]["categorias"]
    caminho_observacoes = RAIZ / config["arquivos"]["observacoes"]

    caminho_saida_csv = RAIZ / config["saida"]["csv"]
    caminho_saida_json = RAIZ / config["saida"]["json"]
    caminho_log = RAIZ / config["saida"]["log"]
    caminho_graficos = RAIZ / config["saida"]["graficos"]

    # ---------------------------------------------------------
    # 2. Verificar arquivos
    # ---------------------------------------------------------

    arquivos_necessarios = [
        caminho_csv,
        caminho_categorias,
        caminho_observacoes,
    ]

    erros = []

    for caminho in arquivos_necessarios:
        if not verificar_arquivo(caminho):
            erros.append(
                f"Arquivo não encontrado: {caminho}"
            )

    if erros:
        salvar_log(
            erros,
            caminho_log,
        )

        for erro in erros:
            print(erro)

        return

    print("\nArquivos encontrados com sucesso.")

    # ---------------------------------------------------------
    # 3. Ler arquivos
    # ---------------------------------------------------------

    print("\nLendo dados...")

    df_original = ler_csv(caminho_csv)
    categorias = ler_json(caminho_categorias)
    observacoes = ler_txt(caminho_observacoes)

    total_original = len(df_original)

    print(
        f"Registros originais: {total_original}"
    )

    print(
        "Observações carregadas: "
        f"{len(observacoes)} caracteres"
    )

    # ---------------------------------------------------------
    # 4. Validar registros
    # ---------------------------------------------------------

    print("\nValidando registros...")

    problemas_validacao = []

    for _, registro in df_original.iterrows():
        valido, problemas = validar_registro(
            registro
        )

        if not valido:
            protocolo = registro["protocolo"]

            problemas_validacao.append(
                {
                    "protocolo": protocolo,
                    "problemas": problemas,
                }
            )

    total_com_problemas = len(
        problemas_validacao
    )

    print(
        "Registros com problemas: "
        f"{total_com_problemas}"
    )

    # ---------------------------------------------------------
    # 5. Processar dados
    # ---------------------------------------------------------

    print("\nProcessando dados...")

    df_processado = processar_dados(
        df_original,
        categorias,
    )

    total_processado = len(
        df_processado
    )

    print(
        "Registros após processamento: "
        f"{total_processado}"
    )

    # ---------------------------------------------------------
    # 6. Calcular indicadores
    # ---------------------------------------------------------

    print("\nCalculando indicadores...")

    indicadores = calcular_indicadores(
        df_processado,
        total_original,
    )

    # ---------------------------------------------------------
    # 7. Adicionar informações da validação
    # ---------------------------------------------------------

    percentual_com_problemas = (
        (
            total_com_problemas
            / total_original
        ) * 100
        if total_original > 0
        else 0.0
    )

    indicadores["qualidade_dados"][
        "registros_com_problemas"
    ] = total_com_problemas

    indicadores["qualidade_dados"][
        "percentual_com_problemas"
    ] = percentual_com_problemas

    indicadores["qualidade_dados"][
        "detalhes_problemas"
    ] = problemas_validacao

    # ---------------------------------------------------------
    # 8. Salvar resultados
    # ---------------------------------------------------------

    print("\nSalvando resultados...")

    salvar_csv(
        df_processado,
        caminho_saida_csv,
    )

    salvar_json(
        indicadores,
        caminho_saida_json,
    )

    # ---------------------------------------------------------
    # 9. Criar log detalhado
    # ---------------------------------------------------------

    mensagens_log = [
        "=" * 60,
        "LOG DE PROCESSAMENTO",
        "=" * 60,
        (
            "[INFO] Registros originais: "
            f"{indicadores['resumo']['total_original']}"
        ),
        (
            "[INFO] Registros processados: "
            f"{indicadores['resumo']['total_processado']}"
        ),
        (
            "[INFO] Duplicidades removidas: "
            f"{indicadores['resumo']['duplicidades_removidas']}"
        ),
        (
            "[INFO] Registros com problemas: "
            f"{total_com_problemas}"
        ),
        "",
    ]

    for item in problemas_validacao:
        protocolo = item["protocolo"]

        for problema in item["problemas"]:
            mensagens_log.append(
                f"[WARNING] {protocolo} - {problema}"
            )

    mensagens_log.extend(
        [
            "",
            (
                "[INFO] Registros incompletos após "
                "processamento: "
                f"{indicadores['qualidade_dados']['registros_incompletos']}"
            ),
            (
                "[INFO] Percentual de incompletos: "
                f"{indicadores['qualidade_dados']['percentual_incompletos']:.2f}%"
            ),
            (
                "[INFO] Percentual de registros "
                "com problemas: "
                f"{percentual_com_problemas:.2f}%"
            ),
            "=" * 60,
        ]
    )

    salvar_log(
        mensagens_log,
        caminho_log,
    )

    # ---------------------------------------------------------
    # 10. Gerar gráficos
    # ---------------------------------------------------------

    print("\nGerando gráficos...")

    gerar_grafico_categorias(
        df_processado,
        caminho_graficos
        / "atendimentos_por_categoria.png",
    )

    gerar_grafico_tempos(
        df_processado,
        caminho_graficos
        / "tempos_atendimento.png",
    )

    # ---------------------------------------------------------
    # 11. Exibir relatório
    # ---------------------------------------------------------

    print()

    resumo = gerar_resumo(
        indicadores
    )

    print(resumo)

    # ---------------------------------------------------------
    # 12. Informar arquivos gerados
    # ---------------------------------------------------------

    print("\nArquivos gerados:")

    print(
        f"- {caminho_saida_csv}"
    )

    print(
        f"- {caminho_saida_json}"
    )

    print(
        f"- {caminho_log}"
    )

    print(
        "- "
        f"{caminho_graficos / 'atendimentos_por_categoria.png'}"
    )

    print(
        "- "
        f"{caminho_graficos / 'tempos_atendimento.png'}"
    )

    print(
        "\nProcessamento concluído com sucesso!"
    )


if __name__ == "__main__":
    main()