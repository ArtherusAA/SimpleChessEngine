from chess_engine.bitboard import (
    FILE_A,
    FILE_H,
    RANK_1,
    RANK_8,
    bits,
    clear_bit,
    east,
    file,
    is_set,
    lsb,
    msb,
    north,
    popcount,
    rank,
    set_bit,
    square_bit,
    south,
    toggle_bit,
    west, RANK_2, RANK_7,
)
from chess_engine.types import Square


def test_square_bit():
    assert square_bit(Square.A1) == 1
    assert square_bit(Square.H1) == 1 << 7
    assert square_bit(Square.A8) == 1 << 56
    assert square_bit(Square.H8) == 1 << 63


def test_set_and_clear_bit():
    board = 0

    board = set_bit(board, Square.E4)

    assert is_set(board, Square.E4)
    assert not is_set(board, Square.D4)

    board = clear_bit(board, Square.E4)

    assert not is_set(board, Square.E4)


def test_toggle_bit():
    board = 0

    board = toggle_bit(board, Square.E4)
    assert is_set(board, Square.E4)

    board = toggle_bit(board, Square.E4)
    assert not is_set(board, Square.E4)


def test_popcount():
    assert popcount(0) == 0
    assert popcount(1) == 1
    assert popcount(0b101010) == 3


def test_bits():
    board = (
        square_bit(Square.A1)
        | square_bit(Square.E4)
        | square_bit(Square.H8)
    )

    assert list(bits(board)) == [
        Square.A1,
        Square.E4,
        Square.H8,
    ]


def test_lsb():
    board = (
        square_bit(Square.A1)
        | square_bit(Square.E4)
        | square_bit(Square.H8)
    )

    assert lsb(board) == Square.A1


def test_msb():
    board = (
        square_bit(Square.A1)
        | square_bit(Square.E4)
        | square_bit(Square.H8)
    )

    assert msb(board) == Square.H8


def test_lsb_and_msb_empty_board():
    try:
        lsb(0)
        assert False
    except ValueError:
        pass

    try:
        msb(0)
        assert False
    except ValueError:
        pass


def test_rank():
    assert rank(Square.A1) == 0
    assert rank(Square.H1) == 0
    assert rank(Square.A8) == 7
    assert rank(Square.H8) == 7
    assert rank(Square.E4) == 3


def test_file():
    assert file(Square.A1) == 0
    assert file(Square.H1) == 7
    assert file(Square.A8) == 0
    assert file(Square.H8) == 7
    assert file(Square.E4) == 4


def test_north():
    assert north(RANK_1) == RANK_2
    assert north(RANK_7) == RANK_8
    assert north(RANK_8) == 0


def test_south():
    assert south(RANK_2) == RANK_1
    assert south(RANK_8) == RANK_7


def test_east_does_not_wrap():
    assert east(FILE_H) == 0


def test_west_does_not_wrap():
    assert west(FILE_A) == 0


def test_file_masks():
    assert popcount(FILE_A) == 8
    assert popcount(FILE_H) == 8