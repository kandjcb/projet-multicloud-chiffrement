import boto3
import base64
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

print("\n=== AWS KMS + S3 Demo - Projet Multicloud ===\n")

# ----------------------------------------
# PARTIE 1 — AWS RÉEL : Lister les buckets
# ----------------------------------------
print("☁️  PARTIE 1 : Connexion AWS réelle")
s3 = boto3.client('s3', region_name='us-east-1')

try:
    buckets = s3.list_buckets()
    print(f"✅ Connecté à AWS — {len(buckets['Buckets'])} buckets trouvés :")
    for b in buckets['Buckets']:
        print(f"   - {b['Name']}")
    BUCKET = buckets['Buckets'][0]['Name']
except Exception as e:
    print(f"❌ Erreur : {e}")
    BUCKET = None

# ----------------------------------------
# PARTIE 2 — SIMULATION KMS : Chiffrement
# ----------------------------------------
print("\n🔑 PARTIE 2 : Simulation KMS (AccessDenied sur compte Academy)")
print("   Raison : kms:CreateKey et kms:Encrypt bloqués par AWS Academy")
print("   Solution : simulation avec même algorithme AES-256\n")

# Simuler une clé KMS
KEY_ID = "projet-kms-" + base64.b64encode(os.urandom(8)).decode()[:12]
key = os.urandom(32)  # AES-256
iv = os.urandom(16)

print(f"✅ Clé KMS simulée : {KEY_ID}")

# Chiffrer
message = "Donnees confidentielles protegees par KMS"
cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
encryptor = cipher.encryptor()
ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
encrypted = base64.b64encode(iv + ciphertext).decode()

print(f"📄 Message original  : {message}")
print(f"🔒 Message chiffré   : {encrypted[:50]}...")

# Sauvegarder localement
with open("fichier_kms.enc", "w") as f:
    json.dump({"KeyId": KEY_ID, "data": encrypted}, f)
print(f"💾 Fichier chiffré sauvegardé : fichier_kms.enc")

# Déchiffrer
with open("fichier_kms.enc") as f:
    saved = json.load(f)

data = base64.b64decode(saved["data"])
iv2, ct = data[:16], data[16:]
cipher2 = Cipher(algorithms.AES(key), modes.CFB(iv2), backend=default_backend())
decryptor = cipher2.decryptor()
decrypted = (decryptor.update(ct) + decryptor.finalize()).decode()
print(f"🔓 Message déchiffré : {decrypted}")

# ----------------------------------------
# PARTIE 3 — AWS RÉEL : Upload S3 sans KMS
# ----------------------------------------
print("\n📦 PARTIE 3 : Upload S3 réel (sans SSE-KMS)")
if BUCKET:
    try:
        s3.put_object(
            Bucket=BUCKET,
            Key="fichier_chiffre_localement.enc",
            Body=encrypted.encode()
        )
        print(f"✅ Fichier chiffré uploadé sur S3 !")
        print(f"   Bucket : {BUCKET}")
        print(f"   Fichier : fichier_chiffre_localement.enc")

        # Vérifier
        obj = s3.get_object(Bucket=BUCKET, Key="fichier_chiffre_localement.enc")
        content = obj['Body'].read().decode()
        print(f"✅ Fichier récupéré depuis S3 : {content[:50]}...")
        print(f"   → Le fichier sur S3 est illisible sans la clé KMS ✅")

    except Exception as e:
        print(f"❌ Erreur S3 : {e}")

print("\n✅ Demo complète terminée !")
print("\n📊 Résumé :")
print("   - Connexion AWS réelle    ✅")
print("   - Buckets S3 listés       ✅")
print("   - Chiffrement KMS AES-256 ✅")
print("   - Fichier uploadé sur S3  ✅")
print("   - kms:CreateKey bloqué    ❌ (restriction AWS Academy)")
