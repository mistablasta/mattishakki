import unittest
import movesets
from board import ChessBoard
from moves import move

class TestMove(unittest.TestCase):
    def setUp(self):
        self.board = ChessBoard()

    def squarehelper(self, move):
        """Helpottaa siirtojen tekemisessä, kääntää esim e2e4 muotoon (12, 28)"""
        ranks = "abcdefgh"
        where = ranks.find(move[0]) + (int(move[1]) -1) * 8
        to =  ranks.find(move[2]) + (int(move[3]) -1) * 8
        return where, to

    def test_move_empty_square(self):
        """Yrittää liikuttaa tyhjän ruudun varattuun ruutuun."""
        where, to = self.squarehelper("e3e2")
        result = move(self.board, where, to)
        self.assertFalse(result)
        self.assertIsNone(self.board.pieces_location[where])
        self.assertIsNotNone(self.board.pieces_location[to])

    def test_move_wrong_turn(self):
        """Liikuttaa väärällä vuorolla valkoisen, sekä mustan hevosen"""
        self.board.white_turn = False
        where, to = self.squarehelper("b1c3")
        result = move(self.board, where, to)
        self.assertFalse(result)
        self.assertEqual(self.board.pieces_location[where], "white_knight")
        self.assertIsNone(self.board.pieces_location[to])

        self.board.white_turn = True
        where, to = self.squarehelper("b8c6")
        result = move(self.board, where, to)
        self.assertFalse(result)
        self.assertEqual(self.board.pieces_location[where], "black_knight")
        self.assertIsNone(self.board.pieces_location[to])

    def test_friendly_capture(self):
        """Yrittää syödä hevosella oman sotilaan"""
        where, to = self.squarehelper("b1d2")
        result = move(self.board, where, to)
        self.assertFalse(result)
        self.assertEqual(self.board.pieces_location[where], "white_knight")
        self.assertEqual(self.board.pieces_location[to], "white_pawn")

    def test_pawn_move_and_capture(self):
        """Liikuttaa valkoisen, sekä mustan sotilaan kaksi askelta. Yrittää uudestaan, sen jälkeen syö mustan sotilaan valkoisella."""
        where, to = self.squarehelper("e2e4")
        result = move(self.board, where, to)
        self.assertTrue(result)
        self.assertEqual(self.board.pieces_location[to], "white_pawn")

        where, to = self.squarehelper("d7d5")
        result = move(self.board, where, to)
        self.assertTrue(result)
        self.assertEqual(self.board.pieces_location[to], "black_pawn")

        where, to = self.squarehelper("d4d6")
        result = move(self.board, where, to)
        self.assertFalse(result)

        where, to = self.squarehelper("d5d3")
        result = move(self.board, where, to)
        self.assertFalse(result)

        where, to = self.squarehelper("e4d5")
        result = move(self.board, where, to)
        self.assertTrue(result)
        self.assertEqual(self.board.pieces_location[to], "white_pawn")

    def test_fools_mate(self):
        """Testaa shakin mahdollisimman nopeasti kuningattaren avulla."""
        where, to = self.squarehelper("f2f3")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("e7e5")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("g2g4")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("d8h4")
        result = move(self.board, where, to)
        self.assertTrue(result)
        self.assertTrue(movesets.checked(self.board))
