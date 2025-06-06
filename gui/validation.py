import re
from typing import Tuple

MIN_KEY_LENGTH = 8
ALLOWED_KEY_PATTERN = re.compile(r'^[\x20-\x7E]+$')  # ASCII imprimibles (espacio a ~)

def validate_key(key: str) -> Tuple[bool, str]:
    """
    Valida que la clave cumpla longitud mínima y caracteres permitidos.

    Args:
        key (str): Clave ingresada por el usuario.

    Returns:
        Tuple[bool, str]: (es válida?, mensaje de error o éxito)
    """
    if not key:
        return False, "La clave no puede estar vacía."
    if len(key) < MIN_KEY_LENGTH:
        return False, f"La clave debe tener al menos {MIN_KEY_LENGTH} caracteres."
    if not ALLOWED_KEY_PATTERN.match(key):
        return False, "La clave contiene caracteres no permitidos."
    return True, "Clave válida."

def validate_message(message: str) -> Tuple[bool, str]:
    """
    Valida que el mensaje no esté vacío.

    Args:
        message (str): Mensaje ingresado por el usuario.

    Returns:
        Tuple[bool, str]: (es válido?, mensaje de error o éxito)
    """
    if not message:
        return False, "El mensaje no puede estar vacío."
    return True, "Mensaje válido."
