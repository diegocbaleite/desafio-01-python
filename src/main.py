from pathlib import Path

from src.leitura import (
    extrair_emails,
    extrair_protocolos,
    extrair_telefones,
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
        print(
            f"Erro: arquivo não encontrado: {caminho_config}"
        )
        return

    config = ler_json(caminho_config)

    caminho_csv_str = config.get("arquivo_atendimentos") or config.get("arquivos", {}).get("atendimentos", "data/atendimentos.csv")
    caminho_cat_str = config.get("arquivo_categorias") or config.get("arquivos", {}).get("categorias", "data/categorias.json")
    caminho_obs_str = config.get("arquivo_observacoes") or config.get("arquivos", {}).get("observacoes", "data/observacoes.txt")
    diretorio_saida_str = config.get("diretorio_saida") or "output"
    separador_csv = config.get("separador_csv", ";")

    caminho_csv = RAIZ / caminho_csv_str
    caminho_categorias = RAIZ / caminho_cat_str
    caminho_observacoes = RAIZ / caminho_obs_str

    diretorio_saida = RAIZ / diretorio_saida_str
    saida_config = config.get("saida", {})

    caminho_saida_csv = RAIZ / saida_config["csv"] if "csv" in saida_config else diretorio_saida / "atendimentos_processados.csv"
    caminho_saida_json = RAIZ / saida_config["json"] if "json" in saida_config else diretorio_saida / "resumo.json"
    caminho_log = RAIZ / saida_config["log"] if "log" in saida_config else diretorio_saida / "erros.log"
    caminho_graficos = RAIZ / saida_config["graficos"] if "graficos" in saida_config else diretorio_saida / "graficos"


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

    df_original = ler_csv(caminho_csv, separador=separador_csv)

    categorias = ler_json(
        caminho_categorias
    )

    observacoes = ler_txt(
        caminho_observacoes
    )

    total_original = len(
        df_original
    )

    print(
        f"Registros originais: {total_original}"
    )

    print(
        "Observações carregadas: "
        f"{len(observacoes)} caracteres"
    )

    # ---------------------------------------------------------
    # 4. Extrair informações do TXT usando Regex
    # ---------------------------------------------------------

    print(
        "\nExtraindo informações das observações..."
    )

    protocolos_txt = extrair_protocolos(
        observacoes
    )

    telefones_txt = extrair_telefones(
        observacoes
    )

    emails_txt = extrair_emails(
        observacoes
    )

    print(
        "Protocolos encontrados nas observações: "
        f"{len(protocolos_txt)}"
    )

    print(
        "Telefones encontrados nas observações: "
        f"{len(telefones_txt)}"
    )

    print(
        "E-mails encontrados nas observações: "
        f"{len(emails_txt)}"
    )

    # ---------------------------------------------------------
    # 5. Validar registros
    # ---------------------------------------------------------

    print("\nValidando registros...")

    problemas_validacao = []

    for _, registro in df_original.iterrows():

        valido, problemas = validar_registro(
            registro
        )

        if not valido:

            protocolo = registro[
                "protocolo"
            ]

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
    # 6. Processar dados
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
    # 7. Calcular indicadores
    # ---------------------------------------------------------

    print("\nCalculando indicadores...")

    indicadores = calcular_indicadores(
        df_processado,
        total_original,
    )

    # ---------------------------------------------------------
    # 8. Adicionar informações da validação
    # ---------------------------------------------------------

    percentual_com_problemas = (
        (
            total_com_problemas
            / total_original
        )
        * 100
        if total_original > 0
        else 0.0
    )

    indicadores[
        "qualidade_dados"
    ][
        "registros_com_problemas"
    ] = total_com_problemas

    indicadores[
        "qualidade_dados"
    ][
        "percentual_com_problemas"
    ] = percentual_com_problemas

    indicadores[
        "qualidade_dados"
    ][
        "detalhes_problemas"
    ] = problemas_validacao

    # ---------------------------------------------------------
    # 9. Adicionar informações extraídas do TXT
    # ---------------------------------------------------------

    indicadores[
        "dados_extraidos_txt"
    ] = {
        "protocolos": protocolos_txt,
        "telefones": telefones_txt,
        "emails": emails_txt,
        "total_protocolos": len(
            protocolos_txt
        ),
        "total_telefones": len(
            telefones_txt
        ),
        "total_emails": len(
            emails_txt
        ),
    }

    # ---------------------------------------------------------
    # 10. Salvar resultados
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
    # 11. Criar log detalhado
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
        (
            "[INFO] Protocolos extraídos do TXT: "
            f"{len(protocolos_txt)}"
        ),
        (
            "[INFO] Telefones extraídos do TXT: "
            f"{len(telefones_txt)}"
        ),
        (
            "[INFO] E-mails extraídos do TXT: "
            f"{len(emails_txt)}"
        ),
        "",
    ]

    for item in problemas_validacao:

        protocolo = item[
            "protocolo"
        ]

        for problema in item[
            "problemas"
        ]:

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
    # 12. Gerar gráficos
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
    # 13. Exibir relatório
    # ---------------------------------------------------------

    print()

    resumo = gerar_resumo(
        indicadores
    )

    print(resumo)

    # ---------------------------------------------------------
    # 14. Informar arquivos gerados
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