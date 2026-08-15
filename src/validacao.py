import re
import pandas as pd


PADRAO_EMAIL = re.compile(
    r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[a-zA-Z]{2,}$"
)


def validar_email(email: str) -> bool:
    """Valida o formato básico de um e-mail."""
    if pd.isna(email):
        return False

    email = str(email).strip()

    if not email:
        return False

    return bool(PADRAO_EMAIL.match(email))


def validar_tempo(tempo) -> bool:
    """Verifica se o tempo de atendimento é válido."""
    if pd.isna(tempo):
        return False

    try:
        tempo = float(tempo)
    except (TypeError, ValueError):
        return False

    return 0 < tempo <= 480


def validar_campos_obrigatorios(registro: pd.Series) -> list[str]:
    """Retorna os problemas encontrados no registro."""
    problemas = []

    campos_obrigatorios = [
        "protocolo",
        "nome",
        "categoria",
        "data",
        "status",
    ]

    for campo in campos_obrigatorios:
        if pd.isna(registro[campo]) or not str(registro[campo]).strip():
            problemas.append(f"{campo} vazio")

    if not validar_email(registro["email"]):
        problemas.append("email inválido")

    if not validar_tempo(registro["tempo_atendimento"]):
        problemas.append("tempo de atendimento inválido")

    return problemas


def validar_registro(registro: pd.Series) -> tuple[bool, list[str]]:
    """Valida um registro e retorna status e motivos."""
    problemas = validar_campos_obrigatorios(registro)

    return len(problemas) == 0, problemas