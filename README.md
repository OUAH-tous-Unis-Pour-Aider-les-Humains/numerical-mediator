# numerical-mediator
An open source application to connect people’s arguments and assemble the solution.

## 🤝 Collaboration humain + IA (Copilot / Coding Agent)
Ce dépôt est préparé pour une contribution assistée par IA avec un cadre explicite :

- Instructions IA : [`.github/copilot-instructions.md`](./.github/copilot-instructions.md)
- Guide de contribution : [`CONTRIBUTING.md`](./CONTRIBUTING.md)
- Politique de sécurité : [`SECURITY.md`](./SECURITY.md)
- Code de conduite : [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md)
- Modèle de Pull Request : [`.github/PULL_REQUEST_TEMPLATE.md`](./.github/PULL_REQUEST_TEMPLATE.md)

Principes d'utilisation :
- l’humain reste responsable des décisions et de la revue finale ;
- les changements doivent rester petits, testés et documentés ;
- aucune donnée sensible ne doit être ajoutée au code.

## 👋 Nouveaux arrivants : rejoignez la discussion
Vous découvrez le projet ? N’hésitez pas à passer par l’onglet **Discussions** du repo pour poser vos questions, partager vos idées et proposer des orientations d’architecture.

## Prototype local disponible (Next.js + PostgreSQL + Ollama)
Le dépôt contient maintenant un premier prototype exécutable en local dans [`/web`](./web) :

- frontend Next.js (TypeScript) ;
- API `/api/graph` connectée à PostgreSQL ;
- affichage d’un schéma avec **React Flow** (zoom/pan natifs) ;
- génération d’un schéma depuis un texte via **Ollama local** (`/api/text-to-graph`) ;
- scripts d’initialisation/seed de base ;
- tests automatiques unitaires de la logique de schéma.

### Démarrage local rapide
Prérequis : Docker + Node.js 20+ + Ollama

**Option 1 : Automatisé (recommandé)**

```bash
# Première utilisation : configuration complète
./launch.sh --full

# Puis démarrer le serveur
./launch.sh --quick
```

Voir `./launch.sh --help` pour toutes les options.

**Option 2 : Manuel**

1. Démarrer PostgreSQL local :

```bash
docker compose up -d db
```

2. Installer l'app web et configurer l'environnement :

```bash
cd web
npm install
cp .env.example .env.local
```

3. Démarrer Ollama et télécharger le modèle local recommandé :

```bash
ollama serve
ollama pull qwen2.5:7b
```

4. Initialiser le schéma SQL et charger des données factices :

```bash
npm run db:init
npm run db:seed
```

5. Lancer le site en local :

```bash
npm run dev
```

Puis ouvrir [http://localhost:3000](http://localhost:3000).

### Variables d’environnement (`web/.env.local`)

```env
DATABASE_URL=postgres://mediator:mediator@localhost:5432/numerical_mediator
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_TIMEOUT_MS=120000
TEXT_TO_GRAPH_MAX_CHARS=5000
```

### Parcours POC (texte → schéma)

1. Saisir un texte dans le panneau "Générer un schéma avec Ollama".
2. Choisir le modèle local (qwen2.5:7b, llama3:latest, mistral:7b) ou saisir un modèle personnalisé.
3. Cliquer sur "Générer le schéma".
4. L’API `/api/text-to-graph` appelle Ollama, génère un graphe JSON puis le persiste en base.
5. Le frontend recharge `/api/graph` et affiche le nouveau schéma dans React Flow.

### Vérification locale
Depuis `web/` :

```bash
npm run lint
npm run test
npm run build
```

### Dépannage rapide

- Erreur `DATABASE_URL doit être défini` : vérifier `web/.env.local`.
- Erreur Ollama indisponible : vérifier `ollama serve` et le port `11434`.
- Modèle absent : exécuter `ollama pull qwen2.5:7b`.

## GUIDE D'ARCHITECTURE D'UN NOUVEAU PROJET
### Contexte (adapté du message Discussions)
Objectif : construire une application web très interactive (hébergée sur Vercel) pour manipuler de grands schémas (milliers de nœuds), avec filtrage, zoom, navigation fluide, regroupements superposables, puis ajouter :
- une IA qui transforme un texte utilisateur en schéma,
- une logique de fusion de schémas,
- un système de comptes avec sauvegarde personnalisée.

### Structure recommandée (vue d’ensemble)
1. **Frontend (Next.js + TypeScript)**  
   - Canvas interactif (zoom, pan, sélection, filtres, labels, flèches, groupes).  
   - Chargement progressif : récupérer uniquement le sous-graphe utile côté client.
   - Envoie des modifications faites au schéma au backend lors de la sauvegarde du schéma.
2. **API / Backend (Route Handlers Next.js ou service dédié Node.js)**  
   - Endpoints pour lecture/écriture de graphes, filtres, fusion, permissions.  
   - Validation stricte des entrées (schémas JSON, ACL utilisateur).
3. **Base de données (PostgreSQL)**  
   - Modèle orienté graphe via tables `nodes`, `edges`, `groups`, `diagrams`, `diagram_versions`.  
   - Indexation et pagination pour supporter des milliers de nœuds.
4. **Moteur de fusion et logique métier**  
   - Service dédié pour merger deux schémas (détection de conflits, stratégie de résolution).  
   - Versionnement pour revenir en arrière.
5. **IA personnalisée (pipeline séparé)**  
   - Étape 1 : extraction structurée texte → entités/relations.  
   - Étape 2 : génération d’un graphe validé contre un schéma métier.  
   - Étape 3 : validation humaine avant fusion dans le schéma principal.
6. **Auth & comptes utilisateurs**  
   - Auth robuste (sessions, rôles, ownership des schémas).  
   - Sauvegarde des schémas personnels et des parties modifiées du schéma principal.

### Technologies conseillées
- **UI Graphe** : React Flow (production-ready pour éditeurs de nœuds), éventuellement Cytoscape.js pour besoins analytiques avancés.
- **App Web** : Next.js + TypeScript (intégration Vercel naturelle).
- **Données** : PostgreSQL + Prisma (ou Drizzle) pour la maintenabilité.
- **Cache / file de tâches** : Redis + queue (BullMQ) pour traitements lourds (fusion, IA).
- **Recherche / filtres** : index SQL + éventuellement moteur dédié (OpenSearch) selon volumétrie.
- **IA** : service isolé (Python/FastAPI) pour itérer sur les modèles sans coupler le frontend.

### Inspirations de projets et sources de confiance
- **Vercel / Next.js docs** : architecture App Router, scaling et déploiement.
- **React Flow documentation** : patterns d’éditeurs de graphes interactifs.
- **PostgreSQL documentation** : indexation, performance et transactions.
- **Prisma documentation** : modélisation et migrations fiables.
- **OWASP ASVS / Cheat Sheets** : sécurité applicative (auth, validation, contrôle d’accès).

### Plan de réalisation conseillé
1. **MVP graphe** : nœuds/edges/groupes + zoom/pan + sauvegarde DB.
2. **Scalabilité** : pagination de graphe, chargement partiel, cache.
3. **Collaboration** : comptes, permissions, versioning.
4. **Fusion métier** : règles de merge + résolution de conflits.
5. **IA assistée** : texte → proposition de schéma, puis validation utilisateur.
