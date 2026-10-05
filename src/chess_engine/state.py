from dataclasses import dataclass

from .bitboard import FULL_BOARD
from .move import Move
from .types import Color, PieceType, Square


# Castling rights are represented as four independent bits.
WHITE_KINGSIDE = 1 << 0
WHITE_QUEENSIDE = 1 << 1
BLACK_KINGSIDE = 1 << 2
BLACK_QUEENSIDE = 1 << 3


@dataclass(frozen=True)
class GameState:
    white_pawns: int
    white_knights: int
    white_bishops: int
    white_rooks: int
    white_queens: int
    white_king: int

    black_pawns: int
    black_knights: int
    black_bishops: int
    black_rooks: int
    black_queens: int
    black_king: int

    turn: Color
    castling_rights: int
    en_passant_square: Square | None = None

    @classmethod
    def initial(cls) -> "GameState":
        """Create the standard initial chess position."""
        return cls(
            white_pawns=0x000000000000FF00,
            white_knights=0x0000000000000042,
            white_bishops=0x0000000000000024,
            white_rooks=0x0000000000000081,
            white_queens=0x0000000000000008,
            white_king=0x0000000000000010,
            black_pawns=0x00FF000000000000,
            black_knights=0x4200000000000000,
            black_bishops=0x2400000000000000,
            black_rooks=0x8100000000000000,
            black_queens=0x0800000000000000,
            black_king=0x1000000000000000,
            turn=Color.WHITE,
            castling_rights=(
                WHITE_KINGSIDE
                | WHITE_QUEENSIDE
                | BLACK_KINGSIDE
                | BLACK_QUEENSIDE
            ),
        )

    def white_pieces(self) -> int:
        """Return a bitboard containing all white pieces."""
        return (
            self.white_pawns
            | self.white_knights
            | self.white_bishops
            | self.white_rooks
            | self.white_queens
            | self.white_king
        )

    def black_pieces(self) -> int:
        """Return a bitboard containing all black pieces."""
        return (
            self.black_pawns
            | self.black_knights
            | self.black_bishops
            | self.black_queens
            | self.black_rooks
            | self.black_king
        )

    def occupied(self) -> int:
        """Return a bitboard containing all occupied squares."""
        return self.white_pieces() | self.black_pieces()

    def empty(self) -> int:
        """Return a bitboard containing all empty squares."""
        return FULL_BOARD & ~self.occupied()

    def has_piece(
        self,
        color: Color,
        piece_type: PieceType,
        square: Square,
    ) -> bool:
        """Return whether the specified piece occupies the specified square."""
        bit = 1 << square

        return bool(self._piece_bitboard(color, piece_type) & bit)

    def piece_at(
        self,
        square: Square,
    ) -> tuple[Color, PieceType] | None:
        """Return the piece occupying a square, or None if it is empty."""
        bit = 1 << square

        if self.white_pieces() & bit:
            color = Color.WHITE
        elif self.black_pieces() & bit:
            color = Color.BLACK
        else:
            return None

        for piece_type in PieceType:
            if self._piece_bitboard(color, piece_type) & bit:
                return color, piece_type

        raise RuntimeError("Inconsistent GameState: occupied square has no piece.")

    def _piece_bitboard(
        self,
        color: Color,
        piece_type: PieceType,
    ) -> int:
        """Return the bitboard for a specific color and piece type."""
        if color == Color.WHITE:
            bitboards = (
                self.white_pawns,
                self.white_knights,
                self.white_bishops,
                self.white_rooks,
                self.white_queens,
                self.white_king,
            )
        else:
            bitboards = (
                self.black_pawns,
                self.black_knights,
                self.black_bishops,
                self.black_rooks,
                self.black_queens,
                self.black_king,
            )

        return bitboards[piece_type]

    def make_move(self, move: Move) -> "GameState":
        piece = self.piece_at(move.from_square)

        if piece is None:
            raise ValueError(f"No piece on {move.from_square}.")

        color, piece_type = piece

        if color != self.turn:
            raise ValueError(
                f"Cannot move {color.name} piece when it is "
                f"{self.turn.name}'s turn."
            )

        if move.is_castling:
            return self._make_castling_move(move)

        if move.is_en_passant and piece_type != PieceType.PAWN:
            raise ValueError("Only a pawn can make an en-passant move.")

        if move.is_en_passant:
            if self.en_passant_square != move.to_square:
                raise ValueError("Invalid en-passant target square.")

        if move.promotion is not None:
            if piece_type != PieceType.PAWN:
                raise ValueError("Only a pawn can promote.")

            if move.promotion in (PieceType.PAWN, PieceType.KING):
                raise ValueError("Invalid promotion piece.")

        bitboards = {
            (Color.WHITE, PieceType.PAWN): self.white_pawns,
            (Color.WHITE, PieceType.KNIGHT): self.white_knights,
            (Color.WHITE, PieceType.BISHOP): self.white_bishops,
            (Color.WHITE, PieceType.ROOK): self.white_rooks,
            (Color.WHITE, PieceType.QUEEN): self.white_queens,
            (Color.WHITE, PieceType.KING): self.white_king,
            (Color.BLACK, PieceType.PAWN): self.black_pawns,
            (Color.BLACK, PieceType.KNIGHT): self.black_knights,
            (Color.BLACK, PieceType.BISHOP): self.black_bishops,
            (Color.BLACK, PieceType.ROOK): self.black_rooks,
            (Color.BLACK, PieceType.QUEEN): self.black_queens,
            (Color.BLACK, PieceType.KING): self.black_king,
        }

        from_bit = 1 << move.from_square
        to_bit = 1 << move.to_square

        bitboards[(color, piece_type)] &= ~from_bit

        captured_square: Square | None = None

        if move.is_en_passant:
            direction = -1 if color == Color.WHITE else 1
            captured_square = Square(move.to_square + direction * 8)

            captured_piece = self.piece_at(captured_square)

            if captured_piece != (color.opposite, PieceType.PAWN):
                raise ValueError(
                    "En-passant target does not contain an opponent pawn."
                )
        else:
            captured_piece = self.piece_at(move.to_square)

            if captured_piece is not None:
                captured_color, captured_type = captured_piece

                if captured_color == color:
                    raise ValueError("Cannot capture own piece.")

                captured_square = move.to_square

        if captured_square is not None:
            captured_color, captured_type = self.piece_at(
                captured_square
            )
            bitboards[(captured_color, captured_type)] &= ~(
                    1 << captured_square
            )

        destination_type = move.promotion or piece_type
        bitboards[(color, destination_type)] |= to_bit

        en_passant_square = None

        if piece_type == PieceType.PAWN:
            from_rank = move.from_square // 8
            to_rank = move.to_square // 8

            if abs(to_rank - from_rank) == 2:
                middle_rank = (from_rank + to_rank) // 2
                file = move.from_square % 8
                en_passant_square = Square(
                    middle_rank * 8 + file
                )

        castling_rights = self._castling_rights_after_move(
            move,
            color,
            piece_type,
            captured_square,
        )

        return GameState(
            white_pawns=bitboards[(Color.WHITE, PieceType.PAWN)],
            white_knights=bitboards[(Color.WHITE, PieceType.KNIGHT)],
            white_bishops=bitboards[(Color.WHITE, PieceType.BISHOP)],
            white_rooks=bitboards[(Color.WHITE, PieceType.ROOK)],
            white_queens=bitboards[(Color.WHITE, PieceType.QUEEN)],
            white_king=bitboards[(Color.WHITE, PieceType.KING)],
            black_pawns=bitboards[(Color.BLACK, PieceType.PAWN)],
            black_knights=bitboards[(Color.BLACK, PieceType.KNIGHT)],
            black_bishops=bitboards[(Color.BLACK, PieceType.BISHOP)],
            black_rooks=bitboards[(Color.BLACK, PieceType.ROOK)],
            black_queens=bitboards[(Color.BLACK, PieceType.QUEEN)],
            black_king=bitboards[(Color.BLACK, PieceType.KING)],
            turn=color.opposite,
            castling_rights=castling_rights,
            en_passant_square=en_passant_square,
        )

    def _make_castling_move(self, move: Move) -> "GameState":
        if self.turn == Color.WHITE:
            if move.from_square != Square.E1:
                raise ValueError("White castling must start from E1.")

            if move.to_square == Square.G1:
                right = WHITE_KINGSIDE
                rook_from = Square.H1
                rook_to = Square.F1
            elif move.to_square == Square.C1:
                right = WHITE_QUEENSIDE
                rook_from = Square.A1
                rook_to = Square.D1
            else:
                raise ValueError("Invalid white castling destination.")
        else:
            if move.from_square != Square.E8:
                raise ValueError("Black castling must start from E8.")

            if move.to_square == Square.G8:
                right = BLACK_KINGSIDE
                rook_from = Square.H8
                rook_to = Square.F8
            elif move.to_square == Square.C8:
                right = BLACK_QUEENSIDE
                rook_from = Square.A8
                rook_to = Square.D8
            else:
                raise ValueError("Invalid black castling destination.")

        if not self.castling_rights & right:
            raise ValueError("Castling right is not available.")

        if self.piece_at(move.from_square) != (
                self.turn,
                PieceType.KING,
        ):
            raise ValueError("King is not on the expected square.")

        if self.piece_at(rook_from) != (
                self.turn,
                PieceType.ROOK,
        ):
            raise ValueError("Rook is not on the expected square.")

        between_squares = {
            (Square.E1, Square.G1): (Square.F1, Square.G1),
            (Square.E1, Square.C1): (Square.B1, Square.C1, Square.D1),
            (Square.E8, Square.G8): (Square.F8, Square.G8),
            (Square.E8, Square.C8): (Square.B8, Square.C8, Square.D8),
        }[(move.from_square, move.to_square)]

        for square in between_squares:
            if self.piece_at(square) is not None:
                raise ValueError(
                    "Squares between king and rook must be empty."
                )

        king_from_bit = 1 << move.from_square
        king_to_bit = 1 << move.to_square
        rook_from_bit = 1 << rook_from
        rook_to_bit = 1 << rook_to

        if self.turn == Color.WHITE:
            return GameState(
                white_pawns=self.white_pawns,
                white_knights=self.white_knights,
                white_bishops=self.white_bishops,
                white_rooks=(
                        (self.white_rooks & ~rook_from_bit)
                        | rook_to_bit
                ),
                white_queens=self.white_queens,
                white_king=(
                        (self.white_king & ~king_from_bit)
                        | king_to_bit
                ),
                black_pawns=self.black_pawns,
                black_knights=self.black_knights,
                black_bishops=self.black_bishops,
                black_rooks=self.black_rooks,
                black_queens=self.black_queens,
                black_king=self.black_king,
                turn=Color.BLACK,
                castling_rights=(
                        self.castling_rights
                        & ~(WHITE_KINGSIDE | WHITE_QUEENSIDE)
                ),
                en_passant_square=None,
            )

        return GameState(
            white_pawns=self.white_pawns,
            white_knights=self.white_knights,
            white_bishops=self.white_bishops,
            white_rooks=self.white_rooks,
            white_queens=self.white_queens,
            white_king=self.white_king,
            black_pawns=self.black_pawns,
            black_knights=self.black_knights,
            black_bishops=self.black_bishops,
            black_rooks=(
                    (self.black_rooks & ~rook_from_bit)
                    | rook_to_bit
            ),
            black_queens=self.black_queens,
            black_king=(
                    (self.black_king & ~king_from_bit)
                    | king_to_bit
            ),
            turn=Color.WHITE,
            castling_rights=(
                    self.castling_rights
                    & ~(BLACK_KINGSIDE | BLACK_QUEENSIDE)
            ),
            en_passant_square=None,
        )

    def _castling_rights_after_move(
            state: "GameState",
            move: Move,
            moving_color: Color,
            moving_piece: PieceType,
            captured_square: Square | None,
    ) -> int:
        rights = state.castling_rights

        # Moving the king permanently removes both castling rights.
        if moving_piece == PieceType.KING:
            if moving_color == Color.WHITE:
                rights &= ~(WHITE_KINGSIDE | WHITE_QUEENSIDE)
            else:
                rights &= ~(BLACK_KINGSIDE | BLACK_QUEENSIDE)

        # Moving a rook permanently removes the right associated
        # with that rook's original square.
        elif moving_piece == PieceType.ROOK:
            if move.from_square == Square.H1:
                rights &= ~WHITE_KINGSIDE
            elif move.from_square == Square.A1:
                rights &= ~WHITE_QUEENSIDE
            elif move.from_square == Square.H8:
                rights &= ~BLACK_KINGSIDE
            elif move.from_square == Square.A8:
                rights &= ~BLACK_QUEENSIDE

        # Capturing a rook on its original square permanently removes
        # the corresponding castling right.
        if captured_square == Square.H1:
            rights &= ~WHITE_KINGSIDE
        elif captured_square == Square.A1:
            rights &= ~WHITE_QUEENSIDE
        elif captured_square == Square.H8:
            rights &= ~BLACK_KINGSIDE
        elif captured_square == Square.A8:
            rights &= ~BLACK_QUEENSIDE

        return rights
