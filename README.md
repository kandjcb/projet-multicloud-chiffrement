# Cloud KMS : AWS KMS & Azure Key Vault

> Projet Multi-Cloud | Axe 2 : Mécanismes de cryptage, authentification et gestion des identités  
> Sujet 5 : Mise en œuvre du chiffrement dans un environnement Multi-Cloud  

---

## 📌 Objectif

Démontrer l'utilisation du **Cloud KMS** (Key Management Service) pour chiffrer et déchiffrer des fichiers, en comparant **AWS KMS** et **Azure Key Vault**.

---

## 📁 Structure du dossier
---

## ⚙️ Technologies utilisées

- **AWS KMS** via SDK `boto3`
- **Azure Key Vault** via SDK `azure-keyvault-keys` + `azure-identity`
- **Algorithme** : RSA-OAEP (Azure) / AES-256 (AWS KMS)
- **Compte** : AWS Academy + Azure Student

---

## 🚀 Exécution

### Prérequis

```bash
pip install boto3 azure-keyvault-keys azure-identity
```

### Azure Key Vault

```bash
az login
python aws_kms_complete.py
```

### AWS KMS

```bash
aws configure
python aws_kms_real.py
```

---

## ⚠️ Note sur AWS Academy

Les comptes AWS Academy ont des restrictions sur AWS KMS (permissions `kms:CreateKey` et `kms:Encrypt` désactivées). Les scripts documentent cette limitation via l'erreur `AccessDenied` et démontrent le concept via le SDK officiel `boto3`.

---

## ✅ Résultats obtenus

| Opération | AWS KMS | Azure Key Vault |
|---|---|---|
| Connexion compte | ✅ | ✅ |
| Création clé | ❌ AccessDenied (Academy) | ✅ RSA-2048 |
| Chiffrement fichier | ✅ (simulé boto3) | ✅ RSA-OAEP |
| Déchiffrement fichier | ✅ (simulé boto3) | ✅ Vérifié |

---

## 👤 Auteur

**Mohamed Kacim EL AFI** — Étudiant ingénieur, ENSA Khouribga  
GitHub : [@kandjcb](https://github.com/kandjcb)
