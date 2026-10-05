from dataclasses import dataclass

from .move import Move
from .search import find_best_move
from .state import GameState
from .types import Color


@dataclass(frozen=True, slots=True)
class ChessBot:
    color: Color
    depth: int = 2

    def choose_move(self, state: GameState) -> Move | None:
        """
        Choose the best move for this bot.

        Returns None when the game is over.
        """
        if state.turn != self.color:
            raise ValueError(
                f"It is {state.turn.name.lower()}'s turn, "
                f"but this bot plays {self.color.name.lower()}."
            )

        move, _ = find_best_move(state, self.depth)
        return move

    def play(self, state: GameState) -> tuple[Move | None, GameState]:
        """
        Choose and apply a move.

        Returns the move and resulting state.
        For a terminal position, returns (None, state).
        """
        move = self.choose_move(state)

        if move is None:
            return None, state

        return move, state.make_move(move)