# ADR-0002 : Stack backend Python (API + donnees + migrations)

**Date** : 2026-04-06  
**Statut** : Accepte

## Contexte

Le projet entre en phase d'implementation backend. Le schema relationnel de reference est decrit dans `schema_bdd_complet.html`.

Un cadrage explicite est necessaire pour:
- la pile API Python;
- l'acces aux donnees PostgreSQL;
- la gestion des migrations;
- la trajectoire des taches asynchrones.

## Decision

Le backend adopte les choix suivants:

- API: FastAPI
- Base de donnees: PostgreSQL
- ORM/acces SQL: SQLAlchemy 2.0 en approche mixte ORM + Core
- Migrations: Alembic
- Asynchrone: Celery avec Redis (broker/result backend)

Le schema V1 implemente couvre les sections suivantes:
- classification;
- experimentation;
- maths;
- science.

## Consequences

- Les evolutions de schema passent par migrations versionnees Alembic.
- Les modeles Python restent separes par section metier dans `backend/app/models/`.
- La structure backend est prete pour brancher des workers Celery sans coupler la logique metier a l'API HTTP.
- Le cout d'entree est faible pour contribuer: stack standard, tooling mature et documentation native FastAPI.

## Decisions differees

- Choix final du mode d'execution production (ASGI workers, observabilite, orchestration).
- Strategie d'authentification et d'autorisation.
- Politique de tests integration DB (conteneurs ephemeres, environnement CI dedie).
