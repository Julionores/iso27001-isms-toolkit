# ISO 27001 ISMS Toolkit — Politique de sécurité + contrôles automatisés

[![CI](https://github.com/Julionores/iso27001-isms-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Julionores/iso27001-isms-toolkit/actions/workflows/ci.yml)

Un **Système de Management de la Sécurité de l'Information (SGSI)** complet, conforme
**ISO/IEC 27001:2022**, pour une PME fictive utilisant un ERP (NovaDistrib) — avec, à côté de la
documentation de gouvernance, un **script Python testé** qui vérifie automatiquement une partie
réelle de cette politique contre un compte AWS.

> Projet réalisé par **Junior Tsafack Megnekeu** ([blog.jtmcloud.com](https://blog.jtmcloud.com) ·
> [GitHub](https://github.com/Julionores) ·
> [LinkedIn](https://www.linkedin.com/in/junior-tsafack-megnekeu-b673151b9)) — pièce d'un
> portfolio technique orienté DevSecOps / gouvernance de la sécurité. Voir aussi
> [`devsecops-pipeline-reference`](https://github.com/Julionores/devsecops-pipeline-reference),
> [`securebank-api`](https://github.com/Julionores/securebank-api) et
> [`postgresql-ha-repmgr`](https://github.com/Julionores/postgresql-ha-repmgr). Ce projet
> complète mon [cours Cybersécurité](https://blog.jtmcloud.com/securite/), qui couvre notamment
> le panorama des certifications dont ISO/IEC 27001. Côté Cloud AWS, voir aussi
> [`dynamodb-streams-cdc-pipeline`](https://github.com/Julionores/dynamodb-streams-cdc-pipeline),
> [`aws-troubleshooting-challenge`](https://github.com/Julionores/aws-troubleshooting-challenge),
> [`s3-cross-region-replication`](https://github.com/Julionores/s3-cross-region-replication),
> [`aws-alb-deployment-patterns`](https://github.com/Julionores/aws-alb-deployment-patterns) et
> [`aws-vpc-connectivity-patterns`](https://github.com/Julionores/aws-vpc-connectivity-patterns).
> Côté Machine Learning, voir aussi [`gradientforge`](https://github.com/Julionores/gradientforge),
> [`radar-risque-impaye`](https://github.com/Julionores/radar-risque-impaye),
> [`collecte-agricole-planner`](https://github.com/Julionores/collecte-agricole-planner),
> [`ticket-tide`](https://github.com/Julionores/ticket-tide),
> [`inspectline`](https://github.com/Julionores/inspectline),
> [`runbook-rag`](https://github.com/Julionores/runbook-rag), un assistant documentaire RAG,
> [`agent-matching-recrutement`](https://github.com/Julionores/agent-matching-recrutement),
> un agent à outils multiples avec relâchement de contraintes, et
> [`mcp-odoo-toolkit`](https://github.com/Julionores/mcp-odoo-toolkit).

## Pourquoi ce projet

Un SGSI ISO 27001 se réduit trop souvent, dans les portfolios techniques, à un classeur de
documents non vérifiables. Ici, chaque contrôle technique important de la
[déclaration d'applicabilité](docs/declaration-applicabilite.md) est relié à un test concret :
un script qui interroge réellement l'API AWS (via `boto3`) et répond « conforme » ou « non
conforme », plutôt qu'une simple case cochée sur la foi d'une déclaration.

## Structure du dépôt

```
docs/
├── politique-securite-information.md   # Document racine du SGSI (portée, rôles, objectifs)
├── analyse-risques.md                  # Registre des risques (méthode ISO 27005 simplifiée)
├── declaration-applicabilite.md        # SoA — les 93 contrôles de l'annexe A, un par un
├── plan-reponse-incident.md            # Runbook : détection → confinement → reprise → REX
└── politiques/                         # 5 politiques thématiques (accès, mots de passe,
                                         # classification des données, incidents, sauvegardes,
                                         # sensibilisation)
controls/
├── aws_compliance_check.py             # Script d'audit (6 contrôles techniques vérifiés)
└── conformance-pack/
    └── isms-conformance-pack.yaml      # Équivalent AWS Config (surveillance continue)
tests/
└── test_aws_compliance_check.py        # 18 tests, dont un test d'intégration avec `moto`
```

## Les 6 contrôles automatisés

| Contrôle ISO 27001 | Vérification | Risque associé |
|---|---|---|
| 8.2 / 8.5 | MFA activé sur le compte racine AWS | R1 |
| 8.2 | Aucune politique IAM n'accorde `Action:*` + `Resource:*` | R9 |
| 5.17 | La politique de mot de passe du compte respecte les exigences minimales | R3 |
| 8.12 | Le blocage d'accès public S3 est actif au niveau du compte | R2 |
| 8.24 | Tous les compartiments S3 ont un chiffrement par défaut | R6 |
| 8.15 | Au moins un trail CloudTrail multi-régions journalise | R5 |

Chaque contrôle est documenté en détail dans la politique thématique correspondante (voir
[`docs/politiques/`](docs/politiques/)) et repris dans le
[registre des risques](docs/analyse-risques.md).

Le [conformance pack AWS Config](controls/conformance-pack/isms-conformance-pack.yaml) couvre
les mêmes contrôles pour une **surveillance continue**, en complément d'une exécution ponctuelle
du script (tâche planifiée, pipeline CI/CD, ou audit manuel).

## Utilisation

### Exécuter l'audit contre un vrai compte AWS

Nécessite des identifiants AWS en lecture seule (`iam:Get*`, `iam:List*`,
`s3:GetBucketEncryption`, `s3:ListAllMyBuckets`, `s3control:GetPublicAccessBlock`,
`cloudtrail:DescribeTrails`, `cloudtrail:GetTrailStatus`, `sts:GetCallerIdentity`).

```bash
pip install -r controls/requirements.txt
python controls/aws_compliance_check.py
echo $?   # 0 si tous les contrôles sont conformes, 1 sinon
```

### Lancer les tests (aucun compte AWS requis)

```bash
python -m venv .venv
source .venv/Scripts/activate   # ou .venv/bin/activate sous Linux/macOS
pip install -r requirements-dev.txt
pytest -v
```

Les tests unitaires simulent les réponses de l'API AWS (`unittest.mock`), et un test
d'intégration exécute le pipeline complet contre un compte AWS entièrement simulé par
[`moto`](https://github.com/getmoto/moto) — aucun coût, aucune dépendance réseau.

### Déployer le conformance pack AWS Config

```bash
aws configservice put-conformance-pack \
  --conformance-pack-name isms-novadistrib \
  --template-body file://controls/conformance-pack/isms-conformance-pack.yaml
```

Nécessite qu'AWS Config soit déjà activé sur le compte (enregistreur de configuration et canal
de livraison).

## Ce que ce projet assume ne pas couvrir

Une déclaration d'applicabilité honnête documente aussi ses limites :

- Les **93 contrôles** de l'annexe A sont tous statués dans la
  [SoA](docs/declaration-applicabilite.md), mais seuls les plus critiques et vérifiables
  techniquement sont **automatisés** — les contrôles organisationnels (RH, contractuel,
  physique) restent, à ce stade, déclaratifs.
- Aucun audit de certification réel n'a été mené : ce dépôt documente la **démarche et l'outillage**
  d'un SGSI, pas une certification obtenue.
- Le scénario NovaDistrib est fictif ; les données chiffrées, montants de risque et indicateurs
  sont illustratifs.

## Feuille de route

- [ ] Automatiser le test trimestriel de restauration des sauvegardes (actuellement manuel,
      voir [`continuite-activite-sauvegardes.md`](docs/politiques/continuite-activite-sauvegardes.md))
- [ ] Étendre le script de conformité aux contrôles réseau (VPC, groupes de sécurité — 8.20/8.22)
- [ ] Ajouter un contrôle vérifiant l'activation d'Amazon GuardDuty (8.16)
- [ ] Premier audit blanc externe avant certification (contrôle 5.35)

## Licence

MIT — voir [`LICENSE`](LICENSE). Projet à but pédagogique et de démonstration.
