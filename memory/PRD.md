# SLA113 — Universal AI Game Studio Operator OS

## Product Overview
SLA113 is the **sovereign root OS** for AI-powered game creation. Cultural backbone: Aztec myth + Chicano SGV + IELA roots. Target: surpass FireKirin/Juwa.

## Game Engines (FireKirin/Juwa Tier)

### Fish Shooter Engine (fish_engine.py)
- 6 weapons: Cannon, Laser, Chain Lightning, Bomb, Auto, Railgun
- 12 fish species (8 tiers), 3 Bosses (Jaguar Warrior, Quetzalcoatl, Tezcatlipoca), 4 Special fish
- Progressive jackpot, 7 bet levels, sprite-based rendering with animated spritesheets
- Sprite loader: loads registered spritesheets from Sprite Registry, animates idle/attack/death

### Video Slots Engine (slots_engine.py)  
- 5x3, 20 paylines, 4 progressive jackpots, cascading wins, hold & spin, bonus wheel
- Custom symbol support (Southern Lifestyle theme)

### Sprite Asset Registry
- CRUD API for spritesheet registration with frame dimensions, grid layout, animation maps
- Supports: fish, boss, special, weapon, background, ui entity types
- Registered: Jaguar Warrior, Quetzalcoatl Fireborn, Mictlantecuilti Bone Sovereign, Quetzalflare Prismwing

## Architecture
```
/app/backend/sla113/
  ├── fish_engine.py        # FireKirin-tier fish shooter with sprite support
  ├── slots_engine.py       # Juwa-tier video slots
  ├── fish_multiplayer.py   # WebSocket multiplayer
  ├── game_templates.py     # Template router
  ├── audio_forge.py, vision_engine.py, logic_engine.py, composer_engine.py, models.py
/app/frontend/src/sla113/panels/
  ├── AudioForgePanel.jsx, FishMultiplayerPanel.jsx, SlotSymbolsPanel.jsx
  ├── SpriteRegistryPanel.jsx  # Sprite asset management UI
  ├── VaultAdminPanels.jsx
```

## Backlog
- [ ] Wire sprites into compile pipeline (inject sprite URLs into GAME_CONFIG.sprites) (P0)
- [ ] Agent/distributor cashier system (P1)
- [ ] Game library lobby with thumbnails (P2)
- [ ] Tournament system (P3)
