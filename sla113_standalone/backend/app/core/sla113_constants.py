"""SLA113 Platform Constants"""

# ─── Game Types (16 supported) ───
GAME_TYPES = {
    # Casino/Arcade
    "fish_shooter": {"name": "Fish Shooter", "description": "Multiplayer fish hunting arcade game with weapon upgrades", "category": "arcade"},
    "slot_machine": {"name": "Slot Machine", "description": "Classic/video slot with reels, paylines, and bonus rounds", "category": "casino"},
    "crash_game": {"name": "Crash Game", "description": "Multiplier-based game with cash-out mechanics", "category": "casino"},
    "card_game": {"name": "Card Game", "description": "Poker, blackjack, or custom card-based game", "category": "casino"},
    # AAA / Universal
    "open_world": {"name": "Open World (GTA Style)", "description": "Cinematic urban open world with missions, vehicles, and NPC AI", "category": "aaa"},
    "tactical_fps": {"name": "Tactical FPS (COD Style)", "description": "Military tactical shooter with loadouts, maps, and multiplayer", "category": "aaa"},
    "fighting_game": {"name": "Fighting Game (MK Style)", "description": "Character movesets, combos, frame data, and fatalities", "category": "aaa"},
    "fantasy_rpg": {"name": "Fantasy RPG", "description": "Magical open world RPG with quests, stats, and crafting", "category": "aaa"},
    "platformer": {"name": "Platformer", "description": "Side-scrolling platform game with levels and enemies", "category": "action"},
    "puzzle": {"name": "Puzzle", "description": "Match-3, tile-based, or logic puzzle game", "category": "casual"},
    "tower_defense": {"name": "Tower Defense", "description": "Strategic tower placement to defend against waves", "category": "strategy"},
    "runner": {"name": "Endless Runner", "description": "Auto-running character with obstacles and power-ups", "category": "casual"},
    "battle_royale": {"name": "Battle Royale", "description": "Last-player-standing arena combat game", "category": "action"},
    "racing": {"name": "Racing", "description": "High-speed vehicle racing with tracks and power-ups", "category": "action"},
    "survival_horror": {"name": "Survival Horror", "description": "Atmospheric horror with resource management and puzzles", "category": "aaa"},
    "sports": {"name": "Sports", "description": "Team or individual sports simulation", "category": "sports"},
}

# ─── Night Queue Job Presets ───
JOB_STAGES = {
    "ARCADE_40": ["Asset Indexing", "Sprite Generation", "Physics Binding", "AI Balancing", "Package Export"],
    "ARCADE_60": ["Asset Indexing", "Sprite Generation", "Physics Binding", "AI Balancing", "Network Layer", "Package Export"],
    "SLOTS_20": ["Reel Mapping", "Paytable Calculation", "RTP Verification", "Visual Rendering", "Package Export"],
    "OPEN_WORLD": ["World Generation", "NPC Scripting", "Physics Binding", "AI Pathing", "Texture Streaming", "LOD Pipeline", "Package Export"],
    "CASINO_SUITE": ["Game Selection Matrix", "RTP Calibration", "Lobby UI", "Payment Gateway", "Package Export"],
    "CUSTOM_OS_BUILD": ["Init Scaffold", "Core Logic", "Asset Pipeline", "Integration Pass", "Package Export"],
    "AAA_FISH_SLOT": ["Asset Indexing", "Sprite Generation", "Boss Patterns", "RTP Verification", "Package Export"],
    "GTA5_TYPE": ["World Generation", "NPC Scripting", "Vehicle Physics", "Mission Logic", "Package Export"],
    "COD_WARFARE": ["Map Generation", "Weapon Balancing", "Netcode Layer", "AI Opponents", "Package Export"],
    "FANTASY_RPG": ["Lore Generation", "Skill Trees", "Monster AI", "Dungeon Layout", "Package Export"],
}
DEFAULT_JOB_STAGES = ["Initialization", "Core Processing", "Asset Compilation", "Quality Check", "Package Export"]

# ─── Compliance Jurisdictions ───
COMPLIANCE_CHECKS = {
    "GLI": ["RTP Verification", "RNG Seed Audit", "Paytable Integrity", "Max Bet Limits", "Session Timeout Compliance", "Responsible Gaming Controls"],
    "MGA": ["RTP Verification", "RNG Certification", "Player Protection", "Anti-Money Laundering", "Game History Logging"],
    "UKGC": ["RTP Verification", "RNG Audit", "Fairness Testing", "Underage Prevention", "Self-Exclusion", "Advertising Compliance"],
    "CURACAO": ["RTP Verification", "RNG Basics", "Fair Play Attestation"],
    "INTERNAL": ["RTP Verification", "RNG Seed Audit", "Stress Test", "Edge Case Validation"],
}

# ─── Vision Smith Asset Types & Styles ───
ASSET_TYPE_PROMPTS = {
    "sprite_sheet": "Create a professional game sprite sheet with multiple animation frames arranged in a grid layout. Each frame should be clearly separated. Characters/objects should be centered in each cell with consistent proportions. Transparent or solid dark background between frames. Suitable for game engine import and slicing. ",
    "concept_art": "Create a AAA-quality game concept art illustration. Rich detail, dramatic lighting, cinematic composition. Professional digital painting quality suitable for a game studio art bible. ",
    "character": "Create a detailed game character design with front-facing full body view. Clean silhouette, distinct features, game-ready proportions. Professional character concept art. Include subtle detail in armor/clothing/accessories. Dynamic but readable pose. ",
    "boss": "Create an imposing game boss character design. Massive scale, intimidating presence, unique silhouette. Multiple attack indicators visible (weapons, magic auras, armored weak points). Epic scale, dramatic lighting. AAA game quality boss concept art. ",
    "tileset": "Create a seamless game tileset with multiple tile variations arranged in a grid. Include ground, walls, corners, edges, and decorative variants. Each tile should seamlessly connect. Consistent art style across all tiles. Top-down or side-view as appropriate. Game-ready quality. ",
    "background": "Create a wide panoramic game background/environment. Parallax-ready with clear foreground, midground, and background layers. Rich atmospheric detail, mood lighting. Suitable for scrolling game backgrounds. Cinematic quality. ",
    "ui_element": "Create a set of game UI elements on a dark/transparent background. Include buttons, frames, health bars, inventory slots, dialog boxes, and icons. Consistent art style, clean edges, scalable design. Professional game UI kit quality with glowing/metallic accents. ",
    "vfx": "Create game visual effects sprites: explosions, fire, lightning, magic particles, smoke, energy beams. Each effect on transparent/dark background, suitable for sprite sheet extraction. Vibrant, dynamic, with alpha-ready edges. Multiple frames showing effect progression. ",
}

STYLE_PROMPTS = {
    "pixel_art": "Pixel art style: crisp 16-32bit pixels, limited but vibrant color palette, no anti-aliasing on edges, retro game aesthetic with modern polish.",
    "vector": "Clean vector illustration: flat bold colors, sharp geometric edges, minimal gradients, modern mobile game aesthetic.",
    "3d_render": "High-quality 3D render: physically-based materials, dramatic volumetric lighting, ambient occlusion, AAA game production quality.",
    "hand_drawn": "Hand-painted illustration: visible brushstrokes, rich watercolor textures, ink outlines, artisan game art quality like Hollow Knight or Hades.",
    "anime": "Japanese anime/manga art style: cel shading, vibrant saturated colors, expressive features, clean lineart, Studio Ghibli meets game art quality.",
    "neon_cyberpunk": "Cyberpunk neon aesthetic: deep black backgrounds, electric neon glows (cyan, magenta, gold), holographic effects, Blade Runner meets arcade game.",
    "dark_fantasy": "Dark fantasy art: muted earth tones with blood red/gold accents, gritty textures, medieval horror atmosphere, Dark Souls quality.",
    "military_realism": "Military realism: tactical gear detail, weathered textures, muted olive/tan/black palette, photorealistic rendering, Call of Duty art direction.",
    "comic_book": "Bold comic book style: thick outlines, halftone dots, dynamic action lines, saturated primary colors, Marvel/DC game adaptation quality.",
    "low_poly": "Stylized low-poly 3D: faceted surfaces, vibrant flat colors per face, clean geometric forms, Monument Valley meets game art.",
}

# ─── Default Pipeline Seeds ───
DEFAULT_PIPELINES = [
    {"name": "Lead Qualification Engine", "type": "Automation", "lane": 1},
    {"name": "CRM Syncing Logic", "type": "Automation", "lane": 1},
    {"name": "Pro Voice Over (SaaS)", "type": "Utility", "lane": 2},
    {"name": "SMS/Email Gateway", "type": "Utility", "lane": 2},
    {"name": "White-Label Instance", "type": "Sovereign", "lane": 3},
    {"name": "Managed Sovereignty", "type": "Sovereign", "lane": 3},
]
