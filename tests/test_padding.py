import unittest
from mesh_cipher.padding import CustomPadding
from mesh_cipher.keygen import KeyGen


class TestCustomPadding(unittest.TestCase):

    def setUp(self):
        kg = KeyGen("testpassword")
        self.subkeys = kg.generate_subkeys()
        self.padder = CustomPadding(self.subkeys)

    def test_pad_length(self):
        for length in range(0, 50):
            data = b"A" * length
            padded = self.padder.pad(data)
            self.assertEqual(len(padded) % 16, 0)
            self.assertTrue(len(padded) >= len(data))

    def test_unpad_valid(self):
        data = b"Example data to pad"
        padded = self.padder.pad(data)
        unpadded = self.padder.unpad(padded)
        self.assertIsNotNone(unpadded)
        self.assertEqual(unpadded, data)

    def test_unpad_invalid(self):
        data = b"Invalid padding data" + b"\x00\x01\x02"
        unpadded = self.padder.unpad(data)
        self.assertIsNone(unpadded)

    def test_round_trip(self):
        for length in range(1, 30):
            data = bytes([x % 256 for x in range(length)])
            padded = self.padder.pad(data)
            unpadded = self.padder.unpad(padded)
            self.assertIsNotNone(unpadded)
            self.assertEqual(unpadded, data)


if __name__ == "__main__":
    unittest.main()
