#!/bin/bash

##############################################################################
# numerical-mediator: Project Launch Script
# 
# This script automates the complete setup and launch of the numerical-mediator
# application, including:
#   - Docker PostgreSQL database
#   - Environment configuration
#   - Node.js dependencies
#   - Database initialization
#   - Development server startup
#
# Usage:
#   ./launch.sh                  # Interactive mode (prompts for choices)
#   ./launch.sh --full           # Full setup + start dev server
#   ./launch.sh --quick          # Quick start (assumes setup is done)
#   ./launch.sh --clean          # Clean slate: reset DB and restart all
#   ./launch.sh --help           # Show this help message
##############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

# Project paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEB_DIR="${SCRIPT_DIR}/web"
ENV_FILE="${WEB_DIR}/.env.local"

##############################################################################
# Helper Functions
##############################################################################

print_header() {
  echo -e "\n${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
  echo -e "${BLUE}║${NC} $1"
  echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}\n"
}

print_success() {
  echo -e "${GREEN}✓${NC} $1"
}

print_error() {
  echo -e "${RED}✗${NC} $1"
}

print_warning() {
  echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
  echo -e "${BLUE}ℹ${NC} $1"
}

check_dependency() {
  if ! command -v "$1" &> /dev/null; then
    print_error "$1 is not installed"
    return 1
  fi
  print_success "$1 is installed"
}

check_prerequisites() {
  print_header "Checking Prerequisites"
  
  local missing_deps=0
  
  if ! check_dependency "node"; then
    missing_deps=1
  fi
  
  if ! check_dependency "npm"; then
    missing_deps=1
  fi
  
  if ! check_dependency "docker"; then
    missing_deps=1
  fi
  
  if ! check_dependency "docker-compose"; then
    missing_deps=1
  fi
  
  if [ $missing_deps -eq 1 ]; then
    print_error "Some dependencies are missing. Please install them:"
    echo "  • Node.js 18+ and npm: https://nodejs.org/"
    echo "  • Docker and Docker Compose: https://www.docker.com/products/docker-desktop"
    return 1
  fi
  
  # Check for Ollama (optional but recommended)
  if ! command -v ollama &> /dev/null; then
    print_warning "Ollama is not installed (optional but recommended for AI features)"
    print_info "Install from: https://ollama.ai"
  else
    print_success "Ollama is installed"
  fi
  
  print_success "All required dependencies are present"
}

check_environment_file() {
  if [ ! -f "$ENV_FILE" ]; then
    print_warning ".env.local not found, creating from template..."
    cat > "$ENV_FILE" << 'EOF'
# Database Configuration
DATABASE_URL=postgres://mediator:mediator@localhost:5432/numerical_mediator

# Ollama Configuration (Local AI)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_TIMEOUT_MS=120000

# Application Settings
TEXT_TO_GRAPH_MAX_CHARS=5000
NODE_ENV=development
EOF
    print_success ".env.local created at ${ENV_FILE}"
    print_info "Update this file with your configuration if needed"
  else
    print_success ".env.local already exists"
  fi
}

start_postgres() {
  print_header "Starting PostgreSQL Database"
  
  if docker ps --filter "name=numerical_mediator_db" --format "{{.State}}" | grep -q "running"; then
    print_success "PostgreSQL is already running"
    return 0
  fi
  
  if docker ps -a --filter "name=numerical_mediator_db" --format "{{.State}}" | grep -q "exited"; then
    print_info "Restarting existing PostgreSQL container..."
    docker compose -f "${SCRIPT_DIR}/docker-compose.yml" start db
  else
    print_info "Starting new PostgreSQL container..."
    docker compose -f "${SCRIPT_DIR}/docker-compose.yml" up -d db
  fi
  
  # Wait for database to be ready
  print_info "Waiting for PostgreSQL to be ready..."
  for i in {1..30}; do
    if docker exec numerical_mediator_db pg_isready -U mediator &> /dev/null; then
      print_success "PostgreSQL is ready"
      return 0
    fi
    echo -n "."
    sleep 1
  done
  
  print_error "PostgreSQL failed to start"
  return 1
}

install_dependencies() {
  print_header "Installing Node.js Dependencies"
  
  if [ -d "${WEB_DIR}/node_modules" ]; then
    print_info "node_modules already exists, checking for updates..."
    cd "$WEB_DIR" && npm install --prefer-offline --no-audit
  else
    print_info "Installing fresh dependencies..."
    cd "$WEB_DIR" && npm install
  fi
  
  print_success "Dependencies installed"
}

initialize_database() {
  print_header "Initializing Database"
  
  cd "$WEB_DIR"
  
  if npm run db:init 2>&1 | grep -q "already exists"; then
    print_info "Database schema already initialized"
  else
    print_success "Database schema initialized"
  fi
  
  print_info "Seeding sample data..."
  npm run db:seed
  print_success "Database seeded"
}

check_ollama() {
  print_header "Checking Ollama Status"
  
  if ! command -v ollama &> /dev/null; then
    print_warning "Ollama is not installed"
    echo "  To enable AI features, install from: https://ollama.ai"
    return 1
  fi
  
  # Try to connect to Ollama API
  if curl -s http://localhost:11434/api/tags &> /dev/null; then
    print_success "Ollama is running"
    
    # Check if the model is available
    if curl -s http://localhost:11434/api/tags | grep -q "qwen2.5"; then
      print_success "qwen2.5 model is available"
    else
      print_warning "qwen2.5 model not found, downloading..."
      print_info "This may take a few minutes on first run"
      ollama pull qwen2.5:7b
    fi
    return 0
  else
    print_warning "Ollama is not running"
    print_info "Start Ollama with: ollama serve"
    return 1
  fi
}

start_dev_server() {
  print_header "Starting Development Server"
  
  cd "$WEB_DIR"
  
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${GREEN}Development server is starting...${NC}"
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  echo -e "${GREEN}📱 Application URL:${NC} ${YELLOW}http://localhost:3000${NC}"
  echo -e "${GREEN}📡 API Routes:${NC}"
  echo -e "   • GET  /api/graph"
  echo -e "   • POST /api/text-to-graph"
  echo ""
  echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
  echo ""
  
  npm run dev
}

show_status() {
  print_header "Project Status"
  
  echo "📦 Project: numerical-mediator"
  echo ""
  
  echo "🔍 Service Status:"
  if docker ps --filter "name=numerical_mediator_db" --format "{{.State}}" | grep -q "running"; then
    print_success "PostgreSQL Database is running"
  else
    print_warning "PostgreSQL Database is not running"
  fi
  
  if curl -s http://localhost:3000 &> /dev/null; then
    print_success "Development Server is running (http://localhost:3000)"
  else
    print_warning "Development Server is not running"
  fi
  
  if curl -s http://localhost:11434/api/tags &> /dev/null; then
    print_success "Ollama is running"
  else
    print_warning "Ollama is not running"
  fi
  
  echo ""
  echo "📁 Directories:"
  echo "   • Web app: ${WEB_DIR}"
  echo "   • Config: ${ENV_FILE}"
  echo ""
}

cleanup() {
  print_header "Cleaning Up"
  
  print_info "Stopping PostgreSQL..."
  docker compose -f "${SCRIPT_DIR}/docker-compose.yml" stop db 2>/dev/null || true
  print_success "PostgreSQL stopped"
  
  print_info "You may also want to stop Ollama manually"
}

full_setup() {
  check_prerequisites || return 1
  check_environment_file
  start_postgres || return 1
  install_dependencies
  initialize_database
  check_ollama
  
  print_header "Setup Complete ✓"
  echo -e "${GREEN}All components are ready!${NC}"
  echo ""
  echo "Next steps:"
  echo "  1. Make sure Ollama is running: ${YELLOW}ollama serve${NC}"
  echo "  2. Start the dev server: ${YELLOW}./launch.sh --quick${NC}"
  echo ""
}

quick_start() {
  print_header "Quick Start"
  
  # Check if PostgreSQL is running
  if ! docker ps --filter "name=numerical_mediator_db" --format "{{.State}}" | grep -q "running"; then
    print_warning "PostgreSQL is not running, starting it..."
    start_postgres || return 1
  fi
  
  # Check if node_modules exists
  if [ ! -d "${WEB_DIR}/node_modules" ]; then
    print_warning "Dependencies not installed, installing..."
    install_dependencies
  fi
  
  print_success "All prerequisites are ready"
  start_dev_server
}

clean_slate() {
  print_header "Clean Slate Setup"
  
  print_warning "This will reset the database and restart all services"
  read -p "Are you sure? (y/N) " -n 1 -r
  echo
  
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Cancelled"
    return 0
  fi
  
  print_info "Stopping services..."
  docker compose -f "${SCRIPT_DIR}/docker-compose.yml" down -v || true
  
  print_info "Removing node_modules..."
  rm -rf "${WEB_DIR}/node_modules"
  
  print_info "Running full setup..."
  full_setup
}

show_help() {
  cat << EOF
${BLUE}numerical-mediator Launch Script${NC}

${YELLOW}Usage:${NC}
  ./launch.sh [OPTION]

${YELLOW}Options:${NC}
  --full       Full setup: check prerequisites, start DB, install deps, init DB, then quit
  --quick      Quick start: assume setup is done, start DB and dev server
  --clean      Clean slate: reset everything and start fresh
  --status     Show current project status
  --stop       Stop all services (PostgreSQL)
  --help       Show this help message

${YELLOW}Examples:${NC}
  # First time setup
  ./launch.sh --full
  ./launch.sh --quick

  # After changes or restart
  ./launch.sh --quick

  # Reset everything
  ./launch.sh --clean

${YELLOW}Prerequisites:${NC}
  • Node.js 18+
  • npm
  • Docker & Docker Compose
  • Ollama (optional but recommended)

${YELLOW}Manual Services:${NC}
  Before running, start Ollama in another terminal:
  $ ollama serve
  $ ollama pull qwen2.5:7b  # First time only

${YELLOW}Development:${NC}
  After setup, access the app at: http://localhost:3000

EOF
}

##############################################################################
# Main Script
##############################################################################

main() {
  case "${1:-}" in
    --full)
      full_setup
      ;;
    --quick)
      quick_start
      ;;
    --clean)
      clean_slate
      ;;
    --status)
      show_status
      ;;
    --stop)
      cleanup
      ;;
    --help|-h|"")
      show_help
      ;;
    *)
      print_error "Unknown option: $1"
      echo ""
      show_help
      exit 1
      ;;
  esac
}

# Run main function
main "$@"
