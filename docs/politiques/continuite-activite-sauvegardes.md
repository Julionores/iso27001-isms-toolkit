# Politique de sauvegarde et de continuité d'activité

| | |
|---|---|
| **Contrôles ISO 27001 couverts** | 5.29, 5.30, 8.13, 8.14 |
| **Applicable à** | Base de données ERP, documents stockés sur S3, configuration de l'infrastructure |

## 1. Objectifs de continuité

| Indicateur | Cible | Justification |
|---|---|---|
| **RPO** (perte de données maximale tolérée) | 24 heures | Une journée de saisie ERP maximum en cas de sinistre |
| **RTO** (délai de reprise maximal) | 8 heures ouvrées | Impact acceptable sur l'activité commerciale d'après la Direction |

## 2. Politique de sauvegarde (contrôle 8.13)

| Actif | Fréquence | Rétention | Méthode |
|---|---|---|---|
| Base de données ERP (PostgreSQL sous-jacent) | Quotidienne (nuit) + réplication continue | 30 jours glissants, puis 1 sauvegarde mensuelle conservée 1 an | Snapshot automatisé + archivage S3 |
| Documents et pièces jointes (S3) | Continue (versioning S3) | 90 jours de versions, purge ensuite | Versioning natif S3 |
| Configuration de l'infrastructure (Infrastructure as Code) | À chaque changement | Historique complet | Contrôle de version Git |

Les sauvegardes sont stockées dans une région ou un compte distinct de la production, afin
qu'une compromission du compte principal ne rende pas les sauvegardes elles-mêmes
inaccessibles ou altérables.

## 3. Vérification de la restaurabilité

Une sauvegarde non testée n'est pas une garantie de continuité. NovaDistrib effectue :

- un **test de restauration trimestriel** de la base de données ERP vers un environnement
  isolé, avec vérification de l'intégrité des données restaurées (contrôle par échantillonnage
  sur les tables critiques : clients, commandes, factures) ;
- une consignation du résultat de chaque test (date, durée de restauration effective,
  écart éventuel avec le RTO cible) dans le registre de continuité.

## 4. Redondance (contrôle 8.14)

L'infrastructure de production est actuellement déployée sur une seule zone de disponibilité
AWS (risque R11 de l'[analyse des risques](../analyse-risques.md), accepté par la Direction
au vu du coût d'une architecture multi-zone rapporté à la taille de l'entreprise). Cette
décision est réévaluée annuellement, ou immédiatement si :

- l'ERP devient support d'une activité e-commerce nécessitant une disponibilité continue ;
- un incident de disponibilité dépasse le RTO cible.

## 5. Plan de reprise simplifié

En cas de sinistre rendant l'infrastructure de production indisponible :

1. Le responsable IT/DevOps provisionne une infrastructure de remplacement à partir des
   définitions Infrastructure as Code versionnées.
2. La base de données est restaurée à partir du dernier snapshot valide.
3. Les documents sont restaurés depuis S3 (versioning).
4. Un contrôle d'intégrité est effectué avant réouverture de l'accès aux utilisateurs.
5. Le script `controls/aws_compliance_check.py` est exécuté sur la nouvelle infrastructure
   avant sa mise en production, pour s'assurer qu'elle respecte la même configuration de
   sécurité que l'environnement d'origine.

---

*Ce contrôle n'est pas encore vérifié automatiquement (test de restauration manuel) — voir la
feuille de route dans le [README](../../README.md#feuille-de-route).*
