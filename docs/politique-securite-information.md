# Politique de sécurité de l'information

| | |
|---|---|
| **Organisation** | NovaDistrib SAS (entreprise fictive, secteur distribution B2B, ~120 collaborateurs) |
| **Référentiel** | ISO/IEC 27001:2022 |
| **Version** | 1.0 |
| **Statut** | Approuvée par la Direction |
| **Périmètre** | Voir section 2 |
| **Propriétaire du document** | RSSI (Responsable de la Sécurité des Systèmes d'Information) |

> Ce document est le document racine du Système de Management de la Sécurité de l'Information
> (SGSI) de NovaDistrib. Toutes les politiques thématiques du dossier
> [`politiques/`](./politiques/) en découlent et ne peuvent le contredire.

## 1. Engagement de la Direction

La Direction de NovaDistrib reconnaît que l'information est un actif critique pour la continuité
et la compétitivité de l'entreprise : données clients et fournisseurs, données financières,
configuration de l'ERP (Odoo) qui pilote les achats, les stocks et la facturation.

La Direction s'engage à :

- allouer les ressources humaines et financières nécessaires au SGSI ;
- nommer un RSSI disposant d'une autorité suffisante et d'un accès direct à la Direction ;
- réviser cette politique et les résultats du SGSI au moins une fois par an, ou après tout
  incident majeur ;
- exiger la conformité à cette politique de tout collaborateur, prestataire et sous-traitant
  ayant accès au système d'information de l'entreprise.

## 2. Périmètre du SGSI

Le périmètre couvre :

- l'infrastructure cloud hébergeant l'ERP Odoo et les bases de données associées (compte AWS
  de production) ;
- les postes de travail et comptes utilisateurs des collaborateurs ayant accès à ces systèmes ;
- les processus métier suivants : gestion des commandes, facturation, gestion des accès
  fournisseurs, sauvegarde et restauration des données.

Sont **exclus** du périmètre à ce stade : les systèmes de badgeage physique des locaux et les
équipements réseau des sites distants, traités dans un plan de mise en conformité séparé.

## 3. Objectifs de sécurité

| Objectif | Indicateur de suivi |
|---|---|
| Garantir la confidentialité des données clients et fournisseurs | 0 fuite de données confirmée sur l'exercice |
| Garantir l'intégrité des données financières et de stock de l'ERP | 100 % des sauvegardes vérifiées avec succès (restauration testée) |
| Garantir la disponibilité de l'ERP aux heures ouvrées | Disponibilité ≥ 99,5 % mensuelle |
| Maîtriser les accès aux systèmes sensibles | 0 compte à privilège sans authentification multifacteur (MFA) |
| Détecter et traiter les incidents de sécurité rapidement | Délai moyen de détection < 24 h ; délai moyen de traitement < 72 h |

## 4. Rôles et responsabilités

| Rôle | Responsabilité |
|---|---|
| **Direction générale** | Approuve la politique, arbitre les budgets, assume la responsabilité finale |
| **RSSI** | Pilote le SGSI, maintient la déclaration d'applicabilité, coordonne les audits, rapporte à la Direction |
| **Responsable IT / DevOps** | Met en œuvre les contrôles techniques, exploite les outils de supervision, applique les correctifs |
| **Gestionnaires de données (data stewards)** | Un référent par processus métier (ventes, achats, RH), garant de la qualité et de la classification des données de son domaine |
| **Ensemble des collaborateurs** | Respectent les politiques, suivent la sensibilisation annuelle, signalent tout incident suspecté |

## 5. Principes directeurs

- **Moindre privilège** : aucun accès n'est accordé au-delà du strict nécessaire à la fonction
  exercée (voir [`politiques/controle-acces.md`](./politiques/controle-acces.md)).
- **Défense en profondeur** : aucun contrôle unique n'est considéré suffisant ; les contrôles
  organisationnels (politiques, sensibilisation) et techniques (chiffrement, supervision,
  authentification) se complètent.
- **Amélioration continue** : le SGSI suit un cycle **Plan-Do-Check-Act** — les résultats des
  audits et des contrôles automatisés (voir [`../controls/`](../controls/)) alimentent la revue
  annuelle de cette politique.
- **Traçabilité** : toute décision d'application ou d'exclusion d'un contrôle de l'annexe A est
  justifiée et documentée dans la [déclaration d'applicabilité](./declaration-applicabilite.md).

## 6. Gestion des exceptions

Toute dérogation temporaire à une politique doit être :

1. demandée par écrit au RSSI, avec justification métier et durée précise ;
2. validée conjointement par le RSSI et le responsable du processus métier concerné ;
3. consignée dans le registre des exceptions (tenu par le RSSI) avec date de fin et mesure
   compensatoire le cas échéant ;
4. revue à son échéance — une exception non renouvelée expire automatiquement.

## 7. Non-conformité et sanctions

Le non-respect délibéré de cette politique (partage d'identifiants, contournement d'un
contrôle de sécurité, désactivation d'un outil de supervision sans autorisation) est traité
selon le règlement intérieur de l'entreprise et peut entraîner des sanctions disciplinaires.

## 8. Révision du document

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-09-11 | RSSI | Version initiale |

---

*Document suivant : [Analyse des risques](./analyse-risques.md)*
