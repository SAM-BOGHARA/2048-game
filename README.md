# 2048 Game - Functional Implementation

A clean, functional implementation of the classic 2048 puzzle game built with Streamlit and Python.

## Deployment link --> https://2048-game.streamlit.app

## Gameplay Instructions

### Objective
- **Goal**: Combine tiles with the same numbers to reach the **2048 tile**
- **How to Win**: Create a tile with the number 2048
- **How to Lose**: No more moves are possible (board is full and no adjacent tiles can be combined)

### How to Play
1. **Movement**: Use the arrow buttons (⬆️ ⬇️ ⬅️ ➡️) to move all tiles in that direction
2. **Combining**: When two tiles with the same number touch, they merge into one tile with double the value
3. **New Tiles**: After each move, a new tile (2 or 4) appears randomly on the board
4. **Scoring**: Your score increases by the value of each new tile created through merging

### Game Controls
- **⬆️ ⬇️ ⬅️ ➡️**: Move tiles in the corresponding direction
- **Restart Game**: Start a new game (preserves best score)
- **Undo Move**: Undo the recent moves
- **Board Size**: Configure board size (2x2 to 8x8, default 4x4)

### Scoring System
- Points are awarded for each tile merge
- **Best score** is automatically saved
- Score resets when you restart the game

## Installation & Running

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start
```bash
# Clone the repository
git clone <your-repo-url>
cd 2048

# Install dependencies
pip install -r requirements.txt

# Run the game
streamlit run game_2048.py
```

The game will open in your web browser at `http://localhost:8501`

### Alternative Setup (with virtual environment)
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
streamlit run game_2048.py
```

## 🏗️ Implementation Details

### Architecture Overview
This implementation follows **functional programming principles** with clean separation of concerns:

```
2048 Game Architecture
├── game_operations.py    # Pure game logic & board operations
├── game_state.py         # Pure state management functions  
├── game_ui.py            # Pure UI rendering components
└── game_2048.py          # Main application
```

### Core Design Principles

#### 1. **Functional Programming**
- **Pure Functions**: All core game logic is implemented as pure functions
- **Immutability**: Functions return new state objects instead of modifying existing ones
- **No Side Effects**: Game logic has no hidden dependencies or mutations
- **Stateless**: State is managed through URL parameters (no persistent session state)

#### 2. **Separation of Concerns**
- **Game Logic** (`game_operations.py`): Board manipulation, move validation, win/lose detection
- **State Management** (`game_state.py`): State creation, transitions, history management
- **UI Components** (`game_ui.py`): Rendering functions that take data as parameters
- **Application Layer** (`game_2048.py`): Orchestrates everything and handles user interactions

### File Structure & Responsibilities

#### `game_operations.py` - Core Game Mechanics
```python
# Pure functional operations
create_empty_board(size)           # Creates new empty board
move_left(board)                   # Returns (new_board, score_gained, moved)
move_right(board)                  # Transpose-based movement
move_up(board)                     # Pure board transformations
move_down(board)                   # No side effects
has_won(board)                     # Win condition check
has_moves_available(board)         # Game over detection
```

**Key Features:**
- All functions are **pure** - same input always produces same output
- **Immutable operations** - original board is never modified
- **Transpose-based movement** - elegant solution for all 4 directions
- **Predictable** - easy to test and reason about

#### `game_state.py` - State Management
```python
# State creation and transitions
create_initial_game_state(size)    # Creates new game state
apply_move_to_state(state, move_fn) # Applies move and returns new state
undo_last_move(state)              # Returns previous state
restart_game_state(state)          # Creates fresh state (preserves best)
```

**Key Features:**
- **Pure state transitions** - functions return new state objects
- **History management** - tracks moves for undo functionality
- **No mutations** - original state is never modified
- **Composable** - functions can be easily combined and tested

#### `game_ui.py` - UI Components
```python
# Pure rendering functions
render_board(board, styling_options)     # Displays game board
render_score_panel(game_state, messages) # Shows score and status
render_sidebar(current_size, limits)     # Settings panel
render_movement_controls(state, callbacks) # Game controls
```

**Key Features:**
- **Data as parameters** - no access to global state
- **Configurable styling** - all visual aspects can be customized
- **Reusable components** - can be used in different contexts
- **Pure rendering** - given same input, produces same output

#### `game_2048.py` - Main Application
```python
# Application orchestration
main()                    # Main game
encode_game_state()       # URL state management
decode_game_state()       # Stateless persistence
handle_move()             # User interaction handling
```

**Key Features:**
- **URL-based state** - no session state, everything in URL parameters
- **Stateless architecture** - each request rebuilds state from URL
- **Shareable game states** - URLs can be bookmarked and shared
- **Side effect isolation** - all Streamlit interactions contained here

**Enjoy playing 2048 with clean, functional code!** 🎉
