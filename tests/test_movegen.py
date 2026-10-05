from chess_engine.movegen import (
    generate_bishop_moves,
    generate_king_moves,
    generate_knight_moves,
    generate_pawn_moves,
    generate_queen_moves,
    generate_rook_moves,
)
from chess_engine.state import GameState
from chess_engine.types import Color, PieceType, Square


def test_initial_white_pawn_moves():
    state = GameState.initial()

    moves = generate_pawn_moves(state, Color.WHITE)

    assert len(moves) == 16


def test_initial_black_pawn_moves():
    state = GameState.initial()

    moves = generate_pawn_moves(state, Color.BLACK)

    assert len(moves) == 16


def test_initial_white_knight_moves():
    state = GameState.initial()

    moves = generate_knight_moves(state, Color.WHITE)

    assert len(moves) == 4


def test_initial_black_knight_moves():
    state = GameState.initial()

    moves = generate_knight_moves(state, Color.BLACK)

    assert len(moves) == 4


def test_initial_bishops_cannot_move():
    state = GameState.initial()

    assert generate_bishop_moves(state, Color.WHITE) == []
    assert generate_bishop_moves(state, Color.BLACK) == []


def test_initial_rooks_cannot_move():
    state = GameState.initial()

    assert generate_rook_moves(state, Color.WHITE) == []
    assert generate_rook_moves(state, Color.BLACK) == []


def test_initial_queens_cannot_move():
    state = GameState.initial()

    assert generate_queen_moves(state, Color.WHITE) == []
    assert generate_queen_moves(state, Color.BLACK) == []


def test_initial_kings_cannot_move():
    state = GameState.initial()

    assert generate_king_moves(state, Color.WHITE) == []
    assert generate_king_moves(state, Color.BLACK) == []

def test_initial_white_pawn_moves_are_one_or_two_squares():
    state = GameState.initial()

    moves = generate_pawn_moves(state, Color.WHITE)

    expected = {
        (Square.A2, Square.A3),
        (Square.A2, Square.A4),
        (Square.B2, Square.B3),
        (Square.B2, Square.B4),
        (Square.C2, Square.C3),
        (Square.C2, Square.C4),
        (Square.D2, Square.D3),
        (Square.D2, Square.D4),
        (Square.E2, Square.E3),
        (Square.E2, Square.E4),
        (Square.F2, Square.F3),
        (Square.F2, Square.F4),
        (Square.G2, Square.G3),
        (Square.G2, Square.G4),
        (Square.H2, Square.H3),
        (Square.H2, Square.H4),
    }

    actual = {
        (move.from_square, move.to_square)
        for move in moves
    }

    assert actual == expected

def empty_state(
    *,
    white_knights: int = 0,
    black_knights: int = 0,
) -> GameState:
    return GameState(
        white_pawns=0,
        white_knights=white_knights,
        white_bishops=0,
        white_rooks=0,
        white_queens=0,
        white_king=1 << Square.E1,
        black_pawns=0,
        black_knights=black_knights,
        black_bishops=0,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.E8,
        turn=Color.WHITE,
        castling_rights=0,
    )

def test_knight_from_center():
    state = empty_state(
        white_knights=1 << Square.D4,
    )

    moves = generate_knight_moves(state, Color.WHITE)

    actual = {
        move.to_square
        for move in moves
    }

    expected = {
        Square.B3,
        Square.B5,
        Square.C2,
        Square.C6,
        Square.E2,
        Square.E6,
        Square.F3,
        Square.F5,
    }

    assert actual == expected

def test_knight_cannot_capture_own_piece():
    state = GameState(
        white_pawns=1 << Square.C6,
        white_knights=1 << Square.D4,
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

    moves = generate_knight_moves(state, Color.WHITE)

    assert all(move.to_square != Square.C6 for move in moves)

def test_bishop_stops_at_own_piece():
    state = GameState(
        white_pawns=1 << Square.E5,
        white_knights=0,
        white_bishops=1 << Square.D4,
        white_rooks=0,
        white_queens=0,
        white_king=1 << Square.A1,
        black_pawns=0,
        black_knights=0,
        black_bishops=0,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.H8,
        turn=Color.WHITE,
        castling_rights=0,
    )

    moves = generate_bishop_moves(state, Color.WHITE)
    destinations = {move.to_square for move in moves}

    # Own piece on E5 blocks this diagonal.
    assert Square.E5 not in destinations
    assert Square.F6 not in destinations
    assert Square.G7 not in destinations

    # Other diagonal remains available.
    assert Square.C5 in destinations
    assert Square.B6 in destinations
    assert Square.A7 in destinations

    assert Square.C3 in destinations
    assert Square.B2 in destinations

def test_rook_can_capture_but_cannot_move_through_enemy():
    state = GameState(
        white_pawns=0,
        white_knights=0,
        white_bishops=0,
        white_rooks=1 << Square.D4,
        white_queens=0,
        white_king=1 << Square.E1,
        black_pawns=1 << Square.D7,
        black_knights=0,
        black_bishops=0,
        black_rooks=0,
        black_queens=0,
        black_king=1 << Square.E8,
        turn=Color.WHITE,
        castling_rights=0,
    )

    moves = generate_rook_moves(state, Color.WHITE)

    actual = {
        move.to_square
        for move in moves
    }

    assert Square.D7 in actual
    assert Square.D8 not in actual
