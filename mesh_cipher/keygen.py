from mesh_cipher.utils import sha3_256, xor_bytes, split_bytes, get_p_array


class KeyGen:
    def __init__(self, password: str):
        """
        Inicializa con contraseña en texto plano.
        """
        self.password = password.encode('utf-8')
        self.master_key = None  # hash SHA3-256 (32 bytes)
        self.subkeys = []       # lista de 16 subclaves (64 bits cada una)
        self.P = get_p_array()  # P-array de 256 bytes inicializado con Pi

    def generate_master_key(self):
        """Genera clave maestra SHA3-256 a partir de la contraseña."""
        self.master_key = sha3_256(self.password)
        return self.master_key

    def feistel_round(self, left: bytes, right: bytes, subkey: bytes) -> tuple[bytes, bytes]:
        """
        Una ronda simplificada Feistel.
        left, right: 64 bits (8 bytes)
        subkey: 64 bits (8 bytes)
        - XOR left con subkey
        - Sustitución (simulada con P-array lookup)
        - Nuevo left = right XOR resultado sustitución
        - Nuevo right = left antiguo
        """
        # XOR left con subkey
        xor_result = xor_bytes(left, subkey)

        # Sustitución byte a byte usando P-array (mod 256)
        substituted = bytes(self.P[b % 256] for b in xor_result)

        # Nuevo left es right XOR substituted
        new_left = xor_bytes(right, substituted)
        new_right = left
        return new_left, new_right

    def generate_subkeys(self):
        """
        Genera 16 subclaves de 64 bits usando esquema Feistel en dos bloques de 128 bits.
        8 rondas por bloque => 16 subclaves en total.
        """
        if self.master_key is None:
            self.generate_master_key()

        blocks = split_bytes(self.master_key, 2)  # dos bloques de 16 bytes (128 bits)
        subkeys = []

        for block in blocks:
            left, right = split_bytes(block, 2)  # cada uno 8 bytes (64 bits)

            # 8 rondas Feistel
            for round_i in range(8):
                # En este ejemplo, la subclave de ronda es parte del P-array desplazado cíclicamente
                p_offset = (round_i * 8) % len(self.P)
                subkey_bytes = bytes(self.P[p_offset:p_offset + 8])

                left, right = self.feistel_round(left, right, subkey_bytes)
                # Guardamos la subclave generada en cada ronda (resultado left)
                subkeys.append(left)

        self.subkeys = subkeys
        return self.subkeys


def main():
    # Ejemplo rápido de uso:
    kg = KeyGen("MiContraseñaSegura123")
    master = kg.generate_master_key()
    print(f"Master key (SHA3-256): {master.hex()}")
    subs = kg.generate_subkeys()
    print(f"Subclaves (16 de 64 bits):")
    for i, sk in enumerate(subs):
        print(f"Subclave {i+1}: {sk.hex()}")


if __name__ == "__main__":
    main()
