from chess_engine.evaluate import MATE_SCORE
from chess_engine.search import find_best_move, minimax
from chess_engine.state import GameState
from chess_engine.status import is_checkmate
from chess_engine.types import Color, Square


def test_minimax_depth_zero_uses_evaluation():
    state = GameState.initial()

    assert minimax(state, 0) == 0


def test_minimax_prefers_material_advantage():
    state = GameState(
        white_pawns=1 << Square.A2,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=1 << Square.D1,
        white_king=1 << Square.E1,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=0,
        black_queens=1 << Square.D8,
        black_king=1 << Square.E8,
        turn=Color.WHITE,
        castling_rights=0,
    )

    # White has a pawn more, so the position is evaluated positively.
    assert minimax(state, 0) == 100


def test_find_best_move_finds_mate_in_one():
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
        turn=Color.WHITE,
        castling_rights=0,
    )

    move, score = find_best_move(state, 1)

    assert move is not None
    assert move.from_square == Square.F7
    assert score == MATE_SCORE

    new_state = state.make_move(move)

    assert is_checkmate(new_state)


def test_find_best_move_returns_none_for_stalemate():
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

    move, score = find_best_move(state, 1)

    assert move is None
    assert score == 0