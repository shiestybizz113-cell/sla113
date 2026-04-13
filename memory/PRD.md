# SLA113 — Universal AI Game Studio Operator OS

## Product Overview
SLA113 is the **sovereign root OS** for AI-powered game creation. All universes are routers under SLA113.

## Game Type Taxonomy (29 types, 5 categories + Audio Middleware)
- **Arcade & Action** (10): Arcade Classic, Fish Shooting, Battle Royale, Tactical FPS, COD Warfare, Platformer, Fighting, Puzzle, Adventure, Open World
- **Casino & Gambling** (8): Slot Machine, Video Poker, Casino Suite, Pachinko, Lottery, Bingo, Sportsbook, Card Games
- **RPG & Narrative** (7): Open World RPG, Dungeon Crawler, Fantasy RPG, Cyberpunk, Horror, Southern Barrio, Sandbox
- **Racing & Simulation** (1): Racing Sim
- **Hybrid & Custom** (3): Hybrid Mix, Generic Game Asset, Custom Partner Games
- **Audio Middleware** (8): SFX, Ambience, Foley, Music Cues, Stems, Loops, TTS, Voice Routing
- **Audio Engines**: FMOD, SonicForge, AudioKing, VoiceKing

## Completed Features
- [x] Vision Smith v2 (Gemini 3 Pro, no watermarks)
- [x] Logic Engine (RTP, RNG, paytable, mechanics)
- [x] Composer Engine (game bundle assembly)
- [x] AI Terminal (Sovereign Overseer)
- [x] Night Queue (asyncio background worker + dependencies)
- [x] Build Pipeline — Real HTML5/PixiJS compilation + downloadable ZIP bundles
- [x] Real Compliance Engine + Auto-Certify
- [x] Deploy Engine — Real static file hosting with playable live game preview URLs + inline iframe preview
- [x] Sprite Cutter + Animation Preview
- [x] Boss Bestiary
- [x] Universe Registry (auto-discovery, interactive cards)
- [x] WebSocket Frontline (real-time metrics)
- [x] Full 29-type game taxonomy with categorized dropdowns
- [x] Standalone project export (sla113_standalone.zip)
- [x] Audio Forge Engine — AI-enhanced DSP + Web Audio API synthesis (play/preview + WAV export)
- [x] Admin Control Vault — ArtTech Nexus Generator + Matrix Parameters + OS Module Map
- [x] Component extraction refactor (AudioForgePanel, VaultAdminPanels)

- [x] Game Template Library — genre-specific PixiJS starters (fish shooting, slot machine, FPS, platformer, RPG, racing)
- [x] Slot Machine — Real weighted RNG, 9 symbols, paytable, bet controls, payline animation

## Architecture
```
/app
├── backend/
│   ├── routers/sla113.py         # SLA113 router (~2000 lines)
│   ├── sla113/
│   │   ├── models.py             # Pydantic models + game taxonomy
│   │   ├── vision_engine.py      # Gemini 3 Pro image gen
│   │   ├── logic_engine.py       # Game math/RTP generation
│   │   ├── composer_engine.py    # Bundle composition
│   │   └── audio_forge.py        # Audio asset generation with AI DSP
│   ├── static/deploys/           # Live deployed game files
│   └── server.py                 # FastAPI + WebSocket mounts
├── frontend/src/sla113/
│   ├── SLA113Page.jsx            # Main dashboard (~2100 lines, down from 2450)
│   ├── panels/
│   │   ├── AudioForgePanel.jsx   # Extracted Audio Forge (219 lines)
│   │   └── VaultAdminPanels.jsx  # ArtTech Nexus + Matrix Params (112 lines)
│   ├── audioSynth.js             # Web Audio API synthesis engine
│   ├── FrontlinePanel.jsx        # WebSocket real-time panel
│   ├── SpriteCutter.jsx          # Sprite sheet cutter
│   └── DependencyGraph.jsx       # Job dependency visualization
```

## Key Integrations
- **OpenAI GPT-4o-mini** — Emergent LLM Key (AI Terminal + Audio DSP enhancement)
- **Gemini 3 Pro** — User GEMINI_API_KEY (Vision Smith, no watermarks)
- **Vertex AI** — User VERTEX_AI_KEY stored (Audio Forge credential ready)

## Backlog
- [ ] Continue refactoring SLA113Page.jsx — extract Foundry (OS Builder, Vision Smith) and Empire panels (P3)
- [ ] APK compilation path in Build Pipeline (P3)
- [ ] Vertex AI actual audio waveform generation when SDK supports it (P3)
