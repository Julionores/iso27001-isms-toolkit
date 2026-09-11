# Politique de classification et de protection des données

| | |
|---|---|
| **Contrôles ISO 27001 couverts** | 5.12, 5.13, 5.23, 8.12, 8.24 |
| **Applicable à** | Toutes les données traitées ou stockées dans le périmètre du SGSI |

## 1. Niveaux de classification

| Niveau | Définition | Exemples | Contrôles minimaux requis |
|---|---|---|---|
| **Public** | Diffusable sans restriction | Plaquette commerciale, catalogue produit public | Aucun contrôle spécifique |
| **Interne** | Réservé aux collaborateurs | Procédures internes, organigramme | Accès restreint aux comptes de l'entreprise |
| **Confidentiel** | Diffusion limitée aux personnes habilitées | Données clients/fournisseurs, contrats commerciaux | Chiffrement au repos et en transit, accès nominatif |
| **Critique** | Impact grave en cas de divulgation | Données financières, identifiants d'accès, données RH/paie | Chiffrement, accès à privilège limité, journalisation systématique |

Chaque donnée nouvellement créée (document, table de l'ERP, export) doit se voir attribuer un
niveau par son propriétaire métier (data steward), par défaut « Interne » en l'absence de
classification explicite.

## 2. Protection technique par niveau

### Chiffrement au repos (contrôle 8.24)

Toutes les données classées **Confidentiel** ou **Critique** stockées sur AWS doivent être
chiffrées au repos :

- compartiments S3 : chiffrement par défaut activé (SSE-S3 ou SSE-KMS) ;
- bases de données (RDS) : chiffrement au repos activé à la création de l'instance.

*(Vérifié automatiquement par le script `check_s3_encryption`.)*

### Chiffrement en transit

Tous les accès aux services AWS et à l'ERP s'effectuent exclusivement via HTTPS/TLS ; les
protocoles non chiffrés (HTTP, FTP simple) sont interdits pour tout transfert de données
classées Confidentiel ou Critique.

### Prévention de la fuite de données (contrôle 8.12)

Aucun compartiment S3 contenant des données Confidentiel ou Critique ne doit être accessible
publiquement. Le blocage d'accès public est activé par défaut au niveau du compte AWS entier.

*(Vérifié automatiquement par le script `check_s3_public_access`.)*

## 3. Sécurité des services cloud (contrôle 5.23)

L'hébergement dans le cloud (AWS) suit le modèle de responsabilité partagée : l'hébergeur
sécurise l'infrastructure physique et le réseau sous-jacent, NovaDistrib reste responsable de
la configuration des services (droits d'accès, chiffrement, journalisation) et des données
qui y sont déposées. Cette politique — et les contrôles automatisés associés — constituent la
mise en œuvre concrète de cette responsabilité côté client.

## 4. Marquage et transfert (contrôles 5.13, 5.14)

- Les documents classés Confidentiel ou Critique portent une mention explicite (en-tête ou
  métadonnée du document).
- Tout envoi externe d'un document classé Confidentiel ou Critique (à un client, un
  fournisseur, un partenaire) est chiffré (pièce jointe protégée par mot de passe transmis
  via un canal distinct, ou plateforme d'échange sécurisée) — l'envoi par e-mail simple non
  protégé est proscrit.

## 5. Durée de conservation et suppression (contrôle 8.10)

La durée de conservation suit les obligations légales applicables (comptables : 10 ans ;
RH : selon la réglementation du travail). Au-delà de cette durée, les données sont supprimées
de façon irréversible plutôt que simplement archivées indéfiniment.

---

*Contrôles vérifiés automatiquement : `controls/aws_compliance_check.py::check_s3_encryption`,
`::check_s3_public_access`*
