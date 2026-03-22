# Prototype web local (Next.js + React Flow + Ollama)

Cette application est la première implémentation locale de **numerical-mediator**.

## Prérequis
- Node.js 20+
- Docker (pour PostgreSQL local)
- Ollama

## Configuration
```bash
npm install
cp .env.example .env.local
```

## IA locale (Ollama)

```bash
ollama serve
ollama pull qwen2.5:7b
```

## Base de données
Depuis la racine du dépôt :

```bash
docker compose up -d db
```

Puis depuis `web/` :

```bash
npm run db:init
npm run db:seed
```

## Lancer en local
```bash
npm run dev
```

Ouvrir [http://localhost:3000](http://localhost:3000).

## Tests et qualité
```bash
npm run lint
npm run test
npm run build
```

## Fonctionnalités MVP incluses
- API `/api/graph` connectée à PostgreSQL
- API `/api/text-to-graph` connectée à Ollama local
- chargement des données réelles côté frontend
- canvas de schéma avec React Flow (zoom/pan natifs)
- données factices injectées via `db:seed`
