# ============================================
# EMPIRE1 ECOSYSTEM — SLA113 OPERATOR OS
# Pre-Launch Checklist
# ============================================

## Before You Start

### Domain & DNS (Tee Architecture)
- [ ] `sla113.southernlifestyle.org` A record pointing to VPS IP
- [ ] DNS propagation complete (check: https://dnschecker.org)

Full ecosystem domains (deploy separately as needed):
| Domain | Universe | Role |
|--------|----------|------|
| `empire1.cloud` | E1 | Creator SaaS Dashboard |
| `southernlifestyle.org` | SL | Brand Root / Identity |
| `lyrica3.com` | L3 | Music Universe (Lyrica 3 Pro) |
| `sluniversal.lyrica3.com` | UL | Universe Portal / Meta-Router |
| `sla113.southernlifestyle.org` | SLA113 | Admin Console / Operator OS |
| `arcade.southernlifestyle.org` | AR | Game Universe / Player Portal |

### Server Access
- [ ] VPS provisioned (IONOS or other)
- [ ] SSH access working
- [ ] Root or sudo access available

---

## External Services Setup

### MongoDB Atlas
- [ ] Account created
- [ ] Cluster created (M0 free tier or higher)
- [ ] Database user created
- [ ] Network access configured (VPS IP whitelisted)
- [ ] Connection string copied

### Stripe (Optional - for billing)
- [ ] Account created
- [ ] Secret key copied
- [ ] Webhook endpoint created
- [ ] Webhook secret copied
- [ ] Products/Prices created

### Resend (Optional - for email)
- [ ] Account created
- [ ] Domain verified
- [ ] API key created

### Google OAuth (Optional)
- [ ] Project created in Google Cloud
- [ ] OAuth credentials created
- [ ] Redirect URI configured

### GitHub OAuth (Optional)
- [ ] OAuth app created
- [ ] Callback URL configured

---

## Server Setup

### Run Setup Script
- [ ] `setup-server.sh` executed successfully
- [ ] Python 3.11 installed
- [ ] Node.js 20 installed
- [ ] NGINX installed
- [ ] Certbot installed
- [ ] Firewall enabled

### Application Files
- [ ] Repository cloned to `/var/www/hybrid-intelligence`
- [ ] Backend `.env` configured
- [ ] Frontend `.env` configured
- [ ] Permissions set correctly

---

## Deployment

### Deploy Application
- [ ] `deploy.sh` executed successfully
- [ ] Backend dependencies installed
- [ ] Frontend built
- [ ] NGINX configured
- [ ] Systemd service created
- [ ] Application running

### SSL Certificate
- [ ] Certbot completed successfully
- [ ] HTTPS accessible
- [ ] Auto-renewal configured

---

## Post-Deployment Verification

### API Health
- [ ] `curl https://sla113.southernlifestyle.org/api/system/health` returns OK
- [ ] `curl https://sla113.southernlifestyle.org/api/system/status` shows services
- [ ] `curl https://sla113.southernlifestyle.org/api/sla113/universes` shows 6 universes

### Authentication
- [ ] Signup works
- [ ] Login works
- [ ] Password reset works (if email configured)
- [ ] OAuth works (if configured)

### Core Features
- [ ] Dashboard loads
- [ ] Team creation works
- [ ] Team switching works
- [ ] Profile page works
- [ ] Team settings work

### Admin Features (if applicable)
- [ ] Admin overview accessible
- [ ] System stats display

---

## Security Final Check

- [ ] .env files have 600 permissions
- [ ] No secrets in git repository
- [ ] SSL/TLS working (check: https://ssllabs.com/ssltest)
- [ ] HSTS header present
- [ ] Rate limiting active
- [ ] Fail2Ban running

---

## Go Live

- [ ] All checks above passed
- [ ] Monitoring set up (optional but recommended)
- [ ] Backup strategy in place
- [ ] Team notified
- [ ] **LAUNCHED!** 🚀

---

## Quick Reference

### Useful Commands
```bash
# Check application status
sudo systemctl status hybrid-intelligence

# View real-time logs
sudo journalctl -u hybrid-intelligence -f

# Restart application
sudo systemctl restart hybrid-intelligence

# Check NGINX
sudo nginx -t
sudo systemctl reload nginx

# Check SSL
sudo certbot certificates
```

### Important Paths
```
Application:  /var/www/hybrid-intelligence
Backend:      /var/www/hybrid-intelligence/backend
Frontend:     /var/www/hybrid-intelligence/frontend/build
Logs:         /var/log/hybrid-intelligence
NGINX config: /etc/nginx/sites-available/hybrid-intelligence
Service:      /etc/systemd/system/hybrid-intelligence.service
```

### Support URLs
- MongoDB Atlas: https://cloud.mongodb.com
- Stripe Dashboard: https://dashboard.stripe.com
- Resend Dashboard: https://resend.com
- SSL Check: https://ssllabs.com/ssltest
- DNS Check: https://dnschecker.org
