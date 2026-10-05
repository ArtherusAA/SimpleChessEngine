import pytest

from chess_engine.legal import generate_legal_moves
from chess_engine.move import Move
from chess_engine.state import GameState
from chess_engine.types import Color, PieceType, Square


def test_pawn_single_push():
    state = GameState.initial()

    new_state = state.make_move(
        Move(Square.E2, Square.E4)
    )

    assert new_state.turn == Color.BLACK
    assert new_state.piece_at(Square.E2) is None
    assert new_state.piece_at(Square.E4) == (
        Color.WHITE,
        PieceType.PAWN,
    )


def test_pawn_double_push_sets_en_passant_square():
    state = GameState.initial()

    new_state = state.make_move(
        Move(Square.E2, Square.E4)
    )

    assert new_state.en_passant_square == Square.E3


def test_capture():
    state = GameState(
        white_pawns=1 << Square.E4,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=0,
        white_king=1 << Square.E1,
        black_pawns=1 << Square.D5,
        black_knights=0,
        black_bishops=0,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.E8,
        turn=Color.WHITE,
        castling_rights=0,
    )

    new_state = state.make_move(
        Move(Square.E4, Square.D5)
    )

    assert new_state.piece_at(Square.E4) is None
    assert new_state.piece_at(Square.D5) == (
        Color.WHITE,
        PieceType.PAWN,
    )


def test_promotion():
    state = GameState(
        white_pawns=1 << Square.E7,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=0,
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

    new_state = state.make_move(
        Move(
            Square.E7,
            Square.E8,
            promotion=PieceType.QUEEN,
        )
    )

    assert new_state.piece_at(Square.E7) is None
    assert new_state.piece_at(Square.E8) == (
        Color.WHITE,
        PieceType.QUEEN,
    )

def test_make_move_does_not_modify_original_state():
    state = GameState.initial()

    new_state = state.make_move(
        Move(Square.E2, Square.E4)
    )

    assert state.piece_at(Square.E2) == (
        Color.WHITE,
        PieceType.PAWN,
    )
    assert state.piece_at(Square.E4) is None

    assert new_state.piece_at(Square.E2) is None
    assert new_state.piece_at(Square.E4) == (
        Color.WHITE,
        PieceType.PAWN,
    )

def test_en_passant():
    state = GameState(
        white_pawns=1 << Square.E5,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=0,
        white_king=1 << Square.E1,
        black_pawns=1 << Square.D5,
        black_knights=0,
        black_bishops=0,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.E8,
        turn=Color.WHITE,
        castling_rights=0,
        en_passant_square=Square.D6,
    )

    new_state = state.make_move(
        Move(
            Square.E5,
            Square.D6,
            is_en_passant=True,
        )
    )

    assert new_state.piece_at(Square.E5) is None
    assert new_state.piece_at(Square.D5) is None
    assert new_state.piece_at(Square.D6) == (
        Color.WHITE,
        PieceType.PAWN,
    )

def test_invalid_en_passant_without_pawn():
    state = GameState(
        white_pawns=1 << Square.E5,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=0,
        white_king=1 << Square.E1,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.E8,
        turn=Color.WHITE,
        castling_rights=0,
        en_passant_square=Square.D6,
    )

    with pytest.raises(ValueError):
        state.make_move(
            Move(
                Square.E5,
                Square.D6,
                is_en_passant=True,
            )
        )

def test_en_passant_that_exposes_king_is_illegal():
    state = GameState(
        white_pawns=1 << Square.E5,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=0,
        white_king=1 << Square.E1,
        black_pawns=1 << Square.F5,
        black_knights=0,
        black_bishops=0,
        black_rooks=1 << Square.E8,
        black_queens=0,
        black_king=1 << Square.H8,
        turn=Color.WHITE,
        castling_rights=0,
        en_passant_square=Square.F6,
    )

    moves = generate_legal_moves(state)

    assert Move(
        Square.E5,
        Square.F6,
        is_en_passant=True,
    ) not in moves
