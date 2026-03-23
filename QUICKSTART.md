# 🚀 Quick Start Guide - numerical-mediator

## TL;DR - Get Running in 3 Steps

### 1. First Time Only
```bash
./launch.sh --full
```
This checks prerequisites, starts PostgreSQL, installs dependencies, and initializes the database.

### 2. Start the Dev Server
```bash
./launch.sh --quick
```
This starts PostgreSQL and the development server.

### 3. Open in Browser
```
http://localhost:3000
```

---

## Commands Reference

| Command | What It Does |
|---------|-------------|
| `./launch.sh --full` | Complete setup (first time) |
| `./launch.sh --quick` | Start services (usual workflow) |
| `./launch.sh --status` | Check what's running |
| `./launch.sh --clean` | Reset everything |
| `./launch.sh --stop` | Stop PostgreSQL |
| `./launch.sh --help` | Show all options |

---

## Prerequisites

Before running, make sure you have:

- ✅ Docker & Docker Compose
- ✅ Node.js 20+
- ✅ npm
- ℹ️ Ollama (optional, for AI features)

## Troubleshooting

### Port Already in Use
If port 3000 or 5432 is already in use, stop existing services:
```bash
# Stop the dev server
Ctrl+C (in the terminal running launch.sh)

# Stop PostgreSQL
./launch.sh --stop
```

### Database Issues
Reset the database:
```bash
./launch.sh --clean
./launch.sh --quick
```

### Missing Dependencies
Install what's needed:
```bash
# Check what's missing
./launch.sh --status

# Install specific tools:
# - Node.js: https://nodejs.org/
# - Docker: https://www.docker.com/products/docker-desktop
# - Ollama: https://ollama.ai
```

### Ollama Not Running
In a separate terminal:
```bash
ollama serve
```

---

## Development Workflow

1. **Make Code Changes**: Edit files in `web/src/`
2. **Dev Server Auto-Reloads**: Changes reflect instantly
3. **Run Tests**: `npm run test` (from `web/` directory)
4. **Build for Production**: `npm run build` (from `web/` directory)

---

## Project Structure

```
numerical-mediator/
├── launch.sh              ← Use this to start!
├── docker-compose.yml     ← PostgreSQL config
├── README.md              ← Full documentation
├── CONTRIBUTING.md        ← How to contribute
└── web/                   ← Next.js application
    ├── src/
    ├── package.json
    └── .env.local         ← Auto-created
```

---

## API Endpoints

Once running, access:

- **Frontend**: http://localhost:3000
- **API - Get Graph**: `GET /api/graph`
- **API - Generate from Text**: `POST /api/text-to-graph`

---

## Useful npm Scripts (from `web/` directory)

```bash
npm run dev       # Start dev server with hot reload
npm run build     # Create production build
npm run start     # Run production build
npm run lint      # Check code quality
npm run test      # Run unit tests
npm run db:init   # Initialize database schema
npm run db:seed   # Load sample data
```

---

## Need Help?

- 📖 **Full Documentation**: Read `README.md`
- 🤝 **Contributing**: See `CONTRIBUTING.md`
- 💬 **Questions**: Use the Discussions tab in GitHub
- 🔒 **Security**: Check `SECURITY.md`

---

**Happy coding! 🎉**
