# PacMan AI with Minimax Algorithm

## Project Overview

This project implements an intelligent PacMan game using the **Minimax algorithm** as the decision-making AI. The goal is to demonstrate adversarial game theory principles by controlling PacMan to collect all dots on the board while avoiding two ghosts. The AI uses depth-limited minimax search to evaluate game states and make optimal moves against adversarial ghost agents.

### Problem Description

The PacMan game is a classic pursuit-evasion problem where:
- **Agent (PacMan)**: Maximizes score by collecting dots and avoiding ghosts
- **Adversaries (Ghosts)**: Minimize PacMan's utility by trying to catch it
- **Environment**: 18x9 grid board with obstacles, creating a constrained search space

The minimax algorithm explores the game tree to find the best move for PacMan while assuming ghosts play optimally to minimize its score.

---

## Project Structure

```
AI-FinalProject-ErfanGhanbari-PacMan/
├── main.py                 # Main game loop and entry point
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── pdf/                   # Documentation files (if any)
└── src/
    ├── __init__.py        # Package initialization
    ├── game_state.py      # GameState class defining game state representation
    ├── minmax.py          # Minimax algorithm implementation
    └── utils.py           # Utility functions for game mechanics
```

### How to Run

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the game**:
   ```bash
   python main.py
   ```

The game will display the board state after each move, with:
- `p` = PacMan
- `g` = Ghost 1
- `s` = Ghost 2
- `#` = Obstacles
- `.` = Collectible dots
- ` ` = Empty space

---

## Input Data

### Game Configuration

The input parameters are defined in `main.py`:

- **BOARD_WIDTH**: 18 (horizontal dimension)
- **BOARD_HEIGHT**: 9 (vertical dimension)
- **OBSTACLES**: Predefined set of (x, y) coordinates representing walls
- **PACMAN_START**: Initial position of PacMan → (0, 0)
- **GHOSTS_START**: Initial positions of two ghosts → [(8, 8), (4, 4)]
- **MOVES**: Available moves dictionary:
  - `'S'`: (0, 0) - Stay
  - `'U'`: (0, 1) - Up
  - `'D'`: (0, -1) - Down
  - `'R'`: (1, 0) - Right
  - `'L'`: (-1, 0) - Left
- **MAX_DEPTH**: 9 (search depth for minimax algorithm)

### Data Points

- **Initial Points**: All positions on the board except obstacles
- **Scoring**:
  - +200 points per dot collected (during minimax utility)
  - +10 points per dot collected (actual gameplay)
  - -10 points per move without collecting a dot
  - -1 point per move in actual gameplay
  - -1000 if within 1 step of a ghost
  - -100 if within 3 steps of a ghost
  - -∞ if caught by a ghost
  - +∞ if all dots are collected

---

## Preprocessing Steps

1. **Board Initialization**:
   - Remove all obstacle positions from the initial point set
   - Ensures search space contains only valid positions

2. **Move Validation**:
   - Check if target position is within board boundaries
   - Verify position is not an obstacle
   - Prevent invalid moves using `is_valid_position()` function

3. **Circle Detection**:
   - Prevent PacMan from moving in circles
   - Checks last 3 moves to avoid patterns: (A→B→A→B) or (A→A→A)

4. **State Representation**:
   - Convert game state to immutable representations for hashing
   - Store positions as tuples for efficiency
   - Maintain points as sets for O(1) membership testing

---

## Model Architecture & Explanation

### GameState Class

Represents a complete snapshot of the game:

```
GameState:
├── pacman: (x, y) position
├── ghosts: tuple of (x, y) positions for each ghost
├── points: set of remaining collectible dot positions
├── score: current accumulated score
├── MOVES: available movement dictionary
├── OBSTACLES: board obstacles
├── BOARD_WIDTH/HEIGHT: board dimensions
└── utility(): Evaluation function for terminal/non-terminal states
```

**Key Methods**:
- `is_terminal()`: Checks if game has ended (all dots collected or PacMan caught)
- `utility()`: Returns numeric evaluation of game state
  - Terminal states: ±∞ based on win/loss
  - Non-terminal states: Score + distance penalty/bonus from ghosts

### Minimax Algorithm

The minimax algorithm alternates between maximizing (PacMan) and minimizing (two ghosts) agents:

**Algorithm Flow**:

```
minimax(state, depth, agent_id):
  - If depth = 0 or terminal state → return state.utility()
  - If agent_id = 0 (PacMan - MAX):
      For each valid move:
        Generate child state
        Recursively call minimax with depth-1, agent=1
      Return maximum evaluation
  - If agent_id = 1 (Ghost 1 - MIN):
      For each valid move:
        Generate child state
        Recursively call minimax with depth-1, agent=2
      Return minimum evaluation
  - If agent_id = 2 (Ghost 2 - MIN):
      For each valid move:
        Generate child state
        Recursively call minimax with depth-1, agent=0
      Return minimum evaluation
```

**Parameters**:
- `state`: Current game state
- `depth`: Remaining search depth (limits branching to manageable size)
- `agent`: Current agent ID (0=PacMan, 1=Ghost1, 2=Ghost2)

**Search Depth = 9**: Balances computational cost with decision quality

### Evaluation Function

```
utility(state):
  If caught by ghost → return -∞ (loss)
  If all dots collected → return +∞ (win)
  Otherwise:
    distance1 = Manhattan distance to Ghost 1
    distance2 = Manhattan distance to Ghost 2
    min_distance = min(distance1, distance2)
    
    If min_distance > 3:
      reward = 100 (safe zone)
    Elif min_distance < 2:
      penalty = -1000 (danger zone)
    Else:
      penalty = -100 (warning zone)
    
    Return score + reward/penalty
```

---

## Training & Evaluation

### Running the Game

```bash
python main.py
```

**Output Example**:
```
Pacman is at (1, 0), Score: 200
Ghost 1 is at (8, 7)
Ghost 2 is at (4, 5)

 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 
 #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  # 
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 
 #  #  .  #  #  #  #  .  #  #  .  #  #  .  #  #  .  # 
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 
 #  g  .  #  .  #  .  #  .  #  .  #  .  #  .  #  .  # 
 p  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 
 #  #  .  #  .  #  .  #  #  .  #  .  #  .  #  #  .  # 
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
```

### Game Termination Conditions

1. **PacMan Wins**: All dots collected
2. **PacMan Loses**: Caught by a ghost
3. **Game Ends**: Display final score and outcome message

### Performance Metrics

- **Score**: Tracks cumulative reward (higher is better)
- **Dots Remaining**: Monitor collection progress
- **Ghost Distance**: Track proximity to threats
- **Move Count**: Number of turns taken

---

## Sample Notebook Execution

Create a Jupyter notebook `game_analysis.ipynb` to visualize and analyze gameplay:

```python
from src import GameState
from src import get_child_state, get_best_child_state, is_valid_position
from src import minimax

# Configuration
BOARD_WIDTH = 18
BOARD_HEIGHT = 9
OBSTACLES = [(1,1),(1,2),(1,3),(1,5),(1,6),(1,7),(2,1),(2,7),(3,3),(3,5),...]
PACMAN_START = (0, 0)
GHOSTS_START = [(8,8), (4,4)]
MOVES = {'S':(0,0), 'U': (0, 1), 'R': (1, 0), 'L': (-1, 0), 'D': (0, -1)}
MAX_DEPTH = 5

# Initialize game
points = {(row, col) for row in range(BOARD_WIDTH) 
          for col in range(BOARD_HEIGHT) 
          if (row, col) not in OBSTACLES}

state = GameState(PACMAN_START, GHOSTS_START, points, 0, MOVES, 
                  OBSTACLES, BOARD_WIDTH, BOARD_HEIGHT, [])

# Test minimax evaluation
best_move = None
best_eval = float("-inf")
for move in [(0,0), (1,0), (-1,0), (0,1), (0,-1)]:
    if is_valid_position((state.pacman[0] + move[0], 
                         state.pacman[1] + move[1]), 
                        BOARD_WIDTH, BOARD_HEIGHT, OBSTACLES):
        child = get_child_state(state, move, True)
        eval_score = minimax(child, MAX_DEPTH-1, 1)
        print(f"Move {move}: Evaluation = {eval_score}")
        if eval_score >= best_eval:
            best_eval = eval_score
            best_move = move

print(f"Best Move: {best_move} with evaluation: {best_eval}")
```

---

## Requirements

### Python Version
- Python 3.7 or higher

### Dependencies

All required packages are listed in `requirements.txt`:

```
# No external dependencies required
# Uses only Python standard library:
# - random: for ghost movements
# - copy or deep copy operations (built-in)
```

### Installation

```bash
pip install -r requirements.txt
```

Or install from source:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### System Requirements
- **RAM**: Minimum 512 MB
- **CPU**: Any modern processor
- **OS**: Windows, macOS, Linux
- **Disk Space**: ~10 MB

---

## Key Features

✓ **Minimax AI**: Depth-limited adversarial search for optimal play  
✓ **Multi-Agent**: Handles PacMan vs. 2 ghosts simultaneously  
✓ **Obstacle Avoidance**: Complex pathfinding around walls  
✓ **Cycle Prevention**: Avoids repetitive movement patterns  
✓ **Real-time Visualization**: ASCII board display each turn  
✓ **Modular Architecture**: Clean separation of game logic, AI, and utilities  

---

## Implementation Notes

### Algorithm Complexity
- **Time**: O(b^d) where b = branching factor (~5 moves), d = search depth (9)
- **Space**: O(b*d) for recursive call stack

### Limitations
- Random ghost behavior (not optimal play)
- Limited search depth (computational constraints)
- No alpha-beta pruning optimization
- ASCII visualization only

### Future Enhancements
- Implement alpha-beta pruning for faster search
- Add ghost learning/optimization
- Use Monte Carlo Tree Search (MCTS)
- GUI-based visualization
- Multiplayer mode
- Difficulty levels with variable search depth

---

## Author
Erfan Ghanbari

## License
This is an educational project for AI coursework.

---

