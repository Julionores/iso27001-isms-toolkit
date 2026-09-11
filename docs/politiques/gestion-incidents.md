# Politique de gestion des incidents et de supervision

| | |
|---|---|
| **Contrôles ISO 27001 couverts** | 5.24, 8.15, 8.16 |
| **Applicable à** | Infrastructure cloud, ERP, messagerie |
| **Voir aussi** | [Plan de réponse aux incidents](../plan-reponse-incident.md) (procédure opérationnelle détaillée) |

Ce document fixe le cadre de **gouvernance** de la gestion des incidents ; la procédure
opérationnelle pas à pas (détection → confinement → éradication → reprise → retour
d'expérience) est détaillée dans le [plan de réponse aux incidents](../plan-reponse-incident.md).

## 1. Journalisation (contrôle 8.15)

Les journaux d'activité suivants sont activés en permanence et conservés au minimum 1 an :

| Source | Contenu journalisé | Conservation |
|---|---|---|
| AWS CloudTrail | Tous les appels d'API sur le compte, dans toutes les régions | 1 an minimum, archivé ensuite en stockage froid |
| Journaux applicatifs Odoo | Connexions, actions sur les données sensibles (factures, paiements) | 1 an |
| Journaux d'accès réseau (VPC Flow Logs) | Trafic entrant/sortant de l'infrastructure de production | 90 jours |

AWS CloudTrail doit être actif sur l'ensemble des régions du compte, y compris celles non
utilisées activement — une région non couverte est un angle mort pour la détection d'activité
malveillante. *(Vérifié automatiquement par le script `check_cloudtrail_enabled`.)*

## 2. Surveillance des activités (contrôle 8.16)

- Une alerte automatique est déclenchée en cas de : connexion au compte racine, désactivation
  de CloudTrail, modification d'une politique IAM à privilège, ou accès public accordé à un
  compartiment S3 précédemment privé.
- Le script `controls/aws_compliance_check.py` est exécuté selon une fréquence définie
  (recommandation : quotidienne, via une tâche planifiée) pour détecter toute dérive de
  configuration par rapport à la politique en vigueur.
- Toute alerte de sévérité P1 ou P2 (voir le [plan de réponse aux incidents](../plan-reponse-incident.md#2-classification-de-la-sévérité))
  déclenche automatiquement la procédure de réponse aux incidents.

## 3. Escalade et responsabilités

| Sévérité | Notifié immédiatement | Décisionnaire |
|---|---|---|
| P1 – Critique | RSSI + Direction | Direction (arbitrage communication/notification légale) |
| P2 – Majeur | RSSI + Responsable IT/DevOps | RSSI |
| P3/P4 | Responsable IT/DevOps | Responsable IT/DevOps, information au RSSI |

## 4. Revue périodique

Un point mensuel entre le RSSI et le responsable IT/DevOps passe en revue :

- les incidents survenus dans le mois (voir le registre des incidents) ;
- les résultats des dernières exécutions du script de conformité automatisée ;
- toute alerte non traitée ou en cours.

---

*Contrôle vérifié automatiquement : `controls/aws_compliance_check.py::check_cloudtrail_enabled`*
