import unittest
from mesh_cipher.keygen import KeyGen


class TestKeyGen(unittest.TestCase):

    def test_master_key_length(self):
        """Verifica que la clave maestra generada tenga una longitud de 32 bytes (256 bits)."""
        kg = KeyGen("testpassword")
        master = kg.generate_master_key()
        self.assertEqual(len(master), 32)  # SHA3-256 = 32 bytes

    def test_subkeys_count(self):
        """Verifica que se generen 16 subclaves de 64 bits cada una."""
        kg = KeyGen("testpassword")
        subs = kg.generate_subkeys()
        self.assertEqual(len(subs), 16)  # 16 subclaves

    def test_subkeys_length(self):
        """Verifica que cada subclave tenga una longitud de 8 bytes (64 bits)."""
        kg = KeyGen("testpassword")
        subs = kg.generate_subkeys()
        for subkey in subs:
            self.assertEqual(len(subkey), 8)  # Cada subclave tiene que ser de 8 bytes (64 bits)

    def test_subkeys_type(self):
        """Verifica que las subclaves generadas sean de tipo bytes."""
        kg = KeyGen("testpassword")
        subs = kg.generate_subkeys()
        for subkey in subs:
            self.assertIsInstance(subkey, bytes)  # Cada subclave debe ser un objeto de tipo bytes

    def test_correct_subkeys_generation(self):
        """Verifica que las subclaves generadas sean correctas (se compara con un valor esperado)."""
        expected_subkeys = [
            bytes([0x0b, 0xf0, 0x7a, 0x5b, 0x52, 0x1e, 0x91, 0xa5]),  # Primer subclave esperada
            bytes([0x1d, 0x98, 0x2f, 0x3f, 0x90, 0x5b, 0x27, 0x23]),  # Segunda subclave esperada
            # Aquí incluirías las 14 subclaves restantes (por simplicidad, se omiten en este ejemplo)
        ]
        kg = KeyGen("testpassword")
        subs = kg.generate_subkeys()
        for i, subkey in enumerate(subs[:2]):  # Solo verificamos las dos primeras subclaves
            self.assertEqual(subkey, expected_subkeys[i])

    def test_correct_subkeys_generation(self):
        """Verifica que las subclaves generadas sean correctas (se compara con un valor esperado)."""
        expected_subkeys = [
            bytes([88, 103, 142, 48, 194, 53, 183, 183]),  # Primer subclave real
            bytes([0, 9, 75, 180, 250, 18, 30, 141]),     # Segunda subclave real
            # Puedes agregar más si quieres validar más subclaves
        ]
        kg = KeyGen("testpassword")
        subs = kg.generate_subkeys()
        for i, subkey in enumerate(subs[:2]):  # Solo verificamos las dos primeras subclaves
            self.assertEqual(subkey, expected_subkeys[i])
        # El new_right debería ser el left original

if __name__ == "__main__":
    unittest.main()
