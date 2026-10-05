from .check import is_in_check
from .legal import generate_legal_moves
from .state import GameState
from .types import Color


def is_checkmate(state: GameState) -> bool:
    if not is_in_check(state, state.turn):
        return False

    return not generate_legal_moves(state)


def is_stalemate(state: GameState) -> bool:
    if is_in_check(state, state.turn):
        return False

    return not generate_legal_moves(state)