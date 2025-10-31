"""
Game State Management for The Evolving Kingdom
Handles JSON persistence and world state tracking
"""

import json
import os
from datetime import datetime
from config import FACTIONS, INITIAL_FACTION_TRUST

class GameState:
    """Manages the persistent game state with JSON serialization"""
    
    def __init__(self, filename="game_state.json"):
        self.filename = filename
        self.state = None
    
    def initialize_new_game(self, player_name):
        """Create a fresh game state"""
        self.state = {
            "player_name": player_name,
            "current_turn": 1,
            "game_started": datetime.now().isoformat(),
            
            # Faction data - this is where LLM outputs accumulate
            "factions": {},
            
            # History tracking - LLM will read and digest these
            "turn_history": [],
            "kingdom_chronicles": [],
            
            # Metadata for analysis
            "story_beats": [],
            "kingdom_state_history": []
        }
        
        # Initialize all factions
        for faction_id, faction_info in FACTIONS.items():
            self.state["factions"][faction_id] = {
                "id": faction_id,
                "name": faction_info["name"],
                "base_personality": faction_info["base_personality"],
                "current_personality": faction_info["base_personality"],
                "trust_score": INITIAL_FACTION_TRUST,
                "memory": [],  # Will store LLM-generated responses
                "personality_evolution_log": []  # Track how personality changes
            }
        
        self.save()
        return self.state
    
    def load(self):
        """Load game state from JSON"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.state = json.load(f)
            return True
        return False
    
    def save(self):
        """Save game state to JSON"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
    
    def add_turn_record(self, turn_data):
        """
        Add a turn's data to history
        This is what the LLM will read to generate future responses
        """
        self.state["turn_history"].append(turn_data)
        self.state["current_turn"] += 1
        self.save()
    
    def add_chronicle(self, turn_range, chronicle_text):
        """
        Add a chronicle summary (LLM-generated)
        Future LLM calls will read this instead of raw turn data
        """
        self.state["kingdom_chronicles"].append({
            "turns": f"{turn_range[0]}-{turn_range[1]}",
            "chronicle": chronicle_text,
            "timestamp": datetime.now().isoformat()
        })
        self.save()
    
    def update_faction_personality(self, faction_id, new_personality, reason):
        """
        Update a faction's personality (LLM transformation)
        This is the KEY "digestion" mechanism
        """
        faction = self.state["factions"][faction_id]
        old_personality = faction["current_personality"]
        
        faction["current_personality"] = new_personality
        faction["personality_evolution_log"].append({
            "turn": self.state["current_turn"],
            "old": old_personality,
            "new": new_personality,
            "reason": reason
        })
        self.save()
    
    def update_faction_trust(self, faction_id, delta, reason):
        """Update trust score based on sentiment analysis"""
        faction = self.state["factions"][faction_id]
        faction["trust_score"] = max(0, min(100, faction["trust_score"] + delta))
        
        # Record in memory
        faction["memory"].append({
            "turn": self.state["current_turn"],
            "trust_change": delta,
            "reason": reason,
            "new_trust": faction["trust_score"]
        })
        self.save()
    
    def add_faction_memory(self, faction_id, decision, response, sentiment_data):
        """
        Add a memory entry for a faction
        Stores the LLM's own output for future reference
        """
        faction = self.state["factions"][faction_id]
        faction["memory"].append({
            "turn": self.state["current_turn"],
            "decision": decision,
            "response": response,
            "sentiment": sentiment_data["sentiment"],
            "intensity": sentiment_data["intensity"]
        })
        self.save()
    
    def add_story_beat(self, beat_text, trigger):
        """Add a narrative story beat"""
        self.state["story_beats"].append({
            "turn": self.state["current_turn"],
            "beat": beat_text,
            "trigger": trigger
        })
        self.save()
    
    def add_kingdom_classification(self, classification):
        """Add kingdom state classification"""
        self.state["kingdom_state_history"].append({
            "turn": self.state["current_turn"],
            "state": classification["state"],
            "reason": classification["reason"]
        })
        self.save()
    
    def get_faction_data(self, faction_id):
        """Get current faction data"""
        return self.state["factions"][faction_id]
    
    def get_all_factions(self):
        """Get all faction data"""
        return self.state["factions"]
    
    def get_average_trust(self):
        """Calculate average trust across all factions"""
        total = sum(f["trust_score"] for f in self.state["factions"].values())
        return total / len(self.state["factions"])
    
    def get_latest_chronicle(self):
        """Get most recent chronicle or None"""
        if self.state["kingdom_chronicles"]:
            return self.state["kingdom_chronicles"][-1]["chronicle"]
        return None
    
    def get_recent_turns(self, count=2):
        """Get recent turn history"""
        return self.state["turn_history"][-count:] if self.state["turn_history"] else []
    
    def get_game_context(self):
        """
        Get current game context for LLM calls
        This packages the world state for the AI to digest
        """
        return {
            "turn": self.state["current_turn"],
            "latest_chronicle": self.get_latest_chronicle(),
            "average_trust": self.get_average_trust(),
            "faction_summary": {
                fid: {
                    "name": f["name"],
                    "personality": f["current_personality"],
                    "trust": f["trust_score"]
                }
                for fid, f in self.state["factions"].items()
            }
        }
    
    def get_full_state_for_review(self):
        """
        Get complete game state for final review generation
        The LLM will digest ALL of its previous outputs here
        """
        return self.state
