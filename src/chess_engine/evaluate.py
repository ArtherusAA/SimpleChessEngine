from .state import GameState
from .status import is_checkmate, is_stalemate
from .types import Color, PieceType


MATE_SCORE = 1_000_000

PIECE_VALUES = {
    PieceType.PAWN: 100,
    PieceType.KNIGHT: 320,
    PieceType.BISHOP: 330,
    PieceType.ROOK: 500,
    PieceType.QUEEN: 900,
    PieceType.KING: 0,
}


def evaluate(state: GameState) -> int:
    """
    Evaluate the position from White's perspective.

    Positive values favor White.
    Negative values favor Black.
    """
    if is_checkmate(state):
        return -MATE_SCORE if state.turn == Color.WHITE else MATE_SCORE

    if is_stalemate(state):
        return 0

    return _evaluate_material(state)


def _evaluate_material(state: GameState) -> int:
    white_material = (
        state.white_pawns.bit_count() * PIECE_VALUES[PieceType.PAWN]
        + state.white_knights.bit_count() * PIECE_VALUES[PieceType.KNIGHT]
        + state.white_bishops.bit_count() * PIECE_VALUES[PieceType.BISHOP]
        + state.white_rooks.bit_count() * PIECE_VALUES[PieceType.ROOK]
        + state.white_queens.bit_count() * PIECE_VALUES[PieceType.QUEEN]
    )

    black_material = (
        state.black_pawns.bit_count() * PIECE_VALUES[PieceType.PAWN]
        + state.black_knights.bit_count() * PIECE_VALUES[PieceType.KNIGHT]
        + state.black_bishops.bit_count() * PIECE_VALUES[PieceType.BISHOP]
        + state.black_rooks.bit_count() * PIECE_VALUES[PieceType.ROOK]
        + state.black_queens.bit_count() * PIECE_VALUES[PieceType.QUEEN]
    )

    return white_material - black_material