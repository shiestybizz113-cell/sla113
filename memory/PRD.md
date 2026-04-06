# SLA113 — Universal AI Game Studio

## Product Overview
SLA113 is a sovereign AI-powered game creation platform that generates complete game packages — from AAA titles (COD, GTA, Mortal Kombat style) to casino/arcade games — using AI engines for vision, logic, and composition. It sits alongside "Empire 1" (the existing Hybrid Intelligence Core SaaS) as its own domain page.

## Architecture
- **Frontend**: React + Tailwind CSS + lucide-react, mounted at `/sla113`
- **Backend**: FastAPI, routes at `/api/sla113/*`
- **Database**: MongoDB (`sla113_projects` collection)
- **AI**: Emergent LLM Key via `emergentintegrations` pip package (OpenAI GPT-4o-mini)

## Partitions (UI)
| Partition | Theme | Tabs |
|-----------|-------|------|
| FACTORY | Cyan (#00C8FF) | Frontline (live feed), White Label Mint |
| EMPIRE 1 | Indigo (#6366f1) | Mint Ledger, Revenue Pipelines |
| FOUNDRY | Gold (#D4AF37) | OS Builder, Vision Smith, Audio Forge |
| VAULT | Deep Red (#8B0000) | System Core, Night Queue |

## Supported Game Types (16)
### Casino/Arcade
- Fish Shooter, Slot Machine, Crash Game, Card Game

### AAA / Universal
- Open World (GTA Style), Tactical FPS (COD Style), Fighting Game (MK Style), Fantasy RPG, Survival Horror

### Action/Casual
- Platformer, Puzzle, Tower Defense, Endless Runner, Battle Royale, Racing, Sports

## AI Engines
1. **Vision Engine** (`/api/sla113/vision/generate`) — Generates sprite/asset specs
2. **Logic Engine** (`/api/sla113/logic/generate`) — Generates game math, mechanics, RTP, paytables
3. **Composer Engine** (`/api/sla113/compose`) — Assembles game bundles

## API Endpoints
- `GET /api/sla113/game-types` — List all 16 game types
- `GET /api/sla113/stats` — Platform stats
- `POST /api/sla113/projects` — Create game project
- `GET /api/sla113/projects` — List projects
- `GET /api/sla113/projects/{id}` — Get project
- `DELETE /api/sla113/projects/{id}` — Delete project
- `POST /api/sla113/vision/generate` — Generate visual assets
- `POST /api/sla113/logic/generate` — Generate game logic
- `POST /api/sla113/compose` — Compose game bundle

## What's Implemented (Feb 2026)
- [x] Full multi-partition UI (Factory, Empire 1, Foundry, Vault)
- [x] 9 panels across 4 partitions
- [x] Backend CRUD for game projects
- [x] AI Vision Engine (real LLM calls)
- [x] AI Logic Engine (real LLM calls)
- [x] AI Composer Engine (real LLM calls)
- [x] AI Terminal (overseer command interface)
- [x] Critical Drift overlay
- [x] Daemon Uplink heartbeat
- [x] 16 game types (casino + AAA)
- [x] LLM integration fixed (proper emergentintegrations pip package)

## Backlog
- [ ] Audio Forge — wire to real audio generation API
- [ ] White Label Mint — real tenant provisioning
- [ ] Revenue Pipelines — real pipeline data from backend
- [ ] Night Queue — persistent job queue with backend workers
- [ ] System Core — real firewall/security toggles
- [ ] Build Pipeline — export to APK/WebGL
- [ ] Compliance Engine — certification automation
- [ ] Deploy Engine — CDN distribution

## Key Files
- `/app/frontend/src/pages/SLA113Page.jsx` — Main SLA113 UI
- `/app/backend/routers/sla113.py` — API router
- `/app/backend/sla113/` — Engine modules (vision, logic, composer)
- `/app/backend/sla113/models.py` — Data models

## Credentials
- Test user: `newuser@example.com` / `NewPass123!`
