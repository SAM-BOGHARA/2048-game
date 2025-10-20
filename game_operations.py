"""
2048 Board Operations
"""

import random
from typing import List, Tuple


def create_empty_board(size: int) -> List[List[int]]:
    """Create an empty board of the specified size."""
    return [[0 for _ in range(size)] for _ in range(size)]


def clone_board(board: List[List[int]]) -> List[List[int]]:
    """Create a deep copy of the board."""
    return [row[:] for row in board]


def add_random_tile(board: List[List[int]]) -> List[List[int]]:
    """Return a new board with one random tile (2 or 4) added."""
    size = len(board)
    empties = [(r, c) for r in range(size) for c in range(size) if board[r][c] == 0]
    if not empties:
        return clone_board(board)
    
    r, c = random.choice(empties)
    value = 2 if random.random() < 0.9 else 4
    newb = clone_board(board)
    newb[r][c] = value
    return newb


def compress_and_merge_row_left(row: List[int]) -> Tuple[List[int], int]:
    """Compress row to the left and merge equal tiles. Returns (new_row, score_gained)."""
    nonzeros = [x for x in row if x != 0]
    result, score = [], 0
    i = 0
    
    while i < len(nonzeros):
        if i + 1 < len(nonzeros) and nonzeros[i] == nonzeros[i+1]:
            merged = nonzeros[i] * 2
            result.append(merged)
            score += merged
            i += 2
        else:
            result.append(nonzeros[i])
            i += 1
    
    result.extend([0] * (len(row) - len(result)))
    return result, score


def transpose(board: List[List[int]]) -> List[List[int]]:
    """Transpose the board (swap rows and columns)."""
    return [list(row) for row in zip(*board)]


def reverse_rows(board: List[List[int]]) -> List[List[int]]:
    """Reverse each row in the board."""
    return [list(reversed(row)) for row in board]


def move_left(board: List[List[int]]) -> Tuple[List[List[int]], int, bool]:
    """Move all tiles left. Returns (new_board, score_gained, moved)."""
    size = len(board)
    new_board, total_score, moved = [], 0, False
    
    for r in range(size):
        new_row, gained = compress_and_merge_row_left(board[r])
        new_board.append(new_row)
        total_score += gained
        if new_row != board[r]:
            moved = True
    
    return new_board, total_score, moved


def move_right(board: List[List[int]]) -> Tuple[List[List[int]], int, bool]:
    """Move all tiles right. Returns (new_board, score_gained, moved)."""
    reversed_b = reverse_rows(board)
    moved_board, score, moved = move_left(reversed_b)
    return reverse_rows(moved_board), score, moved


def move_up(board: List[List[int]]) -> Tuple[List[List[int]], int, bool]:
    """Move all tiles up. Returns (new_board, score_gained, moved)."""
    t = transpose(board)
    moved_board, score, moved = move_left(t)
    return transpose(moved_board), score, moved


def move_down(board: List[List[int]]) -> Tuple[List[List[int]], int, bool]:
    """Move all tiles down. Returns (new_board, score_gained, moved)."""
    t = transpose(board)
    reversed_t = reverse_rows(t)
    moved_board, score, moved = move_left(reversed_t)
    unreversed = reverse_rows(moved_board)
    return transpose(unreversed), score, moved


def has_moves_available(board: List[List[int]]) -> bool:
    """Check if any moves are possible on the board."""
    size = len(board)
    
    for r in range(size):
        for c in range(size):
            # Empty space available
            if board[r][c] == 0:
                return True
            # Can merge vertically
            if r + 1 < size and board[r][c] == board[r+1][c]:
                return True
            # Can merge horizontally
            if c + 1 < size and board[r][c] == board[r][c+1]:
                return True
    
    return False


def has_won(board: List[List[int]], goal: int = 2048) -> bool:
    """Check if the player has reached the winning goal."""
    return any(cell >= goal for row in board for cell in row)
