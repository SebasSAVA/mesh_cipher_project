from mesh_cipher.keygen import KeyGen
from mesh_cipher.substitution import PlayfairExtended
from mesh_cipher.padding import CustomPadding
from mesh_cipher.stream_dispersion import ChaCha20Cipher


def encrypt(plaintext: str, password: str) -> str:
    """
    Flujo completo de cifrado M.E.S.H.

    Args:
        plaintext (str): Texto plano a cifrar.
        password (str): Clave secreta.

    Returns:
        str: Texto cifrado en formato hexadecimal (nonce + ciphertext).
    """
    # 1. Generar subclaves
    kg = KeyGen(password)
    subkeys = kg.generate_subkeys()

    # 2. Padding personalizado
    padder = CustomPadding(subkeys)
    padded = padder.pad(plaintext.encode('utf-8'))

    # 3. Sustitución Playfair extendido
    playfair = PlayfairExtended(subkeys)
    substituted = playfair.encrypt(padded)

    # 4. ChaCha20
    chacha_key = (subkeys[0] * 4)[:32]
    chacha = ChaCha20Cipher(chacha_key)
    nonce, ciphertext = chacha.encrypt(substituted)

    # Concatenar nonce y ciphertext en hex
    return (nonce + ciphertext).hex()


def decrypt(cipher_hex: str, password: str) -> str:
    """
    Flujo completo de descifrado M.E.S.H.

    Args:
        cipher_hex (str): Texto cifrado hexadecimal (nonce + ciphertext).
        password (str): Clave secreta.

    Returns:
        str: Texto plano descifrado.
    """
    data = bytes.fromhex(cipher_hex)
    if len(data) < 12:
        raise ValueError("Datos cifrados inválidos o incompletos")

    nonce = data[:12]
    ciphertext = data[12:]

    kg = KeyGen(password)
    subkeys = kg.generate_subkeys()

    chacha_key = (subkeys[0] * 4)[:32]
    chacha = ChaCha20Cipher(chacha_key)

    substituted = chacha.decrypt(nonce, ciphertext)

    playfair = PlayfairExtended(subkeys)
    padded = playfair.decrypt(substituted)

    padder = CustomPadding(subkeys)
    unpadded = padder.unpad(padded)

    if unpadded is None:
        raise ValueError("Padding inválido o corrupto.")

    return unpadded.decode('utf-8', errors='replace')
