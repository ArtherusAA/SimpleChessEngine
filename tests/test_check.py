from chess_engine.check import is_in_check
from chess_engine.legal import generate_legal_moves
from chess_engine.move import Move
from chess_engine.state import GameState
from chess_engine.types import Color, Square


def test_white_in_check_by_rook():
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=0,
        white_king=1 << Square.E1,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=1 << Square.E8,
        black_queens=0,
        black_king=1 << Square.A8,
        turn=Color.WHITE,
        castling_rights=0,
    )

    assert is_in_check(state, Color.WHITE)

def test_rook_check_is_blocked():
    state = GameState(
        white_pawns=1 << Square.E4,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=0,
        white_king=1 << Square.E1,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=1 << Square.E8,
        black_queens=0,
        black_king=1 << Square.A8,
        turn=Color.WHITE,
        castling_rights=0,
    )

    assert not is_in_check(state, Color.WHITE)

def test_white_in_check_by_bishop():
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=0,
        white_king=1 << Square.E1,
        black_pawns=0,
        black_knights=0,
        black_bishops=1 << Square.B4,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.H8,
        turn=Color.WHITE,
        castling_rights=0,
    )

    assert is_in_check(state, Color.WHITE)

def test_white_in_check_by_knight():
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=0,
        white_king=1 << Square.E4,
        black_pawns=0,
        black_knights=1 << Square.F6,
        black_bishops=0,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.H8,
        turn=Color.WHITE,
        castling_rights=0,
    )

    assert is_in_check(state, Color.WHITE)

def test_white_in_check_by_pawn():
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=0,
        white_king=1 << Square.E4,
        black_pawns=1 << Square.D5,
        black_knights=0,
        black_bishops=0,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.H8,
        turn=Color.WHITE,
        castling_rights=0,
    )

    assert is_in_check(state, Color.WHITE)


def test_move_exposing_king_is_illegal():
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=1 << Square.E2,
        white_queens=0,
        white_king=1 << Square.E1,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=1 << Square.E8,
        black_queens=0,
        black_king=1 << Square.H8,
        turn=Color.WHITE,
        castling_rights=0,
    )

    legal_moves = generate_legal_moves(state)

    assert Move(Square.E2, Square.F2) not in legal_moves
    assert Move(Square.E2, Square.D2) not in legal_moves
    assert Move(Square.E2, Square.E3) in legal_moves
    assert Move(Square.E2, Square.E4) in legal_moves
    assert Move(Square.E2, Square.E5) in legal_moves
    assert Move(Square.E2, Square.E6) in legal_moves
    assert Move(Square.E2, Square.E7) in legal_moves