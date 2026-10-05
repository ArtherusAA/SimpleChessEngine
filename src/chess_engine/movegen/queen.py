from ..move import Move
from ..state import GameState
from ..types import Color
from .sliding import generate_sliding_moves


_DIRECTIONS = (
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
)


def generate_queen_moves(
    state: GameState,
    color: Color,
) -> list[Move]:
    queens = (
        state.white_queens
        if color == Color.WHITE
        else state.black_queens
    )

    own_pieces = (
        state.white_pieces()
        if color == Color.WHITE
        else state.black_pieces()
    )

    return generate_sliding_moves(
        queens,
        own_pieces,
        state.occupied(),
        _DIRECTIONS,
    )