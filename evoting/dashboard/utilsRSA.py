from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import logging

logger = logging.getLogger(__name__)

def generate_rsa_keys(pemilih_id):
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Save private key to file
    private_key_path = f'static/keys/private_key_rsa_{pemilih_id}.pem'
    with open(private_key_path, 'wb') as f:
        f.write(private_key)

    # Save public key to file
    public_key_path = f'static/keys/public_key_rsa_{pemilih_id}.pem'
    with open(public_key_path, 'wb') as f:
        f.write(public_key)

def load_rsa_private_key(pemilih_id):
    private_key_path = f'static/keys/private_key_rsa_{pemilih_id}.pem'
    with open(private_key_path, 'rb') as f:
        private_key = RSA.import_key(f.read())
    return private_key

def load_rsa_public_key(pemilih_id):
    public_key_path = f'static/keys/public_key_rsa_{pemilih_id}.pem'
    with open(public_key_path, 'rb') as f:
        public_key = RSA.import_key(f.read())
    return public_key

def encrypt_with_public_key(public_key_str, data):
    logger.debug(f"Encrypting data: {data}")
    public_key = RSA.import_key(public_key_str)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher.encrypt(data.encode())
    encrypted_b64 = base64.b64encode(encrypted_data).decode()
    logger.debug(f"Encrypted data (base64): {encrypted_b64}")
    return encrypted_b64

def decrypt_with_private_key(private_key, encrypted_data_b64):
    try:
        encrypted_data = base64.b64decode(encrypted_data_b64)
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_data = cipher.decrypt(encrypted_data)
        decrypted_data_str = decrypted_data.decode()
        logger.debug(f"Decrypted data: {decrypted_data_str}")
        return decrypted_data_str
    except Exception as e:
        logger.error(f"Error decrypting data: {str(e)}")
        raise


