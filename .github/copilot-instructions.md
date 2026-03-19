# Instructions Copilot — numerical-mediator

## Projet en bref
- Objectif : connecter les arguments de plusieurs personnes et assembler une solution commune.
- Langue principale de la documentation : français.
- Le dépôt est actuellement centré sur la documentation et le cadrage d’architecture.

## Langages et technologies à privilégier (contexte cible)
- Frontend/app web : **TypeScript** avec **Next.js**.
- Service IA : **Python** (API dédiée type **FastAPI**).
- Données : **PostgreSQL** (modélisation de graphes via tables).
- Tâches lourdes / asynchrones : **Redis + queue** (ex: BullMQ).
- Ce dépôt ne contient pas encore l’implémentation complète : utiliser ce cadre comme direction d’architecture.

## Règles de contribution assistée par IA
- Faire le changement minimal correct, ciblé sur la demande.
- Ne pas ajouter de dépendance sans justification explicite.
- Ne pas introduire de secrets, clés, tokens ou données personnelles.
- Mettre à jour la documentation si le comportement ou le workflow change.
- Demander clarification si une exigence est ambiguë.
- Privilégier des PR petites, relisibles et faciles à reviewer.

## Standards de qualité attendus
- L’humain reste responsable de la validation finale.
- Respecter **Conventional Commits** (`feat:`, `fix:`, `docs:`, etc.).
- Séparer clairement faits, explications et guides pratiques dans la documentation.
- Documenter les décisions d’architecture importantes dans `docs/adr/`.
- Maintenir une hygiène sécurité minimale (pas de secrets, validation des entrées, moindre privilège).

## Documentation (IA-friendly)
- Écrire des sections courtes, avec titres explicites et listes actionnables.
- Ajouter des exemples concrets et copier-coller quand utile.
- Relier les documents entre eux (`README.md`, `CONTRIBUTING.md`, `docs/`).
- Éviter le jargon non expliqué.

## Vérifications avant proposition finale
- Vérifier localement tout ce qui est disponible dans ce dépôt.
- Si une infra lint/test/build existe, la lancer avant de finaliser.
- Ne pas corriger des sujets hors périmètre de la demande.
