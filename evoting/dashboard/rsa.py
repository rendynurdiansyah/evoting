from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def generate_rsa_keys(pemilih_id):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Simpan private key ke file
    private_key_path = f'keys/rsa_private_key_{pemilih_id}.pem'
    with open(private_key_path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Simpan public key ke file
    public_key_path = f'keys/rsa_public_key_{pemilih_id}.pem'
    with open(public_key_path, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def load_rsa_private_key(pemilih_id):
    private_key_path = f'keys/rsa_private_key_{pemilih_id}.pem'
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )
    return private_key

def load_rsa_public_key(pemilih_id):
    public_key_path = f'keys/rsa_public_key_{pemilih_id}.pem'
    with open(public_key_path, 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read()
        )
    return public_key

def encrypt_with_public_key(public_key, plaintext):
    ciphertext = public_key.encrypt(
        plaintext.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(ciphertext).decode('utf-8')
