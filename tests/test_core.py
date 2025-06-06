import unittest
from mesh_cipher.core import encrypt, decrypt

class TestCoreEncryption(unittest.TestCase):

    def test_encrypt_decrypt(self):
        password = "ClaveMuySegura123"
        plaintext = "Este es un mensaje de prueba para el algoritmo M.E.S.H."

        cipher = encrypt(plaintext, password)
        self.assertIsInstance(cipher, str)
        self.assertNotEqual(cipher, plaintext)

        decrypted = decrypt(cipher, password)
        self.assertEqual(decrypted, plaintext)

    def test_decrypt_with_wrong_password(self):
        password = "ClaveMuySegura123"
        wrong_password = "ClaveIncorrecta"
        plaintext = "Mensaje secreto"

        cipher = encrypt(plaintext, password)
        with self.assertRaises(Exception):
            decrypt(cipher, wrong_password)

    def test_encrypt_empty_string(self):
        password = "ClaveMuySegura123"
        plaintext = ""

        cipher = encrypt(plaintext, password)
        self.assertIsInstance(cipher, str)

        decrypted = decrypt(cipher, password)
        self.assertEqual(decrypted, plaintext)

if __name__ == "__main__":
    unittest.main()
