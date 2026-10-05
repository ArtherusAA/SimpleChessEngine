from .evaluate import evaluate
from .legal import generate_legal_moves
from .move import Move
from .state import GameState
from .types import Color


def minimax(state: GameState, depth: int) -> int:
    """
    Search the position to the given depth using plain minimax.

    The returned score is always from White's perspective:
    positive values favor White, negative values favor Black.
    """
    legal_moves = generate_legal_moves(state)

    if depth == 0 or not legal_moves:
        return evaluate(state)

    if state.turn == Color.WHITE:
        return max(
            minimax(state.make_move(move), depth - 1)
            for move in legal_moves
        )

    return min(
        minimax(state.make_move(move), depth - 1)
        for move in legal_moves
    )


def find_best_move(
    state: GameState,
    depth: int,
) -> tuple[Move | None, int]:
    """
    Find the best move for the side to move.

    Returns:
        (best_move, score)

    best_move is None if the position is terminal.
    The score is from White's perspective.
    """
    legal_moves = generate_legal_moves(state)

    if not legal_moves:
        return None, evaluate(state)

    best_move = legal_moves[0]

    if state.turn == Color.WHITE:
        best_score = float("-inf")

        for move in legal_moves:
            score = minimax(state.make_move(move), depth - 1)

            if score > best_score:
                best_score = score
                best_move = move

    else:
        best_score = float("inf")

        for move in legal_moves:
            score = minimax(state.make_move(move), depth - 1)

            if score < best_score:
                best_score = score
                best_move = move

    return best_move, int(best_score)