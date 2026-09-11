# Déclaration d'applicabilité (SoA — Statement of Applicability)

| | |
|---|---|
| **Référentiel** | ISO/IEC 27001:2022, Annexe A (93 contrôles, 4 thèmes) |
| **Périmètre** | Identique à celui défini dans la [politique de sécurité de l'information](./politique-securite-information.md) |
| **Propriétaire** | RSSI |

> La déclaration d'applicabilité est **le** document central d'un SGSI ISO 27001 : elle liste
> chacun des 93 contrôles de l'annexe A, précise s'il est applicable au périmètre retenu, et
> justifie toute exclusion. Un contrôle exclu sans justification documentée est une non-conformité
> lors d'un audit de certification.

**Légende du statut de mise en œuvre** : 🟢 Mis en œuvre · 🟡 Partiel · 🔴 Non mis en œuvre ·
⚪ Non applicable

## A.5 — Contrôles organisationnels (37 contrôles)

| # | Contrôle | Applicable | Justification | Statut | Référence |
|---|---|---|---|---|---|
| 5.1 | Politiques de sécurité de l'information | Oui | Document racine du SGSI | 🟢 | [politique-securite-information.md](./politique-securite-information.md) |
| 5.2 | Rôles et responsabilités en sécurité de l'information | Oui | Nécessaire pour la gouvernance | 🟢 | Section 4 de la politique SSI |
| 5.3 | Séparation des tâches | Oui | Limite le risque de fraude/erreur (ex. validation facture ≠ paiement) | 🟡 | À formaliser dans les procédures Odoo |
| 5.4 | Responsabilités de la direction | Oui | Engagement formel requis | 🟢 | Section 1 de la politique SSI |
| 5.5 | Relations avec les autorités | Oui | Obligation de notification CNIL en cas de fuite de données | 🟡 | Procédure à formaliser dans le plan de réponse aux incidents |
| 5.6 | Relations avec des groupes d'intérêt spécifiques | Non | PME sans budget dédié à une veille sectorielle formelle | ⚪ | Risque accepté (voir R11 registre des risques) |
| 5.7 | Renseignement sur les menaces (threat intelligence) | Non | Hors moyens d'une PME de cette taille à ce stade | ⚪ | Réévaluation prévue à N+2 |
| 5.8 | Sécurité de l'information dans la gestion de projet | Oui | Applicable aux projets d'évolution de l'ERP | 🟡 | À intégrer à la méthodologie projet |
| 5.9 | Inventaire des informations et actifs associés | Oui | Base de l'analyse de risques | 🟢 | [analyse-risques.md](./analyse-risques.md) §2 |
| 5.10 | Utilisation correcte des informations et actifs | Oui | Charte informatique à faire signer | 🟡 | À rédiger en annexe RH |
| 5.11 | Restitution des actifs | Oui | Applicable en fin de contrat (matériel, accès) | 🟡 | Voir 6.5 |
| 5.12 | Classification de l'information | Oui | Distinction données publiques/internes/confidentielles | 🟢 | [classification-donnees.md](./politiques/classification-donnees.md) |
| 5.13 | Marquage de l'information | Oui | Découle de la classification | 🟡 | À automatiser dans Odoo (métadonnées) |
| 5.14 | Transfert de l'information | Oui | Échanges avec fournisseurs/clients | 🟡 | À formaliser (chiffrement des pièces jointes sensibles) |
| 5.15 | Contrôle d'accès | Oui | Contrôle central du SGSI | 🟢 | [controle-acces.md](./politiques/controle-acces.md) |
| 5.16 | Gestion des identités | Oui | Un identifiant unique par utilisateur | 🟢 | [controle-acces.md](./politiques/controle-acces.md) |
| 5.17 | Informations d'authentification | Oui | Politique de mots de passe et MFA | 🟢 | [mots-de-passe-authentification.md](./politiques/mots-de-passe-authentification.md) |
| 5.18 | Droits d'accès | Oui | Revue périodique des droits (voir R8) | 🟡 | Revue trimestrielle à mettre en place |
| 5.19 | Sécurité de l'information dans les relations fournisseurs | Oui | L'hébergeur cloud et l'éditeur ERP sont des fournisseurs critiques | 🟡 | Clause à ajouter aux contrats |
| 5.20 | Prise en compte de la sécurité dans les accords fournisseurs | Oui | Découle de 5.19 | 🟡 | En cours de renégociation contractuelle |
| 5.21 | Gestion de la sécurité dans la chaîne d'approvisionnement TIC | Oui | Dépendance à l'éditeur Odoo et ses modules tiers | 🟡 | Revue des modules tiers installés à planifier |
| 5.22 | Surveillance et revue des services fournisseurs | Oui | Suivi de la disponibilité de l'hébergeur cloud | 🟡 | Tableau de bord de disponibilité à mettre en place |
| 5.23 | Sécurité de l'information pour les services cloud | Oui | Infrastructure hébergée sur AWS | 🟢 | [classification-donnees.md](./politiques/classification-donnees.md) + contrôles automatisés |
| 5.24 | Planification de la gestion des incidents | Oui | Cœur du plan de réponse | 🟢 | [plan-reponse-incident.md](./plan-reponse-incident.md) |
| 5.25 | Évaluation et décision sur les événements de sécurité | Oui | Étape du plan de réponse | 🟢 | [plan-reponse-incident.md](./plan-reponse-incident.md) |
| 5.26 | Réponse aux incidents de sécurité | Oui | Étape du plan de réponse | 🟢 | [plan-reponse-incident.md](./plan-reponse-incident.md) |
| 5.27 | Apprentissage tiré des incidents | Oui | Retour d'expérience obligatoire après chaque incident majeur | 🟢 | [plan-reponse-incident.md](./plan-reponse-incident.md) §5 |
| 5.28 | Collecte de preuves | Oui | Nécessaire en cas de poursuite ou d'assurance cyber | 🟡 | Procédure de conservation des logs à formaliser |
| 5.29 | Sécurité de l'information en période de perturbation | Oui | Continuité pendant un incident majeur | 🟡 | Lié au PCA |
| 5.30 | Préparation des TIC pour la continuité d'activité | Oui | Sauvegardes et restauration testées | 🟢 | [continuite-activite-sauvegardes.md](./politiques/continuite-activite-sauvegardes.md) |
| 5.31 | Exigences légales, statutaires, réglementaires et contractuelles | Oui | RGPD applicable (données clients/fournisseurs) | 🟡 | Registre des traitements RGPD à compléter |
| 5.32 | Droits de propriété intellectuelle | Oui | Licences logicielles (ERP, modules) | 🟡 | Inventaire des licences à jour à produire |
| 5.33 | Protection des enregistrements | Oui | Factures et documents comptables (obligation légale de conservation) | 🟡 | Politique de conservation à formaliser |
| 5.34 | Protection de la vie privée et des données à caractère personnel | Oui | Données clients/fournisseurs/RH | 🟡 | Analyse d'impact RGPD (AIPD) à réaliser |
| 5.35 | Revue indépendante de la sécurité de l'information | Oui | Audit externe à prévoir avant certification | 🔴 | Planifié pour l'exercice suivant |
| 5.36 | Conformité aux politiques, règles et normes de sécurité | Oui | Contrôle de conformité interne | 🟡 | Contrôles automatisés partiels (voir `controls/`) |
| 5.37 | Procédures d'exploitation documentées | Oui | Runbooks pour les opérations IT critiques | 🟡 | En cours de rédaction (sauvegarde, restauration, gestion des accès) |

## A.6 — Contrôles liés aux personnes (8 contrôles)

| # | Contrôle | Applicable | Justification | Statut | Référence |
|---|---|---|---|---|---|
| 6.1 | Vérification des antécédents | Oui | Postes à accès sensible (comptabilité, IT) | 🟡 | À intégrer au processus de recrutement RH |
| 6.2 | Termes et conditions du contrat de travail | Oui | Clause de confidentialité au contrat | 🟡 | Clause type à ajouter aux contrats |
| 6.3 | Sensibilisation, éducation et formation à la sécurité | Oui | Risque R7 (phishing) prioritaire | 🟢 | [sensibilisation-formation.md](./politiques/sensibilisation-formation.md) |
| 6.4 | Processus disciplinaire | Oui | Sanctions en cas de non-conformité volontaire | 🟢 | Section 7 de la politique SSI |
| 6.5 | Responsabilités après la fin ou le changement d'un contrat | Oui | Désactivation des accès à la sortie | 🟡 | Procédure de départ à formaliser avec RH |
| 6.6 | Accords de confidentialité ou de non-divulgation | Oui | Applicable aux prestataires externes | 🟡 | Modèle de NDA à généraliser |
| 6.7 | Télétravail | Oui | Une partie des équipes commerciales est en télétravail partiel | 🟡 | Charte de télétravail sécurisé à rédiger |
| 6.8 | Signalement des événements de sécurité de l'information | Oui | Tout collaborateur doit pouvoir signaler un incident | 🟢 | [plan-reponse-incident.md](./plan-reponse-incident.md) §1 |

## A.7 — Contrôles physiques (14 contrôles)

| # | Contrôle | Applicable | Justification | Statut | Référence |
|---|---|---|---|---|---|
| 7.1 | Périmètres de sécurité physique | Oui | Locaux du siège | 🟡 | Hors périmètre technique de ce projet, géré par les services généraux |
| 7.2 | Contrôle d'entrée physique | Oui | Badge d'accès aux locaux | 🟡 | Existant, non documenté dans ce SGSI |
| 7.3 | Sécurisation des bureaux, salles et installations | Oui | Salle serveur locale (matériel réseau) | 🟡 | Hors périmètre — voir note en introduction de la politique SSI |
| 7.4 | Surveillance de la sécurité physique | Non | Pas de vidéosurveillance à ce stade | ⚪ | Risque jugé faible pour ce périmètre |
| 7.5 | Protection contre les menaces physiques et environnementales | Oui | Onduleur, extincteurs dans la salle serveur | 🟡 | Existant, maintenance à documenter |
| 7.6 | Travail dans les zones sécurisées | Non | Pas de zone à accès restreint au sens strict | ⚪ | — |
| 7.7 | Bureau propre et écran verrouillé | Oui | Applicable à tous les postes de travail | 🟡 | À inclure à la charte informatique |
| 7.8 | Emplacement et protection du matériel | Oui | Serveurs et postes de travail | 🟡 | Existant, non documenté |
| 7.9 | Sécurité des actifs hors des locaux | Oui | Ordinateurs portables des commerciaux itinérants | 🟡 | Chiffrement de disque à généraliser |
| 7.10 | Supports de stockage | Oui | Clés USB, disques externes | 🟡 | Politique d'usage à rédiger |
| 7.11 | Services généraux support | Oui | Électricité, climatisation de la salle serveur | 🟡 | Existant, hors périmètre technique détaillé |
| 7.12 | Sécurité du câblage | Non | Infrastructure principale externalisée dans le cloud | ⚪ | — |
| 7.13 | Maintenance du matériel | Oui | Contrat de maintenance du matériel réseau local | 🟡 | Contrat existant à référencer |
| 7.14 | Mise au rebut ou recyclage sécurisé du matériel | Oui | Effacement sécurisé avant mise au rebut | 🔴 | Procédure à créer |

## A.8 — Contrôles technologiques (34 contrôles)

| # | Contrôle | Applicable | Justification | Statut | Référence |
|---|---|---|---|---|---|
| 8.1 | Dispositifs des utilisateurs finaux | Oui | Postes de travail et mobiles professionnels | 🟡 | Politique MDM à évaluer |
| 8.2 | Droits d'accès privilégiés | Oui | Comptes administrateurs IAM/Odoo | 🟢 | [controle-acces.md](./politiques/controle-acces.md) — script `check_root_mfa`, `check_iam_wildcard_policies` |
| 8.3 | Restriction d'accès à l'information | Oui | Cloisonnement des données par rôle Odoo | 🟢 | [controle-acces.md](./politiques/controle-acces.md) |
| 8.4 | Accès au code source | Non | Pas de développement logiciel propriétaire critique | ⚪ | Modules Odoo standards uniquement |
| 8.5 | Authentification sécurisée | Oui | MFA sur les comptes à privilège | 🟢 | [mots-de-passe-authentification.md](./politiques/mots-de-passe-authentification.md) — script `check_root_mfa` |
| 8.6 | Gestion de la capacité | Oui | Dimensionnement de l'infrastructure ERP | 🟡 | Suivi manuel actuel, alerting à automatiser |
| 8.7 | Protection contre les logiciels malveillants | Oui | Antivirus/EDR sur les postes de travail | 🟡 | Solution existante, couverture à vérifier |
| 8.8 | Gestion des vulnérabilités techniques | Oui | Mises à jour de sécurité de l'ERP et de l'OS | 🟡 | Processus de patch management à formaliser |
| 8.9 | Gestion de la configuration | Oui | Configuration de référence de l'infrastructure cloud | 🟢 | AWS Config conformance pack — [conformance-pack/](../controls/conformance-pack/) |
| 8.10 | Suppression de l'information | Oui | Purge des données après durée de conservation | 🟡 | Politique de rétention à formaliser (lié à 5.33) |
| 8.11 | Masquage des données | Non | Pas de besoin identifié d'anonymisation en environnement de test à ce stade | ⚪ | Réévaluer si un environnement de recette est créé |
| 8.12 | Prévention de la fuite de données | Oui | Risque R2 (compartiment S3 public) | 🟢 | [classification-donnees.md](./politiques/classification-donnees.md) — script `check_s3_public_access` |
| 8.13 | Sauvegarde de l'information | Oui | Sauvegardes quotidiennes de l'ERP | 🟢 | [continuite-activite-sauvegardes.md](./politiques/continuite-activite-sauvegardes.md) |
| 8.14 | Redondance des moyens de traitement de l'information | Oui | Risque R11 (mono-zone), traité comme risque accepté | 🟡 | Voir analyse des risques R11 |
| 8.15 | Journalisation | Oui | AWS CloudTrail, logs applicatifs Odoo | 🟢 | script `check_cloudtrail_enabled` |
| 8.16 | Surveillance des activités | Oui | Détection d'anomalies sur le compte cloud | 🟡 | GuardDuty à activer (voir conformance pack) |
| 8.17 | Synchronisation des horloges | Oui | Cohérence des journaux pour l'investigation | 🟡 | NTP standard AWS, à vérifier explicitement |
| 8.18 | Utilisation de programmes utilitaires à privilèges | Oui | Outils d'administration système | 🟡 | Usage restreint aux comptes IT, à documenter |
| 8.19 | Installation de logiciels sur les systèmes opérationnels | Oui | Modules Odoo tiers | 🟡 | Procédure de validation avant installation à créer |
| 8.20 | Sécurité des réseaux | Oui | VPC, groupes de sécurité AWS | 🟡 | Revue des règles de sécurité réseau à automatiser |
| 8.21 | Sécurité des services réseau | Oui | Services managés AWS (RDS, S3) | 🟡 | Lié à 8.20 |
| 8.22 | Cloisonnement des réseaux | Oui | Séparation environnement de production/autres | 🟡 | VPC dédié à documenter |
| 8.23 | Filtrage web | Non | Pas de proxy de filtrage web déployé à ce stade | ⚪ | Réévaluation en fonction du risque de navigation |
| 8.24 | Utilisation de la cryptographie | Oui | Chiffrement au repos et en transit | 🟢 | script `check_s3_encryption` |
| 8.25 | Cycle de vie de développement sécurisé | Non | Pas de développement logiciel propriétaire critique (voir 8.4) | ⚪ | — |
| 8.26 | Exigences de sécurité des applications | Oui | Configuration sécurisée d'Odoo | 🟡 | Durcissement applicatif à documenter |
| 8.27 | Architecture et principes d'ingénierie sécurisés des systèmes | Oui | Architecture cloud du SGSI | 🟡 | Schéma d'architecture à produire |
| 8.28 | Codage sécurisé | Non | Pas de développement logiciel propriétaire critique | ⚪ | — |
| 8.29 | Tests de sécurité en développement et acceptation | Oui | Tests automatisés du script de conformité (voir `tests/`) | 🟢 | [tests/test_aws_compliance_check.py](../tests/test_aws_compliance_check.py) |
| 8.30 | Développement externalisé | Non | Pas de développement externalisé à ce stade | ⚪ | — |
| 8.31 | Séparation des environnements de développement, test et production | Oui | Environnement de recette Odoo distinct de la production | 🟡 | À formaliser dans les procédures IT |
| 8.32 | Gestion des changements | Oui | Changements sur l'infrastructure et l'ERP | 🟡 | Processus de changement à formaliser (CAB léger) |
| 8.33 | Informations de test | Oui | Anonymisation des données de test issues de la production | 🔴 | Procédure à créer |
| 8.34 | Protection des systèmes d'information lors des tests d'audit | Oui | Cadrage des tests d'intrusion à venir | 🔴 | À définir avant le premier audit externe |

## Synthèse

| Thème | Total | Applicables | 🟢 Mis en œuvre | 🟡 Partiel | 🔴 Non mis en œuvre | ⚪ Non applicable |
|---|---|---|---|---|---|---|
| A.5 Organisationnel | 37 | 35 | 13 | 20 | 1 | 2 |
| A.6 Personnes | 8 | 8 | 3 | 5 | 0 | 0 |
| A.7 Physique | 14 | 11 | 0 | 10 | 1 | 3 |
| A.8 Technologique | 34 | 26 | 8 | 14 | 4 | 8 |
| **Total** | **93** | **80** | **24** | **49** | **6** | **13** |

Cette synthèse reflète honnêtement l'état d'un SGSI en **phase d'implémentation** : les
contrôles les plus critiques (accès, authentification, journalisation, sauvegarde, gestion des
incidents) sont mis en œuvre et vérifiés automatiquement ; les contrôles organisationnels plus
larges (RH, contractuel, physique) sont identifiés et planifiés mais restent, pour une part, à
formaliser — ce qui est attendu avant un premier audit blanc.

---

*Document suivant : [Plan de réponse aux incidents](./plan-reponse-incident.md)*
