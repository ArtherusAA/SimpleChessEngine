import pytest

from chess_engine.bot import ChessBot
from chess_engine.legal import generate_legal_moves
from chess_engine.state import GameState
from chess_engine.types import Color, Square


def test_bot_selects_legal_move():
    state = GameState.initial()

    bot = ChessBot(Color.WHITE, depth=1)

    move = bot.choose_move(state)

    assert move is not None
    assert move in generate_legal_moves(state)


def test_bot_applies_move():
    state = GameState.initial()

    bot = ChessBot(Color.WHITE, depth=1)

    move, new_state = bot.play(state)

    assert move is not None
    assert new_state != state
    assert new_state.turn == Color.BLACK
    assert move not in generate_legal_moves(new_state)


def test_bot_rejects_wrong_turn():
    state = GameState.initial()

    bot = ChessBot(Color.BLACK, depth=1)

    with pytest.raises(ValueError):
        bot.choose_move(state)


def test_bot_returns_none_for_stalemate():
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

    bot = ChessBot(Color.BLACK, depth=1)

    move, new_state = bot.play(state)

    assert move is None
    assert new_state == state