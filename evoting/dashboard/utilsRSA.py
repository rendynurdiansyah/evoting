from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import logging

logger = logging.getLogger(__name__)

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return public_key.decode(), private_key.decode()

def encrypt_with_public_key(public_key_str, data):
    logger.debug(f"Encrypting data: {data}")
    public_key = RSA.import_key(public_key_str)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher.encrypt(data.encode())
    encrypted_b64 = base64.b64encode(encrypted_data).decode()
    logger.debug(f"Encrypted data (base64): {encrypted_b64}")
    return encrypted_b64

def decrypt_with_private_key(private_key_str, encrypted_data):
    logger.debug(f"Decrypting data (base64): {encrypted_data}")
    private_key = RSA.import_key(private_key_str)
    cipher = PKCS1_OAEP.new(private_key)
    decoded_encrypted_data = base64.b64decode(encrypted_data)
    decrypted_data = cipher.decrypt(decoded_encrypted_data).decode()
    logger.debug(f"Decrypted data: {decrypted_data}")
    return decrypted_data

def load_public_key(pemilih):
    return pemilih.public_key

def load_private_key(pemilih):
    return pemilih.private_key
