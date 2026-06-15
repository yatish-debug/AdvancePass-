import os
import json
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

VAULT_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "vault.enc")

def _derive_key(master_password: str, salt: bytes) -> bytes:
    """Derives a 256-bit key from the master password using Scrypt."""
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
    )
    return kdf.derive(master_password.encode())

def init_vault(master_password: str):
    """Initializes an empty vault with the given master password."""
    salt = os.urandom(16)
    key = _derive_key(master_password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    
    empty_vault = json.dumps([]).encode()
    ciphertext = aesgcm.encrypt(nonce, empty_vault, None)
    
    # Store salt + nonce + ciphertext
    os.makedirs(os.path.dirname(VAULT_FILE), exist_ok=True)
    with open(VAULT_FILE, "wb") as f:
        f.write(salt + nonce + ciphertext)

def load_vault(master_password: str) -> list:
    """Loads and decrypts the vault."""
    if not os.path.exists(VAULT_FILE):
        return []
        
    with open(VAULT_FILE, "rb") as f:
        data = f.read()
        
    if len(data) < 28: # 16 (salt) + 12 (nonce)
        raise ValueError("Vault file corrupted.")
        
    salt = data[:16]
    nonce = data[16:28]
    ciphertext = data[28:]
    
    key = _derive_key(master_password, salt)
    aesgcm = AESGCM(key)
    
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return json.loads(plaintext.decode())
    except Exception:
        raise ValueError("Invalid master password or corrupted vault.")

def save_vault(master_password: str, vault_data: list):
    """Encrypts and saves the vault data."""
    salt = os.urandom(16)
    key = _derive_key(master_password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    
    plaintext = json.dumps(vault_data).encode()
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    
    with open(VAULT_FILE, "wb") as f:
        f.write(salt + nonce + ciphertext)

def add_entry(master_password: str, site: str, username: str, password: str):
    """Adds a new entry to the vault."""
    vault = load_vault(master_password)
    vault.append({"site": site, "username": username, "password": password})
    save_vault(master_password, vault)
