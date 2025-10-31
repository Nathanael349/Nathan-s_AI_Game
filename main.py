"""
The Evolving Kingdom - Main Game Loop
A diplomacy simulator where faction personalities evolve based on AI-generated responses
"""

import os
import sys
from dotenv import load_dotenv
from config import TOTAL_TURNS, FACTIONS, DECISION_CATEGORIES, COLORS
from game_state import GameState
from openai_client import KingdomAI

class EvolvinKingdom:
    """Main game controller"""
    
    def __init__(self):
        load_dotenv()
        self.game_state = GameState()
        self.ai = KingdomAI()
        self.colors = COLORS
    
    def print_colored(self, text, color="reset", bold=False):
        """Print colored text to terminal"""
        prefix = self.colors["bold"] if bold else ""
        print(f"{prefix}{self.colors.get(color, '')}{text}{self.colors['reset']}")
    
    def print_header(self, text):
        """Print a section header"""
        print("\n" + "=" * 70)
        self.print_colored(text, "header", bold=True)
        print("=" * 70 + "\n")
    
    def display_welcome(self):
        """Display welcome screen"""
        self.print_header("🏰 THE EVOLVING KINGDOM 🏰")
        print("A Diplomacy Simulator with AI-Powered Faction Evolution\n")
        print("In this game, you are a monarch making crucial decisions.")
        print("Each decision affects your relationship with four factions.")
        print("But beware: factions REMEMBER and their personalities EVOLVE")
        print("based on how you treat them...\n")
        print(f"You have {TOTAL_TURNS} turns to prove yourself as a leader.")
        print("\n" + "-" * 70 + "\n")
    
    def get_player_name(self):
        """Get player name"""
        name = input("Enter your name, Your Majesty: ").strip()
        return name if name else "Anonymous Monarch"
    
    def display_factions(self):
        """Display all factions and their current state"""
        self.print_header("📊 FACTION STATUS")
        
        for faction_id, faction_info in FACTIONS.items():
            faction_data = self.game_state.get_faction_data(faction_id)
            color = faction_info["color"]
            icon = faction_info["icon"]
            
            print(f"{color}{icon} {faction_data['name']}{self.colors['reset']}")
            print(f"   Personality: {faction_data['current_personality']}")
            print(f"   Trust: {faction_data['trust_score']}/100")
            
            # Show personality evolution if it happened
            if faction_data['personality_evolution_log']:
                last_evolution = faction_data['personality_evolution_log'][-1]
                self.print_colored(f"   ⚡ Recently evolved: {last_evolution['reason']}", "warning")
            print()
    
    def generate_decision_options(self, turn):
        """Generate decision options for this turn"""
        # Create varied decision categories
        category = DECISION_CATEGORIES[(turn - 1) % len(DECISION_CATEGORIES)]
        
        # Predefined interesting decisions
        decisions = {
            1: [
                "Raise taxes to fund a grand festival",
                "Lower taxes to win the people's favor",
                "Keep taxes the same but audit the wealthy"
            ],
            2: [
                "Conscript commoners for border defense",
                "Hire expensive mercenaries instead",
                "Negotiate a peace treaty with neighbors"
            ],
            3: [
                "Build a grand cathedral",
                "Build markets and trade roads",
                "Build fortifications and walls"
            ],
            4: [
                "Execute a corrupt noble as an example",
                "Exile the noble but seize their lands",
                "Pardon the noble for a large fine"
            ],
            5: [
                "Host a diplomatic summit with rival kingdoms",
                "Declare neutrality and isolate the kingdom",
                "Form a military alliance with a powerful neighbor"
            ],
            6: [
                "Fund new irrigation projects for farms",
                "Invest in merchant shipping ventures",
                "Build a royal academy of learning"
            ],
            7: [
                "Declare a week-long tournament and feast",
                "Commission epic poetry about your reign",
                "Ban public celebrations to save resources"
            ],
            8: [
                "A plague outbreak - quarantine the city",
                "A plague outbreak - pray and trust in faith",
                "A plague outbreak - evacuate to the countryside"
            ]
        }
        
        return decisions.get(turn, [
            "Make a conservative, safe decision",
            "Make a bold, risky decision",
            "Delegate the decision to advisors"
        ])
    
    def get_player_decision(self, turn, options):
        """Get player's decision"""
        self.print_header(f"👑 TURN {turn}/{TOTAL_TURNS}")
        
        # Show kingdom state classification if available
        if turn > 1:
            context = self.game_state.get_game_context()
            self.print_colored(f"Kingdom Average Trust: {context['average_trust']:.1f}/100", "info")
            print()
        
        print("What is your decision, Your Majesty?\n")
        
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        # Optional: Show AI prediction
        if turn > 2:
            show_prediction = input("\nWould you like to consult your advisor? (y/n): ").lower() == 'y'
            if show_prediction:
                print("\n💭 Your advisor whispers...\n")
                faction_states = {
                    fid: {
                        "personality": f["current_personality"],
                        "trust": f["trust_score"]
                    }
                    for fid, f in self.game_state.get_all_factions().items()
                }
                prediction = self.ai.predict_faction_reactions(options, faction_states)
                self.print_colored(prediction, "info")
                print()
        
        # Get choice
        while True:
            try:
                choice = int(input(f"\nEnter your choice (1-{len(options)}): "))
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number.")
    
    def process_turn(self, turn, decision):
        """
        Process a turn - this is where the magic happens!
        The LLM generates responses, analyzes them, and updates state
        """
        self.print_header("🗣️  FACTION RESPONSES")
        
        turn_data = {
            "turn": turn,
            "decision": decision,
            "responses": {}
        }
        
        game_context = self.game_state.get_game_context()
        
        # STEP 1: Generate faction responses (LLM Task: Generation)
        for faction_id, faction_info in FACTIONS.items():
            faction_data = self.game_state.get_faction_data(faction_id)
            
            print(f"\n{faction_info['color']}{faction_info['icon']} {faction_data['name']} speaks:{self.colors['reset']}")
            print("Thinking...", end="", flush=True)
            
            # LLM generates response based on current personality and memory
            response = self.ai.generate_faction_response(
                faction_data,
                decision,
                game_context
            )
            
            print("\r" + " " * 20 + "\r", end="")  # Clear "Thinking..."
            print(f'"{response}"')
            
            # STEP 2: Analyze sentiment (LLM Task: Sentiment Analysis)
            sentiment = self.ai.analyze_sentiment(response)
            
            # Show sentiment indicator
            sentiment_icons = {"positive": "😊", "negative": "😠", "neutral": "😐"}
            sentiment_colors = {"positive": "success", "negative": "fail", "neutral": "warning"}
            icon = sentiment_icons.get(sentiment["sentiment"], "😐")
            
            self.print_colored(
                f"{icon} Sentiment: {sentiment['sentiment']} (intensity: {sentiment['intensity']:.2f})",
                sentiment_colors.get(sentiment["sentiment"], "reset")
            )
            
            # STEP 3: Update trust based on sentiment
            trust_delta = 0
            if sentiment["sentiment"] == "positive":
                trust_delta = int(sentiment["intensity"] * 15)
            elif sentiment["sentiment"] == "negative":
                trust_delta = -int(sentiment["intensity"] * 15)
            
            if trust_delta != 0:
                self.game_state.update_faction_trust(faction_id, trust_delta, decision)
                change_text = f"+{trust_delta}" if trust_delta > 0 else str(trust_delta)
                self.print_colored(f"Trust changed: {change_text}", "info")
            
            # Store response in game state (for LLM to read later)
            self.game_state.add_faction_memory(faction_id, decision, response, sentiment)
            
            turn_data["responses"][faction_id] = {
                "response": response,
                "sentiment": sentiment,
                "trust_change": trust_delta
            }
        
        # STEP 4: Save turn data
        self.game_state.add_turn_record(turn_data)
        
        # STEP 5: Every 2 turns, create chronicle and evolve personalities
        if turn % 2 == 0 and turn < TOTAL_TURNS:
            self.create_chronicle(turn)
            self.evolve_personalities(turn)
        
        # STEP 6: Classify kingdom state
        if turn % 2 == 0:
            context = self.game_state.get_game_context()
            classification = self.ai.classify_kingdom_state(context)
            self.game_state.add_kingdom_classification(classification)
            
            print("\n" + "-" * 70)
            self.print_colored(f"📜 Kingdom State: {classification['state'].upper()}", "header", bold=True)
            self.print_colored(f"   {classification['reason']}", "info")
            print("-" * 70)
        
        # STEP 7: Generate story beats for dramatic moments
        avg_trust = self.game_state.get_average_trust()
        if avg_trust > 80 and turn > 3:
            beat = self.ai.generate_story_beat(game_context, "high_trust")
            self.game_state.add_story_beat(beat, "high_trust")
            print(f"\n✨ {beat}")
        elif avg_trust < 30:
            beat = self.ai.generate_story_beat(game_context, "rebellion_risk")
            self.game_state.add_story_beat(beat, "rebellion_risk")
            self.print_colored(f"\n⚠️  {beat}", "fail", bold=True)
        
        input("\nPress Enter to continue...")
    
    def create_chronicle(self, turn):
        """
        Create a chronicle summarizing recent turns
        This is LLM Task: Summarization (digesting its own outputs)
        """
        print("\n" + "~" * 70)
        self.print_colored("📖 The Royal Chronicler writes...", "info", bold=True)
        
        turn_range = (turn - 1, turn)
        recent_turns = self.game_state.get_recent_turns(2)
        
        chronicle = self.ai.create_chronicle(recent_turns, turn_range)
        self.game_state.add_chronicle(turn_range, chronicle)
        
        print(f'\n"{chronicle}"')
        print("~" * 70 + "\n")
    
    def evolve_personalities(self, turn):
        """
        Evolve faction personalities based on accumulated experiences
        This is LLM Task: Transformation (digesting its own outputs!)
        """
        self.print_colored("\n⚡ FACTION PERSONALITIES EVOLVING...\n", "warning", bold=True)
        
        for faction_id, faction_info in FACTIONS.items():
            faction_data = self.game_state.get_faction_data(faction_id)
            recent_memory = faction_data["memory"][-4:]  # Last 4 interactions
            
            if len(recent_memory) >= 2:  # Need some history to evolve
                evolution = self.ai.evolve_personality(faction_data, recent_memory)
                
                if evolution["new_personality"] != faction_data["current_personality"]:
                    self.game_state.update_faction_personality(
                        faction_id,
                        evolution["new_personality"],
                        evolution["key_change"]
                    )
                    
                    print(f"{faction_info['icon']} {faction_data['name']}:")
                    self.print_colored(f"   Was: {faction_data['current_personality']}", "warning")
                    self.print_colored(f"   Now: {evolution['new_personality']}", "success")
                    print(f"   Why: {evolution['key_change']}\n")
        
        input("Press Enter to continue...")
    
    def generate_final_review(self):
        """
        Generate the epic final review
        This is where the LLM digests ALL of its previous outputs!
        """
        self.print_header("📜 THE EPIC KINGDOM HISTORY 📜")
        print("The Master Chronicler compiles the complete history of your reign...\n")
        print("This may take a moment...\n")
        
        full_state = self.game_state.get_full_state_for_review()
        review = self.ai.generate_epic_review(full_state)
        
        print(review)
        print("\n" + "=" * 70)
        print("Thank you for playing The Evolving Kingdom!")
        print("=" * 70 + "\n")
        
        # Save review to file
        with open("kingdom_history.md", "w", encoding="utf-8") as f:
            f.write(f"# Kingdom History: {full_state['player_name']}\n\n")
            f.write(review)
        
        self.print_colored("📄 Full history saved to kingdom_history.md", "success")
    
    def play(self):
        """Main game loop"""
        self.display_welcome()
        
        # Initialize or load game
        player_name = self.get_player_name()
        self.game_state.initialize_new_game(player_name)
        
        print(f"\nWelcome, {player_name}! Your reign begins now.\n")
        input("Press Enter to begin...")
        
        # Main game loop
        for turn in range(1, TOTAL_TURNS + 1):
            self.display_factions()
            
            options = self.generate_decision_options(turn)
            decision = self.get_player_decision(turn, options)
            
            self.process_turn(turn, decision)
        
        # Game over - generate final review
        self.generate_final_review()

def main():
    """Entry point"""
    try:
        game = EvolvinKingdom()
        game.play()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Your kingdom falls into chaos!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        print("The kingdom has encountered an unexpected crisis!")
        sys.exit(1)

if __name__ == "__main__":
    main()
