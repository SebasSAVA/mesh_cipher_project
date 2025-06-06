from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
from typing import Tuple


class ChaCha20Cipher:
    """
    Implementa cifrado y descifrado usando ChaCha20.
    """

    NONCE_SIZE = 12  # bytes recomendados para nonce ChaCha20

    def __init__(self, key: bytes):
        """
        Inicializa con una clave de 256 bits (32 bytes).

        Args:
            key (bytes): clave de cifrado (32 bytes)
        """
        if not isinstance(key, bytes) or len(key) != 32:
            raise ValueError("La clave debe ser de 32 bytes (256 bits)")
        self.key = key

    def encrypt(self, plaintext: bytes) -> Tuple[bytes, bytes]:
        """
        Cifra el texto plano y genera un nonce aleatorio.

        Args:
            plaintext (bytes): datos a cifrar

        Returns:
            Tuple[nonce, ciphertext]: nonce y texto cifrado
        """
        nonce = get_random_bytes(self.NONCE_SIZE)
        cipher = ChaCha20.new(key=self.key, nonce=nonce)
        ciphertext = cipher.encrypt(plaintext)
        return nonce, ciphertext

    def decrypt(self, nonce: bytes, ciphertext: bytes) -> bytes:
        """
        Descifra el texto cifrado usando nonce y clave.

        Args:
            nonce (bytes): nonce usado en el cifrado
            ciphertext (bytes): datos cifrados

        Returns:
            bytes: texto plano descifrado
        """
        if not isinstance(nonce, bytes) or len(nonce) != self.NONCE_SIZE:
            raise ValueError(f"Nonce debe ser de {self.NONCE_SIZE} bytes")
        cipher = ChaCha20.new(key=self.key, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext
