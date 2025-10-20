import streamlit as st
from game_operations import move_up, move_down, move_left, move_right
from game_state import (
    create_initial_game_state, apply_move_to_state, 
    undo_last_move
)
from game_ui import render_board, render_score_panel, render_sidebar, render_button_styles, render_movement_controls
import json
import base64
from typing import Dict, Any, Optional


def encode_game_state(state: Dict[str, Any]) -> str:
    """Encode game state to URL-safe string."""
    json_str = json.dumps(state, separators=(',', ':'))
    encoded = base64.urlsafe_b64encode(json_str.encode()).decode()
    return encoded


def decode_game_state(encoded: str) -> Optional[Dict[str, Any]]:
    """Decode game state from URL-safe string."""
    try:
        json_str = base64.urlsafe_b64decode(encoded.encode()).decode()
        return json.loads(json_str)
    except:
        return None


def get_state_from_url() -> Optional[Dict[str, Any]]:
    """Extract game state from URL parameters."""
    query_params = st.query_params
    if 'state' in query_params:
        return decode_game_state(query_params['state'])
    return None


def update_url_with_state(state: Dict[str, Any]) -> None:
    """Update URL with current game state."""
    encoded_state = encode_game_state(state)
    st.query_params['state'] = encoded_state


def handle_move(current_state, move_function):
    """Handle a move operation with state transitions."""
    new_state, moved = apply_move_to_state(current_state, move_function)
    if moved:
        update_url_with_state(new_state)
        st.rerun()


def main():
    """
    Main function to run the 2048 game.
    """
    st.set_page_config(page_title="Shubham Boghara - 2048", layout="wide")
    st.title("2048")
    
    # Get current state from URL or create initial state
    current_state = get_state_from_url()
    if current_state is None:
        current_state = create_initial_game_state(4)
        update_url_with_state(current_state)
        st.rerun()
        return
    
    # Sidebar controls
    with st.sidebar:
        size = render_sidebar(current_state.get('board_size', 4))
        
        if st.button("Restart Game"):
            new_state = create_initial_game_state(size, current_state.get('best', 0))
            update_url_with_state(new_state)
            st.rerun()
            
        if st.button("Undo Move"):
            undone_state = undo_last_move(current_state)
            if undone_state is not None:
                update_url_with_state(undone_state)
                st.rerun()
    
    # Check if board size changed
    if size != current_state.get('board_size', 4):
        new_state = create_initial_game_state(size, current_state.get('best', 0))
        update_url_with_state(new_state)
        st.rerun()
        return
    
    # Main game layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Game Board")
        render_board(current_state['board'])
    
    with col2:
        render_score_panel(current_state)
    
    st.markdown("---")
    
    # Movement controls
    render_button_styles()
    
    # Setup move callbacks and functions
    move_callbacks = {
        'up': handle_move,
        'down': handle_move,
        'left': handle_move,
        'right': handle_move
    }
    
    move_functions = {
        'up': move_up,
        'down': move_down,
        'left': move_left,
        'right': move_right
    }
    
    render_movement_controls(current_state, move_callbacks, move_functions)
    
    # Display current state for debugging
    with st.expander("Debug: Current State", expanded=False):
        st.json(current_state)
        st.code(f"URL State: {encode_game_state(current_state)}")


if __name__ == "__main__":
    main()
