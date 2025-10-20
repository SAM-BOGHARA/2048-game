"""
2048 Game State Management Module
"""

from typing import Optional, Dict, Any, List, Tuple, Callable
from game_operations import (
    create_empty_board, add_random_tile, clone_board, 
    has_won, has_moves_available
)

GameState = Dict[str, Any]
GameHistory = List[Tuple[List[List[int]], int]]


def create_initial_game_state(size: int = 4, existing_best: int = 0) -> GameState:
    """
    Create a new initial game state with the specified board size.
    """
    board = create_empty_board(size)
    board = add_random_tile(add_random_tile(board))
    
    return {
        'board': board,
        'score': 0,
        'best': existing_best,
        'won': False,
        'game_over': False,
        'history': [],
        'board_size': size
    }


def should_initialize_state(current_state: Optional[GameState], size: int, force: bool = False) -> bool:
    """
    Pure function to determine if state should be initialized.
    """
    if force or current_state is None:
        return True
    
    return current_state.get('board_size') != size


def add_to_history(state: GameState) -> GameState:
    """
    Create a new state with current board/score added to history.
    """
    new_history = state['history'].copy()
    new_history.append((clone_board(state['board']), int(state['score'])))
    
    return {**state, 'history': new_history}


def undo_last_move(state: GameState) -> Optional[GameState]:
    """
    Create a new state with the last move undone.
    Returns None if no moves to undo.
    """
    if not state['history']:
        return None
    
    new_history = state['history'].copy()
    board, score = new_history.pop()
    
    return {
        **state,
        'board': clone_board(board),
        'score': score,
        'history': new_history,
        'won': has_won(board),
        'game_over': not has_moves_available(board)
    }


def restart_game_state(state: GameState, size: Optional[int] = None) -> GameState:
    """
    Create a fresh game state, preserving the best score.
    """
    board_size = size or state.get('board_size', 4)
    return create_initial_game_state(board_size, state.get('best', 0))


def apply_move_to_state(state: GameState, move_fn: Callable) -> Tuple[GameState, bool]:
    """
    Apply a move function to the game state.
    Returns (new_state, move_was_applied).
    """
    # Return unchanged state if game is over
    if state.get('game_over', False):
        return state, False

    current_board = clone_board(state['board'])
    new_board, gained, moved = move_fn(current_board)

    if not moved:
        return state, False

    state_with_history = add_to_history(state)
    
    # Add random tile and calculate new state
    final_board = add_random_tile(new_board)
    new_score = state['score'] + int(gained)
    new_best = max(state['best'], new_score)
    
    new_state = {
        **state_with_history,
        'board': final_board,
        'score': new_score,
        'best': new_best,
        'won': has_won(final_board),
        'game_over': not has_moves_available(final_board)
    }
    
    return new_state, True
