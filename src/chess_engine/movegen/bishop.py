from ..move import Move
from ..state import GameState
from ..types import Color
from .sliding import generate_sliding_moves


_DIRECTIONS = (
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
)


def generate_bishop_moves(
    state: GameState,
    color: Color,
) -> list[Move]:
    bishops = (
        state.white_bishops
        if color == Color.WHITE
        else state.black_bishops
    )

    own_pieces = (
        state.white_pieces()
        if color == Color.WHITE
        else state.black_pieces()
    )

    return generate_sliding_moves(
        bishops,
        own_pieces,
        state.occupied(),
        _DIRECTIONS,
    )