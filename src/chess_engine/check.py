from .bitboard import bits
from .state import GameState
from .types import Color, PieceType, Square


KNIGHT_OFFSETS = (
    (-2, -1),
    (-2, 1),
    (-1, -2),
    (-1, 2),
    (1, -2),
    (1, 2),
    (2, -1),
    (2, 1),
)

KING_OFFSETS = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)

DIAGONAL_DIRECTIONS = (
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
)

STRAIGHT_DIRECTIONS = (
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
)


def is_in_check(state: GameState, color: Color) -> bool:
    """Return True if `color`'s king is currently attacked."""
    king = state.white_king if color == Color.WHITE else state.black_king

    if king == 0:
        raise ValueError(f"{color.name} has no king.")

    king_square = next(bits(king))

    opponent = color.opposite

    return (
        _is_attacked_by_pawn(state, king_square, opponent)
        or _is_attacked_by_knight(state, king_square, opponent)
        or _is_attacked_by_king(state, king_square, opponent)
        or _is_attacked_by_sliding_piece(
            state,
            king_square,
            opponent,
            DIAGONAL_DIRECTIONS,
            PieceType.BISHOP,
            PieceType.QUEEN,
        )
        or _is_attacked_by_sliding_piece(
            state,
            king_square,
            opponent,
            STRAIGHT_DIRECTIONS,
            PieceType.ROOK,
            PieceType.QUEEN,
        )
    )


def _is_attacked_by_pawn(
    state: GameState,
    square: Square,
    attacker: Color,
) -> bool:
    file = square % 8
    rank = square // 8

    # A white pawn attacks one rank upward.
    # Therefore, when checking a square attacked by white,
    # look one rank below it.
    direction = -1 if attacker == Color.WHITE else 1

    pawn_rank = rank + direction

    if not 0 <= pawn_rank < 8:
        return False

    pawns = (
        state.white_pawns
        if attacker == Color.WHITE
        else state.black_pawns
    )

    for pawn_file in (file - 1, file + 1):
        if 0 <= pawn_file < 8:
            pawn_square = Square(pawn_rank * 8 + pawn_file)

            if pawns & (1 << pawn_square):
                return True

    return False


def _is_attacked_by_knight(
    state: GameState,
    square: Square,
    attacker: Color,
) -> bool:
    file = square % 8
    rank = square // 8

    knights = (
        state.white_knights
        if attacker == Color.WHITE
        else state.black_knights
    )

    for file_offset, rank_offset in KNIGHT_OFFSETS:
        attacker_file = file + file_offset
        attacker_rank = rank + rank_offset

        if not (0 <= attacker_file < 8):
            continue
        if not (0 <= attacker_rank < 8):
            continue

        attacker_square = Square(
            attacker_rank * 8 + attacker_file
        )

        if knights & (1 << attacker_square):
            return True

    return False


def _is_attacked_by_king(
    state: GameState,
    square: Square,
    attacker: Color,
) -> bool:
    file = square % 8
    rank = square // 8

    king = (
        state.white_king
        if attacker == Color.WHITE
        else state.black_king
    )

    for file_offset, rank_offset in KING_OFFSETS:
        attacker_file = file + file_offset
        attacker_rank = rank + rank_offset

        if not (0 <= attacker_file < 8):
            continue
        if not (0 <= attacker_rank < 8):
            continue

        attacker_square = Square(
            attacker_rank * 8 + attacker_file
        )

        if king & (1 << attacker_square):
            return True

    return False


def _is_attacked_by_sliding_piece(
    state: GameState,
    square: Square,
    attacker: Color,
    directions: tuple[tuple[int, int], ...],
    *piece_types: PieceType,
) -> bool:
    file = square % 8
    rank = square // 8

    attacker_bitboards = {
        PieceType.BISHOP: (
            state.white_bishops
            if attacker == Color.WHITE
            else state.black_bishops
        ),
        PieceType.ROOK: (
            state.white_rooks
            if attacker == Color.WHITE
            else state.black_rooks
        ),
        PieceType.QUEEN: (
            state.white_queens
            if attacker == Color.WHITE
            else state.black_queens
        ),
    }

    for file_offset, rank_offset in directions:
        current_file = file + file_offset
        current_rank = rank + rank_offset

        while 0 <= current_file < 8 and 0 <= current_rank < 8:
            current_square = Square(
                current_rank * 8 + current_file
            )
            current_bit = 1 << current_square

            piece = state.piece_at(current_square)

            if piece is not None:
                piece_color, piece_type = piece

                if (
                    piece_color == attacker
                    and piece_type in piece_types
                ):
                    return True

                # Any piece blocks the ray.
                break

            current_file += file_offset
            current_rank += rank_offset

    return False

def is_square_attacked(
    state: GameState,
    square: Square,
    attacker: Color,
) -> bool:
    return (
        _is_attacked_by_pawn(state, square, attacker)
        or _is_attacked_by_knight(state, square, attacker)
        or _is_attacked_by_king(state, square, attacker)
        or _is_attacked_by_sliding_piece(
            state,
            square,
            attacker,
            DIAGONAL_DIRECTIONS,
            PieceType.BISHOP,
            PieceType.QUEEN,
        )
        or _is_attacked_by_sliding_piece(
            state,
            square,
            attacker,
            STRAIGHT_DIRECTIONS,
            PieceType.ROOK,
            PieceType.QUEEN,
        )
    )


def is_in_check(state: GameState, color: Color) -> bool:
    king = state.white_king if color == Color.WHITE else state.black_king

    if king == 0:
        raise ValueError(f"{color.name} has no king.")

    king_square = next(bits(king))

    return is_square_attacked(
        state,
        king_square,
        color.opposite,
    )