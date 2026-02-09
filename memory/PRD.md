# Hybrid Intelligence Core - PRD

## Original Problem Statement
Build a "Hybrid Intelligence Core," a sophisticated multi-model AI pipeline composed of specialized, single-purpose engines. The system uses GPT-5.2, Claude Sonnet 4.5, and Gemini 3 Flash via the `emergentintegrations` library with a universal key for seamless LLM access.

## Project Overview
A comprehensive backend system featuring 19 specialized AI engines orchestrated by a Hybrid Intelligence Core. Each engine is a distinct service responsible for a specific AI task, exposed via modular API endpoints.

## Architecture Summary
```
                    ┌─────────────────────────────┐
                    │  HYBRID INTELLIGENCE CORE   │
                    │    (Master Orchestrator)    │
                    └─────────────┬───────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│   GPT-5.2     │       │Claude Sonnet  │       │Gemini 3 Flash │
│   (Code)      │       │ 4.5 (Strategy)│       │   (Quick)     │
└───────────────┘       └───────────────┘       └───────────────┘
                                  │
                    ┌─────────────┴───────────────┐
                    │    19 SPECIALIZED ENGINES   │
                    └─────────────────────────────┘
```

## What's Been Implemented

| Date | Feature | Status |
|------|---------|--------|
| 2026-01-03 | Integration playbook (HYBRID_AI_STACK_PLAYBOOK.md) | ✅ Done |
| 2026-01-03 | Hybrid Intelligence Core | ✅ Done |
| 2026-01-03 | Core engines (Strategy, Plan, Analysis, Opportunity, Evaluator, Pricing, Blueprint, Persona) | ✅ Done |
| 2026-01-03 | Infrastructure (Canon Enforcer, Drift Monitor, Error Handler, Routing Engine) | ✅ Done |
| 2026-01-03 | Anime Character Engine | ✅ Done |
| 2026-01-03 | Pipeline Composer Engine | ✅ Done |
| 2026-02-03 | **Router Refactoring** - Split 1450-line monolithic router into 16 modular files | ✅ Done |
| 2026-02-03 | Anime Lore Engine + API endpoints | ✅ Done |
| 2026-02-03 | Anime Story Engine + API endpoints | ✅ Done |
| 2026-02-03 | Art Direction Engine + API endpoints | ✅ Done |
| 2026-02-03 | **Universal Money Pipeline Engine** | ✅ Done |
| 2026-02-03 | Pipeline Composer updated with all 13 engines + 7 templates | ✅ Done |
| 2026-02-03 | **Frontend Dashboard** - 3 pages with real backend integration | ✅ Done |
| 2026-02-07 | **Codebase Cleanup** - Removed abandoned FireKirin project and AI Arcade files | ✅ Done |
| 2026-02-09 | **Monitoring & Analytics Dashboard** - Real-time analytics with charts | ✅ Done |

## Frontend Pages

| Page | Route | Features |
|------|-------|----------|
| **Home** | `/` | Health status, engine count, model status, Quick Actions (6 cards), Engine preview |
| **Engines Dashboard** | `/engines` | Table of all 19 engines with Method, Endpoint, Description, Test buttons with modal |
| **Money Pipeline** | `/money-pipeline` | Full form (idea, target revenue, industry, context), sample ideas, tabbed results view |
| **Pipeline Composer** | `/pipeline-composer` | Chain engines, reorder steps, execute pipeline, timeline results, save/load presets |
| **Execution History** | `/history` | Searchable/filterable log of all engine calls with input/output details |
| **Analytics Dashboard** | `/analytics` | Real-time monitoring: Performance charts, AI drift detection, System health gauges |

## Engine Test Modal Features
- Shows endpoint info (Method + Path)
- Description of engine purpose
- Editable JSON payload for POST requests
- "Run Test" button with loading state
- Success badge on completion
- Full JSON response display
- Supports all 17 testable engines (2 internal engines excluded)

## Pipeline Composer Features
- **Engine Selection**: Click any of 13 engines to add to pipeline
- **Step Management**: Reorder with ↑↓ buttons, remove with × button
- **5 Preset Pipelines**: Full Business Plan, Startup Validation, Idea to Money, Anime Full Concept, Product Launch
- **Save/Load Custom Pipelines**: Persist to localStorage
- **Execution Timeline**: Vertical timeline showing each step's input/output
- **Real-time Progress**: Shows "Executing Step X/Y" during execution

## Execution History Features
- **Auto-logging Middleware**: All engine POST calls automatically logged
- **Stats Dashboard**: Total executions, success rate, avg duration, error count
- **Searchable Table**: Search across engine names, endpoints, inputs
- **Filters**: By engine, status (success/error), source (api/pipeline)
- **Expandable Details**: Click to view full input/output JSON for each call
- **Pagination**: Navigate through large log sets
- **Clear History**: Delete all logs with confirmation
- **Persistent Storage**: Logs saved to `/app/backend/execution_logs.json`

## Engine Inventory (19 Total)

### Business & Strategy Engines
| Engine | Purpose | Default Model |
|--------|---------|---------------|
| Strategy Engine | High-level strategy generation | Claude |
| Plan Builder Engine | Tactical execution planning | GPT-5.2 |
| Analysis Engine | Deep SWOT analysis | Claude |
| Opportunity Mapper | Identify high-leverage opportunities | Claude |
| Evaluator Engine | Score and evaluate with criteria | Claude |
| Pricing Engine | Generate pricing structures | Claude |
| Blueprint Engine | System architecture blueprints | GPT-5.2 |
| Persona Engine | User/customer persona generation | Claude |
| **Money Pipeline Engine** | Complete monetization system | Claude |

### Creative Engines
| Engine | Purpose | Default Model |
|--------|---------|---------------|
| Anime Character Engine | Original anime character creation | Claude |
| Anime Lore Engine | World-building, mythology, factions | Claude |
| Anime Story Engine | Narrative structure, story arcs | Claude |
| Art Direction Engine | Visual direction for creative projects | Claude |

### Infrastructure Engines
| Engine | Purpose |
|--------|---------|
| Hybrid Intelligence Core | Master orchestrator |
| Routing Engine | Task classification → model selection |
| Pipeline Composer Engine | Multi-engine workflow orchestration |
| Canon Enforcer | Output normalization |
| Drift Monitor | Behavioral tracking |
| Error Handler | Structured errors |

## API Endpoints (77 Total)

### Core Endpoints
- `POST /api/core/execute` - Unified execution via Hybrid Core
- `GET /api/core/status` - Core system status
- `GET /api/health` - Pipeline health check (lists all 19 engines)

### Money Pipeline Endpoints
- `POST /api/money-pipeline` - Full monetization pipeline
- `POST /api/money-pipeline/quick` - Quick monetization
- `POST /api/money-pipeline/saas` - SaaS-specific pipeline
- `POST /api/money-pipeline/service` - Service business pipeline
- `POST /api/money-pipeline/ecommerce` - E-commerce pipeline
- `POST /api/money-pipeline/api` - API product pipeline

### Pipeline Composer Endpoints
- `POST /api/pipeline/compose` - Compose multi-engine pipeline
- `GET /api/pipeline/engines` - List all 13 chainable engines
- `GET /api/pipeline/templates` - List 7 pre-built templates

### Creative Endpoints
- `POST /api/anime/character` - Generate anime character
- `POST /api/anime/lore` - Generate world lore
- `POST /api/anime/story` - Generate story structure
- `POST /api/art-direction` - Generate art direction

## Pipeline Templates (7)

| Template | Engines Chain |
|----------|---------------|
| full_business_plan | strategy → analysis → opportunity → plan → pricing → evaluator |
| product_launch | persona → strategy → pricing → plan |
| startup_validation | analysis → persona → opportunity → evaluator |
| system_design | strategy → blueprint → plan → evaluator |
| **idea_to_money** | money_pipeline → persona → blueprint → evaluator |
| **anime_full_concept** | lore → story → character → character → art_direction |
| **saas_monetization** | money_pipeline → blueprint → plan |

## Code Architecture
```
/app/backend/
├── services/                    # 19 engine service files
│   ├── hybrid_core.py
│   ├── strategy_engine.py
│   ├── money_pipeline_engine.py # NEW
│   ├── anime_lore_engine.py
│   ├── anime_story_engine.py
│   ├── art_direction_engine.py
│   └── ... (13 more)
├── routers/
│   ├── engines/                 # 16 modular router files
│   │   ├── __init__.py
│   │   ├── core.py
│   │   ├── money_pipeline.py    # NEW
│   │   ├── anime_lore.py
│   │   ├── anime_story.py
│   │   ├── art_direction.py
│   │   └── ... (10 more)
├── server.py
├── requirements.txt
└── .env
```

## Key Technical Details
- **API Key**: Emergent Universal Key (EMERGENT_LLM_KEY)
- **Library**: emergentintegrations
- **Models**: 
  - OpenAI: gpt-5.2
  - Anthropic: claude-sonnet-4-5-20250929
  - Google: gemini-3-flash-preview

## Cleanup Completed (Feb 7, 2025)
- Removed abandoned FireKirin game engine project (`/app/firekirin/`)
- Deleted abandoned AI Arcade components (`ArcadeHub.jsx`, `ArcadeSubpages.jsx`, `CanonRoom.jsx`, `MachineModal.jsx`)
- Deleted obsolete monolithic router (`/app/backend/routers/strategy.py`)

## Current State
✅ Clean, functional Hybrid Intelligence app with:
- 19 specialized AI engines
- Multi-page React frontend (6 pages including Analytics Dashboard)
- Modular FastAPI backend
- Execution logging & history
- **Premium Monitoring & Analytics Dashboard** with all polish features

## Analytics Dashboard (Feb 9, 2025)
New `/analytics` page with 3 tabs and premium polish:
- **Engine Performance**: Bar charts, latency metrics, error rates table, mini sparklines
- **AI Quality & Drift**: Confidence trends, drift alerts with pulse animations, model comparison
- **System Health**: Gauges with animations, detailed metrics, load average, pipeline flow

### Tier 1 — Must-Have Polish ✅
- Threshold-based alerts (CPU>80%, Memory>90%, Disk>95%)
- Toast notifications for critical alerts
- Last Updated timestamp with 5-second refresh
- Skeleton loaders during initial load
- Smooth animations on all metric changes

### Tier 2 — Premium Polish ✅
- WebSocket support for sub-second updates (`/api/analytics/ws`)
- Auto-fallback to 5-second polling if WebSocket fails
- Drift event notifications with visual highlighting
- Mini sparklines showing recent trends
- Metrics source indicator (LIVE/POLLING)

### Tier 3 — Luxury Polish ✅
- Historical export (JSON + CSV download)
- Customizable widgets (show/hide sections)
- Preferences saved to localStorage
- Dark/Light theme toggle with smooth transitions

**10 API Endpoints**: 9 REST + 1 WebSocket
**psutil Integration**: ✅ Real system metrics with safe fallbacks

## Next Tasks
- TBD (awaiting user direction)

## Backlog
- Additional dashboard themes/skins
- Alert notification history/log
- Engine performance comparison charts
