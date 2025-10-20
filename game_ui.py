"""
2048 Game UI Components Module
"""

import streamlit as st
from typing import List, Dict, Any

TILE_COLORS: Dict[int, str] = {
    0: "#e8e7e6", 2: "#E1C5AA", 4: "#f09b1b", 8: "#45602d", 16: "#e15d16",
    32: "#e0826a", 64: "#e80303", 128: "#ffbf00", 256: "#897124", 512: "#05bbe4",
    1024: "#f00880", 2048: "#ff0404"
}


def tile_style(val: int, tile_size: int = 70, border_radius: int = 6, font_weight: int = 700) -> str:
    """Generate CSS style for a tile based on its value."""
    bg = TILE_COLORS.get(val, "#3c3a32")
    fg = "#776e65" if val in (2, 4) else "#f9f6f2"
    
    if val < 128:
        font_size = int(tile_size * 0.4)
    elif val < 1024:
        font_size = int(tile_size * 0.3)
    else:
        font_size = int(tile_size * 0.25)

    return (
        f"background:{bg}; color:{fg}; font-weight:{font_weight}; font-size:{font_size}px; "
        f"height:{tile_size}px; width:{tile_size}px; display:flex; align-items:center; "
        f"justify-content:center; border-radius:{border_radius}px;"
    )


def render_board(board: List[List[int]], tile_gap: int = 8, board_padding: int = 16, 
                 board_bg: str = "#bbada0", board_radius: int = 8, tile_size: int = 70) -> None:
    """Render the game board using HTML and CSS."""
    rows_html = []
    
    for row in board:
        tiles = [
            f'<div style="{tile_style(v, tile_size)}">{v if v != 0 else ""}</div>' 
            for v in row
        ]
        rows_html.append(
            f'<div style="display:flex; gap:{tile_gap}px; margin-bottom:{tile_gap}px">' + 
            ''.join(tiles) + 
            '</div>'
        )
    
    board_html = (
        f'<div style="background:{board_bg}; padding:{board_padding}px; border-radius:{board_radius}px; display:inline-block">' + 
        ''.join(rows_html) + 
        '</div>'
    )
    
    st.markdown(board_html, unsafe_allow_html=True)


def render_sidebar(current_board_size: int, min_size: int = 2, max_size: int = 8) -> int:
    """Render the sidebar with game settings. Returns the selected board size."""
    st.header("Settings")
    size = st.number_input(
        f"Board size ({min_size}-{max_size})", 
        min_value=min_size, 
        max_value=max_size, 
        value=current_board_size
    )
    return size


def render_score_panel(game_state: Dict[str, Any], win_message: str = "🎉 You reached 2048!", 
                      game_over_message: str = "Game Over 😢", score_label: str = "Score", 
                      best_label: str = "Best") -> None:
    """Render the score panel with current score, best score, and game status."""
    st.subheader(score_label)
    st.write(f"**{score_label}:** {game_state['score']}")
    st.write(f"**{best_label}:** {game_state['best']}")
    
    if game_state.get('won', False):
        st.success(win_message)
    elif not game_state.get('game_over', False):
        pass
    else:
        st.error(game_over_message)


def render_button_styles(button_height: int = 70, button_font_size: int = 28, 
                        button_radius: int = 12, button_gap: str = "0.25rem") -> None:
    """Render CSS styles for control buttons."""
    st.markdown(f"""
    <style>
    div.stButton > button {{
        height: {button_height}px !important;
        font-size: {button_font_size}px !important;
        font-weight: bold;
        border-radius: {button_radius}px !important;
    }}
    div[data-testid="stHorizontalBlock"] {{
        gap: {button_gap} !important;
    }}
    </style>
    """, unsafe_allow_html=True)


def render_movement_controls(current_state: Dict[str, Any], move_callbacks: Dict[str, Any], move_functions: Dict[str, Any]) -> None:
    
    up_col = st.columns([4, 2, 4], gap="small")
    with up_col[1]:
        if st.button("⬆️", use_container_width=True, key="btn_up"):
            move_callbacks['up'](current_state, move_functions['up'])

    middle_col = st.columns([2, 4, 2], gap="small")
    with middle_col[0]:
        if st.button("⬅️", use_container_width=True, key="btn_left"):
            move_callbacks['left'](current_state, move_functions['left'])
    with middle_col[2]:
        if st.button("➡️", use_container_width=True, key="btn_right"):
            move_callbacks['right'](current_state, move_functions['right'])

    down_col = st.columns([4, 2, 4], gap="small")
    with down_col[1]:
        if st.button("⬇️", use_container_width=True, key="btn_down"):
            move_callbacks['down'](current_state, move_functions['down'])
