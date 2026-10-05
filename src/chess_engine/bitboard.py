from collections.abc import Iterator

from .types import Square


# All 64 bits set.
FULL_BOARD = (1 << 64) - 1

# Individual ranks.
RANK_1 = 0x00000000000000FF
RANK_2 = 0x000000000000FF00
RANK_3 = 0x0000000000FF0000
RANK_4 = 0x00000000FF000000
RANK_5 = 0x000000FF00000000
RANK_6 = 0x0000FF0000000000
RANK_7 = 0x00FF000000000000
RANK_8 = 0xFF00000000000000

# Individual files.
FILE_A = 0x0101010101010101
FILE_B = 0x0202020202020202
FILE_C = 0x0404040404040404
FILE_D = 0x0808080808080808
FILE_E = 0x1010101010101010
FILE_F = 0x2020202020202020
FILE_G = 0x4040404040404040
FILE_H = 0x8080808080808080


def square_bit(square: Square) -> int:
    """Return the bit corresponding to a square."""
    return 1 << square


def is_set(bitboard: int, square: Square) -> bool:
    """Return whether a square is occupied in the bitboard."""
    return bool(bitboard & square_bit(square))


def set_bit(bitboard: int, square: Square) -> int:
    """Set the bit corresponding to a square."""
    return bitboard | square_bit(square)


def clear_bit(bitboard: int, square: Square) -> int:
    """Clear the bit corresponding to a square."""
    return bitboard & ~square_bit(square)


def toggle_bit(bitboard: int, square: Square) -> int:
    """Toggle the bit corresponding to a square."""
    return bitboard ^ square_bit(square)


def popcount(bitboard: int) -> int:
    """Return the number of set bits."""
    return bitboard.bit_count()


def bits(bitboard: int) -> Iterator[Square]:
    """Iterate over all occupied squares."""
    while bitboard:
        least_significant_bit = bitboard & -bitboard
        square = least_significant_bit.bit_length() - 1

        yield Square(square)

        bitboard &= bitboard - 1


def lsb(bitboard: int) -> Square:
    """Return the square corresponding to the least significant set bit."""
    if bitboard == 0:
        raise ValueError("Cannot find LSB of an empty bitboard.")

    return Square((bitboard & -bitboard).bit_length() - 1)


def msb(bitboard: int) -> Square:
    """Return the square corresponding to the most significant set bit."""
    if bitboard == 0:
        raise ValueError("Cannot find MSB of an empty bitboard.")

    return Square(bitboard.bit_length() - 1)


def rank(square: Square) -> int:
    """Return the zero-based rank of a square."""
    return square // 8


def file(square: Square) -> int:
    """Return the zero-based file of a square."""
    return square % 8


def north(bitboard: int) -> int:
    """Shift all bits one rank north."""
    return (bitboard << 8) & FULL_BOARD


def south(bitboard: int) -> int:
    """Shift all bits one rank south."""
    return bitboard >> 8


def east(bitboard: int) -> int:
    """Shift all bits one file east."""
    return (bitboard << 1) & ~FILE_A & FULL_BOARD


def west(bitboard: int) -> int:
    """Shift all bits one file west."""
    return (bitboard >> 1) & ~FILE_H