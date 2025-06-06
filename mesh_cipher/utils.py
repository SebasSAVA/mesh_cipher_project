import hashlib

# Primeros 256 decimales de Pi (en bytes)
# Para simplificar, aquí uso primeros 256 bytes (0-255) derivados de Pi
PI_BYTES = bytes([
    3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3, 2, 3, 8, 4,
    6, 2, 6, 4, 3, 3, 8, 3, 2, 7, 9, 5, 0, 2, 8, 8, 4, 1, 9, 7,
    1, 6, 9, 3, 9, 9, 3, 7, 5, 1, 0, 5, 8, 2, 0, 9, 7, 4, 9, 4,
    4, 5, 9, 2, 3, 0, 7, 8, 1, 6, 4, 0, 6, 2, 8, 6, 2, 0, 8, 9,
    9, 8, 6, 2, 8, 0, 3, 4, 8, 2, 5, 3, 4, 2, 1, 1, 7, 0, 6, 7,
    9, 8, 2, 1, 4, 8, 0, 8, 6, 5, 1, 3, 2, 8, 2, 3, 0, 6, 6, 4,
    7, 0, 9, 3, 8, 4, 4, 6, 0, 9, 5, 5, 0, 5, 8, 2, 2, 3, 1, 7,
    2, 5, 3, 5, 9, 4, 0, 8, 1, 2, 8, 4, 8, 1, 1, 1, 7, 4, 5, 0,
    2, 8, 4, 1, 0, 2, 7, 0, 1, 9, 3, 8, 5, 2, 1, 1, 0, 5, 5, 5,
    9, 6, 4, 4, 6, 2, 2, 9, 4, 8, 9, 5, 4, 9, 3, 0, 3, 8, 1, 9,
    6, 4, 4, 2, 8, 8, 1, 0, 9, 7, 5, 6, 6, 5, 9, 3, 3, 4, 4, 6,
    1, 2, 8, 4, 7, 5, 6, 4, 8, 2, 3, 3, 7, 8, 6, 7, 8, 3, 1, 6,
    5, 2, 7, 1, 2, 0, 1, 9, 0, 9, 1, 4, 5, 6, 4, 8, 5, 6, 6, 9,
    2, 3, 4, 6, 0, 3, 4, 8, 6, 1, 0, 4, 5, 4, 3, 2, 6, 6, 4, 8,
    2, 1, 3, 3, 9, 3, 6, 0, 7, 2, 6, 0, 2, 4, 9, 1, 4, 1, 2, 7,
    3, 7, 2, 4, 5, 8, 7, 0, 0, 6, 6, 0, 6, 3, 1, 5, 5, 8, 8, 1
])


def sha3_256(data: bytes) -> bytes:
    """Genera hash SHA3-256 para los datos dados."""
    return hashlib.sha3_256(data).digest()


def xor_bytes(b1: bytes, b2: bytes) -> bytes:
    """XOR bit a bit entre dos bytes de igual longitud."""
    if len(b1) != len(b2):
        raise ValueError("Los bytes deben tener la misma longitud para XOR")
    return bytes([x ^ y for x, y in zip(b1, b2)])


def split_bytes(data: bytes, parts: int) -> list[bytes]:
    """Divide bytes en partes iguales."""
    if len(data) % parts != 0:
        raise ValueError("Los datos no son divisibles en partes iguales")
    part_len = len(data) // parts
    return [data[i * part_len:(i + 1) * part_len] for i in range(parts)]


def get_p_array() -> list[int]:
    """
    Devuelve P-array inicializado con primeros 256 decimales de Pi (byte por byte).
    Valor entero entre 0 y 255.
    """
    return list(PI_BYTES[:256])

def vigenere_matrix() -> list[list[int]]:
    """Genera una matriz Vigenère 256x256."""
    matrix = [[(i + j) % 256 for j in range(256)] for i in range(256)]
    return matrix