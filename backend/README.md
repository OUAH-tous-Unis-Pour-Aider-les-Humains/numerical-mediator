# Backend starter (FastAPI + SQLAlchemy + Alembic)

Ce dossier contient une base de travail pour l'API Python du projet.

## Stack

- FastAPI
- SQLAlchemy 2.0
- Alembic
- PostgreSQL (driver psycopg v3)
- Celery + Redis (prepare, non branche sur des workers metier pour l'instant)

## Prerequis

- Python 3.11+
- PostgreSQL 16+
- Redis 7+ (si vous voulez tester Celery)

## Demarrage rapide avec Docker (PostgreSQL 16 + Redis 7)

Si vous n'avez pas PostgreSQL/Redis en local, vous pouvez lancer les deux services avec Docker.

PostgreSQL 16 (une seule ligne):

```bash
docker run -d --name nm-postgres -e POSTGRES_DB=numerical_mediator -e POSTGRES_USER=mediator -e POSTGRES_PASSWORD=mediator -p 5432:5432 postgres:16
```

Redis 7 (une seule ligne):

```bash
docker run -d --name nm-redis -p 6379:6379 redis:7
```

Verification rapide:

```bash
docker ps
docker exec -it nm-postgres psql -U mediator -d numerical_mediator -c "select version();"
docker exec -it nm-redis redis-cli ping
```

Resultat attendu pour Redis: `PONG`.

Important (commande multi-lignes):

Si vous copiez la commande `docker run` sur plusieurs lignes, chaque ligne doit se terminer par `\` (sauf la derniere), sinon Bash execute `-e` et `-p` comme des commandes separees.

Exemple correct:

```bash
docker run -d --name nm-postgres \
  -e POSTGRES_DB=numerical_mediator \
  -e POSTGRES_USER=mediator \
  -e POSTGRES_PASSWORD=mediator \
  -p 5432:5432 \
  postgres:16
```

## Installation

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Lancer l'API

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Ou via Makefile:

```bash
cd backend
make run
```

Le Makefile utilise automatiquement `backend/.venv` si present, sinon `../.venv`.

Endpoints de base:

- GET /health
- GET /docs
- POST /system/celery/ping
- GET /system/celery/tasks/{task_id}

CRUD V1 expose:

- /classification-objets
- /donnees
- /formules-maths
- /hypotheses

## Migrations

```bash
cd backend
source .venv/bin/activate
alembic upgrade head
```

Pour generer une nouvelle migration apres modification des modeles:

```bash
alembic revision --autogenerate -m "describe change"
```

Ou via Makefile:

```bash
cd backend
make migrate
```

## Worker Celery

```bash
cd backend
source .venv/bin/activate
celery -A app.worker.celery_app.celery_app worker --loglevel=info
```

Ou via Makefile:

```bash
cd backend
make worker
```

## Tests

```bash
cd backend
source .venv/bin/activate
pytest -q
```

Ou via Makefile:

```bash
cd backend
make test
```

## Couverture de tests V1

La suite actuelle couvre les checks de base sur l'API et le contrat de schéma:

- `test_healthcheck`
- `test_classification_crud`
- `test_donnee_crud`
- `test_formule_maths_crud`
- `test_hypothese_crud`
- `test_celery_ping_and_status`
- `test_classification_schema_contract`
- `test_experimentation_schema_contract`
- `test_science_schema_contract`

Total actuel: 9 tests passants.

## Structure

- app/main.py: entree FastAPI
- app/core/config.py: configuration centralisee via variables d'environnement
- app/db/: base declarative SQLAlchemy + session
- app/models/: modeles metier (classification, experimentation, maths, science)
- app/schemas/: schemas d'entree/sortie API (Pydantic v2)
- app/repositories/: acces DB par agregat
- app/services/: logique applicative par agregat
- app/worker/: configuration Celery et tasks
- alembic/: configuration et scripts de migration

## Limites V1

- Authentification/autorisation non implementees.
- Pas de controles d'acces par utilisateur (ACL) sur les ressources.
- Regles metier avancees de fusion pour/contre non implementees.
- Pas de versioning/audit pour tracer les modifications.
- Suite de tests concentree sur smoke API + contrats de schema (pas encore de tests d'integration DB reelle).

## Prochaines etapes post-V1

1. Ajouter authentification + autorisations par ressource.
2. Etendre les validations metier transverses et la logique de fusion.
3. Ajouter des tests d'integration avec PostgreSQL/Redis reels.
4. Renforcer la qualite continue (lint/type-check/CI).

## Notes schema

Le schema implemente suit le diagramme de reference dans le fichier:

- ../schema_bdd_complet.html
