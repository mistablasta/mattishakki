import sys
from board import ChessBoard
from moves import move_manual, is_checkmate
from ai import get_best_move
import moves

def play_human_vs_human():
    board = ChessBoard()
    board.print_gameboard()
    print("Welcome to Chess! Type help for instructions.")
    print("--------------------")
    while True:
        move_manual(board)

def play_human_vs_ai(): #pylint: disable=too-many-statements
    board = ChessBoard()
    board.print_gameboard()
    print("Welcome to Chess! You are White. Type help for instructions.")
    print("--------------------")

    while True: #pylint: disable=too-many-nested-blocks
        if board.white_turn:
            move_manual(board)
        else:
            print("AI is thinking...")
            best = get_best_move(board, depth=3)
            if best:
                moves.move_ai(board, *best)
                board.print_gameboard()
                if moves.movesets.checked(board):
                    if is_checkmate(board):
                        print("CHECKMATE! AI WINS!")
                    else:
                        print("CHECK!")
            else:
                if is_checkmate(board):
                    print("CHECKMATE! WHITE WINS!")
                else:
                    print("STALEMATE!")
                break

        if is_checkmate(board):
            winner = "AI" if board.white_turn else "WHITE"
            print("CHECKMATE! " + winner + " WINS!")
            break

# Suorita ohjelma --ai flagilla pelataaksesi tekoälyä vastaan.
if __name__ == "__main__":
    if "--ai" in sys.argv:
        play_human_vs_ai()
    else:
        play_human_vs_human()
