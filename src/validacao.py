import re
import pandas as pd


PADRAO_EMAIL = re.compile(
    r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[a-zA-Z]{2,}$"
)

PADRAO_PROTOCOLO = re.compile(
    r"^(?:[A-Z]+-)?\d{4}-\d{4}$|^ATD\d{3,4}$",
    re.IGNORECASE,
)


def validar_email(email: str) -> bool:
    """Valida o formato básico de um e-mail com TLD."""
    if pd.isna(email):
        return False

    email = str(email).strip()

    if not email:
        return False

    return bool(PADRAO_EMAIL.match(email))


def validar_tempo(tempo) -> bool:
    """Verifica se o tempo de atendimento é válido (0 < tempo <= 480 minutos)."""
    if pd.isna(tempo):
        return False

    try:
        tempo = float(tempo)
    except (TypeError, ValueError):
        return False

    return 0 < tempo <= 480


def validar_data(valor) -> bool:
    """Verifica se a data é válida e pode ser convertida."""
    if pd.isna(valor):
        return False

    if isinstance(valor, (pd.Timestamp, pd.DatetimeIndex)):
        return True

    valor = str(valor).strip()
    if not valor:
        return False

    formatos = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%d-%m-%Y",
    ]

    for formato in formatos:
        try:
            pd.to_datetime(valor, format=formato)
            return True
        except ValueError:
            continue

    return False


def validar_protocolo(protocolo: str) -> bool:
    """Valida o formato do protocolo de atendimento."""
    if pd.isna(protocolo):
        return False

    proto = str(protocolo).strip()
    if not proto:
        return False

    return bool(PADRAO_PROTOCOLO.match(proto))


def validar_campos_obrigatorios(registro: pd.Series) -> list[str]:
    """Retorna a lista de problemas/inconsistências encontrados no registro."""
    problemas = []

    # Campos simples obrigatórios
    campos = ["protocolo", "categoria", "status"]
    if "nome" in registro.index:
        campos.append("nome")

    for campo in campos:
        if pd.isna(registro.get(campo)) or not str(registro.get(campo)).strip():
            problemas.append(f"{campo} vazio")

    # Validação de e-mail
    if not validar_email(registro.get("email")):
        problemas.append("email inválido")

    # Validação de tempo (suporta tanto tempo_atendimento quanto tempo_minutos)
    tempo = registro.get("tempo_atendimento") if "tempo_atendimento" in registro.index else registro.get("tempo_minutos")
    if not validar_tempo(tempo):
        problemas.append("tempo de atendimento inválido")

    # Validação de data
    if not validar_data(registro.get("data")):
        problemas.append("data inválida")

    return problemas


def validar_registro(registro: pd.Series) -> tuple[bool, list[str]]:
    """Valida um registro e retorna uma tupla (é_válido, lista_de_motivos)."""
    problemas = validar_campos_obrigatorios(registro)
    return len(problemas) == 0, problemas