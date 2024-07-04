from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import base64

def generate_dsa_keys():
    private_key = dsa.generate_private_key(key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem.decode('utf-8'), public_pem.decode('utf-8')

def load_dsa_private_key(private_key_bytes):
    private_key = serialization.load_pem_private_key(
        private_key_bytes.encode('utf-8'),
        password=None
    )
    return private_key

def load_dsa_public_key(public_key_bytes):
    public_key = serialization.load_pem_public_key(
        public_key_bytes.encode('utf-8')
    )
    return public_key
