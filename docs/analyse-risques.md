# Analyse et registre des risques

| | |
|---|---|
| **Méthodologie** | Inspirée d'ISO/IEC 27005 (approche simplifiée) |
| **Périmètre** | Identique à celui défini dans la [politique de sécurité de l'information](./politique-securite-information.md) |
| **Fréquence de révision** | Annuelle, ou après tout changement majeur d'infrastructure ou incident |
| **Propriétaire** | RSSI, en lien avec le responsable IT/DevOps et les data stewards |

## 1. Méthodologie d'évaluation

Chaque risque est évalué selon deux axes, notés de 1 à 4 :

**Probabilité (vraisemblance)**

| Niveau | Description |
|---|---|
| 1 – Rare | N'est jamais survenu, mécanisme de protection déjà robuste |
| 2 – Possible | Peut survenir dans certaines circonstances, quelques cas connus dans le secteur |
| 3 – Probable | Susceptible de survenir dans l'année, contrôles actuels partiels |
| 4 – Quasi certain | Récurrent dans le secteur ou déjà observé en interne |

**Impact**

| Niveau | Description |
|---|---|
| 1 – Mineur | Gêne opérationnelle limitée, aucun impact financier ou réglementaire notable |
| 2 – Modéré | Interruption partielle < 1 jour, coût maîtrisable |
| 3 – Majeur | Interruption > 1 jour, fuite de données limitée, impact réputationnel |
| 4 – Critique | Fuite de données massive, obligation de notification CNIL/RGPD, arrêt de l'ERP > 3 jours |

**Niveau de risque = Probabilité × Impact**

| | Impact 1 | Impact 2 | Impact 3 | Impact 4 |
|---|---|---|---|---|
| **Probabilité 4** | 4 (Modéré) | 8 (Élevé) | 12 (Critique) | 16 (Critique) |
| **Probabilité 3** | 3 (Faible) | 6 (Modéré) | 9 (Élevé) | 12 (Critique) |
| **Probabilité 2** | 2 (Faible) | 4 (Modéré) | 6 (Modéré) | 8 (Élevé) |
| **Probabilité 1** | 1 (Faible) | 2 (Faible) | 3 (Faible) | 4 (Modéré) |

**Options de traitement** : Réduire (contrôle supplémentaire) · Accepter (risque résiduel toléré
par la Direction) · Transférer (assurance, contrat prestataire) · Éviter (arrêt de l'activité à
risque).

## 2. Registre des risques

| # | Actif concerné | Menace | Vulnérabilité exploitée | Prob. | Impact | Risque brut | Contrôles existants | Traitement | Risque résiduel | Contrôle(s) associé(s) |
|---|---|---|---|---|---|---|---|---|---|---|
| R1 | Compte root AWS | Prise de contrôle du compte cloud | Absence de MFA sur le compte racine | 3 | 4 | 12 (Critique) | Aucun avant SGSI | Réduire | 3 (Faible) | [controle-acces.md](./politiques/controle-acces.md) — script `check_root_mfa` |
| R2 | Bases de données ERP (S3/RDS) | Fuite de données clients/fournisseurs | Compartiment S3 mal configuré (accès public) | 2 | 4 | 8 (Élevé) | Revue manuelle ponctuelle | Réduire | 2 (Faible) | [classification-donnees.md](./politiques/classification-donnees.md) — script `check_s3_public_access` |
| R3 | Comptes utilisateurs IAM | Compromission par mot de passe faible | Absence de politique de mot de passe robuste | 3 | 3 | 9 (Élevé) | Aucune politique formalisée | Réduire | 4 (Modéré) | [mots-de-passe-authentification.md](./politiques/mots-de-passe-authentification.md) — script `check_password_policy` |
| R4 | ERP Odoo (disponibilité) | Ransomware sur les serveurs applicatifs | Postes/serveurs sans EDR, sauvegardes non testées | 3 | 4 | 12 (Critique) | Sauvegardes quotidiennes non vérifiées | Réduire | 6 (Modéré) | [continuite-activite-sauvegardes.md](./politiques/continuite-activite-sauvegardes.md) |
| R5 | Journal d'activité cloud | Actions malveillantes non détectées | AWS CloudTrail non activé sur toutes les régions | 2 | 3 | 6 (Modéré) | Aucun | Réduire | 2 (Faible) | [gestion-incidents.md](./politiques/gestion-incidents.md) — script `check_cloudtrail_enabled` |
| R6 | Données au repos (S3/RDS) | Vol de support ou accès non autorisé au stockage | Chiffrement au repos non systématique | 2 | 3 | 6 (Modéré) | Chiffrement par défaut S3 seulement | Réduire | 2 (Faible) | [classification-donnees.md](./politiques/classification-donnees.md) — script `check_s3_encryption` |
| R7 | Collaborateurs | Hameçonnage (phishing) ciblant les identifiants ERP | Absence de sensibilisation formalisée | 4 | 3 | 12 (Critique) | Sensibilisation informelle | Réduire | 6 (Modéré) | [sensibilisation-formation.md](./politiques/sensibilisation-formation.md) |
| R8 | Accès prestataires/fournisseurs | Abus d'un compte tiers non désactivé après mission | Absence de revue périodique des accès externes | 3 | 3 | 9 (Élevé) | Revue ad hoc | Réduire | 4 (Modéré) | [controle-acces.md](./politiques/controle-acces.md) |
| R9 | Comptes à privilège cloud (IAM) | Élévation de privilèges par erreur de configuration | Politiques IAM trop permissives (`*:*`) | 2 | 3 | 6 (Modéré) | Aucune revue automatisée | Réduire | 2 (Faible) | [controle-acces.md](./politiques/controle-acces.md) — script `check_iam_wildcard_policies` |
| R10 | Personnel clé (RSSI, DevOps) | Perte de connaissance critique (départ) | Documentation SGSI incomplète avant ce projet | 2 | 2 | 4 (Modéré) | Aucune | Réduire | 2 (Faible) | Ensemble de la documentation SGSI |
| R11 | Infrastructure cloud | Indisponibilité fournisseur cloud (panne AWS) | Absence de plan de reprise multi-zone documenté | 1 | 3 | 3 (Faible) | Architecture mono-zone | Accepter | 3 (Faible) | [continuite-activite-sauvegardes.md](./politiques/continuite-activite-sauvegardes.md) |
| R12 | Service de messagerie | Usurpation de domaine (spoofing) pour fraude au virement | Absence de SPF/DKIM/DMARC stricts | 2 | 3 | 6 (Modéré) | Configuration partielle | Réduire | 3 (Faible) | [gestion-incidents.md](./politiques/gestion-incidents.md) |

## 3. Synthèse

- **3 risques critiques bruts** (R1, R4, R7) ramenés à un niveau modéré ou faible après
  traitement — priorité de mise en œuvre des contrôles associés.
- **1 risque accepté** (R11) : le coût d'une architecture multi-zone est jugé disproportionné
  par rapport à l'impact pour une PME de cette taille ; décision documentée et validée par la
  Direction, à réévaluer si la criticité de l'ERP augmente.
- Les risques R1, R2, R3, R5, R6, R9 disposent chacun d'un **contrôle automatisé vérifiable**
  dans [`../controls/aws_compliance_check.py`](../controls/aws_compliance_check.py), ce qui
  permet de mesurer objectivement le risque résiduel plutôt que de se fier à une déclaration.

---

*Document suivant : [Déclaration d'applicabilité](./declaration-applicabilite.md)*
