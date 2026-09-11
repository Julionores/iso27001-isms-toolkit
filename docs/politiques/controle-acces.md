# Politique de contrôle d'accès

| | |
|---|---|
| **Contrôles ISO 27001 couverts** | 5.15, 5.16, 5.18, 8.2, 8.3 |
| **Applicable à** | Tous les systèmes du périmètre : compte AWS, ERP Odoo, messagerie |

## 1. Principe du moindre privilège

Aucun utilisateur, service ou compte technique ne dispose d'un accès au-delà du strict
nécessaire à sa fonction. Toute demande d'accès supplémentaire doit être justifiée par un
besoin métier explicite et approuvée par le responsable du processus concerné.

## 2. Identifiants individuels (contrôle 5.16)

- Chaque collaborateur dispose d'un identifiant **unique et nominatif** — aucun compte
  partagé n'est toléré, y compris pour les comptes de service ou d'astreinte.
- Les comptes AWS suivent le modèle IAM : un utilisateur IAM par personne, jamais de partage
  des identifiants du compte racine.
- Le compte racine AWS n'est utilisé que pour les rares opérations qui l'exigent
  (facturation) ; il est protégé par une authentification multifacteur (MFA) matérielle et
  ses clés d'accès programmatiques sont désactivées. *(Vérifié automatiquement par le script
  `check_root_mfa`.)*

## 3. Attribution et revue des droits (contrôle 5.18)

| Étape | Responsable | Fréquence |
|---|---|---|
| Attribution d'un accès à l'arrivée | Responsable IT, sur validation du manager | À l'arrivée |
| Revue des droits en cours de contrat | RSSI + manager | Trimestrielle |
| Révocation à la sortie ou au changement de poste | Responsable IT, sur notification RH | Sous 24 heures |
| Revue des accès des comptes prestataires/fournisseurs | RSSI | Trimestrielle (traite le risque R8) |

Les comptes IAM inactifs depuis plus de 90 jours sont désactivés automatiquement puis
supprimés après validation du RSSI.

## 4. Comptes et accès à privilège (contrôle 8.2)

- Les comptes disposant de droits d'administration (IAM, base de données, ERP) sont
  **distincts** des comptes utilisés pour les tâches courantes — un administrateur utilise un
  compte nominatif standard au quotidien, et n'endosse un rôle à privilège que pour les
  opérations qui l'exigent.
- Toute politique IAM accordant un accès large (`"Action": "*"` ou `"Resource": "*"`) doit être
  justifiée explicitement et documentée ; à défaut, elle est considérée non conforme.
  *(Vérifié automatiquement par le script `check_iam_wildcard_policies`.)*
- L'authentification multifacteur est **obligatoire** pour tout compte disposant de droits
  d'administration, sur le cloud comme sur l'ERP.

## 5. Restriction d'accès à l'information (contrôle 8.3)

Dans l'ERP Odoo, les droits sont organisés par rôle métier (ventes, achats, comptabilité,
RH) et non par individu, afin de garantir la cohérence lors des changements de poste :

| Rôle Odoo | Périmètre de données accessible |
|---|---|
| Commercial | Fiches clients et commandes de son portefeuille uniquement |
| Comptabilité | Factures, paiements, aucune donnée RH |
| Responsable achats | Fournisseurs, bons de commande, aucune donnée de facturation client |
| Administrateur système | Configuration technique — pas d'accès direct aux données métier sans levée de droit temporaire |

## 6. Accès distant

Tout accès distant à l'ERP ou à l'infrastructure cloud s'effectue via une connexion chiffrée
(HTTPS/TLS) et un compte nominatif avec MFA. L'usage d'un réseau Wi-Fi public sans VPN pour
accéder aux systèmes de gestion est proscrit (voir la charte de télétravail, contrôle 6.7).

---

*Contrôle vérifié automatiquement : `controls/aws_compliance_check.py::check_root_mfa`,
`::check_iam_wildcard_policies`*
