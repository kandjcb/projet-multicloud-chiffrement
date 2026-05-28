from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os, base64, json

# ============================================
# SIMULATION CLOUD KMS - Projet Multicloud
# ============================================

class CloudKMS:
    """Simule un service Cloud KMS (AWS KMS / Azure Key Vault)"""
    
    def __init__(self):
        self.keys = {}
    
    def create_key(self, key_id):
        """Créer une clé KMS (AES-256)"""
        self.keys[key_id] = os.urandom(32)  # 256 bits
        print(f"✅ Clé créée : {key_id}")
        return key_id
    
    def encrypt(self, key_id, plaintext):
        """Chiffrer avec la clé KMS"""
        key = self.keys[key_id]
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        result = base64.b64encode(iv + ciphertext).decode()
        print(f"🔒 Fichier chiffré avec la clé [{key_id}]")
        return result
    
    def decrypt(self, key_id, ciphertext_b64):
        """Déchiffrer avec la clé KMS"""
        key = self.keys[key_id]
        data = base64.b64decode(ciphertext_b64)
        iv, ciphertext = data[:16], data[16:]
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        print(f"🔓 Fichier déchiffré avec la clé [{key_id}]")
        return plaintext.decode()

# ============================================
# DEMO
# ============================================
print("\n=== Cloud KMS Demo - Projet Multicloud ===\n")

kms = CloudKMS()

# 1. Créer une clé
kms.create_key("projet-multicloud-key")

# 2. Chiffrer un fichier
message = "Ceci est un fichier secret a proteger dans le cloud"
print(f"\n📄 Fichier original : {message}")
chiffre = kms.encrypt("projet-multicloud-key", message)
print(f"🔒 Chiffré : {chiffre[:50]}...")

# 3. Sauvegarder
with open("fichier.enc", "w") as f:
    json.dump({"key_id": "projet-multicloud-key", "data": chiffre}, f)
print("\n💾 Fichier chiffré sauvegardé : fichier.enc")

# 4. Déchiffrer
with open("fichier.enc", "r") as f:
    saved = json.load(f)
original = kms.decrypt(saved["key_id"], saved["data"])
print(f"📄 Fichier déchiffré : {original}")

print("\n✅ Demo KMS terminée avec succès !")
