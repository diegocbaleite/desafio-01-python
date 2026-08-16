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


def test_verificar_arquivo_existente(tmp_path):
    arquivo = tmp_path / "teste.txt"
    arquivo.write_text(
        "conteudo",
        encoding="utf-8",
    )

    assert verificar_arquivo(arquivo) is True


def test_verificar_arquivo_inexistente(tmp_path):
    arquivo = tmp_path / "nao_existe.txt"

    assert verificar_arquivo(arquivo) is False


def test_ler_txt(tmp_path):
    arquivo = tmp_path / "observacoes.txt"

    arquivo.write_text(
        "ATD001 - atendimento realizado",
        encoding="utf-8",
    )

    resultado = ler_txt(arquivo)

    assert resultado == (
        "ATD001 - atendimento realizado"
    )


def test_ler_json(tmp_path):
    arquivo = tmp_path / "config.json"

    arquivo.write_text(
        '{"nome": "teste"}',
        encoding="utf-8",
    )

    resultado = ler_json(arquivo)

    assert resultado == {
        "nome": "teste"
    }


def test_ler_csv(tmp_path):
    arquivo = tmp_path / "dados.csv"

    arquivo.write_text(
        "protocolo,nome\nATD001,Ana",
        encoding="utf-8",
    )

    resultado = ler_csv(arquivo)

    assert len(resultado) == 1
    assert resultado.iloc[0]["protocolo"] == "ATD001"
    assert resultado.iloc[0]["nome"] == "Ana"


def test_extrair_protocolos():
    texto = """
    ATD001 - atendimento realizado.
    ATD002 - instalação concluída.
    ATD003 - retorno solicitado pelo protocolo ATD003.
    """

    resultado = extrair_protocolos(texto)

    assert resultado == [
        "ATD001",
        "ATD002",
        "ATD003",
        "ATD003",
    ]


def test_extrair_telefones():
    texto = """
    Contato: (65) 99999-1111
    Retorno: (65) 98888-2222
    Telefone: (65) 99999-3333
    """

    resultado = extrair_telefones(texto)

    assert resultado == [
        "(65) 99999-1111",
        "(65) 98888-2222",
        "(65) 99999-3333",
    ]


def test_extrair_emails():
    texto = """
    suporte@ficdevia.com.br
    atendimento@ficdevia.com.br
    """

    resultado = extrair_emails(texto)

    assert resultado == [
        "suporte@ficdevia.com.br",
        "atendimento@ficdevia.com.br",
    ]


def test_extracoes_com_texto_vazio():
    assert extrair_protocolos("") == []
    assert extrair_telefones("") == []
    assert extrair_emails("") == []