from ..bitboard import (
    FILE_A,
    FILE_H,
    RANK_2,
    RANK_7,
)
from ..move import Move
from ..state import GameState
from ..types import Color, PieceType, Square


PROMOTION_PIECES = (
    PieceType.QUEEN,
    PieceType.ROOK,
    PieceType.BISHOP,
    PieceType.KNIGHT,
)


def generate_pawn_moves(
    state: GameState,
    color: Color,
) -> list[Move]:
    moves: list[Move] = []

    pawns = (
        state.white_pawns
        if color == Color.WHITE
        else state.black_pawns
    )

    own_pieces = (
        state.white_pieces()
        if color == Color.WHITE
        else state.black_pieces()
    )

    opponent_pieces = (
        state.black_pieces()
        if color == Color.WHITE
        else state.white_pieces()
    )

    occupied = state.occupied()

    for from_square in _squares(pawns):
        file = from_square % 8
        rank = from_square // 8

        direction = 1 if color == Color.WHITE else -1

        # One-square advance.
        to_rank = rank + direction

        if 0 <= to_rank < 8:
            to_square = Square(to_rank * 8 + file)

            if not (occupied & (1 << to_square)):
                if to_rank == 7 or to_rank == 0:
                    moves.extend(
                        _promotion_moves(from_square, to_square)
                    )
                else:
                    moves.append(
                        Move(
                            from_square=from_square,
                            to_square=to_square,
                        )
                    )

                # Two-square advance from the starting rank.
                starting_rank = 1 if color == Color.WHITE else 6

                if rank == starting_rank:
                    double_rank = rank + 2 * direction
                    double_square = Square(double_rank * 8 + file)

                    if not (occupied & (1 << double_square)):
                        moves.append(
                            Move(
                                from_square=from_square,
                                to_square=double_square,
                            )
                        )

        # Captures.
        for capture_file in (file - 1, file + 1):
            if not 0 <= capture_file < 8:
                continue

            capture_rank = rank + direction

            if not 0 <= capture_rank < 8:
                continue

            to_square = Square(capture_rank * 8 + capture_file)
            to_bit = 1 << to_square

            if opponent_pieces & to_bit:
                if capture_rank == 7 or capture_rank == 0:
                    moves.extend(
                        _promotion_moves(from_square, to_square)
                    )
                else:
                    moves.append(
                        Move(
                            from_square=from_square,
                            to_square=to_square,
                        )
                    )

            # En passant.
            if state.en_passant_square == to_square:
                captured_rank = capture_rank - direction
                captured_square = Square(
                    captured_rank * 8 + capture_file
                )

                if state.piece_at(captured_square) == (
                        color.opposite,
                        PieceType.PAWN,
                ):
                    moves.append(
                        Move(
                            from_square=from_square,
                            to_square=to_square,
                            is_en_passant=True,
                        )
                    )

    return moves


def _promotion_moves(
    from_square: Square,
    to_square: Square,
) -> list[Move]:
    return [
        Move(
            from_square=from_square,
            to_square=to_square,
            promotion=piece,
        )
        for piece in PROMOTION_PIECES
    ]


def _squares(bitboard: int) -> list[Square]:
    squares = []

    while bitboard:
        bit = bitboard & -bitboard
        square = bit.bit_length() - 1
        squares.append(Square(square))
        bitboard &= bitboard - 1

    return squares