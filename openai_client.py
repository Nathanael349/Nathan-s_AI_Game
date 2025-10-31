"""
OpenAI GPT Client Module for The Evolving Kingdom
Handles all LLM tasks with clear separation of concerns
"""

import os
import json
from openai import OpenAI
from config import OPENAI_MODEL, OPENAI_TEMPERATURE

class KingdomAI:
    """Handles all AI interactions for the game"""
    
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = OPENAI_MODEL
        self.temperature = OPENAI_TEMPERATURE
    
    def _call_gpt(self, system_prompt, user_prompt, temperature=None):
        """Internal method to call GPT with error handling"""
        if temperature is None:
            temperature = self.temperature
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None
    
    # ==================== LLM TASK 1: GENERATION ====================
    def generate_faction_response(self, faction_data, decision, game_context):
        """
        Generate a faction's response to a player decision
        Uses current personality and memory of past events
        """
        system_prompt = """You are a faction in a medieval kingdom. Generate a response to the monarch's decision.
Your response should:
1. Be 2-3 sentences
2. Reflect your current personality and past experiences
3. Show emotion appropriate to the situation
4. Reference past events if they're relevant
Keep it dramatic and memorable!"""
        
        user_prompt = f"""Faction: {faction_data['name']}
Current Personality: {faction_data['current_personality']}
Trust Score: {faction_data['trust_score']}/100
Recent Memory: {json.dumps(faction_data['memory'][-3:] if faction_data['memory'] else [])}

The Monarch's Decision: {decision}

Game Context:
Turn: {game_context['turn']}
Previous Chronicle: {game_context.get('latest_chronicle', 'This is the beginning of the reign.')}

Generate this faction's response:"""
        
        return self._call_gpt(system_prompt, user_prompt)
    
    # ==================== LLM TASK 2: SENTIMENT ANALYSIS ====================
    def analyze_sentiment(self, faction_response):
        """
        Analyze the sentiment of a faction's response
        Returns: positive, negative, or neutral with confidence score
        """
        system_prompt = """You are a sentiment analyzer. Analyze the sentiment of faction responses.
Return ONLY a JSON object with this exact format:
{"sentiment": "positive" or "negative" or "neutral", "intensity": 0.0 to 1.0, "reasoning": "brief explanation"}"""
        
        user_prompt = f"""Analyze the sentiment of this faction response:

"{faction_response}"

Return JSON only:"""
        
        response = self._call_gpt(system_prompt, user_prompt, temperature=0.3)
        try:
            # Extract JSON from response (in case GPT adds extra text)
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
            return {"sentiment": "neutral", "intensity": 0.5, "reasoning": "Parse error"}
        except:
            return {"sentiment": "neutral", "intensity": 0.5, "reasoning": "Parse error"}
    
    # ==================== LLM TASK 3: SUMMARIZATION ====================
    def create_chronicle(self, turns_data, turn_range):
        """
        Create a historical chronicle summarizing recent events
        This summary will be fed back into future responses
        """
        system_prompt = """You are the Royal Chronicler. Summarize the kingdom's recent history.
Write in a dramatic, historical narrative style (3-4 sentences).
Capture the key events and their emotional impact on the realm."""
        
        user_prompt = f"""Summarize turns {turn_range[0]}-{turn_range[1]} of the kingdom's history:

{json.dumps(turns_data, indent=2)}

Write a dramatic chronicle entry:"""
        
        return self._call_gpt(system_prompt, user_prompt)
    
    # ==================== LLM TASK 4: TRANSFORMATION/PERSONALITY EVOLUTION ====================
    def evolve_personality(self, faction_data, recent_events):
        """
        Transform a faction's personality based on accumulated experiences
        This is where the LLM "digests" its previous outputs!
        """
        system_prompt = """You are a personality evolution engine. Based on a faction's experiences, describe how their personality has evolved.
Return ONLY a JSON object with this format:
{"new_personality": "brief personality description", "key_change": "what changed and why"}

The personality should be different but believable based on events."""
        
        user_prompt = f"""Faction: {faction_data['name']}
Original Personality: {faction_data['base_personality']}
Current Personality: {faction_data['current_personality']}
Trust Score: {faction_data['trust_score']}/100

Recent Events and Their Reactions:
{json.dumps(recent_events, indent=2)}

How has this faction's personality evolved? Return JSON only:"""
        
        response = self._call_gpt(system_prompt, user_prompt, temperature=0.6)
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
            return {"new_personality": faction_data['current_personality'], "key_change": "No change"}
        except:
            return {"new_personality": faction_data['current_personality'], "key_change": "Parse error"}
    
    # ==================== LLM TASK 5: PREDICTION ====================
    def predict_faction_reactions(self, decision_options, faction_states):
        """
        Predict how factions might react to potential decisions
        Helps player make informed choices
        """
        system_prompt = """You are a royal advisor. Predict how factions will likely react to each decision option.
Be brief but insightful. Consider each faction's current state."""
        
        user_prompt = f"""Decision Options:
{json.dumps(decision_options, indent=2)}

Current Faction States:
{json.dumps(faction_states, indent=2)}

Provide a brief prediction for each option (1-2 sentences each):"""
        
        return self._call_gpt(system_prompt, user_prompt, temperature=0.5)
    
    # ==================== LLM TASK 6: CLASSIFICATION ====================
    def classify_kingdom_state(self, game_state):
        """
        Classify the overall kingdom state based on faction relationships
        Returns: prosperity, rebellion, stability, or decline
        """
        system_prompt = """You are a kingdom analyst. Classify the kingdom's overall state.
Return ONLY a JSON object:
{"state": "prosperity" or "rebellion" or "stability" or "decline", "reason": "brief explanation"}"""
        
        user_prompt = f"""Analyze this kingdom state:

Average Trust: {game_state['average_trust']:.1f}/100
Faction States: {json.dumps(game_state['faction_summary'], indent=2)}
Recent Chronicle: {game_state.get('latest_chronicle', 'Beginning of reign')}

Classify the kingdom state (JSON only):"""
        
        response = self._call_gpt(system_prompt, user_prompt, temperature=0.3)
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
            return {"state": "stability", "reason": "Parse error"}
        except:
            return {"state": "stability", "reason": "Parse error"}
    
    # ==================== LLM TASK 7: REVIEW GENERATION ====================
    def generate_epic_review(self, full_game_state):
        """
        Generate the final 'Epic Kingdom History' review
        This reads ALL previous LLM outputs and creates a comprehensive narrative
        """
        system_prompt = """You are the Master Chronicler writing the definitive history of a monarch's reign.
Create an engaging, dramatic review that:
1. Shows how faction personalities evolved over time
2. Identifies key turning points
3. Rates the monarch's leadership style
4. Creates a narrative arc with dramatic flair
5. Includes memorable quotes from factions
6. Suggests an alternative timeline

Use markdown formatting with headers, bold text, and emojis. Make it enjoyable to read!"""
        
        user_prompt = f"""Create the Epic Kingdom History for this reign:

{json.dumps(full_game_state, indent=2)}

Write a comprehensive, dramatic review:"""
        
        return self._call_gpt(system_prompt, user_prompt, temperature=0.8)
    
    # ==================== LLM TASK 8: NARRATIVE GENERATION ====================
    def generate_story_beat(self, game_context, trigger_type):
        """
        Generate narrative story beats based on relationship trajectories
        Creates dramatic moments when relationships cross thresholds
        """
        system_prompt = """You are a narrative generator. Create a dramatic story moment based on the kingdom's state.
Write 2-3 vivid sentences that capture the moment. Make it memorable!"""
        
        user_prompt = f"""Trigger: {trigger_type}
Game Context: {json.dumps(game_context, indent=2)}

Generate a dramatic story beat:"""
        
        return self._call_gpt(system_prompt, user_prompt)
