from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import base64

def generate_dsa_keys(pemilih_id):
    private_key = dsa.generate_private_key(key_size=2048)
    public_key = private_key.public_key()

    # Simpan private key ke file
    private_key_path = f'static/keys/private_key_{pemilih_id}.pem'
    with open(private_key_path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Simpan public key ke file
    public_key_path = f'static/keys/public_key_{pemilih_id}.pem'
    with open(public_key_path, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def load_dsa_private_key(pemilih_id):
    private_key_path = f'static/keys/private_key_{pemilih_id}.pem'
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )
    return private_key

def load_dsa_public_key(pemilih_id):
    public_key_path = f'static/keys/public_key_{pemilih_id}.pem'
    with open(public_key_path, 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read()
        )
    return public_key
