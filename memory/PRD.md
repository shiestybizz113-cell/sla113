# SLA113 — Universal AI Game Studio Operator OS

## Product Overview
SLA113 is the **sovereign root OS** for AI-powered game creation. All universes (Empire1, Southern, Soulfire/Lyrica 3 Pro) are routers/modules under SLA113.

## Architecture Decision
- SLA113 = sovereign root (owns everything)
- Empire 1 = universe router under SLA113
- Southern = universe router under SLA113  
- Soulfire Ecosystem (ASW + El Coro + Sentinel + SL Universal) = single domain, powers Lyrica 3 Pro

## Core Engines
1. **Vision Smith v2** — Gemini 3 Pro image generation (user API key, no proxy watermarks)
2. **Logic Engine** — AI game math, RTP, paytables, RNG (Emergent LLM Key)
3. **Composer Engine** — Game bundle assembly (Emergent LLM Key)
4. **AI Terminal** — Sovereign Overseer command interface
5. **Night Queue** — Background asyncio worker with job dependencies
6. **Build Pipeline** — Simulated APK/WebGL builds
7. **Compliance Engine** — Simulated regulatory checks (GLI, MGA, UKGC, etc.)
8. **Deploy Engine** — Simulated CDN deployment
9. **Sprite Cutter** — Canvas-based sprite sheet slicing with animation preview
10. **Boss Bestiary** — Gallery of boss benchmark assets
11. **Universe Registry** — Auto-discovery of all mounted universe routers with dynamic registration

## Completed Features
- [x] Micro-frontend architecture (Empire 1 on `/`, SLA113 on `/sla113`)
- [x] SLA113 removed from Empire's public nav (decontaminated)
- [x] Vision Smith v2 with Gemini 3 Pro direct API
- [x] Night Queue with asyncio background worker
- [x] Job dependency graph (visual node graph)
- [x] Build/Compliance/Deploy engine panels (simulated)
- [x] Sprite Cutter + Animation Preview
- [x] Boss Bestiary gallery
- [x] Cinematic splash loading screen
- [x] Revenue Pipeline Pulse
- [x] Standalone SLA113 project export matching production layout
- [x] **Universe Registry** with auto-discovery, dynamic registration/deregistration, and visual dashboard

## Standalone Export Structure
```
sla113_standalone/
├── backend/app/
│   ├── main.py (FastAPI entrypoint — 14 routers, 50+ endpoints)
│   ├── core/ (config, database, constants)
│   ├── models/ (Pydantic schemas)
│   ├── routers/
│   │   ├── sla113_admin.py, sla113_billing.py, sla113_dashboard_context.py
│   │   ├── sla113_engine_dashboard.py, sla113_factory.py, sla113_foundry.py
│   │   ├── sla113_health.py, sla113_orchestration.py, sla113_regulatory.py
│   │   ├── sla113_universe.py (Universe Registry — auto-discovery)
│   │   ├── sla113/factory.py (deploy engine)
│   │   ├── empire1.py, southern.py, soulfire.py (universe stubs)
│   ├── services/ (vision, logic, composer engines)
│   └── vertexai/ (music_client placeholder)
├── frontend/src/ (SLA113 React components)
├── Dockerfile, docker-compose.yml, requirements.txt
└── split_repo.sh
```

## Backlog
- [ ] Wire Audio Forge to Vertex AI (user to provide API later)
- [ ] Upgrade Build/Compliance/Deploy from simulated to real
- [ ] Real-time Frontline data via WebSocket
- [ ] Refactor SLA113Page.jsx into sub-components
