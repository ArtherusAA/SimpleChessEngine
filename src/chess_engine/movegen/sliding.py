from collections.abc import Iterable

from ..move import Move
from ..types import Square


def generate_sliding_moves(
    pieces: int,
    own_pieces: int,
    occupied: int,
    directions: Iterable[tuple[int, int]],
) -> list[Move]:
    moves: list[Move] = []

    for from_square in _squares(pieces):
        from_file = from_square % 8
        from_rank = from_square // 8

        for file_offset, rank_offset in directions:
            to_file = from_file + file_offset
            to_rank = from_rank + rank_offset

            while 0 <= to_file < 8 and 0 <= to_rank < 8:
                to_square = Square(to_rank * 8 + to_file)
                to_bit = 1 << to_square

                if own_pieces & to_bit:
                    break

                moves.append(
                    Move(
                        from_square=from_square,
                        to_square=to_square,
                    )
                )

                if occupied & to_bit:
                    break

                to_file += file_offset
                to_rank += rank_offset

    return moves


def _squares(bitboard: int) -> list[Square]:
    squares = []

    while bitboard:
        bit = bitboard & -bitboard
        squares.append(Square(bit.bit_length() - 1))
        bitboard &= bitboard - 1

    return squares