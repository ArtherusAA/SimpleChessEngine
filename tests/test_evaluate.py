from chess_engine.evaluate import MATE_SCORE, evaluate
from chess_engine.state import GameState
from chess_engine.types import Color, Square


def test_initial_position_is_equal():
    state = GameState.initial()

    assert evaluate(state) == 0


def test_white_up_a_queen():
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=1 << Square.D1,
        white_king=1 << Square.E1,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.E8,
        turn=Color.WHITE,
        castling_rights=0,
    )

    assert evaluate(state) == 900


def test_black_up_a_rook():
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
        black_rooks=1 << Square.A8,
        black_queens=0,
        black_king=1 << Square.E8,
        turn=Color.WHITE,
        castling_rights=0,
    )

    assert evaluate(state) == -500


def test_stalemate_is_draw():
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

    assert evaluate(state) == 0


def test_black_checkmate_is_winning_for_white():
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

    assert evaluate(state) == MATE_SCORE


def test_white_checkmate_is_winning_for_black():
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=0,
        white_king=1 << Square.H1,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=0,
        black_queens=1 << Square.G2,
        black_king=1 << Square.F3,
        turn=Color.WHITE,
        castling_rights=0,
    )

    assert evaluate(state) == -MATE_SCORE