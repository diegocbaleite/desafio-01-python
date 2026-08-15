import pandas as pd

from src.validacao import (
    validar_email,
    validar_tempo,
    validar_campos_obrigatorios,
    validar_registro,
)


def test_email_valido():
    assert validar_email("usuario@email.com") is True


def test_email_invalido():
    assert validar_email("usuario@email") is False


def test_email_vazio():
    assert validar_email("") is False


def test_tempo_valido():
    assert validar_tempo(30) is True


def test_tempo_zero():
    assert validar_tempo(0) is False


def test_tempo_negativo():
    assert validar_tempo(-10) is False


def test_tempo_acima_do_limite():
    assert validar_tempo(481) is False


def test_tempo_vazio():
    assert validar_tempo(None) is False


def test_registro_valido():
    registro = pd.Series(
        {
            "protocolo": "ATD001",
            "nome": "Ana Silva",
            "email": "ana@email.com",
            "categoria": "Acesso ao AVA",
            "data": pd.Timestamp("2026-08-01"),
            "tempo_atendimento": 30,
            "status": "Resolvido",
        }
    )

    valido, problemas = validar_registro(registro)

    assert valido is True
    assert problemas == []


def test_registro_com_email_invalido():
    registro = pd.Series(
        {
            "protocolo": "ATD003",
            "nome": "Carla Mendes",
            "email": "carla@email",
            "categoria": "Configuração Python",
            "data": pd.Timestamp("2026-08-02"),
            "tempo_atendimento": 35,
            "status": "Pendente",
        }
    )

    valido, problemas = validar_registro(registro)

    assert valido is False
    assert "email inválido" in problemas


def test_registro_com_tempo_invalido():
    registro = pd.Series(
        {
            "protocolo": "ATD007",
            "nome": "Gabriel Santos",
            "email": "gabriel@email.com",
            "categoria": "Configuração Python",
            "data": pd.Timestamp("2026-08-04"),
            "tempo_atendimento": -10,
            "status": "Resolvido",
        }
    )

    valido, problemas = validar_registro(registro)

    assert valido is False
    assert "tempo de atendimento inválido" in problemas