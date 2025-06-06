import unittest
from mesh_cipher.substitution import PlayfairExtended
from mesh_cipher.keygen import KeyGen


class TestPlayfairExtended(unittest.TestCase):

    def setUp(self):
        kg = KeyGen("testpassword")
        self.subkeys = kg.generate_subkeys()
        self.playfair = PlayfairExtended(self.subkeys)

    def test_encrypt_decrypt(self):
        plaintext = b"HelloWorld!"  # Bytes arbitrarios (11 bytes, impar)
        ciphertext = self.playfair.encrypt(plaintext)
        self.assertNotEqual(plaintext, ciphertext, "Texto cifrado debe diferir del texto plano")
        
        decrypted = self.playfair.decrypt(ciphertext)
        
        # Quitar padding \x00 al final si existe
        decrypted = decrypted.rstrip(b'\x00')
        
        # Ahora sí validar igualdad
        self.assertEqual(decrypted, plaintext)
        
        # Además validamos que el texto descifrado sea de longitud par (ya sin padding)
        self.assertEqual(len(decrypted) % 2, 1 if len(plaintext) % 2 == 1 else 0)

    def test_digraph_same_row(self):
        row = 10
        col1, col2 = 5, 6
        a = self.playfair.matrix[row][col1]
        b = self.playfair.matrix[row][col2]
        enc_a, enc_b = self.playfair.encrypt_digraph(a, b)
        dec_a, dec_b = self.playfair.decrypt_digraph(enc_a, enc_b)
        # Validamos que descifrar el cifrado regresa los valores originales
        self.assertEqual((a, b), (dec_a, dec_b))

    def test_digraph_same_column(self):
        col = 20
        row1, row2 = 3, 4
        a = self.playfair.matrix[row1][col]
        b = self.playfair.matrix[row2][col]
        enc_a, enc_b = self.playfair.encrypt_digraph(a, b)
        dec_a, dec_b = self.playfair.decrypt_digraph(enc_a, enc_b)
        self.assertEqual((a, b), (dec_a, dec_b))

    def test_digraph_rectangle(self):
        a_row, a_col = 5, 10
        b_row, b_col = 7, 20
        a = self.playfair.matrix[a_row][a_col]
        b = self.playfair.matrix[b_row][b_col]
        enc_a, enc_b = self.playfair.encrypt_digraph(a, b)
        dec_a, dec_b = self.playfair.decrypt_digraph(enc_a, enc_b)
        self.assertEqual((a, b), (dec_a, dec_b))

    def test_decrypt_digraph(self):
        a, b = 50, 100
        enc_a, enc_b = self.playfair.encrypt_digraph(a, b)
        dec_a, dec_b = self.playfair.decrypt_digraph(enc_a, enc_b)
        self.assertEqual((a, b), (dec_a, dec_b))


if __name__ == "__main__":
    unittest.main()
