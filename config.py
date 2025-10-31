# Configuration for The Evolving Kingdom Game

# Game Settings
TOTAL_TURNS = 8
INITIAL_FACTION_TRUST = 50  # 0-100 scale

# Faction Definitions
FACTIONS = {
    "merchants": {
        "name": "The Merchant Guild",
        "base_personality": "pragmatic and profit-oriented",
        "color": "\033[93m",  # Yellow
        "icon": "💰"
    },
    "nobles": {
        "name": "The Noble Houses",
        "base_personality": "proud and traditional",
        "color": "\033[95m",  # Magenta
        "icon": "👑"
    },
    "clergy": {
        "name": "The Sacred Order",
        "base_personality": "devout and moralistic",
        "color": "\033[96m",  # Cyan
        "icon": "⛪"
    },
    "commoners": {
        "name": "The Common Folk",
        "base_personality": "simple and hardworking",
        "color": "\033[92m",  # Green
        "icon": "🌾"
    }
}

# Decision Types (for variety in gameplay)
DECISION_CATEGORIES = [
    "Economic Policy",
    "Military Action",
    "Religious Matter",
    "Justice & Law",
    "Diplomacy",
    "Infrastructure",
    "Cultural Event",
    "Crisis Response"
]

# Color codes for terminal output
COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "header": "\033[94m",
    "success": "\033[92m",
    "warning": "\033[93m",
    "fail": "\033[91m",
    "info": "\033[96m"
}

# OpenAI Settings
OPENAI_MODEL = "gpt-3.5-turbo"  # Using GPT-3.5 for cost efficiency
OPENAI_TEMPERATURE = 0.7
