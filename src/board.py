class ChessBoard: # pylint: disable=too-many-instance-attributes
    """Shakkilaudan peruslogiikka"""
    def __init__(self):
        """Alustaa nappuloiden sijainnit bitboardeina, sekä unicodet tulostamista varten."""
        self.white_pawn = 0x000000000000ff00
        self.white_rook = 0x0000000000000081
        self.white_knight = 0x0000000000000042
        self.white_bishop = 0x0000000000000024
        self.white_queen = 0x0000000000000008
        self.white_king = 0x0000000000000010

        self.black_pawn = 0x00ff000000000000
        self.black_rook = 0x8100000000000000
        self.black_knight = 0x4200000000000000
        self.black_bishop = 0x2400000000000000
        self.black_queen = 0x800000000000000
        self.black_king = 0x1000000000000000

        self.white_board = 0
        self.black_board = 0
        self.combined_board = 0


        self.pieces = {
            "♙": "black_pawn", "♖": "black_rook", "♘": "black_knight",
            "♗": "black_bishop", "♕": "black_queen", "♔": "black_king", 
            "♟": "white_pawn", "♜": "white_rook", "♞": "white_knight",
            "♝": "white_bishop", "♛": "white_queen", "♚": "white_king" 
        }


        self.pieces_location = [None] * 64

        self.white_turn = True
        self.update_board()
        self.update_location()

    def copy(self):
        """Palauttaa kopion laudasta"""
        new_board = ChessBoard.__new__(ChessBoard)

        new_board.white_pawn = self.white_pawn
        new_board.white_rook = self.white_rook
        new_board.white_knight = self.white_knight
        new_board.white_bishop = self.white_bishop
        new_board.white_queen = self.white_queen
        new_board.white_king = self.white_king
        new_board.black_pawn = self.black_pawn
        new_board.black_rook = self.black_rook
        new_board.black_knight = self.black_knight
        new_board.black_bishop = self.black_bishop
        new_board.black_queen = self.black_queen
        new_board.black_king = self.black_king
        new_board.white_board = self.white_board
        new_board.black_board = self.black_board
        new_board.combined_board = self.combined_board
        new_board.pieces_location = self.pieces_location.copy()
        new_board.white_turn = self.white_turn
        new_board.pieces = self.pieces

        return new_board

    def update_board(self):
        """Päivittää laudan tilan."""
        self.white_board = (self.white_pawn | self.white_rook | self.white_knight |
                           self.white_bishop | self.white_queen | self.white_king)

        self.black_board = (self.black_pawn | self.black_rook | self.black_knight |
                           self.black_bishop | self.black_queen | self.black_king)

        self.combined_board = self.black_board | self.white_board

    def update_location(self):
        """Päivittää nappuloiden sijainnit liikkumisen seurantaan. Käytetään vain alussa."""
        for square in range(64):
            self.pieces_location[square] = None
            for bitboardhelper in self.pieces.values():
                bitboard = getattr(self, bitboardhelper)
                if bitboard & (1 << square):
                    self.pieces_location[square] = bitboardhelper
                    break

    def print_gameboard(self):
        """Tulostaa pelaajalle shakkilaudan. Pelinäkymä, ei käytetä sisäisessä logiikassa."""
        for rank in range(7, -1, -1): # pylint: disable=too-many-nested-blocks
            line = ""
            for file in range(8):
                square = 1 << (rank * 8 + file)
                for symbol, bitboard in self.pieces.items():
                    if square & getattr(self, bitboard):
                        line += symbol + "    "
                        break
                else:
                    line += ".    "
            print(line)
        if self.white_turn:
            print("PLAYER 1's TURN")
        else:
            print("PLAYER 2's TURN")

    def print_board(self, bitboard):
        """Tulostaa bitboardin. Visualisoidaan muodossa: 1 = nappula, . = tyhjä.
        
        Args:
            bitboard: Kohde bitboard joka tulostetaan.
        """
        for rank in range(7, -1, -1):
            line = ""
            for file in range(8):
                square = 1 << (rank * 8 + file)
                if square & bitboard:
                    line += "1    "
                else:
                    line += ".    "
            print(line)
        print()
