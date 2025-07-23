# 🐤 Flappy Firebolt Edition


A Flappy Bird clone built with Python and Pygame, featuring:
- Firebolt logo as the bird
- Firebolt-red database cylinder pillars
- Dynamic difficulty (speed, gap, and obstacles increase over time)
- Score saving to Firebolt database
- Player name entry in the game window

## Setup Instructions

## Prerequisites
- Python 3.7+
- Pygame
- python-dotenv
- firebolt-sdk

### 1. Clone the repository
```
git clone https://github.com/firebolt-db/firebolt-demo.git
cd firebolt-demo/FlappyFirebolt
```

### 2. Create and activate a virtual environment
On macOS/Linux:
```
python3 -m venv .venv
source .venv/bin/activate
```
On Windows:
```
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Configure Firebolt credentials
Create a `.env` file in the FlappyFirebolt folder with the following content:
```
FIREBOLT_API_ENDPOINT=api.app.firebolt.io
FIREBOLT_API_KEY=your_client_id_here
FIREBOLT_API_SECRET=your_client_secret_here
FIREBOLT_DATABASE=your_database_name
FIREBOLT_ACCOUNT_NAME=your_account_name
FIREBOLT_ENGINE=your_engine_name
```

### 5. Run the game
```
python flappy_bird.py
```
> **First-run tip:** Firebolt engines “cold-start”.
Your very first game-over can take ~30 s while the engine spins up; every round after that writes scores instantly.

## Gameplay
- Type your player name in the game window and press ENTER.
- Press SPACE to flap.
- Press R to restart the game.
- Avoid the Firebolt-red database pillars.
- The game gets harder as you play!
- Your score and stats are saved to Firebolt after each game.

All dependencies are listed in `requirements.txt`.

---
Enjoy and may your bird soar through the Firebolt clouds!
