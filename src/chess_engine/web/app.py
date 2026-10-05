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

    def reset(self) -> None:
        self.state = GameState.initial()

    def status(self) -> str:
        if is_checkmate(self.state):
            return "checkmate"

        if is_stalemate(self.state):
            return "stalemate"

        if is_in_check(self.state, self.state.turn):
            return "check"

        return "ongoing"


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

    return {
        "pieces": pieces,
        "turn": game.state.turn.name.lower(),
        "status": game.status(),
        "legal_moves": legal_moves,
        "human_move": human_move,
        "bot_move": bot_move,
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
    game.state = game.state.make_move(move)

    if game.status() in {"checkmate", "stalemate"}:
        return serialize_state(human_move=human_move)

    bot_move = game.bot.choose_move(game.state)

    if bot_move is None:
        return serialize_state(human_move=human_move)

    bot_move_string = move_to_string(bot_move)
    game.state = game.state.make_move(bot_move)

    return serialize_state(
        human_move=human_move,
        bot_move=bot_move_string,
    )