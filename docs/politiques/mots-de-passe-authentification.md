# Politique de mots de passe et d'authentification

| | |
|---|---|
| **Contrôles ISO 27001 couverts** | 5.17, 8.5 |
| **Applicable à** | Comptes AWS IAM, ERP Odoo, messagerie professionnelle |

## 1. Exigences de robustesse

| Type de compte | Longueur minimale | Complexité | Renouvellement | MFA |
|---|---|---|---|---|
| Compte racine AWS | 20 caractères | Majuscules, minuscules, chiffres, symboles | N/A (accès très restreint) | **Obligatoire** (matériel) |
| Compte IAM à privilège (admin) | 16 caractères | Majuscules, minuscules, chiffres, symboles | 90 jours | **Obligatoire** |
| Compte IAM standard | 14 caractères | Majuscules, minuscules, chiffres | 180 jours | Recommandé |
| Compte Odoo (utilisateur métier) | 12 caractères | Majuscules, minuscules, chiffres | 180 jours | Recommandé pour les rôles sensibles (comptabilité, RH) |

Ces exigences sont **supérieures** aux anciennes recommandations de rotation fréquente sans
complexité, conformément aux évolutions récentes des bonnes pratiques (NIST, ANSSI) : la
priorité va à la **longueur** et à l'usage systématique du MFA plutôt qu'à une rotation trop
fréquente qui pousse les utilisateurs vers des mots de passe faibles et prévisibles.

## 2. Application technique de la politique de mot de passe IAM

La politique de mot de passe du compte AWS est configurée au niveau du compte (et non laissée
à l'appréciation individuelle), avec :

- longueur minimale de 14 caractères ;
- au moins un caractère de chaque catégorie (majuscule, minuscule, chiffre, symbole) ;
- interdiction de réutiliser les 5 derniers mots de passe ;
- expiration à 90 jours pour les comptes disposant de droits d'administration.

*(Vérifié automatiquement par le script `check_password_policy`.)*

## 3. Authentification multifacteur (MFA)

- **Obligatoire** pour : le compte racine, tout compte IAM disposant de droits d'administration,
  et tout accès distant à l'infrastructure de production.
- **Recommandé** pour : l'ensemble des comptes ERP à des fins de sensibilisation progressive.
- Les dispositifs MFA matériels ou applications d'authentification (TOTP) sont préférés aux
  codes envoyés par SMS, plus vulnérables au détournement de numéro.

## 4. Gestion des identifiants

- Aucun mot de passe n'est communiqué par e-mail en clair, y compris lors de la création
  d'un compte — le premier mot de passe est transmis via un canal séparé (SMS, oral) et son
  changement est imposé à la première connexion.
- Aucun identifiant applicatif (clé d'accès IAM, mot de passe de service) n'est stocké en clair
  dans un dépôt de code, un fichier de configuration versionné, ou un e-mail. Les secrets sont
  gérés via un coffre-fort dédié (AWS Secrets Manager ou équivalent).
- Un identifiant compromis (suspecté ou confirmé) est immédiatement révoqué et remplacé — voir
  le [plan de réponse aux incidents](../plan-reponse-incident.md).

---

*Contrôle vérifié automatiquement : `controls/aws_compliance_check.py::check_password_policy`,
`::check_root_mfa`*
