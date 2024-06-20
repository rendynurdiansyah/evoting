from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return public_key.decode(), private_key.decode()

# Fungsi untuk memuat kunci privat dari pemilih
def load_private_key(pemilih):
    private_key_data = pemilih.private_key  # Asumsikan private_key disimpan dalam field private_key
    private_key = RSA.import_key(private_key_data)
    return private_key

# Fungsi untuk mengenkripsi data menggunakan kunci privat
def encrypt_with_private_key(private_key, data):
    cipher = PKCS1_OAEP.new(private_key)
    encrypted_data = cipher.encrypt(data.encode())
    encoded_encrypted_data = base64.b64encode(encrypted_data).decode()  # Encode hasil enkripsi menjadi string
    return encoded_encrypted_data

# Fungsi untuk mendekripsi data menggunakan kunci privat
def decrypt_with_private_key(private_key, encrypted_data):
    cipher = PKCS1_OAEP.new(private_key)
    decoded_encrypted_data = base64.b64decode(encrypted_data)
    decrypted_data = cipher.decrypt(decoded_encrypted_data).decode()  # Decode hasil dekripsi menjadi string
    return decrypted_data