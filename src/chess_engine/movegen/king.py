from ..move import Move
from ..state import GameState
from ..types import Color, Square, PieceType
from ..bitboard import bits
from ..move import Move
from ..state import (
    BLACK_KINGSIDE,
    BLACK_QUEENSIDE,
    WHITE_KINGSIDE,
    WHITE_QUEENSIDE,
    GameState,
)
from ..types import Color, Square
from ..check import is_in_check

from ..check import is_in_check, is_square_attacked

_DIRECTIONS = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def generate_king_moves(
    state: GameState,
    color: Color,
) -> list[Move]:
    moves: list[Move] = []

    king = (
        state.white_king
        if color == Color.WHITE
        else state.black_king
    )

    own_pieces = (
        state.white_pieces()
        if color == Color.WHITE
        else state.black_pieces()
    )

    for from_square in _squares(king):
        from_file = from_square % 8
        from_rank = from_square // 8

        for file_offset, rank_offset in _DIRECTIONS:
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
    moves.extend(_generate_castling_moves(state, color))
    return moves

def _generate_castling_moves(
    state: GameState,
    color: Color,
) -> list[Move]:
    if is_in_check(state, color):
        return []

    moves: list[Move] = []

    if color == Color.WHITE:
        if state.castling_rights & WHITE_KINGSIDE:
            if (
                state.piece_at(Square.H1)
                == (Color.WHITE, PieceType.ROOK)
                and state.piece_at(Square.F1) is None
                and state.piece_at(Square.G1) is None
            ):
                if not is_square_attacked(state, Square.F1, Color.BLACK):
                    if not is_square_attacked(
                        state,
                        Square.G1,
                        Color.BLACK,
                    ):
                        moves.append(
                            Move(
                                Square.E1,
                                Square.G1,
                                is_castling=True,
                            )
                        )

        if state.castling_rights & WHITE_QUEENSIDE:
            if (
                state.piece_at(Square.A1)
                == (Color.WHITE, PieceType.ROOK)
                and state.piece_at(Square.B1) is None
                and state.piece_at(Square.C1) is None
                and state.piece_at(Square.D1) is None
            ):
                if not is_square_attacked(state, Square.D1, Color.BLACK):
                    if not is_square_attacked(
                        state,
                        Square.C1,
                        Color.BLACK,
                    ):
                        moves.append(
                            Move(
                                Square.E1,
                                Square.C1,
                                is_castling=True,
                            )
                        )

    else:
        if state.castling_rights & BLACK_KINGSIDE:
            if (
                state.piece_at(Square.H8)
                == (Color.BLACK, PieceType.ROOK)
                and state.piece_at(Square.F8) is None
                and state.piece_at(Square.G8) is None
            ):
                if not is_square_attacked(state, Square.F8, Color.WHITE):
                    if not is_square_attacked(
                        state,
                        Square.G8,
                        Color.WHITE,
                    ):
                        moves.append(
                            Move(
                                Square.E8,
                                Square.G8,
                                is_castling=True,
                            )
                        )

        if state.castling_rights & BLACK_QUEENSIDE:
            if (
                state.piece_at(Square.A8)
                == (Color.BLACK, PieceType.ROOK)
                and state.piece_at(Square.B8) is None
                and state.piece_at(Square.C8) is None
                and state.piece_at(Square.D8) is None
            ):
                if not is_square_attacked(state, Square.D8, Color.WHITE):
                    if not is_square_attacked(
                        state,
                        Square.C8,
                        Color.WHITE,
                    ):
                        moves.append(
                            Move(
                                Square.E8,
                                Square.C8,
                                is_castling=True,
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