from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return public_key.decode(), private_key.decode()

def load_private_key(pemilih):
    private_key_data = pemilih.private_key
    private_key = RSA.import_key(private_key_data)
    return private_key

def load_public_key(pemilih):
    public_key_data = pemilih.public_key
    public_key = RSA.import_key(public_key_data)
    return public_key

def encrypt_with_private_key(private_key, data):
    cipher = PKCS1_OAEP.new(private_key)
    encrypted_data = cipher.encrypt(data.encode())
    encoded_encrypted_data = base64.b64encode(encrypted_data).decode()
    return encoded_encrypted_data

def decrypt_with_public_key(public_key, encrypted_data):
    cipher = PKCS1_OAEP.new(public_key)
    decoded_encrypted_data = base64.b64decode(encrypted_data)
    decrypted_data = cipher.decrypt(decoded_encrypted_data).decode()
    return decrypted_data
