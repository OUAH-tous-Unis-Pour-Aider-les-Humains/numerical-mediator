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
   - Modèle orienté graphe via tables
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
1. **Base de données** : postgreSQL
2. **MVP graphe** : nœuds/edges/groupes + zoom/pan + sauvegarde DB.
3. **Scalabilité** : pagination de graphe, chargement partiel, cache.
4. **Collaboration** : comptes, permissions, versioning.
5. **Fusion métier** : règles de merge + résolution de conflits.
6. **IA assistée** : texte → proposition de schéma, puis validation utilisateur.

## Backend Python (démarrage implémentation)

Le dossier [`backend/`](./backend/) est maintenant initialisé avec un starter exécutable :

- FastAPI (`app/main.py`) ;
- SQLAlchemy 2.0 avec modèles du schéma complet ;
- Alembic avec une migration initiale ;
- configuration d'environnement via `.env`.

Fonctionnalités V1 déjà implémentées :

- CRUD API pour `classification_objet`, `donnee`, `formule_maths`, `hypothese` ;
- endpoint de test asynchrone `POST /system/celery/ping` ;
- structure `schemas/repositories/services` pour industrialiser la suite.

Pour démarrer rapidement, suivre le guide :

- [`backend/README.md`](./backend/README.md)

Source de vérité du schéma relationnel implémenté :

- [`schema_bdd_complet.html`](./schema_bdd_complet.html)
