class ChessBoard:
    """Shakkilaudan peruslogiikka"""
    def __init__(self):
        """Alustaa nappuloiden sijainnit bitboardeina, sekä unicodet tulostamista varten."""
        self.WhitePawn = 0x000000000000ff00
        self.WhiteRook = 0x0000000000000081
        self.WhiteKnight = 0x0000000000000042
        self.WhiteBishop = 0x0000000000000024
        self.WhiteQueen = 0x0000000000000008
        self.WhiteKing = 0x0000000000000010

        self.BlackPawn = 0xff000000000000
        self.BlackRook = 0x8100000000000000
        self.BlackKnight = 0x4200000000000000
        self.BlackBishop = 0x2400000000000000
        self.BlackQueen = 0x800000000000000
        self.BlackKing = 0x1000000000000000

        self.WhiteBoard = self.WhitePawn | self.WhiteRook | self.WhiteKnight | self.WhiteBishop | self.WhiteQueen | self.WhiteKing
        self.BlackBoard = self.BlackPawn | self.BlackRook | self.BlackKnight | self.BlackBishop | self.BlackQueen | self.BlackKing
        self.CombinedBoard = self.BlackBoard | self.WhiteBoard

        self.pieces = {
            "♙": "WhitePawn", "♖": "WhiteRook", "♘": "WhiteKnight", "♗": "WhiteBishop", "♕": "WhiteQueen", "♔": "WhiteKing", 
            "♟": "BlackPawn", "♜": "BlackRook", "♞": "BlackKnight", "♝": "BlackBishop", "♛": "BlackQueen", "♚": "BlackKing" 
        }

        self.WhiteTurn = True

    def update_board(self):
        """Päivittää laudan tilan."""
        self.WhiteBoard = self.WhitePawn | self.WhiteRook | self.WhiteKnight | self.WhiteBishop | self.WhiteQueen | self.WhiteKing
        self.BlackBoard = self.BlackPawn | self.BlackRook | self.BlackKnight | self.BlackBishop | self.BlackQueen | self.BlackKing
        self.CombinedBoard = self.BlackBoard | self.WhiteBoard
        
    def print_gameboard(self):
        """Tulostaa pelaajalle shakkilaudan. Pelinäkymä, ei käytetä sisäisessä logiikassa."""
        for rank in range(7, -1, -1):
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
        if self.WhiteTurn:
            print("Valkoisen vuoro.")
        else:
            print("Mustan vuoro.")

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
