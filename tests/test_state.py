from chess_engine.bitboard import popcount
from chess_engine.state import (
    BLACK_KINGSIDE,
    BLACK_QUEENSIDE,
    WHITE_KINGSIDE,
    WHITE_QUEENSIDE,
    GameState,
)
from chess_engine.types import Color, PieceType, Square


def test_initial_position_turn():
    state = GameState.initial()

    assert state.turn == Color.WHITE


def test_initial_position_castling_rights():
    state = GameState.initial()

    expected = (
        WHITE_KINGSIDE
        | WHITE_QUEENSIDE
        | BLACK_KINGSIDE
        | BLACK_QUEENSIDE
    )

    assert state.castling_rights == expected


def test_initial_position_has_32_pieces():
    state = GameState.initial()

    assert popcount(state.occupied()) == 32


def test_initial_position_white_has_16_pieces():
    state = GameState.initial()

    assert popcount(state.white_pieces()) == 16


def test_initial_position_black_has_16_pieces():
    state = GameState.initial()

    assert popcount(state.black_pieces()) == 16


def test_initial_position_piece_counts():
    state = GameState.initial()

    assert popcount(state.white_pawns) == 8
    assert popcount(state.white_knights) == 2
    assert popcount(state.white_bishops) == 2
    assert popcount(state.white_rooks) == 2
    assert popcount(state.white_queens) == 1
    assert popcount(state.white_king) == 1

    assert popcount(state.black_pawns) == 8
    assert popcount(state.black_knights) == 2
    assert popcount(state.black_bishops) == 2
    assert popcount(state.black_rooks) == 2
    assert popcount(state.black_queens) == 1
    assert popcount(state.black_king) == 1


def test_initial_position_piece_locations():
    state = GameState.initial()

    assert state.has_piece(
        Color.WHITE,
        PieceType.KING,
        Square.E1,
    )

    assert state.has_piece(
        Color.WHITE,
        PieceType.QUEEN,
        Square.D1,
    )

    assert state.has_piece(
        Color.WHITE,
        PieceType.ROOK,
        Square.A1,
    )

    assert state.has_piece(
        Color.WHITE,
        PieceType.KNIGHT,
        Square.B1,
    )

    assert state.has_piece(
        Color.BLACK,
        PieceType.KING,
        Square.E8,
    )

    assert state.has_piece(
        Color.BLACK,
        PieceType.QUEEN,
        Square.D8,
    )


def test_piece_at():
    state = GameState.initial()

    assert state.piece_at(Square.E1) == (
        Color.WHITE,
        PieceType.KING,
    )

    assert state.piece_at(Square.D1) == (
        Color.WHITE,
        PieceType.QUEEN,
    )

    assert state.piece_at(Square.E8) == (
        Color.BLACK,
        PieceType.KING,
    )

    assert state.piece_at(Square.E4) is None


def test_initial_position_is_not_empty():
    state = GameState.initial()

    assert state.empty() != state.occupied()


def test_initial_position_occupied_and_empty_are_complements():
    state = GameState.initial()

    assert state.occupied() | state.empty() == (1 << 64) - 1
    assert state.occupied() & state.empty() == 0


def test_color_opposite():
    assert Color.WHITE.opposite == Color.BLACK
    assert Color.BLACK.opposite == Color.WHITE