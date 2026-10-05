from chess_engine.check import is_in_check
from chess_engine.state import GameState
from chess_engine.status import is_checkmate, is_stalemate
from chess_engine.types import Color, Square


def test_stalemate():
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=1 << Square.F7,
        white_king=1 << Square.G6,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.H8,
        turn=Color.BLACK,
        castling_rights=0,
    )

    assert not is_in_check(state, Color.BLACK)
    assert is_stalemate(state)
    assert not is_checkmate(state)


def test_not_stalemate_when_legal_move_exists():
    state = GameState.initial()

    assert not is_stalemate(state)


def test_not_stalemate_when_in_check():
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=1 << Square.H7,
        white_king=1 << Square.F6,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.H8,
        turn=Color.BLACK,
        castling_rights=0,
    )

    assert is_in_check(state, Color.BLACK)
    assert not is_stalemate(state)

def test_checkmate():
    # Black king is checkmated in the corner.
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=1 << Square.G7,
        white_king=1 << Square.F6,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.H8,
        turn=Color.BLACK,
        castling_rights=0,
    )

    assert is_in_check(state, Color.BLACK)
    assert is_checkmate(state)
    assert not is_stalemate(state)


def test_not_checkmate_when_king_has_escape_square():
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=1 << Square.F7,
        white_king=1 << Square.G6,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.G8,
        turn=Color.BLACK,
        castling_rights=0,
    )

    assert is_in_check(state, Color.BLACK)
    assert not is_checkmate(state)

def test_not_checkmate_when_checking_piece_can_be_captured():
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=1 << Square.H7,
        white_king=1 << Square.F6,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.G8,
        turn=Color.BLACK,
        castling_rights=0,
    )

    assert is_in_check(state, Color.BLACK)
    assert not is_checkmate(state)