from chess_engine.check import is_in_check
from chess_engine.legal import generate_legal_moves
from chess_engine.move import Move
from chess_engine.state import (
    BLACK_KINGSIDE,
    BLACK_QUEENSIDE,
    WHITE_KINGSIDE,
    WHITE_QUEENSIDE,
    GameState,
)
from chess_engine.types import Color, PieceType, Square


def empty_castling_state() -> GameState:
    return GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=(1 << Square.A1) | (1 << Square.H1),
        white_queens=0,
        white_king=1 << Square.E1,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.E8,
        turn=Color.WHITE,
        castling_rights=(
            WHITE_KINGSIDE
            | WHITE_QUEENSIDE
        ),
    )

def test_white_kingside_castling():
    state = empty_castling_state()

    moves = generate_legal_moves(state)

    assert Move(
        Square.E1,
        Square.G1,
        is_castling=True,
    ) in moves

def test_white_queenside_castling():
    state = empty_castling_state()

    moves = generate_legal_moves(state)

    assert Move(
        Square.E1,
        Square.C1,
        is_castling=True,
    ) in moves

def test_kingside_castling_moves_rook():
    state = empty_castling_state()

    new_state = state.make_move(
        Move(
            Square.E1,
            Square.G1,
            is_castling=True,
        )
    )

    assert new_state.piece_at(Square.E1) is None
    assert new_state.piece_at(Square.G1) == (
        Color.WHITE,
        PieceType.KING,
    )

    assert new_state.piece_at(Square.H1) is None
    assert new_state.piece_at(Square.F1) == (
        Color.WHITE,
        PieceType.ROOK,
    )

def test_cannot_castle_through_attacked_square():
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=1 << Square.H1,
        white_queens=0,
        white_king=1 << Square.E1,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=1 << Square.F8,
        black_queens=0,
        black_king=1 << Square.A8,
        turn=Color.WHITE,
        castling_rights=WHITE_KINGSIDE,
    )

    moves = generate_legal_moves(state)

    assert Move(
        Square.E1,
        Square.G1,
        is_castling=True,
    ) not in moves


def test_cannot_castle_while_in_check():
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=1 << Square.H1,
        white_queens=0,
        white_king=1 << Square.E1,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=1 << Square.E8,
        black_queens=0,
        black_king=1 << Square.A8,
        turn=Color.WHITE,
        castling_rights=WHITE_KINGSIDE,
    )

    assert is_in_check(state, Color.WHITE)

    moves = generate_legal_moves(state)

    assert Move(
        Square.E1,
        Square.G1,
        is_castling=True,
    ) not in moves


def test_king_move_removes_castling_rights():
    state = empty_castling_state()

    new_state = state.make_move(
        Move(Square.E1, Square.F1)
    )

    assert not new_state.castling_rights & WHITE_KINGSIDE
    assert not new_state.castling_rights & WHITE_QUEENSIDE


def test_rook_move_removes_kingside_right():
    state = empty_castling_state()

    new_state = state.make_move(
        Move(Square.H1, Square.G1)
    )

    assert not new_state.castling_rights & WHITE_KINGSIDE
    assert new_state.castling_rights & WHITE_QUEENSIDE

def test_capturing_rook_removes_castling_right():
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=0,
        white_queens=1 << Square.A8,
        white_king=1 << Square.E1,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=1 << Square.H8,
        black_queens=0,
        black_king=1 << Square.E8,
        turn=Color.WHITE,
        castling_rights=BLACK_KINGSIDE,
    )

    new_state = state.make_move(
        Move(Square.A8, Square.H8)
    )

    assert not new_state.castling_rights & BLACK_KINGSIDE
