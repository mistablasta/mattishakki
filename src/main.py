from board import ChessBoard
from moves import move

board = ChessBoard()
board.print_gameboard()
print("Tervetuloa Shakkiin!\n--------------------")
for i in range(100):
    move(board)