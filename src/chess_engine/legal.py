from .check import is_in_check
from .move import Move
from .movegen import (
    generate_bishop_moves,
    generate_king_moves,
    generate_knight_moves,
    generate_pawn_moves,
    generate_queen_moves,
    generate_rook_moves,
)
from .state import GameState
from .types import Color


def generate_pseudo_legal_moves(
    state: GameState,
    color: Color,
) -> list[Move]:
    moves: list[Move] = []

    moves.extend(generate_pawn_moves(state, color))
    moves.extend(generate_knight_moves(state, color))
    moves.extend(generate_bishop_moves(state, color))
    moves.extend(generate_rook_moves(state, color))
    moves.extend(generate_queen_moves(state, color))
    moves.extend(generate_king_moves(state, color))

    return moves


def generate_legal_moves(state: GameState) -> list[Move]:
    color = state.turn

    legal_moves: list[Move] = []

    for move in generate_pseudo_legal_moves(state, color):
        new_state = state.make_move(move)

        if not is_in_check(new_state, color):
            legal_moves.append(move)

    return legal_moves