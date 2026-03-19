# Agent context — architecture

## Objectif
- Aider à formuler des décisions d’architecture cohérentes avec le dépôt.

## Cadre technique cible
- Frontend : **Next.js + TypeScript**
- Service IA : **Python + FastAPI**
- Données : **PostgreSQL**
- Asynchrone (côté TypeScript/Next.js) : **Redis + BullMQ**
- Asynchrone (côté Python/FastAPI) : utiliser une queue Python compatible Redis.

## Contraintes
- Proposer des changements minimaux et relisibles.
- Documenter les décisions importantes dans `docs/adr/`.
- Rester aligné avec `.github/copilot-instructions.md`.
