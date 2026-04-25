import unittest
from board import ChessBoard
from moves import move
from ai import get_best_move


class TestMove(unittest.TestCase):
    def setUp(self):
        self.board = ChessBoard()

    def test_ai_finds_mate_in_two(self):
        """Testaa, löytääkö algoritmi pakotetun shakin kahdella siirrolla."""

        for attr in ['white_pawn', 'white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king',
                    'black_pawn', 'black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king']:
            setattr(self.board, attr, 0)

        self.board.white_king = 1 << 0
        self.board.white_rook = 1 << 3
        self.board.white_rook |= 1 << 11
        self.board.black_king = 1 << 60

        self.board.white_turn = True
        self.board.update_board()
        self.board.update_location()

        expected = (11, 59)
        ai_move = get_best_move(self.board, max_depth=4)
        self.assertEqual(ai_move, expected)
        where, to = ai_move

        move(self.board, where, to)
        move(self.board, 60, 52)

        expected = (3, 51)
        ai_move = get_best_move(self.board, max_depth=4)
        self.assertEqual(ai_move, expected)

    def test_ai_finds_mate_in_three(self):
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

