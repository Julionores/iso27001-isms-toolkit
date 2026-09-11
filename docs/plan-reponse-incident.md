# Plan de réponse aux incidents de sécurité

| | |
|---|---|
| **Contrôles ISO 27001 couverts** | 5.24, 5.25, 5.26, 5.27, 5.28, 6.8 |
| **Propriétaire** | RSSI |
| **Activation** | Dès qu'un événement de sécurité est suspecté, par n'importe quel collaborateur |

## 1. Signalement (contrôle 6.8)

Tout collaborateur qui suspecte un incident (e-mail de phishing reçu, comportement anormal
de l'ERP, message de rançongiciel, perte d'un poste de travail) doit :

1. **Ne pas tenter de corriger seul** un incident technique (ne pas éteindre un serveur
   compromis, ne pas supprimer un e-mail suspect avant signalement).
2. Signaler immédiatement à `securite@novadistrib.example` ou par téléphone au RSSI en
   dehors des heures ouvrées.
3. Consigner l'heure exacte, ce qui a été observé, et toute action déjà entreprise.

## 2. Classification de la sévérité

| Niveau | Exemple | Délai de première réponse |
|---|---|---|
| **P1 – Critique** | Fuite de données confirmée, rançongiciel actif, ERP indisponible | < 1 heure |
| **P2 – Majeur** | Compte à privilège compromis, activité suspecte confirmée sur le cloud | < 4 heures |
| **P3 – Modéré** | Tentative de phishing détectée sans compromission avérée | < 1 jour ouvré |
| **P4 – Mineur** | Anomalie mineure sans impact confirmé | < 3 jours ouvrés |

## 3. Cycle de traitement (contrôles 5.24 à 5.26)

### 3.1 Détection et qualification

Le RSSI (ou l'astreinte IT) confirme la réalité de l'incident et lui attribue un niveau de
sévérité. Les sources de détection incluent :

- alertes AWS CloudTrail / GuardDuty ;
- signalement d'un collaborateur ;
- résultat en échec d'un contrôle du script `controls/aws_compliance_check.py` exécuté en
  routine (par exemple, détection d'un accès public sur un compartiment S3 auparavant privé).

### 3.2 Confinement (containment)

Objectif : stopper la propagation sans détruire les preuves.

- Isoler la ressource concernée (révoquer une clé d'accès IAM compromise, couper l'accès
  réseau d'un poste infecté) plutôt que l'éteindre.
- Désactiver — sans supprimer — le compte utilisateur suspecté d'être compromis.
- Conserver les journaux concernés avant toute action corrective (contrôle 5.28 — collecte
  de preuves).

### 3.3 Éradication

- Identifier la cause racine (identifiant compromis, vulnérabilité non corrigée, erreur de
  configuration).
- Appliquer le correctif définitif (rotation des identifiants, application du correctif de
  sécurité, correction de la configuration IAM/S3).

### 3.4 Reprise (recovery)

- Restaurer le service à partir d'une sauvegarde saine si nécessaire (voir
  [continuite-activite-sauvegardes.md](./politiques/continuite-activite-sauvegardes.md)).
- Vérifier, avant remise en production, que le script `aws_compliance_check.py` repasse au
  vert sur les contrôles concernés.
- Surveiller la ressource concernée pendant au moins 7 jours après reprise.

### 3.5 Notification légale (contrôle 5.5, RGPD)

Si l'incident implique des données à caractère personnel de clients, fournisseurs ou
collaborateurs :

- Le RSSI évalue, avec la Direction, si le risque pour les personnes concernées déclenche
  l'obligation de notification à la CNIL (délai réglementaire : 72 heures après prise de
  connaissance).
- Si le risque est élevé pour les personnes concernées, celles-ci doivent également être
  informées directement.

## 4. Retour d'expérience (contrôle 5.27)

Dans les 10 jours ouvrés suivant la clôture d'un incident P1 ou P2, une réunion de retour
d'expérience réunit le RSSI, le responsable IT/DevOps et le responsable métier concerné, pour
produire une fiche courte :

- Chronologie factuelle de l'incident.
- Cause racine identifiée.
- Ce qui a bien fonctionné / ce qui a manqué.
- Actions correctives, avec responsable et échéance.
- Mise à jour, si nécessaire, de l'[analyse des risques](./analyse-risques.md) et de la
  [déclaration d'applicabilité](./declaration-applicabilite.md).

## 5. Registre des incidents

| Date | Sévérité | Résumé | Cause racine | Action corrective | Clôturé le |
|---|---|---|---|---|---|
| *(exemple)* 2026-03-04 | P3 | Campagne de phishing ciblant le service comptabilité | Absence de formation récente | Session de sensibilisation planifiée (voir [sensibilisation-formation.md](./politiques/sensibilisation-formation.md)) | 2026-03-06 |

> Ce registre est tenu à jour par le RSSI et revu lors de la revue annuelle du SGSI.

## 6. Contacts d'urgence

| Rôle | Contact |
|---|---|
| RSSI | securite@novadistrib.example |
| Astreinte IT/DevOps | astreinte-it@novadistrib.example |
| CNIL (notification RGPD) | https://www.cnil.fr/fr/notifier-une-violation-de-donnees-personnelles |
| Hébergeur cloud (support) | Console de support AWS |

---

*Document suivant : [Politiques thématiques](./politiques/)*
