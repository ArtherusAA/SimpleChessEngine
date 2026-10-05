from ..move import Move
from ..state import GameState
from ..types import Color, Square


_KNIGHT_OFFSETS = (
    (-2, -1),
    (-2, 1),
    (-1, -2),
    (-1, 2),
    (1, -2),
    (1, 2),
    (2, -1),
    (2, 1),
)


def generate_knight_moves(
    state: GameState,
    color: Color,
) -> list[Move]:
    moves: list[Move] = []

    knights = (
        state.white_knights
        if color == Color.WHITE
        else state.black_knights
    )

    own_pieces = (
        state.white_pieces()
        if color == Color.WHITE
        else state.black_pieces()
    )

    for from_square in _squares(knights):
        from_file = from_square % 8
        from_rank = from_square // 8

        for file_offset, rank_offset in _KNIGHT_OFFSETS:
            to_file = from_file + file_offset
            to_rank = from_rank + rank_offset

            if not (0 <= to_file < 8 and 0 <= to_rank < 8):
                continue

            to_square = Square(to_rank * 8 + to_file)

            if own_pieces & (1 << to_square):
                continue

            moves.append(
                Move(
                    from_square=from_square,
                    to_square=to_square,
                )
            )

    return moves


def _squares(bitboard: int) -> list[Square]:
    squares = []

    while bitboard:
        bit = bitboard & -bitboard
        squares.append(Square(bit.bit_length() - 1))
        bitboard &= bitboard - 1

    return squares