from pathlib import Path


def test_arquivos_de_saida_existentes():
    raiz = Path(__file__).resolve().parent.parent

    arquivos = [
        raiz / "output" / "atendimentos_processados.csv",
        raiz / "output" / "resumo.json",
        raiz / "output" / "erros.log",
        (
            raiz
            / "output"
            / "graficos"
            / "atendimentos_por_categoria.png"
        ),
        (
            raiz
            / "output"
            / "graficos"
            / "distribuicao_tempos.png"
        ),

    ]

    for arquivo in arquivos:
        assert arquivo.exists(), (
            f"Arquivo não encontrado: {arquivo}"
        )