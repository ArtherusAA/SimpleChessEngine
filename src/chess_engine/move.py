from dataclasses import dataclass

from .types import PieceType, Square


@dataclass(frozen=True)
class Move:
    """
    A chess move from one square to another.

    Promotion is set for pawn promotions.
    The special-move flags are used for en passant and castling.
    """

    from_square: Square
    to_square: Square

    promotion: PieceType | None = None
    is_en_passant: bool = False
    is_castling: bool = False

    def is_promotion(self) -> bool:
        """Return whether this move promotes a pawn."""
        return self.promotion is not None