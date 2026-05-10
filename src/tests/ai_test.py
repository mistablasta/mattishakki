import unittest
from board import ChessBoard
from moves import move
from ai import get_best_move, minimax


class TestMove(unittest.TestCase):
    def setUp(self):
        self.board = ChessBoard()

    def test_capture_board_evaluation(self):
        "Testaa, löytääkö algoritmin ilmaisen syönnin ja varmistaa sen vaikutuksen laudan evaluaatioon."

        for attr in ['white_pawn', 'white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king',
                    'black_pawn', 'black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king']:
            setattr(self.board, attr, 0)

        self.board.white_king = 1 << 0
        self.board.white_knight = 1 << 21
        self.board.black_king = 1 << 56
        self.board.black_pawn = 1 << 36

        self.board.white_turn = True
        self.board.update_board()
        self.board.update_location()

        eval_expected = 190
        eval = minimax(self.board, 0, -float("inf"), float("inf"), False)
        self.assertEqual(eval, eval_expected)
        
        ai_move = get_best_move(self.board, max_depth=4)
        expected = (21, 36)
        self.assertEqual(ai_move, expected)
        where, to = ai_move
        move(self.board, where, to)

        eval_expected = 320
        eval = minimax(self.board, 0, -float("inf"), float("inf"), False)
        self.assertEqual(eval, eval_expected)

    def test_ai_defends_mate(self):
        "Testaa, puolustaako algoritmi helppoa shakkimattia vastaan."

        for attr in ['white_pawn', 'white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king',
                    'black_pawn', 'black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king']:
            setattr(self.board, attr, 0)

        self.board.white_king = 1 << 7
        self.board.white_pawn = 1 << 15
        self.board.white_pawn |= 1 << 14
        self.board.white_pawn |= 1 << 13
        self.board.white_rook = 1 << 44
        self.board.black_king = 1 << 56
        self.board.black_knight = 1 << 57
        self.board.black_rook = 1 << 8

        self.board.white_turn = True
        self.board.update_board()
        self.board.update_location()

        ai_move = get_best_move(self.board, max_depth=4)
        expected = (44, 4)
        self.assertEqual(ai_move, expected)
        
    def test_ai_uses_promotion(self):
        "Testaa, käyttääkö algoritmi ylentämistä ja varmistaa, että se vaikuttaa evaluaatioon."

        for attr in ['white_pawn', 'white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king',
                    'black_pawn', 'black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king']:
            setattr(self.board, attr, 0)

        self.board.white_king = 1 << 3
        self.board.white_pawn = 1 << 55
        self.board.black_king = 1 << 58

        self.board.white_turn = True
        self.board.update_board()
        self.board.update_location()

        eval_expected = 140
        eval = minimax(self.board, 0, -float("inf"), float("inf"), False)
        self.assertEqual(eval, eval_expected)

        ai_move = get_best_move(self.board, max_depth=4)
        expected = (55, 63)
        self.assertEqual(ai_move, expected)
        where, to = ai_move
        move(self.board, where, to)

        eval_expected = 870
        eval = minimax(self.board, 0, -float("inf"), float("inf"), False)
        self.assertEqual(eval, eval_expected)


    def test_ai_finds_mate_in_two(self):
        """Testaa, löytääkö algoritmi pakotetun shakin kahdella siirrolla ja varmistaa evaluaation."""

        for attr in ['white_pawn', 'white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king',
                    'black_pawn', 'black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king']:
            setattr(self.board, attr, 0)

        self.board.white_king = 1 << 6
        self.board.white_rook = 1 << 45
        self.board.white_rook |= 1 << 38
        self.board.black_king = 1 << 31

        self.board.white_turn = True
        self.board.update_board()
        self.board.update_location()

        expected = (45, 46)
        ai_move = get_best_move(self.board, max_depth=4)
        self.assertEqual(ai_move, expected)
        where, to = ai_move
        move(self.board, where, to)

        move(self.board, 31, 23)

        expected = (46, 47), (38,39)
        ai_move = get_best_move(self.board, max_depth=4)
        self.assertIn(ai_move, expected)
        where, to = ai_move
        move(self.board, where, to)

        eval_expected = 1000000
        eval = minimax(self.board, 0, -float("inf"), float("inf"), False)
        self.assertEqual(eval, eval_expected)


    def test_ai_finds_mate_in_three(self):
        """Testaa, löytääkö algoritmi pakotetun shakin kolmella siirrolla ja varmistaa evaluaation."""
        for attr in ['white_pawn', 'white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king',
                    'black_pawn', 'black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king']:
            setattr(self.board, attr, 0)

        self.board.black_king = 1 << 56
        self.board.white_king = 1 << 26
        self.board.black_bishop = 1 << 2
        self.board.white_rook = 1 << 54
        self.board.white_rook |= 1 << 46
        self.board.black_pawn = 1 << 47

        self.board.white_turn = True
        self.board.update_board()
        self.board.update_location()

        expected = (54, 50)
        ai_move = get_best_move(self.board, max_depth=5)
        self.assertEqual(ai_move, expected)
        where, to = ai_move
        move(self.board, where, to)

        ai_move = get_best_move(self.board, max_depth=3)
        where, to = ai_move
        move(self.board, where, to)

        expected = (50, 52)
        ai_move = get_best_move(self.board, max_depth=5)
        self.assertEqual(ai_move, expected)
        where, to = ai_move
        move(self.board, where, to)

        ai_move = get_best_move(self.board, max_depth=3)
        where, to = ai_move
        move(self.board, where, to)

        expected = (46, 62)
        ai_move = get_best_move(self.board, max_depth=5)
        self.assertEqual(ai_move, expected)
        where, to = ai_move
        move(self.board, where, to)

        eval_expected = 1000000
        eval = minimax(self.board, 0, -float("inf"), float("inf"), False)
        self.assertEqual(eval, eval_expected)
