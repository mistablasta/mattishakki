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
            "♙": self.WhitePawn, "♖": self.WhiteRook, "♘": self.WhiteKnight, "♗": self.WhiteBishop, "♕": self.WhiteQueen, "♔": self.WhiteKing, 
            "♟": self.BlackPawn, "♜": self.BlackRook, "♞": self.BlackKnight, "♝": self.BlackBishop, "♛": self.BlackQueen, "♚": self.BlackKing, 
        }

    def print_gameboard(self):
        """Tulostaa pelaajalle shakkilaudan. Pelinäkymä, ei käytetä sisäisessä logiikassa."""
        for rank in range(7, -1, -1):
            line = ""
            for file in range(8):
                square = 1 << (rank * 8 + file)                     # Bit-shiftaa 1 jokaiseen bittiin vuorotellen 8x8 ruudukon tavoin...
                for symbol, bitboard in self.pieces.items():        
                    if square & bitboard:                           # ja vertaa nappulatyyppisiin bitboardeihin.
                        line += symbol + "    "
                        break
                else:
                    line += ".    "
            print(line)
        print()

    def move(self):
        """Nappuloiden liikkumislogiikka"""
        ranks = "abcdefgh"
        move = input("Tee siirto (esim: e2e4): ")
        where = ranks.find(move[0]) + (int(move[1]) -1) * 8
        to = ranks.find(move[2]) + (int(move[3]) -1) * 8
        print("Liikuit ruudusta", where, "ruutuun", to)

board = ChessBoard()
board.print_gameboard()
board.move()

