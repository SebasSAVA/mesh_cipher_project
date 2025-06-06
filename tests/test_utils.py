import unittest
from mesh_cipher.utils import xor_bytes, split_bytes, get_p_array, vigenere_matrix


class TestUtils(unittest.TestCase):

    def test_xor_bytes(self):
        b1 = bytes([1, 2, 3, 4])
        b2 = bytes([4, 3, 2, 1])
        result = xor_bytes(b1, b2)
        expected = bytes([5, 1, 1, 5])
        self.assertEqual(result, expected)

    def test_split_bytes(self):
        data = bytes([1, 2, 3, 4, 5, 6, 7, 8])
        result = split_bytes(data, 2)
        expected = [bytes([1, 2, 3, 4]), bytes([5, 6, 7, 8])]
        self.assertEqual(result, expected)

    def test_get_p_array(self):
        result = get_p_array()
        self.assertEqual(len(result), 256)  # P-array debe tener 256 elementos
        self.assertEqual(result[0], 3)  # Primer valor debería ser 3 (de Pi)

    def test_vigenere_matrix(self):
        result = vigenere_matrix()
        self.assertEqual(len(result), 256)  # 256 filas
        self.assertEqual(len(result[0]), 256)  # 256 columnas
        self.assertEqual(result[0][0], 0)  # La primera posición debe ser 0
        self.assertEqual(result[255][255], 254)  # Última posición


if __name__ == "__main__":
    unittest.main()
