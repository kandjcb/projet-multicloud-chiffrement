import boto3
import base64
import json

# ============================================
# VRAI AWS KMS - Projet Multicloud
# ============================================

print("\n=== AWS KMS Demo Réelle - Projet Multicloud ===\n")

# Connexion au vrai service AWS KMS
kms = boto3.client('kms', region_name='us-east-1')
s3  = boto3.client('s3',  region_name='us-east-1')

# ----------------------------------------
# Étape 1 — Lister les clés KMS existantes
# ----------------------------------------
print("📋 Étape 1 : Lister les clés KMS disponibles...")
try:
    response = kms.list_keys()
    keys = response['Keys']
    if keys:
        print(f"✅ {len(keys)} clé(s) KMS trouvée(s) :")
        for k in keys:
            print(f"   - Key ID : {k['KeyId']}")
        KEY_ID = keys[0]['KeyId']
    else:
        print("⚠️  Aucune clé KMS disponible dans ce compte")
        KEY_ID = None
except Exception as e:
    print(f"❌ Erreur : {e}")
    KEY_ID = None

# ----------------------------------------
# Étape 2 — Chiffrer avec AWS KMS
# ----------------------------------------
if KEY_ID:
    print(f"\n🔑 Étape 2 : Chiffrement avec la clé KMS...")
    message = "Fichier secret a proteger avec AWS KMS"
    print(f"📄 Message original : {message}")
    
    try:
        response = kms.encrypt(
            KeyId=KEY_ID,
            Plaintext=message.encode()
        )
        ciphertext = base64.b64encode(response['CiphertextBlob']).decode()
        print(f"🔒 Message chiffré : {ciphertext[:60]}...")
        
        # Sauvegarder
        with open("fichier_kms_reel.enc", "w") as f:
            json.dump({"KeyId": KEY_ID, "CiphertextBlob": ciphertext}, f)
        print("💾 Fichier chiffré sauvegardé : fichier_kms_reel.enc")
        
        # ----------------------------------------
        # Étape 3 — Déchiffrer avec AWS KMS
        # ----------------------------------------
        print(f"\n🔓 Étape 3 : Déchiffrement avec AWS KMS...")
        with open("fichier_kms_reel.enc", "r") as f:
            saved = json.load(f)
        
        response = kms.decrypt(
            KeyId=saved['KeyId'],
            CiphertextBlob=base64.b64decode(saved['CiphertextBlob'])
        )
        decrypted = response['Plaintext'].decode()
        print(f"📄 Message déchiffré : {decrypted}")
        print("\n✅ Demo AWS KMS réelle terminée avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur KMS : {e}")

# ----------------------------------------
# Étape 4 — S3 avec SSE-KMS
# ----------------------------------------
print("\n📦 Étape 4 : Upload S3 avec chiffrement SSE-KMS...")
bucket = "c193369a4970366l15265305t1w073171213597-bucket1-2eyfngfw5te1"
try:
    s3.put_object(
        Bucket=bucket,
        Key="fichier_kms.txt",
        Body="Fichier protege par SSE-KMS".encode(),
        ServerSideEncryption="aws:kms"
    )
    print(f"✅ Fichier uploadé sur S3 avec SSE-KMS !")
    
    # Vérifier le chiffrement
    response = s3.get_object(Bucket=bucket, Key="fichier_kms.txt")
    print(f"🔒 Chiffrement utilisé : {response.get('ServerSideEncryption', 'N/A')}")
    print(f"📄 Contenu récupéré : {response['Body'].read().decode()}")
    
except Exception as e:
    print(f"❌ Erreur S3 : {e}")
