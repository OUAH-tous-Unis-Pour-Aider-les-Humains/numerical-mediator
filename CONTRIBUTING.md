# Guide de contribution

Merci de contribuer à **numerical-mediator**.

## Démarrage rapide (Local)

Pour lancer le projet localement, utilisez le script d'automatisation :

```bash
# Première utilisation : setup complet
./launch.sh --full

# Puis démarrer le serveur
./launch.sh --quick
```

Pour plus d'options, consultez : `./launch.sh --help`

**Prérequis :**
- Docker + Docker Compose
- Node.js 20+
- Ollama (optionnel mais recommandé)

## Workflow de contribution (humain + IA)

1. Ouvrir une issue avec contexte, problème et résultat attendu.
2. Créer une branche dédiée depuis `main`.
3. Demander une proposition IA sur un périmètre réduit.
4. Relire chaque changement (code et documentation).
5. Vérifier localement ce qui est disponible dans ce dépôt.
6. Ajouter/mettre à jour les tests quand une infrastructure de tests existe.
7. Mettre à jour la documentation liée.
8. Ouvrir une Pull Request avec une description claire.

## Conventions

- Commits : style **Conventional Commits** (`feat:`, `fix:`, `docs:`, etc.).
- PR : utiliser le template de Pull Request.
- Sécurité : suivre [`SECURITY.md`](./SECURITY.md), ne jamais publier de secret.
- Conduite : suivre [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md).

## Besoin d'aide

- Utiliser l'onglet Discussions pour échanger sur l'architecture et les choix de mise en œuvre.
