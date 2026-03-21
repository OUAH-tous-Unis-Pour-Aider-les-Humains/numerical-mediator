# Prototype web local (Next.js)

Cette application est la première implémentation locale de **numerical-mediator**.

## Prérequis
- Node.js 20+
- Docker (pour PostgreSQL local)

## Configuration
```bash
npm install
cp .env.example .env.local
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
- chargement des données réelles côté frontend
- canvas de schéma avec :
  - zoom (+/− et molette)
  - déplacement (cliquer + glisser)
- données factices injectées via `db:seed`
