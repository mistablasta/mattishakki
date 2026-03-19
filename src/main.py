from board import ChessBoard
from moves import move_manual

board = ChessBoard()
board.print_gameboard()
print("Welcome to Chess! Type help for instructions.\n--------------------")
while True:
    move_manual(board)
