# Roadmap

Prioritized feature backlog for the Hybrid Intelligence Core platform.

## Current Status: Production Ready (v2.1.0)

All core features implemented through Phase D-Lite. The platform is ready for production deployment.

---

## P0 - Production Blockers (Required before launch)

| Feature | Status | Notes |
|---------|--------|-------|
| Configure Stripe API Keys | ⏳ Pending | Requires user to add `STRIPE_SECRET_KEY` |
| Configure Email Service | ⏳ Pending | Requires user to add `RESEND_API_KEY` |
| Configure OAuth Credentials | ⏳ Pending | Google and GitHub OAuth client IDs/secrets |
| Set production `JWT_SECRET_KEY` | ⏳ Pending | Strong random key for production |

---

## P1 - High Priority Enhancements

| Feature | Description | Effort |
|---------|-------------|--------|
| Email Templates | Branded HTML email templates for invites, password reset | Medium |
| Rate Limiting | API rate limiting by plan tier | Medium |
| Webhook Events | Outgoing webhooks for team events | Medium |
| Two-Factor Auth (2FA) | TOTP-based 2FA for enhanced security | High |
| Audit Log Export | Export audit logs to CSV/JSON | Low |

---

## P2 - Nice to Have Features

| Feature | Description | Effort |
|---------|-------------|--------|
| Team Custom Domains | Custom domains for team workspaces | High |
| Dark/Light Theme Toggle | User preference for UI theme | Low |
| Notification Preferences | Email notification settings | Medium |
| API Usage Analytics | Detailed API usage graphs | Medium |
| Team Activity Charts | Visual charts for team activity | Medium |
| Engine Performance Comparison | Side-by-side engine benchmarks | Medium |

---

## P3 - Future Considerations

| Feature | Description |
|---------|-------------|
| Multi-region Support | Deploy to multiple regions |
| SSO/SAML Integration | Enterprise SSO support |
| Custom Roles | User-defined roles beyond owner/admin/member |
| Webhooks Builder | Visual webhook configuration |
| Plugin System | Third-party engine plugins |
| Mobile App | React Native mobile companion |

---

## Completed Phases

- ✅ Phase 1-4: Database, Auth, Teams, Migration
- ✅ Phase 5: Frontend Integration
- ✅ Phase 6: Profile & RBAC
- ✅ Phase 7: Team Invitations
- ✅ Macro Phase A: Identity & Access (OAuth, Password Reset, Sessions)
- ✅ Macro Phase B: Billing & Usage (Stripe, API Keys, Usage Limits)
- ✅ Phase C-Lite: Minimal Governance (Activity Log, Admin Overview)
- ✅ Phase D-Lite: Launch Polish (UI Consistency, Loading States, Error Handling)

---

## External Service Configuration

### Required Environment Variables

```bash
# Backend (.env)
MONGO_URL=mongodb://...
DB_NAME=hybrid_intelligence
JWT_SECRET_KEY=your-strong-secret-key
JWT_REFRESH_SECRET_KEY=your-refresh-secret-key

# Stripe (for billing)
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_ID_PRO=price_...
STRIPE_PRICE_ID_ENTERPRISE=price_...

# Email (for invites, password reset)
RESEND_API_KEY=re_...
EMAIL_FROM=noreply@yourdomain.com

# OAuth (for social login)
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...

# Frontend (.env)
REACT_APP_BACKEND_URL=https://your-domain.com
```

### Mocked Services Status

| Service | Status | Impact |
|---------|--------|--------|
| Stripe | MOCKED | Billing features simulated, no real payments |
| Resend Email | MOCKED | Emails not sent, tokens logged to console |
| Google OAuth | DISABLED | Social login button hidden |
| GitHub OAuth | DISABLED | Social login button hidden |
