import sys
import time
from board import ChessBoard
from moves import move_manual, is_checkmate
from ai import get_best_move
import moves

def play_human_vs_human():
    board = ChessBoard()
    board.print_gameboard()
    print("Welcome to Chess! Type help for instructions.")
    while True:
        move_manual(board)

def play_human_vs_ai(debug=False):
    board = ChessBoard()
    ai_depth = int(input("Depth of your AI opponent (3 is default): "))
    board.print_gameboard()
    print("Welcome to Chess! Type help for instructions.")

    while True:
        if is_checkmate(board):
            winner = "AI" if board.white_turn else "WHITE"
            print("CHECKMATE!", winner, "WINS!")
            break

        if board.white_turn:
            move_manual(board)
        else:
            print("AI is thinking...")
            if debug:
                start = time.perf_counter()
            best = get_best_move(board, depth=ai_depth)
            if debug:
                stop = time.perf_counter()
                print("Move took", stop-start, "seconds.")

            if not best:
                print("STALEMATE!")
                break

            moves.move_ai(board, *best)

        board.print_gameboard()

def play_ai_vs_ai(debug=False):
    board = ChessBoard()

    white_depth = int(input("Depth of the first AI: "))
    black_depth = int(input("Depth of the second AI: "))

    board.print_gameboard()
    print("Welcome to Chess! Type help for instructions.")


    while True:
        if is_checkmate(board):
            winner = "BLACK" if board.white_turn else "WHITE"
            print("CHECKMATE!", winner, "WINS!")
            break


        print("AI is thinking...")
        if debug:
            start = time.perf_counter()
        best = get_best_move(board, depth=white_depth if board.white_turn else black_depth)
        if debug:
            stop = time.perf_counter()
            print("Move took", stop-start, "seconds.")

        if not best:
            print("STALEMATE!")
            break

        moves.move_ai(board, *best)
        board.print_gameboard()



if __name__ == "__main__":
    if "--debug" in sys.argv:
        toggle = True
    else:
        toggle = False

    if "--ai" in sys.argv:
        play_human_vs_ai(debug=toggle)
    elif "--battle" in sys.argv:
        play_ai_vs_ai(debug=toggle)
    else:
        play_human_vs_human()
