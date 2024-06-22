from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
from dotenv import load_dotenv
import os

load_dotenv()

def generate_dsa_keys():
    private_key = dsa.generate_private_key(key_size=1024)
    public_key = private_key.public_key()
    private_pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo
    )
    return public_pem.decode(), private_pem.decode()

def save_dsa_keys_to_env(nama_pemilih, dsa_public_key, dsa_private_key):
    env_var_public_key = f'PEMILIH_{nama_pemilih}_DSA_PUBLIC_KEY'
    env_var_private_key = f'PEMILIH_{nama_pemilih}_DSA_PRIVATE_KEY'
    os.environ[env_var_public_key] = dsa_public_key
    os.environ[env_var_private_key] = dsa_private_key

def get_dsa_keys_from_env(nama_pemilih):
    env_var_public_key = f'PEMILIH_{nama_pemilih}_DSA_PUBLIC_KEY'
    env_var_private_key = f'PEMILIH_{nama_pemilih}_DSA_PRIVATE_KEY'
    public_key = os.getenv(env_var_public_key)
    private_key = os.getenv(env_var_private_key)
    return public_key, private_key

def sign_dsa(private_key_pem, data):
    private_key = dsa.load_pem_private_key(private_key_pem.encode(), password=None)
    signature = private_key.sign(data.encode(), hashes.SHA256())
    return signature

def verify_dsa(public_key_pem, data, signature):
    public_key = dsa.load_pem_public_key(public_key_pem.encode())
    try:
        public_key.verify(signature, data.encode(), hashes.SHA256())
        return True
    except Exception as e:
        return False
