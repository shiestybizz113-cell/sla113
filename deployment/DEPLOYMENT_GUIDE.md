# ============================================
# EMPIRE1 ECOSYSTEM — SLA113 OPERATOR OS
# Production Deployment Guide
# ============================================

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Server Setup](#server-setup)
3. [MongoDB Atlas Setup](#mongodb-atlas-setup)
4. [External Services Setup](#external-services-setup)
5. [Application Deployment](#application-deployment)
6. [SSL Certificate Setup](#ssl-certificate-setup)
7. [DNS Configuration](#dns-configuration)
8. [Post-Deployment Verification](#post-deployment-verification)
9. [Maintenance Commands](#maintenance-commands)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Server Requirements
- **OS**: Ubuntu 22.04 LTS
- **RAM**: Minimum 2GB (4GB recommended)
- **CPU**: 2 vCPUs minimum
- **Storage**: 20GB SSD minimum
- **Provider**: IONOS, DigitalOcean, AWS, etc.

### Domain (Tee Architecture)
This repo deploys the **SLA113 Operator OS** at `sla113.southernlifestyle.org`.

Full ecosystem domain map:
| Domain | Universe | Role |
|--------|----------|------|
| `empire1.cloud` | E1 | Creator SaaS Dashboard |
| `southernlifestyle.org` | SL | Brand Root / Identity |
| `lyrica3.com` | L3 | Music Universe (Lyrica 3 Pro) |
| `sluniversal.lyrica3.com` | UL | Universe Portal / Meta-Router |
| `sla113.southernlifestyle.org` | SLA113 | Admin Console / Operator OS |
| `arcade.southernlifestyle.org` | AR | Game Universe / Player Portal |

### Accounts Needed
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (free tier available)
- [Stripe](https://stripe.com) (for payments)
- [Resend](https://resend.com) (for emails)
- [Google Cloud Console](https://console.cloud.google.com) (for OAuth)
- [GitHub Developer Settings](https://github.com/settings/developers) (for OAuth)

---

## Server Setup

### 1. SSH into your IONOS VPS
```bash
ssh root@YOUR_SERVER_IP
```

### 2. Create deploy user (recommended)
```bash
adduser deploy
usermod -aG sudo deploy
su - deploy
```

### 3. Run the setup script
```bash
# Download and run setup
curl -O https://raw.githubusercontent.com/yourusername/hybrid-intelligence/main/deployment/setup-server.sh
sudo bash setup-server.sh
```

This installs:
- Python 3.11
- Node.js 20 LTS
- NGINX
- Certbot
- UFW Firewall
- Fail2Ban

---

## MongoDB Atlas Setup

### 1. Create a Cluster
1. Go to [MongoDB Atlas](https://cloud.mongodb.com)
2. Create a new project: "Hybrid Intelligence"
3. Create a cluster (M0 free tier is fine to start)
4. Select your preferred region (close to your VPS)

### 2. Create Database User
1. Go to **Database Access**
2. Add new database user
3. Username: `hybrid_app`
4. Password: Generate a strong password (save it!)
5. Privileges: `readWriteAnyDatabase`

### 3. Configure Network Access
1. Go to **Network Access**
2. Add IP Address
3. Add your VPS IP address
4. Or add `0.0.0.0/0` for access from anywhere (less secure)

### 4. Get Connection String
1. Go to **Clusters** → **Connect**
2. Choose "Connect your application"
3. Copy the connection string:
```
mongodb+srv://hybrid_app:PASSWORD@cluster0.xxxxx.mongodb.net/hybrid_intelligence?retryWrites=true&w=majority
```

---

## External Services Setup

### Stripe (Payments)
1. Create account at [stripe.com](https://stripe.com)
2. Go to **Developers** → **API Keys**
3. Copy:
   - `STRIPE_SECRET_KEY`: sk_live_...
   - `STRIPE_PUBLISHABLE_KEY`: pk_live_...
4. Set up webhook:
   - URL: `https://sla113.southernlifestyle.org/api/billing/webhook`
   - Events: `checkout.session.completed`, `customer.subscription.*`
   - Copy `STRIPE_WEBHOOK_SECRET`
5. Create Products/Prices:
   - Pro Plan: Copy `price_id`
   - Enterprise Plan: Copy `price_id`

### Resend (Email)
1. Create account at [resend.com](https://resend.com)
2. Verify your domain
3. Go to **API Keys** → Create API key
4. Copy `RESEND_API_KEY`: re_...

### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project or select existing
3. Go to **APIs & Services** → **Credentials**
4. Create **OAuth 2.0 Client ID**
   - Type: Web application
   - Authorized redirect URIs: `https://sla113.southernlifestyle.org/api/auth/oauth/google/callback`
5. Copy:
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`

### GitHub OAuth
1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create **New OAuth App**
   - Homepage URL: `https://sla113.southernlifestyle.org`
   - Callback URL: `https://sla113.southernlifestyle.org/api/auth/oauth/github/callback`
3. Copy:
   - `GITHUB_CLIENT_ID`
   - `GITHUB_CLIENT_SECRET`

---

## Application Deployment

### 1. Clone the Repository
```bash
cd /var/www/hybrid-intelligence
sudo git clone https://github.com/yourusername/hybrid-intelligence.git .
```

### 2. Configure Environment Variables

**Backend (.env)**
```bash
sudo cp deployment/.env.production.template backend/.env
sudo nano backend/.env
```

Fill in all values from the services you set up above.

**Frontend (.env)**
```bash
sudo cp deployment/.env.frontend.template frontend/.env
sudo nano frontend/.env
```

Update `REACT_APP_BACKEND_URL` to `https://sla113.southernlifestyle.org`.

### 3. Update Domain in Deployment Scripts
```bash
# Edit deploy.sh and change DOMAIN variable
sudo nano deployment/deploy.sh
# Domain is already set to sla113.southernlifestyle.org
```

### 4. Run Deployment
```bash
sudo bash deployment/deploy.sh
```

---

## SSL Certificate Setup

### 1. Ensure DNS is pointing to your server
```bash
dig +short sla113.southernlifestyle.org
# Should return your server IP
```

### 2. Run Certbot
```bash
sudo certbot --nginx -d sla113.southernlifestyle.org
```

### 3. Verify Auto-Renewal
```bash
sudo certbot renew --dry-run
```

---

## DNS Configuration

### A Records
| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | YOUR_SERVER_IP | 300 |
| A | www | YOUR_SERVER_IP | 300 |

### MX Records (if using Resend for sending)
Follow Resend's domain verification instructions.

---

## Post-Deployment Verification

### 1. Check Service Status
```bash
sudo systemctl status hybrid-intelligence
sudo systemctl status nginx
```

### 2. Test API Health
```bash
curl https://sla113.southernlifestyle.org/api/system/health
# Expected: {"status":"healthy","version":"2.1.0",...}
```

### 3. Test Frontend
Open `https://sla113.southernlifestyle.org` in browser

### 4. Test Authentication
1. Go to signup page
2. Create an account
3. Log in
4. Verify team creation

### 5. Check Logs
```bash
# Application logs
sudo journalctl -u hybrid-intelligence -f

# NGINX logs
sudo tail -f /var/log/nginx/hybrid-intelligence.access.log
sudo tail -f /var/log/nginx/hybrid-intelligence.error.log
```

---

## Maintenance Commands

### Restart Application
```bash
sudo systemctl restart hybrid-intelligence
```

### View Logs
```bash
# Real-time logs
sudo journalctl -u hybrid-intelligence -f

# Last 100 lines
sudo journalctl -u hybrid-intelligence -n 100
```

### Update Application
```bash
cd /var/www/hybrid-intelligence

# Pull latest code
sudo git pull origin main

# Install any new backend dependencies
source venv/bin/activate
pip install -r backend/requirements.txt

# Rebuild frontend
cd frontend
yarn install
yarn build

# Restart service
sudo systemctl restart hybrid-intelligence
```

### Backup Database
```bash
# MongoDB Atlas handles backups automatically
# For manual backup, use mongodump
mongodump --uri="mongodb+srv://..." --out=/backup/$(date +%Y%m%d)
```

### Monitor Resources
```bash
htop
df -h
free -m
```

---

## Troubleshooting

### Application Won't Start
```bash
# Check logs
sudo journalctl -u hybrid-intelligence -n 50

# Common issues:
# - Missing .env file
# - Invalid MongoDB connection string
# - Port 8001 already in use
```

### NGINX 502 Bad Gateway
```bash
# Check if backend is running
sudo systemctl status hybrid-intelligence

# Check if port 8001 is listening
sudo netstat -tlnp | grep 8001

# Check NGINX error log
sudo tail -f /var/log/nginx/hybrid-intelligence.error.log
```

### SSL Certificate Issues
```bash
# Renew certificate
sudo certbot renew

# Check certificate status
sudo certbot certificates
```

### MongoDB Connection Issues
```bash
# Test connection
python3 -c "from pymongo import MongoClient; c = MongoClient('YOUR_MONGO_URL'); print(c.server_info())"

# Check if IP is whitelisted in Atlas
```

### Permission Denied
```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/hybrid-intelligence
sudo chown -R www-data:www-data /var/log/hybrid-intelligence
```

---

## Security Checklist

- [ ] SSH key authentication enabled
- [ ] Password authentication disabled
- [ ] UFW firewall enabled
- [ ] Fail2Ban configured
- [ ] SSL certificate installed
- [ ] HSTS enabled
- [ ] Secure .env file permissions (600)
- [ ] MongoDB IP whitelist configured
- [ ] Strong JWT secrets generated
- [ ] Rate limiting enabled in NGINX

---

## Support

For issues, check:
1. Application logs: `journalctl -u hybrid-intelligence`
2. NGINX logs: `/var/log/nginx/hybrid-intelligence.error.log`
3. MongoDB Atlas logs in the web console

---

*Last updated: 2026-02-09*
*Version: 2.1.0*
