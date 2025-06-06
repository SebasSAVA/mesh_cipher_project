import time
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from Crypto.Cipher import AES, DES3, Blowfish, CAST, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

from mesh_cipher.core import encrypt as mesh_encrypt
from mesh_cipher.core import decrypt as mesh_decrypt

sns.set(style="whitegrid")

def generar_datos_prueba(tamano_bytes=5000):  # Tamaño mediano para tiempos notables
    return os.urandom(tamano_bytes)

# AES-CBC
def aes_cbc_encrypt(key, data):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ct_bytes

def aes_cbc_decrypt(key, data):
    iv = data[:16]
    ct = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt

# 3DES CBC
def des3_encrypt(key, data):
    cipher = DES3.new(key, DES3.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, DES3.block_size))
    return cipher.iv + ct_bytes

def des3_decrypt(key, data):
    iv = data[:8]
    ct = data[8:]
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), DES3.block_size)
    return pt

# Blowfish CBC
def blowfish_encrypt(key, data):
    cipher = Blowfish.new(key, Blowfish.MODE_CBC)
    plen = Blowfish.block_size - len(data) % Blowfish.block_size
    data += bytes([plen]) * plen
    return cipher.iv + cipher.encrypt(data)

def blowfish_decrypt(key, data):
    iv = data[:8]
    ct = data[8:]
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    pt_padded = cipher.decrypt(ct)
    plen = pt_padded[-1]
    return pt_padded[:-plen]

# CAST5 CBC
def cast5_encrypt(key, data):
    cipher = CAST.new(key, CAST.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, CAST.block_size))
    return cipher.iv + ct_bytes

def cast5_decrypt(key, data):
    iv = data[:8]
    ct = data[8:]
    cipher = CAST.new(key, CAST.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), CAST.block_size)
    return pt

# RSA (usa bloques para evitar error tamaño)
def rsa_encrypt(private_key, data):
    public_key = private_key.publickey()
    cipher = PKCS1_OAEP.new(public_key)
    chunk_size = 190
    encrypted = b""
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        encrypted += cipher.encrypt(chunk)
    return encrypted

def rsa_decrypt(private_key, data):
    cipher = PKCS1_OAEP.new(private_key)
    chunk_size = 256
    decrypted = b""
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        decrypted += cipher.decrypt(chunk)
    return decrypted

# M.E.S.H.
def mesh_encrypt_wrapper(key, data):
    texto = data.decode('utf-8', errors='ignore')
    return mesh_encrypt(texto, key)

def mesh_decrypt_wrapper(key, data):
    texto_desc = mesh_decrypt(data, key)
    return texto_desc.encode('utf-8', errors='ignore')

def medir_tiempos(alg, enc, dec, key, data, repeticiones=3):
    # Reduce repeticiones para menos tiempo total
    start_enc = time.perf_counter()
    for _ in range(repeticiones):
        ct = enc(key, data)
    tiempo_enc = (time.perf_counter() - start_enc) * 1000 / repeticiones

    start_dec = time.perf_counter()
    for _ in range(repeticiones):
        pt = dec(key, ct)
    tiempo_dec = (time.perf_counter() - start_dec) * 1000 / repeticiones

    integridad = pt == data
    return tiempo_enc, tiempo_dec, integridad

def generar_claves():
    aes_key = get_random_bytes(32)        # AES-256 CBC
    des3_key = DES3.adjust_key_parity(get_random_bytes(24))
    blowfish_key = get_random_bytes(16)
    cast5_key = get_random_bytes(16)
    rsa_key = RSA.generate(2048)
    mesh_key = "ClaveDePruebaSegura123!"

    return {
        "AES-CBC": aes_key,
        "3DES": des3_key,
        "Blowfish": blowfish_key,
        "CAST5": cast5_key,
        "RSA": rsa_key,
        "M.E.S.H.": mesh_key
    }

def ejecutar_pruebas(n=20):
    data = generar_datos_prueba()
    claves = generar_claves()
    resultados = []

    for _ in range(n):
        t_enc, t_dec, ok = medir_tiempos("AES-CBC", aes_cbc_encrypt, aes_cbc_decrypt, claves["AES-CBC"], data)
        resultados.append({"Algoritmo": "AES-CBC", "Tiempo Cifrado (ms)": t_enc, "Tiempo Descifrado (ms)": t_dec, "Integridad": ok})

        t_enc, t_dec, ok = medir_tiempos("3DES", des3_encrypt, des3_decrypt, claves["3DES"], data)
        resultados.append({"Algoritmo": "3DES", "Tiempo Cifrado (ms)": t_enc, "Tiempo Descifrado (ms)": t_dec, "Integridad": ok})

        t_enc, t_dec, ok = medir_tiempos("Blowfish", blowfish_encrypt, blowfish_decrypt, claves["Blowfish"], data)
        resultados.append({"Algoritmo": "Blowfish", "Tiempo Cifrado (ms)": t_enc, "Tiempo Descifrado (ms)": t_dec, "Integridad": ok})

        t_enc, t_dec, ok = medir_tiempos("CAST5", cast5_encrypt, cast5_decrypt, claves["CAST5"], data)
        resultados.append({"Algoritmo": "CAST5", "Tiempo Cifrado (ms)": t_enc, "Tiempo Descifrado (ms)": t_dec, "Integridad": ok})

        t_enc, t_dec, ok = medir_tiempos("RSA", rsa_encrypt, rsa_decrypt, claves["RSA"], data)
        resultados.append({"Algoritmo": "RSA", "Tiempo Cifrado (ms)": t_enc, "Tiempo Descifrado (ms)": t_dec, "Integridad": ok})

        t_enc, t_dec, ok = medir_tiempos("M.E.S.H.", mesh_encrypt_wrapper, mesh_decrypt_wrapper, claves["M.E.S.H."], data)
        resultados.append({"Algoritmo": "M.E.S.H.", "Tiempo Cifrado (ms)": t_enc, "Tiempo Descifrado (ms)": t_dec, "Integridad": ok})

    return pd.DataFrame(resultados)

def graficar_barras(df):
    resumen = df.groupby("Algoritmo")[["Tiempo Cifrado (ms)", "Tiempo Descifrado (ms)"]].mean().reset_index()

    plt.figure(figsize=(14,8))
    width = 0.35
    x = range(len(resumen))

    plt.bar([p - width/2 for p in x], resumen["Tiempo Cifrado (ms)"], width, label="Cifrado", color='tab:blue')
    plt.bar([p + width/2 for p in x], resumen["Tiempo Descifrado (ms)"], width, label="Descifrado", color='tab:orange')

    plt.xticks(x, resumen["Algoritmo"])
    plt.ylabel("Tiempo promedio (ms)")
    plt.yscale('log')  # <-- Aquí cambio a escala logarítmica
    plt.title("Comparación de Tiempos de Cifrado y Descifrado (escala logarítmica)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("comparacion_rendimiento_log.png")
    plt.show()


if __name__ == "__main__":
    print("Ejecutando pruebas... esto puede tardar")

    df = ejecutar_pruebas(n=10)  # 20 repeticiones para acelerar
    print(df.groupby("Algoritmo")[["Tiempo Cifrado (ms)", "Tiempo Descifrado (ms)"]].agg(['mean', 'std', 'min', 'max']).round(2))

    graficar_barras(df)
    print("Análisis completo. Gráfico guardado como 'comparacion_rendimiento.png'")
