from typing import Optional
from mesh_cipher.utils import xor_bytes


class CustomPadding:
    """
    Implementa un padding personalizado para el cifrado,
    añadiendo bytes de relleno generados con XOR usando subclaves.
    """

    def __init__(self, subkeys):
        self.subkeys = subkeys  # Lista de subclaves (bytes)

    def pad(self, data: bytes, block_size: int = 16) -> bytes:
        """
        Añade padding para que la longitud de `data` sea múltiplo de block_size.
        Padding con bytes controlados mezclados vía XOR con subclaves.

        Args:
            data: bytes a rellenar
            block_size: tamaño base para padding (default 16)

        Returns:
            bytes con padding añadido
        """
        pad_len = (block_size - (len(data) % block_size)) % block_size
        if pad_len == 0:
            pad_len = block_size  # Siempre añadimos padding

        # Generamos relleno usando XOR de valores fijos con subclave 0
        base_pad = bytes([(i + 1) % 256 for i in range(pad_len)])
        key = self.subkeys[0] if self.subkeys else bytes([0] * pad_len)
        # Si subclave es menor que pad_len, repetir subclave
        key_repeated = (key * (pad_len // len(key) + 1))[:pad_len]
        padding = xor_bytes(base_pad, key_repeated)

        return data + padding

    def unpad(self, data: bytes, block_size: int = 16) -> Optional[bytes]:
        """
        Elimina el padding agregado al final de los datos.
        Asume que el padding fue agregado con el método `pad`.

        Args:
            data: bytes con padding
            block_size: tamaño base para padding

        Returns:
            bytes sin padding, o None si padding inválido
        """
        if len(data) == 0 or len(data) % block_size != 0:
            return None  # No es válido

        # Tomamos la longitud del padding por el último byte XOR inverso
        # Como padding es bytes mezclados, buscamos patrón del padding
        # Estrategia: calculamos posible longitud y verificamos coincidencia
        for pad_len in range(1, block_size + 1):
            base_pad = bytes([(i + 1) % 256 for i in range(pad_len)])
            key = self.subkeys[0] if self.subkeys else bytes([0] * pad_len)
            key_repeated = (key * (pad_len // len(key) + 1))[:pad_len]
            expected_pad = xor_bytes(base_pad, key_repeated)

            if data[-pad_len:] == expected_pad:
                # padding válido encontrado
                return data[:-pad_len]

        return None  # No se encontró padding válido
