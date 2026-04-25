import unittest
from board import ChessBoard
from moves import move
from ai import get_best_move, get_board_score
from moves import is_checkmate

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

    def test_all_pieces_move_once(self):
        """Liikuttaa kaikkia nappuloita ainakin kerran"""
        where, to = self.squarehelper("e2e4")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("e7e5")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("g1f3")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("b8c6")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("f1c4")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("f8c5")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("d1e2")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("d8e7")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("a2a4")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("a7a5")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("a1a3")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("a8a6")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("e1f1")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("e8f8")
        result = move(self.board, where, to)
        self.assertTrue(result)

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
        """Testaa shakkimatin mahdollisimman nopeasti kuningattaren avulla."""
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
        self.assertTrue(is_checkmate(self.board))

    def test_ai_notices_fools_mate(self):
        where, to = self.squarehelper("f2f3")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("e7e5")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("g2g4")
        result = move(self.board, where, to)
        self.assertTrue(result)

        ai_move = get_best_move(self.board)
        expected = self.squarehelper("d8h4")
        self.assertEqual(ai_move, expected)

    def test_no_checkmate_at_start(self):
        """Tarkistaa, ettei ole shakkimattia alkutilanteessa"""
        self.assertFalse(is_checkmate(self.board))

    def test_initial_board_score(self):
        """Testaa laudan pisteytyksen alkutilanteessa."""
        score = get_board_score(self.board)
        self.assertEqual(score, 0)

    def test_king_cannot_move_into_check(self):
        """Varmistaa, että kuningas ei voi liikkua shakkiin."""
        where, to = self.squarehelper("e2e4")
        result = move(self.board, where, to)
        self.assertTrue(result)
        self.board.white_turn = True

        where, to = self.squarehelper("e1e2")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("c7c6")
        result = move(self.board, where, to)
        self.assertTrue(result)
        self.board.white_turn = False

        where, to = self.squarehelper("d8b6")
        result = move(self.board, where, to)
        self.assertTrue(result)

        where, to = self.squarehelper("e2e3")
        result = move(self.board, where, to)
        self.assertFalse(result)
