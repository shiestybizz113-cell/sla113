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
- [x] Deploy Engine — Real static file hosting with live playable game preview (iframe in dashboard)
- [x] Sprite Cutter + Animation Preview
- [x] Boss Bestiary
- [x] Universe Registry (auto-discovery, interactive cards)
- [x] WebSocket Frontline (real-time metrics)
- [x] Full 29-type game taxonomy with categorized dropdowns
- [x] Standalone project export (sla113_standalone.zip)
- [x] Audio Forge Engine — AI-enhanced DSP + Web Audio API synthesis (play/preview + WAV export)
- [x] Admin Control Vault — ArtTech Nexus Generator + Matrix Parameters + OS Module Map
- [x] Game Template Library — Genre-specific PixiJS starters (fish, slots, FPS, platformer, RPG, racing)
- [x] **5-Reel Video Slots** — Wilds, Scatters, Free Spins with multiplier, 9 paylines, expanding wilds
- [x] **Custom Slot Symbol Sets** — Create themed reel symbols (e.g., Southern Lifestyle: LOWRIDER/SKULL/ROSE/CROSS)
- [x] **Multiplayer Fish Shooting Lobby** — WebSocket rooms, real-time shared fish, scoreboard, chat, ammo system
- [x] Component extraction (AudioForgePanel, VaultAdminPanels, FishMultiplayerPanel, SlotSymbolsPanel)

## Architecture
```
/app
├── backend/
│   ├── routers/sla113.py           # SLA113 router (~2200 lines)
│   ├── sla113/
│   │   ├── models.py               # Pydantic models + game taxonomy
│   │   ├── vision_engine.py        # Gemini 3 Pro image gen
│   │   ├── logic_engine.py         # Game math/RTP generation
│   │   ├── composer_engine.py      # Bundle composition
│   │   ├── audio_forge.py          # Audio asset generation with AI DSP
│   │   ├── game_templates.py       # Genre-specific PixiJS game code generators
│   │   └── fish_multiplayer.py     # WebSocket multiplayer fish shooting server
│   ├── static/deploys/             # Live deployed game files
│   └── server.py                   # FastAPI + WebSocket mounts
├── frontend/src/sla113/
│   ├── SLA113Page.jsx              # Main dashboard (~2180 lines)
│   ├── panels/
│   │   ├── AudioForgePanel.jsx     # Audio Forge with Web Audio synthesis
│   │   ├── VaultAdminPanels.jsx    # ArtTech Nexus + Matrix Params
│   │   ├── FishMultiplayerPanel.jsx # Multiplayer Fish Arena UI
│   │   └── SlotSymbolsPanel.jsx    # Custom Reel Symbol Creator
│   ├── audioSynth.js               # Web Audio API synthesis engine
│   ├── FrontlinePanel.jsx          # WebSocket real-time panel
│   ├── SpriteCutter.jsx            # Sprite sheet cutter
│   └── DependencyGraph.jsx         # Job dependency visualization
```

## Key Integrations
- **OpenAI GPT-4o-mini** — Emergent LLM Key (AI Terminal + Audio DSP enhancement)
- **Gemini 3 Pro** — User GEMINI_API_KEY (Vision Smith, no watermarks)
- **Vertex AI** — User VERTEX_AI_KEY stored (Audio Forge credential ready)

## Backlog
- [ ] Continue extracting Foundry (OS Builder, Vision Smith) + Empire (Mint Ledger, Revenue, Bestiary) panels (P3)
- [ ] Wire custom symbols into 5-reel build pipeline (pass symbol set ID to compile) (P2)
- [ ] Tournament system across tenants (P3)
- [ ] APK compilation path in Build Pipeline (P3)
