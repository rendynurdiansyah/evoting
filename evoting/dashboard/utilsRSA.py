from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generate_keys():
    key = RSA.generate(1024)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return public_key.decode(), private_key.decode()

def encrypt_with_private_key(private_key_str, data):
    private_key = RSA.import_key(private_key_str)
    cipher = PKCS1_OAEP.new(private_key)
    encrypted_data = cipher.encrypt(data.encode())
    return base64.b64encode(encrypted_data).decode()

def decrypt_with_public_key(public_key_str, encrypted_data):
    public_key = RSA.import_key(public_key_str)
    cipher = PKCS1_OAEP.new(public_key)
    decoded_encrypted_data = base64.b64decode(encrypted_data)
    decrypted_data = cipher.decrypt(decoded_encrypted_data).decode()
    return decrypted_data

def load_public_key(pemilih):
    return pemilih.public_key

def load_private_key(pemilih):
    return pemilih.private_key
