from typing import Tuple, List
from mesh_cipher.utils import vigenere_matrix


class PlayfairExtended:
    def __init__(self, subkeys: List[bytes]):
        """
        Inicializa el cifrado Playfair extendido con las subclaves.

        Args:
            subkeys (List[bytes]): Lista de subclaves para generar la matriz de sustitución.
        """
        self.subkeys = subkeys
        self.matrix = self._generate_matrix()
        self.char_pos = self._create_char_pos_map()

    def _generate_matrix(self) -> List[List[int]]:
        """
        Genera la matriz 256x256 de sustitución para el cifrado.

        Usa la matriz base Vigenère y aplica una permutación Fisher-Yates
        por fila usando la primera subclave como semilla para modificarla.

        Returns:
            List[List[int]]: Matriz 256x256 con valores permutados para cifrado.
        """
        base = vigenere_matrix()
        key = list(self.subkeys[15]) if self.subkeys else [0]

        matrix = []
        for i, row in enumerate(base):
            new_row = row[:]
            for j in range(len(new_row) - 1, 0, -1):
                k = key[(i + j) % len(key)] % (j + 1)
                new_row[j], new_row[k] = new_row[k], new_row[j]
            matrix.append(new_row)
        return matrix

    def _create_char_pos_map(self) -> dict:
        """
        Crea un diccionario que mapea cada valor a todas sus posiciones en la matriz.

        Returns:
            dict: Mapeo valor -> lista de posiciones (fila, columna).
        """
        char_pos = {}
        for i, row in enumerate(self.matrix):
            for j, val in enumerate(row):
                if val not in char_pos:
                    char_pos[val] = []
                char_pos[val].append((i, j))
        return char_pos

    def _find_position(self, val: int) -> Tuple[int, int]:
        """
        Obtiene la primera posición (fila, columna) donde aparece un valor en la matriz.

        Args:
            val (int): Valor a buscar.

        Returns:
            Tuple[int, int]: Primera posición encontrada (fila, columna).
        """
        return self.char_pos[val][0]

    def encrypt_digraph(self, a: int, b: int) -> Tuple[int, int]:
        """
        Cifra un dígrafo (par de valores) aplicando reglas Playfair extendidas.

        Args:
            a (int): Primer valor del dígrafo.
            b (int): Segundo valor del dígrafo.

        Returns:
            Tuple[int, int]: Dígrafo cifrado.
        """
        row_a, col_a = self._find_position(a)
        row_b, col_b = self._find_position(b)
        if row_a == row_b:
            return self.matrix[row_a][(col_a + 1) % 256], self.matrix[row_b][(col_b + 1) % 256]
        elif col_a == col_b:
            return self.matrix[(row_a + 1) % 256][col_a], self.matrix[(row_b + 1) % 256][col_b]
        else:
            return self.matrix[row_a][col_b], self.matrix[row_b][col_a]

    def decrypt_digraph(self, a: int, b: int) -> Tuple[int, int]:
        """
        Descifra un dígrafo cifrado aplicando reglas inversas al cifrado.

        Args:
            a (int): Primer valor cifrado.
            b (int): Segundo valor cifrado.

        Returns:
            Tuple[int, int]: Dígrafo descifrado.
        """
        row_a, col_a = self._find_position(a)
        row_b, col_b = self._find_position(b)
        if row_a == row_b:
            return self.matrix[row_a][(col_a - 1) % 256], self.matrix[row_b][(col_b - 1) % 256]
        elif col_a == col_b:
            return self.matrix[(row_a - 1) % 256][col_a], self.matrix[(row_b - 1) % 256][col_b]
        else:
            return self.matrix[row_a][col_b], self.matrix[row_b][col_a]

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Cifra un texto plano (bytes) usando el cifrado Playfair extendido.

        Si la longitud del texto es impar, se rellena con b'\x00'.

        Args:
            plaintext (bytes): Texto plano a cifrar.

        Returns:
            bytes: Texto cifrado.
        """
        if len(plaintext) % 2 != 0:
            plaintext += b'\x00'
        ciphertext = bytearray()
        for i in range(0, len(plaintext), 2):
            a, b = plaintext[i], plaintext[i + 1]
            enc_a, enc_b = self.encrypt_digraph(a, b)
            ciphertext.extend([enc_a, enc_b])
        return bytes(ciphertext)

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Descifra un texto cifrado (bytes) usando el cifrado Playfair extendido.

        Args:
            ciphertext (bytes): Texto cifrado a descifrar.

        Returns:
            bytes: Texto descifrado.
        """
        if len(ciphertext) % 2 != 0:
            raise ValueError("Ciphertext length must be even")
        plaintext = bytearray()
        for i in range(0, len(ciphertext), 2):
            a, b = ciphertext[i], ciphertext[i + 1]
            dec_a, dec_b = self.decrypt_digraph(a, b)
            plaintext.extend([dec_a, dec_b])
        return bytes(plaintext)
