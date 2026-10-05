from ..move import Move
from ..state import GameState
from ..types import Color
from .sliding import generate_sliding_moves


_DIRECTIONS = (
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
)


def generate_rook_moves(
    state: GameState,
    color: Color,
) -> list[Move]:
    rooks = (
        state.white_rooks
        if color == Color.WHITE
        else state.black_rooks
    )

    own_pieces = (
        state.white_pieces()
        if color == Color.WHITE
        else state.black_pieces()
    )

    return generate_sliding_moves(
        rooks,
        own_pieces,
        state.occupied(),
        _DIRECTIONS,
    )