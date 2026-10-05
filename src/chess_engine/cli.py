from .bot import ChessBot
from .check import is_in_check
from .legal import generate_legal_moves
from .move import Move
from .state import GameState
from .status import is_checkmate, is_stalemate
from .types import Color, PieceType, Square
from .notation import move_to_string, parse_move

PIECE_SYMBOLS = {
    (Color.WHITE, PieceType.PAWN): "P",
    (Color.WHITE, PieceType.KNIGHT): "N",
    (Color.WHITE, PieceType.BISHOP): "B",
    (Color.WHITE, PieceType.ROOK): "R",
    (Color.WHITE, PieceType.QUEEN): "Q",
    (Color.WHITE, PieceType.KING): "K",
    (Color.BLACK, PieceType.PAWN): "p",
    (Color.BLACK, PieceType.KNIGHT): "n",
    (Color.BLACK, PieceType.BISHOP): "b",
    (Color.BLACK, PieceType.ROOK): "r",
    (Color.BLACK, PieceType.QUEEN): "q",
    (Color.BLACK, PieceType.KING): "k",
}

PROMOTION_PIECES = {
    "q": PieceType.QUEEN,
    "r": PieceType.ROOK,
    "b": PieceType.BISHOP,
    "n": PieceType.KNIGHT,
}


def square_to_string(square: Square) -> str:
    file_name = chr(ord("a") + (square % 8))
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



def print_board(state: GameState) -> None:
    print()
    print("  +-----------------+")

    for rank in range(7, -1, -1):
        row = []

        for file_index in range(8):
            square = Square(rank * 8 + file_index)
            piece = state.piece_at(square)

            if piece is None:
                row.append(".")
            else:
                row.append(PIECE_SYMBOLS[piece])

        print(f"{rank + 1} | {' '.join(row)} |")

    print("  +-----------------+")
    print("    a b c d e f g h")
    print()


def print_game_status(state: GameState) -> bool:
    if is_checkmate(state):
        winner = state.turn.opposite
        print(f"Checkmate! {winner.name.title()} wins.")
        return True

    if is_stalemate(state):
        print("Stalemate! Draw.")
        return True

    if is_in_check(state, state.turn):
        print(f"{state.turn.name.title()} is in check.")

    return False


def play_game() -> None:
    state = GameState.initial()

    human_color = Color.WHITE
    human_turn = ChessBot(Color.BLACK, depth=2)

    print("Simple Chess")
    print("You are White.")
    print("Enter moves in UCI notation, for example: e2e4")
    print("Type 'quit' to exit.")

    while True:
        print_board(state)

        if print_game_status(state):
            break

        if state.turn == human_color:
            while True:
                value = input("Your move: ").strip()

                if value.lower() in {"quit", "exit"}:
                    return

                try:
                    move = parse_move(value, state)
                except ValueError as exc:
                    print(exc)
                    continue

                state = state.make_move(move)
                break

        else:
            move, state = human_turn.play(state)

            if move is None:
                break

            print(f"Bot: {move_to_string(move)}")


if __name__ == "__main__":
    play_game()