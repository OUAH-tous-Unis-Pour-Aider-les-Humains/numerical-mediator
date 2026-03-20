# Instructions Copilot — numerical-mediator

## Contexte du projet

**numerical-mediator** est une application open source pour relier des arguments et construire des solutions collectives.

## Stack cible

- **Front-end** : Next.js / TypeScript
- **Base de données** : PostgreSQL 16
- **File de messages** : Redis + BullMQ
- **Service IA** : Python / FastAPI

## Conventions

- Documentation et commentaires en **français**
- Commits au format [Conventional Commits](https://www.conventionalcommits.org/)
- Revues de code via Pull Requests avec le template `.github/PULL_REQUEST_TEMPLATE.md`

## Infrastructure locale (Docker)

L'environnement local est géré via `docker-compose.yml` à la racine.  
Voir `README.md` pour les instructions de démarrage.
