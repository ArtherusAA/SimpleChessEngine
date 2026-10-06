from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ..bot import ChessBot
from ..check import is_in_check
from ..legal import generate_legal_moves
from ..notation import move_to_string, parse_move, square_to_string
from ..state import GameState
from ..status import is_checkmate, is_stalemate
from ..types import Color, PieceType, Square
from ..evaluate import evaluate, PIECE_VALUES
from ..move import Move

BASE_DIR = Path(__file__).parent

app = FastAPI(title="Simple Chess")

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


PIECE_SYMBOLS = {
    (Color.WHITE, PieceType.PAWN): "♙",
    (Color.WHITE, PieceType.KNIGHT): "♘",
    (Color.WHITE, PieceType.BISHOP): "♗",
    (Color.WHITE, PieceType.ROOK): "♖",
    (Color.WHITE, PieceType.QUEEN): "♕",
    (Color.WHITE, PieceType.KING): "♔",
    (Color.BLACK, PieceType.PAWN): "♟",
    (Color.BLACK, PieceType.KNIGHT): "♞",
    (Color.BLACK, PieceType.BISHOP): "♝",
    (Color.BLACK, PieceType.ROOK): "♜",
    (Color.BLACK, PieceType.QUEEN): "♛",
    (Color.BLACK, PieceType.KING): "♚",
}


class MoveRequest(BaseModel):
    move: str


class ChessGame:
    def __init__(self) -> None:
        self.state = GameState.initial()
        self.bot = ChessBot(Color.BLACK, depth=2)
        self.captured_white: list[PieceType] = []
        self.captured_black: list[PieceType] = []

    def reset(self) -> None:
        self.state = GameState.initial()
        self.captured_white = []
        self.captured_black = []

    def status(self) -> str:
        if is_checkmate(self.state):
            return "checkmate"

        if is_stalemate(self.state):
            return "stalemate"

        if is_in_check(self.state, self.state.turn):
            return "check"

        return "ongoing"

    def make_move(self, move: Move) -> None:
        captured_piece = self._captured_piece(move)

        if captured_piece is not None:
            captured_color, captured_type = captured_piece

            if captured_color == Color.WHITE:
                self.captured_white.append(captured_type)
            else:
                self.captured_black.append(captured_type)

        self.state = self.state.make_move(move)

    def _captured_piece(
        self,
        move: Move,
    ) -> tuple[Color, PieceType] | None:
        if move.is_en_passant:
            captured_square = (
                Square(move.to_square - 8)
                if self.state.turn == Color.WHITE
                else Square(move.to_square + 8)
            )
            return self.state.piece_at(captured_square)

        return self.state.piece_at(move.to_square)

def material_value(state: GameState, color: Color) -> int:
    if color == Color.WHITE:
        return (
            state.white_pawns.bit_count() * PIECE_VALUES[PieceType.PAWN]
            + state.white_knights.bit_count() * PIECE_VALUES[PieceType.KNIGHT]
            + state.white_bishops.bit_count() * PIECE_VALUES[PieceType.BISHOP]
            + state.white_rooks.bit_count() * PIECE_VALUES[PieceType.ROOK]
            + state.white_queens.bit_count() * PIECE_VALUES[PieceType.QUEEN]
        )

    return (
        state.black_pawns.bit_count() * PIECE_VALUES[PieceType.PAWN]
        + state.black_knights.bit_count() * PIECE_VALUES[PieceType.KNIGHT]
        + state.black_bishops.bit_count() * PIECE_VALUES[PieceType.BISHOP]
        + state.black_rooks.bit_count() * PIECE_VALUES[PieceType.ROOK]
        + state.black_queens.bit_count() * PIECE_VALUES[PieceType.QUEEN]
    )

game = ChessGame()


def serialize_state(
    human_move: str | None = None,
    bot_move: str | None = None,
) -> dict:
    pieces = []

    for square in Square:
        piece = game.state.piece_at(square)

        if piece is None:
            continue

        color, piece_type = piece

        pieces.append(
            {
                "square": square_to_string(square),
                "color": color.name.lower(),
                "type": piece_type.name.lower(),
                "symbol": PIECE_SYMBOLS[piece],
            }
        )

    legal_moves = [
        move_to_string(move)
        for move in generate_legal_moves(game.state)
    ]

    white_material = material_value(game.state, Color.WHITE)
    black_material = material_value(game.state, Color.BLACK)

    return {
        "pieces": pieces,
        "turn": game.state.turn.name.lower(),
        "status": game.status(),
        "legal_moves": legal_moves,
        "human_move": human_move,
        "bot_move": bot_move,

        "evaluation": evaluate(game.state),
        "white_material": white_material,
        "black_material": black_material,

        "captured_white": [
            PIECE_SYMBOLS[(Color.WHITE, piece_type)]
            for piece_type in game.captured_white
        ],
        "captured_black": [
            PIECE_SYMBOLS[(Color.BLACK, piece_type)]
            for piece_type in game.captured_black
        ],
    }


@app.get("/")
def index() -> FileResponse:
    return FileResponse(BASE_DIR / "templates" / "index.html")


@app.get("/api/state")
def get_state() -> dict:
    return serialize_state()


@app.post("/api/new")
def new_game() -> dict:
    game.reset()
    return serialize_state()


@app.post("/api/move")
def make_move(request: MoveRequest) -> dict:
    if game.status() in {"checkmate", "stalemate"}:
        raise HTTPException(status_code=400, detail="The game is already over.")

    if game.state.turn != Color.WHITE:
        raise HTTPException(status_code=400, detail="It is not White's turn.")

    try:
        move = parse_move(request.move, game.state)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    human_move = move_to_string(move)
    game.make_move(move)

    return serialize_state(human_move=human_move)

@app.post("/api/bot-move")
def make_bot_move() -> dict:
    if game.status() in {"checkmate", "stalemate"}:
        return serialize_state()

    if game.state.turn != game.bot.color:
        raise HTTPException(
            status_code=400,
            detail="It is not the bot's turn.",
        )

    bot_move = game.bot.choose_move(game.state)

    if bot_move is None:
        return serialize_state()

    bot_move_string = move_to_string(bot_move)
    game.make_move(bot_move)

    return serialize_state(bot_move=bot_move_string)
