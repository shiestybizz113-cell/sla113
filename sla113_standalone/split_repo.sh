#!/bin/bash
# ============================================================
# SLA113 Split Repo Script
# ============================================================
# Extracts SLA113 as a standalone project from the parent
# monorepo. Creates a clean, deployable project structure
# matching the production layout.
#
# Usage:
#   chmod +x split_repo.sh
#   ./split_repo.sh [output_dir]
#
# Default output: ./sla113_export/
# ============================================================

set -euo pipefail

OUTPUT_DIR="${1:-./sla113_export}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "================================================"
echo "  SLA113 — Split Repo Export"
echo "  Output: $OUTPUT_DIR"
echo "================================================"

# Clean previous export
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Copy backend
echo "[1/6] Copying backend..."
cp -r "$SCRIPT_DIR/backend" "$OUTPUT_DIR/backend"

# Copy frontend
echo "[2/6] Copying frontend..."
cp -r "$SCRIPT_DIR/frontend" "$OUTPUT_DIR/frontend"

# Copy infrastructure
echo "[3/6] Copying infrastructure files..."
cp "$SCRIPT_DIR/docker-compose.yml" "$OUTPUT_DIR/"
cp "$SCRIPT_DIR/README.md" "$OUTPUT_DIR/"

# Init git
echo "[4/6] Initializing git repo..."
cd "$OUTPUT_DIR"
git init
git add .
git commit -m "Initial SLA113 standalone export"

# Create .env from example
echo "[5/6] Creating .env from example..."
if [ -f backend/.env.example ]; then
    cp backend/.env.example backend/.env
    echo "  -> Created backend/.env (fill in your keys)"
fi

# Summary
echo "[6/6] Verifying structure..."
echo ""
echo "Project structure:"
find . -type f -not -path './.git/*' | sort | head -50
echo ""
echo "================================================"
echo "  SLA113 export complete!"
echo ""
echo "  Next steps:"
echo "    1. cd $OUTPUT_DIR"
echo "    2. Edit backend/.env with your keys"
echo "    3. docker-compose up --build"
echo "       OR"
echo "    3. cd backend && pip install -r requirements.txt"
echo "    4. uvicorn app.main:app --reload --port 8000"
echo "================================================"
