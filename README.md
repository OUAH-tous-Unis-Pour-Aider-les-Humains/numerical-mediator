# numerical-mediator

An open source application to connect people's arguments and assemble the solution.

## Prérequis

- [Docker](https://docs.docker.com/get-docker/) ≥ 24
- [Docker Compose](https://docs.docker.com/compose/install/) ≥ 2 (inclus dans Docker Desktop ; sur Linux, vérifiez avec `docker compose version`)

## Démarrage rapide (Linux)

```bash
# 1. Copiez le fichier d'environnement et renseignez POSTGRES_PASSWORD
cp .env.example .env

# 2. Démarrez la base de données PostgreSQL
docker compose up -d postgres

# 3. Vérifiez que le service est en bonne santé
docker compose ps
```

Le service est prêt quand la colonne **Status** affiche `healthy`.

## Problèmes courants sur Linux

| Symptôme | Cause probable | Solution |
|---|---|---|
| `Error: password authentication failed` | `POSTGRES_PASSWORD` absent ou vide | Assurez-vous que `.env` contient `POSTGRES_PASSWORD=<valeur>` |
| `Bind for 0.0.0.0:5432 failed: port is already allocated` | Le port 5432 est déjà utilisé | Changez `POSTGRES_PORT=5433` dans `.env` |
| `permission denied` sur le volume | SELinux/AppArmor ou droits insuffisants | Ajoutez `:z` au volume dans `docker-compose.yml` (ex: `postgres_data:/var/lib/postgresql/data:z`) ou corrigez l'appartenance du dossier : `sudo chown -R 999:999 <dossier>` (UID/GID de l'utilisateur postgres dans le conteneur) |
| `Cannot connect to the Docker daemon` | Le démon Docker n'est pas démarré | `sudo systemctl start docker` puis ajoutez votre utilisateur au groupe docker : `sudo usermod -aG docker $USER` (reconnectez-vous ensuite) |

## Variables d'environnement

Voir `.env.example` pour la liste complète.
