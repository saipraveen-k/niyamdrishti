#!/usr/bin/env bash
# NiyamDrishti — local development setup script
# Usage: bash scripts/setup.sh

set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

info()    { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }
header()  { echo -e "\n${BOLD}==> $*${NC}"; }

# ── Prerequisites ──────────────────────────────────────────────────────────────
header "Checking prerequisites"

command -v python3 >/dev/null 2>&1 || error "Python 3.10+ is required."
command -v node    >/dev/null 2>&1 || error "Node.js 20+ is required."
command -v npm     >/dev/null 2>&1 || error "npm is required."

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
NODE_VERSION=$(node --version)
info "Python: $PYTHON_VERSION"
info "Node:   $NODE_VERSION"

# ── Backend ────────────────────────────────────────────────────────────────────
header "Setting up backend"

cd backend

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        warn ".env created from .env.example — fill in your secrets before running."
    else
        warn ".env.example not found. Create backend/.env manually."
    fi
else
    info ".env already exists."
fi

if [ ! -d "venv" ]; then
    info "Creating Python virtual environment..."
    python3 -m venv venv
fi

info "Activating venv and installing dependencies..."
# shellcheck disable=SC1091
source venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
info "Backend dependencies installed."

cd ..

# ── Frontend ───────────────────────────────────────────────────────────────────
header "Setting up frontend"

cd frontend

if [ ! -f ".env.local" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env.local
        warn ".env.local created from .env.example — fill in your Supabase keys."
    else
        warn ".env.example not found. Create frontend/.env.local manually."
    fi
else
    info ".env.local already exists."
fi

info "Installing Node dependencies..."
npm install --silent
info "Frontend dependencies installed."

cd ..

# ── Summary ────────────────────────────────────────────────────────────────────
header "Setup complete"

echo ""
echo "  To start the backend:"
echo "    cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo ""
echo "  To start the frontend:"
echo "    cd frontend && npm run dev"
echo ""
echo "  Or start everything with Docker:"
echo "    docker compose up"
echo ""
echo "  Run backend tests:"
echo "    cd backend && source venv/bin/activate && pytest"
echo ""
warn "Remember to populate backend/.env and frontend/.env.local with real credentials."
