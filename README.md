# 🏰 The Evolving Kingdom - Game Manual

**An AI-Powered Diplomacy Simulator**  
*By Nathanael Richard Ha Hanes*

---

## 🎮 What is This Game?

**The Evolving Kingdom** is a text-based diplomacy simulator where you play as a monarch making crucial decisions that affect four factions in your kingdom. The unique twist? The factions have AI-powered personalities that **genuinely evolve** based on how you treat them throughout the game.

---

## 📋 Table of Contents

1. [Quick Start](#-quick-start)
2. [Requirements](#-requirements)
3. [Installation](#-installation)
4. [How to Play](#-how-to-play)
5. [Game Mechanics](#-game-mechanics)
6. [Understanding the Interface](#-understanding-the-interface)
7. [Tips & Strategies](#-tips--strategies)
8. [How to End](#-how-to-end)
9. [Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start

**For the impatient:**

```bash
# 1. Install dependencies
pip install openai python-dotenv

# 2. Add your OpenAI API key to .env file
echo "OPENAI_API_KEY=your_key_here" > .env

# 3. Run the game
python3 main.py
```

That's it! Continue reading for detailed instructions.

---

## 💻 Requirements

### System Requirements
- **Python**: 3.7 or higher
- **Internet Connection**: Required for OpenAI API calls
- **Terminal**: Any modern terminal (macOS Terminal, Windows Command Prompt, Linux shell)

### API Requirements
- **OpenAI API Key**: You need a valid OpenAI API key
  - Get one at: https://platform.openai.com/api-keys
  - Cost per game: ~$0.10 (very affordable!)

### Python Packages
- `openai` (>= 1.0.0)
- `python-dotenv` (>= 1.0.0)

---

## 📦 Installation

### Step 1: Clone or Download the Repository

If you have git:
```bash
git clone https://github.com/Nathanael349/Nathan-s_AI_Game.git
cd Nathan-s_AI_Game
```

Or download as ZIP and extract.

### Step 2: Install Python Dependencies

**Option A: Using pip (recommended)**
```bash
pip install -r requirements.txt
```

**Option B: Manual installation**
```bash
pip install openai python-dotenv
```

**Option C: Using the setup script (macOS/Linux)**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Configure Your OpenAI API Key

**Create a `.env` file:**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
nano .env
# or use any text editor
```

**Add your key to the `.env` file:**
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

⚠️ **Important**: 
- Never commit your `.env` file to git (it's already in `.gitignore`)
- Keep your API key secret!
- Make sure there are no spaces around the `=` sign

### Step 4: Verify Installation

Test that everything is working:
```bash
python3 -c "import openai; print('✓ OpenAI installed')"
python3 -c "from dotenv import load_dotenv; print('✓ dotenv installed')"
```

You should see both checkmarks if installation was successful.

---

## 🎮 How to Play

### Starting the Game

1. **Open your terminal** and navigate to the game directory:
   ```bash
   cd path/to/Nathan-s_AI_Game
   ```

2. **Run the game**:
   ```bash
   python3 main.py
   ```

3. **Enter your name** when prompted:
   ```
   Enter your name, Your Majesty: Richard
   ```

4. **Press Enter** to begin your reign!

### Gameplay Flow

The game consists of **8 turns**. Each turn follows this pattern:

#### 1. **Review Faction Status**
You'll see the current state of all four factions:
- 💰 **The Merchant Guild** - Business and trade
- 👑 **The Noble Houses** - Aristocracy and power
- ⛪ **The Sacred Order** - Religion and faith
- 🌾 **The Common Folk** - Ordinary citizens

Each faction shows:
- Current personality (e.g., "pragmatic and profit-oriented")
- Trust score (0-100)
- Recent personality changes (if any)

#### 2. **Make Your Decision**
You'll be presented with **3 decision options**. These vary by turn and category:
- Economic policies
- Military actions
- Religious matters
- Justice and law
- Diplomacy
- Infrastructure
- Cultural events
- Crisis responses

**Example:**
```
What is your decision, Your Majesty?

1. Raise taxes to fund a grand festival
2. Lower taxes to win the people's favor
3. Keep taxes the same but audit the wealthy

Enter your choice (1-3):
```

#### 3. **Optional: Consult Your Advisor**
After turn 2, you can ask for predictions:
```
Would you like to consult your advisor? (y/n): y
```

Your advisor will tell you how factions might react to each option.

#### 4. **Watch Faction Responses**
Each faction will respond to your decision with:
- A unique response (2-3 sentences)
- Sentiment indicator (😊 positive / 😐 neutral / 😠 negative)
- Trust score change

**Example:**
```
💰 The Merchant Guild speaks:
"This is outrageous! After we supported your coronation, 
you burden us with additional taxes? Our profits will 
suffer greatly from this decision."

� Sentiment: negative (intensity: 0.85)
Trust changed: -12
```

#### 5. **Every 2 Turns: Special Events**

**Chronicle Creation:**
After turns 2, 4, and 6, the Royal Chronicler summarizes recent events:
```
📖 The Royal Chronicler writes...

"The early days of the reign were marked by economic 
turmoil. The Merchant Guild bristled at new taxation 
while the Common Folk cheered the promise of festivals..."
```

**Personality Evolution:**
Faction personalities evolve based on their experiences:
```
⚡ FACTION PERSONALITIES EVOLVING...

💰 The Merchant Guild:
   Was: pragmatic and profit-oriented
   Now: resentful and defensive
   Why: Repeated taxation has made them distrustful
```

**Kingdom State Assessment:**
The game classifies your kingdom's overall condition:
- 🌟 **Prosperity** - High trust, thriving kingdom
- ⚖️ **Stability** - Balanced, steady state
- 📉 **Decline** - Low trust, trouble brewing
- ⚠️ **Rebellion** - Very low trust, danger!

#### 6. **Continue Through All 8 Turns**
Repeat this process for all 8 turns, watching how your choices compound and how faction personalities evolve over time.

---

## 🎯 Game Mechanics

### Trust System

**Trust Score (0-100):**
- **High (70-100)**: Faction strongly supports you
- **Medium (40-69)**: Faction is neutral or cautiously supportive
- **Low (20-39)**: Faction is unhappy and distrustful
- **Critical (0-19)**: Faction is hostile, rebellion risk!

**Trust Changes Based On:**
- Sentiment of faction responses
- Intensity of their emotions
- Your accumulated decisions

**Example:**
```
Positive response (0.8 intensity) → +12 trust
Negative response (0.6 intensity) → -9 trust
Neutral response → 0 trust change
```

### Personality Evolution

**How It Works:**
1. Every 2 turns, the AI analyzes each faction's recent experiences
2. It looks at patterns in their responses
3. Personalities transform based on accumulated interactions
4. Changes are meaningful, not random

**Example Evolution:**
```
Base: "pragmatic and profit-oriented"
After 4 turns of taxation: "resentful and defensive"
Reason: "Repeated taxation has made them distrustful"
```

### Memory System

Factions **remember** your past decisions:
- Recent decisions are referenced in responses
- Past actions influence current reactions
- Long-term grudges or gratitude develop

**Example:**
```
Turn 1: You raise taxes
Turn 5: Merchant says "After the tax burden you imposed 
        at the start of your reign, we cannot support this..."
```

### Story Beats

At certain thresholds, special narrative moments occur:

**High Trust (>80):**
```
✨ The streets fill with celebrations as your name is 
chanted in every tavern. Children play games pretending 
to be the beloved monarch.
```

**Low Trust (<30):**
```
⚠️ Dark clouds gather over the kingdom. Whispers of 
rebellion echo through the streets. Your advisors warn 
of imminent danger.
```

---

## 📺 Understanding the Interface

### Color Coding

The game uses colors to help you understand information quickly:

- **Yellow (💰)**: Merchant Guild
- **Magenta (👑)**: Noble Houses
- **Cyan (⛪)**: Sacred Order
- **Green (🌾)**: Common Folk
- **Blue**: Headers and important information
- **Green**: Positive outcomes
- **Red**: Negative outcomes
- **Yellow**: Warnings or special events

### Icons & Symbols

- **💰 👑 ⛪ 🌾**: Faction icons
- **😊 😐 😠**: Sentiment indicators
- **⚡**: Personality evolution
- **📖**: Chronicle creation
- **📜**: Kingdom state assessment
- **✨**: Positive story beat
- **⚠️**: Warning or negative story beat
- **👑**: Your decisions
- **📊**: Status information

### Reading Faction Status

```
💰 The Merchant Guild               ← Faction name with icon
   Personality: resentful and defensive    ← Current personality
   Trust: 32/100                           ← Trust score
   ⚡ Recently evolved: Repeated taxation... ← Recent change (if any)
```

---

## 💡 Tips & Strategies

### For New Players

1. **Read Carefully**: Pay attention to faction responses—they give hints about future behavior
2. **Balance is Key**: Don't favor one faction too heavily; others will turn against you
3. **Long-Term Thinking**: Early decisions compound over time
4. **Use the Advisor**: After turn 2, consult your advisor for predictions
5. **Watch Evolution**: Notice how personalities change—it affects future interactions

### Strategy Approaches

**The Diplomat (Balanced)**
- Keep all factions at medium-high trust
- Make compromises
- Goal: End with average trust 60-70

**The Tyrant (Authoritarian)**
- Focus on Nobles and Military
- Ignore commoner sentiment
- Goal: Maintain power through strength

**The Populist (People's Champion)**
- Favor Commoners and Clergy
- Challenge Nobles and Merchants
- Goal: High trust from common folk

**The Merchant Prince (Economic)**
- Support trade and prosperity
- Favor Merchants and economic growth
- Goal: Wealthy, stable kingdom

### Advanced Tips

1. **Personality Synergy**: Once a faction evolves, adapt your strategy to their new personality
2. **Crisis Management**: If trust drops below 30, focus on damage control
3. **Chronicle Reading**: Chronicles give narrative context—use them to understand the story arc
4. **Sentiment Intensity**: High-intensity reactions (>0.8) cause bigger trust swings
5. **Final Review**: The ending changes based on your overall performance

---

## 🏁 How to End

### Normal Game Completion

The game **automatically ends** after turn 8. You'll then receive:

1. **Epic Kingdom History**: A comprehensive AI-generated review of your reign including:
   - Overview of your leadership style
   - Faction personality evolution timelines
   - Key turning points in your reign
   - Alternative history ("What if you had...")
   - Memorable quotes from factions
   - Final verdict and rating

2. **Saved Files**:
   - `game_state.json` - Complete game data
   - `kingdom_history.md` - The epic review (saved to file)

### Early Exit

If you need to quit before completing the game:

**Method 1: Graceful Exit**
- Press `Ctrl+C` at any prompt
- The game will display: "Game interrupted. Your kingdom falls into chaos!"
- Current progress is saved in `game_state.json`

**Method 2: Force Quit**
- Press `Ctrl+C` twice
- Immediately terminates
- Progress may not be saved

### After the Game

**View Your Kingdom History:**
```bash
cat kingdom_history.md
# or open in any markdown viewer
```

**View Raw Game Data:**
```bash
cat game_state.json
# or open in any JSON viewer
```

**Play Again:**
```bash
python3 main.py
```
Note: This will overwrite `game_state.json` and `kingdom_history.md`

**Save Multiple Playthroughs:**
```bash
# Before playing again, backup your files
cp game_state.json game_state_playthrough1.json
cp kingdom_history.md kingdom_history_playthrough1.md

# Then play again
python3 main.py
```

---

## 🐛 Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'openai'"
**Problem**: OpenAI package not installed  
**Solution**: 
```bash
pip install openai
# or
pip install -r requirements.txt
```

#### "OPENAI_API_KEY not found"
**Problem**: API key not configured  
**Solution**:
1. Check `.env` file exists: `ls -la .env`
2. Verify contents: `cat .env`
3. Ensure format is: `OPENAI_API_KEY=sk-...` (no spaces!)
4. Restart the terminal

#### "AuthenticationError" or "Invalid API Key"
**Problem**: Wrong or expired API key  
**Solution**:
1. Get a new key from https://platform.openai.com/api-keys
2. Update `.env` file with new key
3. Verify no extra spaces or quotes

#### "RateLimitError"
**Problem**: Too many API requests  
**Solution**:
- Wait 1 minute between turns
- Check your OpenAI account quota
- Consider upgrading your OpenAI plan

#### "Insufficient quota"
**Problem**: No credits in OpenAI account  
**Solution**:
- Add credits to your OpenAI account
- Each game costs ~$0.10

#### Game feels too expensive
**Problem**: Using expensive model or too many turns  
**Solution**:
Edit `config.py`:
```python
OPENAI_MODEL = "gpt-4o-mini"  # Cheaper model (default)
TOTAL_TURNS = 4  # Reduce turns
```

#### JSON parse errors or unexpected responses
**Problem**: OpenAI API returned unexpected format  
**Solution**:
- The game has fallback handling
- Should continue despite errors
- If persistent, check your internet connection

#### Import errors on Windows
**Problem**: Windows path or Python version issues  
**Solution**:
- Use `python` instead of `python3`
- Ensure Python 3.7+ is installed: `python --version`
- Install packages: `python -m pip install -r requirements.txt`

### Getting Help

If problems persist:

1. **Check Configuration**:
   ```bash
   python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key loaded' if os.getenv('OPENAI_API_KEY') else 'API Key missing')"
   ```

2. **Verify Python Version**:
   ```bash
   python3 --version
   # Should be 3.7 or higher
   ```

3. **Test OpenAI Connection**:
   ```bash
   python3 -c "from openai import OpenAI; import os; from dotenv import load_dotenv; load_dotenv(); client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')); print('Connection OK')"
   ```

4. **Run Demo** (simpler test):
   ```bash
   python3 demo.py
   ```

---

## 📊 Game Information

### Cost Information

**Using gpt-3.5-turbo:**
- Per turn: ~$0.003-0.006
- Full 8-turn game: ~$0.03-0.05
- Extremely affordable for casual play!

### Time Requirements

- **Installation**: 2-5 minutes
- **Single playthrough**: 10-15 minutes
- **Reading final review**: 2-3 minutes
- **Total**: ~15-20 minutes per game

### Output Files

After playing, you'll have:
- `game_state.json` (~5-15 KB) - Complete game data
- `kingdom_history.md` (~3-8 KB) - Epic review

These can be shared, archived, or analyzed.

---

## 🎓 About This Game

**The Evolving Kingdom** is an AI-powered game created for Introduction to AI (Lab 2.2). It demonstrates:
- Multiple distinct LLM tasks
- AI self-digestion (AI analyzing its own outputs)
- Dynamic personality evolution
- Emergent storytelling

**Technical Details**: See `REPORT.md` for complete lab report

**Created By**: Nathanael Richard Ha Hanes  
**Date**: October 31, 2025  
**License**: Apache License 2.0 (see LICENSE file)

---

## 🚀 Ready to Play?

Now that you know how everything works, it's time to begin your reign!

```bash
python3 main.py
```

**Good luck, Your Majesty! May your kingdom prosper!** 👑

---

**Questions?** Check REPORT.md for technical details or review the troubleshooting section above.
