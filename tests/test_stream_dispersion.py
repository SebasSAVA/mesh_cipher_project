import unittest
from mesh_cipher.stream_dispersion import ChaCha20Cipher
from mesh_cipher.keygen import KeyGen


class TestChaCha20Cipher(unittest.TestCase):

    def setUp(self):
        kg = KeyGen("testpassword")
        subkeys = kg.generate_subkeys()
        # Usamos la primera subclave y expandimos/repetimos a 32 bytes para clave ChaCha20
        key_64 = subkeys[0]  # 8 bytes
        self.key = (key_64 * 4)[:32]  # 32 bytes clave
        self.cipher = ChaCha20Cipher(self.key)

    def test_encrypt_decrypt(self):
        plaintext = b"Mensaje de prueba para ChaCha20 con longitud variable..."
        nonce, ciphertext = self.cipher.encrypt(plaintext)
        self.assertNotEqual(plaintext, ciphertext, "Texto cifrado no debe ser igual al original")
        decrypted = self.cipher.decrypt(nonce, ciphertext)
        self.assertEqual(plaintext, decrypted, "El texto descifrado debe coincidir con el original")

    def test_different_nonces(self):
        plaintext = b"Texto para probar nonces diferentes"
        nonce1, ciphertext1 = self.cipher.encrypt(plaintext)
        nonce2, ciphertext2 = self.cipher.encrypt(plaintext)
        self.assertNotEqual(nonce1, nonce2, "Los nonces deben ser diferentes")
        self.assertNotEqual(ciphertext1, ciphertext2, "Los cifrados deben ser diferentes con nonces distintos")

    def test_nonce_size_validation(self):
        plaintext = b"Test texto"
        nonce, ciphertext = self.cipher.encrypt(plaintext)
        with self.assertRaises(ValueError):
            self.cipher.decrypt(b"shortnonce", ciphertext)  # nonce corto inválido

    def test_key_length_validation(self):
        with self.assertRaises(ValueError):
            ChaCha20Cipher(b"shortkey")  # clave inválida


if __name__ == "__main__":
    unittest.main()
