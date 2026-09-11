# Politique de sensibilisation et de formation à la sécurité

| | |
|---|---|
| **Contrôles ISO 27001 couverts** | 6.3 |
| **Applicable à** | L'ensemble des collaborateurs, y compris les nouveaux arrivants |
| **Risque traité** | R7 (hameçonnage) — voir [analyse des risques](../analyse-risques.md) |

## 1. Pourquoi cette politique

Le risque R7 (hameçonnage ciblant les identifiants ERP) a été évalué comme critique
(probabilité quasi certaine, impact majeur) alors même qu'aucun contrôle technique ne peut
totalement neutraliser une erreur humaine. La sensibilisation des collaborateurs est donc un
contrôle à part entière du SGSI, au même titre qu'un contrôle technique.

## 2. Programme de sensibilisation

| Moment | Contenu | Format | Public |
|---|---|---|---|
| Arrivée (dans les 15 jours) | Charte informatique, reconnaissance des tentatives de phishing, procédure de signalement | Session de 45 min + support écrit signé | Tout nouvel arrivant |
| Annuelle | Rappel des bonnes pratiques, retour sur les incidents de l'année (anonymisés), nouveautés réglementaires | Session de 1 heure | Tous les collaborateurs |
| Ciblée | Sensibilisation renforcée après un incident ou une campagne de phishing simulée | Session courte (20 min) | Service concerné |

## 3. Contenu minimal de la formation

- Reconnaître un e-mail de phishing (expéditeur usurpé, urgence artificielle, lien suspect,
  pièce jointe inattendue).
- Ne jamais communiquer un mot de passe, y compris à une personne se présentant comme le
  support IT.
- Procédure de signalement immédiat (voir le
  [plan de réponse aux incidents](../plan-reponse-incident.md#1-signalement-contrôle-68)).
- Bonnes pratiques de mot de passe et usage du MFA (voir
  [mots-de-passe-authentification.md](./mots-de-passe-authentification.md)).
- Règles de classification des données et de partage sécurisé (voir
  [classification-donnees.md](./classification-donnees.md)).
- Bonnes pratiques du télétravail (réseaux Wi-Fi publics, verrouillage de session).

## 4. Campagnes de simulation de phishing

Une campagne de simulation d'e-mail de phishing (interne, sans conséquence disciplinaire pour
les premiers clics) est menée deux fois par an, avec :

- mesure du taux de clic et du taux de signalement ;
- session de sensibilisation ciblée pour les services ayant un taux de clic élevé, sans jamais
  nommer individuellement les collaborateurs concernés ;
- suivi de la tendance du taux de clic d'une campagne à l'autre comme indicateur du programme.

## 5. Suivi et indicateurs

| Indicateur | Cible |
|---|---|
| Taux de collaborateurs ayant suivi la sensibilisation annuelle | 100 % |
| Taux de clic lors des campagnes de simulation de phishing | < 10 %, en baisse d'une campagne à l'autre |
| Taux de signalement spontané d'un e-mail suspect | En hausse d'une campagne à l'autre |

Ces indicateurs sont présentés en revue annuelle du SGSI, avec les résultats des contrôles
techniques automatisés, pour donner une vision complète de la maturité sécurité de
l'organisation (humaine et technique).

---

*Contrôle non automatisable par nature — suivi déclaratif et mesure des campagnes de simulation.*
