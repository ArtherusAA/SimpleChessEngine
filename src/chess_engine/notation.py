from .legal import generate_legal_moves
from .move import Move
from .state import GameState
from .types import PieceType, Square


PROMOTION_PIECES = {
    "q": PieceType.QUEEN,
    "r": PieceType.ROOK,
    "b": PieceType.BISHOP,
    "n": PieceType.KNIGHT,
}

PROMOTION_NAMES = {
    PieceType.QUEEN: "q",
    PieceType.ROOK: "r",
    PieceType.BISHOP: "b",
    PieceType.KNIGHT: "n",
}


def square_to_string(square: Square) -> str:
    file_name = chr(ord("a") + square % 8)
    rank_name = str(square // 8 + 1)
    return file_name + rank_name


def parse_square(value: str) -> Square:
    if len(value) != 2:
        raise ValueError(f"Invalid square: {value}")

    file_index = ord(value[0].lower()) - ord("a")
    rank_index = ord(value[1]) - ord("1")

    if not (0 <= file_index < 8 and 0 <= rank_index < 8):
        raise ValueError(f"Invalid square: {value}")

    return Square(rank_index * 8 + file_index)


def parse_move(value: str, state: GameState) -> Move:
    value = value.strip().lower()

    if len(value) not in (4, 5):
        raise ValueError(
            "Move must use UCI notation, for example e2e4 or e7e8q."
        )

    from_square = parse_square(value[:2])
    to_square = parse_square(value[2:4])

    promotion = None

    if len(value) == 5:
        try:
            promotion = PROMOTION_PIECES[value[4]]
        except KeyError as exc:
            raise ValueError(f"Invalid promotion piece: {value[4]}") from exc

    for move in generate_legal_moves(state):
        if (
            move.from_square == from_square
            and move.to_square == to_square
            and move.promotion == promotion
        ):
            return move

    raise ValueError(f"Illegal move: {value}")


def move_to_string(move: Move) -> str:
    result = (
        square_to_string(move.from_square)
        + square_to_string(move.to_square)
    )

    if move.promotion is not None:
        result += PROMOTION_NAMES[move.promotion]

    return result