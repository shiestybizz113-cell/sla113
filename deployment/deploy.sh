#!/bin/bash
# ============================================
# Hybrid Intelligence Core - Deployment Script
# ============================================
# Run this script after setup-server.sh and cloning the repo
# Usage: bash deploy.sh
#
# This script will:
# 1. Install backend dependencies
# 2. Build frontend
# 3. Configure NGINX
# 4. Set up systemd service
# 5. Start the application
# ============================================

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

APP_DIR="/var/www/hybrid-intelligence"
DOMAIN="yourdomain.com"  # CHANGE THIS

echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}Hybrid Intelligence Core - Deployment${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root (sudo bash deploy.sh)${NC}"
    exit 1
fi

# ==================== CHECK .ENV ====================
echo -e "${YELLOW}[1/7] Checking environment files...${NC}"

if [ ! -f "$APP_DIR/backend/.env" ]; then
    echo -e "${RED}ERROR: Backend .env file not found!${NC}"
    echo "Please copy .env.production.template to $APP_DIR/backend/.env and configure it"
    exit 1
fi

if [ ! -f "$APP_DIR/frontend/.env" ]; then
    echo -e "${RED}ERROR: Frontend .env file not found!${NC}"
    echo "Please create $APP_DIR/frontend/.env with REACT_APP_BACKEND_URL"
    exit 1
fi

echo -e "${GREEN}✓ Environment files found${NC}"

# ==================== BACKEND SETUP ====================
echo -e "${YELLOW}[2/7] Installing backend dependencies...${NC}"
cd "$APP_DIR/backend"

# Activate virtual environment
source "$APP_DIR/venv/bin/activate"

# Install dependencies
pip install -r requirements.txt

# Install emergentintegrations
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

echo -e "${GREEN}✓ Backend dependencies installed${NC}"

# ==================== FRONTEND BUILD ====================
echo -e "${YELLOW}[3/7] Building frontend...${NC}"
cd "$APP_DIR/frontend"

# Install dependencies
yarn install --frozen-lockfile

# Build production bundle
yarn build

echo -e "${GREEN}✓ Frontend built successfully${NC}"

# ==================== NGINX CONFIGURATION ====================
echo -e "${YELLOW}[4/7] Configuring NGINX...${NC}"

# Copy nginx config
cp "$APP_DIR/deployment/nginx.conf" /etc/nginx/sites-available/hybrid-intelligence

# Update domain in config
sed -i "s/yourdomain.com/$DOMAIN/g" /etc/nginx/sites-available/hybrid-intelligence

# Enable site
ln -sf /etc/nginx/sites-available/hybrid-intelligence /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test nginx config
nginx -t

# Reload nginx
systemctl reload nginx

echo -e "${GREEN}✓ NGINX configured${NC}"

# ==================== SYSTEMD SERVICE ====================
echo -e "${YELLOW}[5/7] Setting up systemd service...${NC}"

# Copy service file
cp "$APP_DIR/deployment/hybrid-intelligence.service" /etc/systemd/system/

# Reload systemd
systemctl daemon-reload

# Enable service
systemctl enable hybrid-intelligence

echo -e "${GREEN}✓ Systemd service configured${NC}"

# ==================== SET PERMISSIONS ====================
echo -e "${YELLOW}[6/7] Setting permissions...${NC}"

chown -R www-data:www-data "$APP_DIR"
chown -R www-data:www-data /var/log/hybrid-intelligence
chmod 600 "$APP_DIR/backend/.env"
chmod 600 "$APP_DIR/frontend/.env"

echo -e "${GREEN}✓ Permissions set${NC}"

# ==================== START APPLICATION ====================
echo -e "${YELLOW}[7/7] Starting application...${NC}"

systemctl restart hybrid-intelligence
sleep 3

# Check if service is running
if systemctl is-active --quiet hybrid-intelligence; then
    echo -e "${GREEN}✓ Application started successfully${NC}"
else
    echo -e "${RED}✗ Application failed to start${NC}"
    echo "Check logs: journalctl -u hybrid-intelligence -f"
    exit 1
fi

# ==================== SUMMARY ====================
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "${BLUE}Application Status:${NC}"
systemctl status hybrid-intelligence --no-pager | head -10
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Point your domain DNS to this server's IP"
echo "  2. Set up SSL: sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo "  3. Test the application: curl -I https://$DOMAIN"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "  - View logs: journalctl -u hybrid-intelligence -f"
echo "  - Restart: sudo systemctl restart hybrid-intelligence"
echo "  - Status: sudo systemctl status hybrid-intelligence"
echo ""
