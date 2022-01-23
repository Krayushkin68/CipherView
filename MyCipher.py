import base64
import hashlib
import os

from cryptography import fernet
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes


class MyCipher:
    def __init__(self, password):
        self.key = hashlib.sha3_256(password.encode()).digest()
        self.cipher = fernet.Fernet(key=base64.urlsafe_b64encode(self.key))

    def encrypt_str(self, message):
        return self.cipher.encrypt(message.encode())

    def decrypt_str(self, crypt_msg):
        return self.cipher.decrypt(crypt_msg)

    def encrypt_file_fern(self, path):
        with open(path + '.crypt', 'wb') as crypt_file, open(path, 'rb') as plain_file:
            while True:
                block = plain_file.read(2048)
                if not block:
                    break
                crypta = self.cipher.encrypt(block)
                crypt_file.write(crypta)

    def decrypt_file_fern(self, path):
        try:
            with open(path[:-6], 'wb') as decrypt_file, open(path, 'rb') as crypt_file:
                while True:
                    block = crypt_file.read(2828)
                    if not block:
                        break
                    decrypt_file.write(self.cipher.decrypt(block))
        except fernet.InvalidToken:
            print('Ошибка расшифрования, неверный ключ!')

    def encrypt_file_aes(self, path_real, path_encr):
        iv = os.urandom(16)
        with open(path_encr, 'wb') as crypt_file, open(path_real, 'rb') as plain_file:
            crypt_file.write(iv)
            while True:
                block = plain_file.read(1048576)
                if not block:
                    break
                cipher_aes = Cipher(algorithms.AES(self.key), modes.CBC(iv)).encryptor()
                pad = padding.PKCS7(algorithms.AES.block_size).padder()
                padded_data = pad.update(block) + pad.finalize()
                cipher_text = cipher_aes.update(padded_data) + cipher_aes.finalize()
                crypt_file.write(cipher_text)
        os.remove(path_real)
        return

    def decrypt_file_aes(self, path_encr, path_real):
        with open(path_real, 'wb') as decrypt_file, open(path_encr, 'rb') as crypt_file:
            iv = crypt_file.read(16)
            while True:
                block = crypt_file.read(1048592)
                if not block:
                    break
                decryptor = Cipher(algorithms.AES(self.key), modes.CBC(iv)).decryptor()
                unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
                plaintext_padded = decryptor.update(block)
                try:
                    plaintext_padded += decryptor.finalize()
                except Exception:
                    print('Ошибка расшифрования, неверный ключ!')
                    return 'error'
                unpadded = unpadder.update(plaintext_padded)
                try:
                    unpadded += unpadder.finalize()
                except Exception:
                    print('Ошибка снятия вставки!')
                    return 'error'
                decrypt_file.write(unpadded)
        os.remove(path_encr)
        return

    def hash_file(self, path):
        with open(path, 'rb') as f:
            h = hashlib.sha3_256(f.read()).hexdigest()
        return h
