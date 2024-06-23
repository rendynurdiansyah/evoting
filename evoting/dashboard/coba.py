from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generate_keys():
    """
    Generates RSA public and private keys of 128 bits.
    Returns:
        public_key (str): RSA public key in PEM format.
        private_key (str): RSA private key in PEM format.
    """
    key = RSA.generate(128)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return public_key.decode(), private_key.decode()

def encrypt_with_public_key(public_key_str, data):
    """
    Encrypts data using RSA public key.
    Args:
        public_key_str (str): RSA public key in PEM format.
        data (str): Data to encrypt.
    Returns:
        str: Base64-encoded encrypted data.
    """
    public_key = RSA.import_key(public_key_str)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher.encrypt(data.encode())
    encoded_encrypted_data = base64.b64encode(encrypted_data).decode()
    return encoded_encrypted_data

def decrypt_with_private_key(private_key_str, encrypted_data):
    """
    Decrypts data using RSA private key.
    Args:
        private_key_str (str): RSA private key in PEM format.
        encrypted_data (str): Base64-encoded encrypted data.
    Returns:
        str: Decrypted data.
    """
    private_key = RSA.import_key(private_key_str)
    cipher = PKCS1_OAEP.new(private_key)
    decoded_encrypted_data = base64.b64decode(encrypted_data)
    decrypted_data = cipher.decrypt(decoded_encrypted_data).decode()
    return decrypted_data

# Contoh penggunaan
if __name__ == "__main__":
    # Generate keys
    public_key =""
    private_key = ""
    print("Public Key:")
    print(public_key)
    print("\nPrivate Key:")
    print(private_key)

    # Data to encrypt
    data_to_encrypt = "Hello, world!"

    # Encrypt with public key
    encrypted_data = encrypt_with_public_key(public_key, data_to_encrypt)
    print("\nEncrypted Data:")
    print(encrypted_data)

    # Decrypt with private key
    decrypted_data = decrypt_with_private_key(private_key, encrypted_data)
    print("\nDecrypted Data:")
    print(decrypted_data)
