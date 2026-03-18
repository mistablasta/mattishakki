def is_own_piece(board, square):
    """Kertoo, onko nappulan vääri sama kuin vuorossa olevan pelaajan väri.
        
    Args:
        square: Ruutu, jota tutkitaan.

    Returns:
        True, jos ruudussa olevan nappulan väri on oma väri, muuten False.
    """
    if board.WhiteTurn:
        return bool(square & board.WhiteBoard)
    else:
        return bool(square & board.BlackBoard)

def move(board):
    """Nappuloiden liikkumislogiikka"""
    ranks = "abcdefgh"
    move = input("Tee siirto (esim: e2e4): ")
    where = 1 << (ranks.find(move[0]) + (int(move[1]) -1) * 8)
    to = 1 << (ranks.find(move[2]) + (int(move[3]) -1) * 8)

    for _, bitboardhelper in board.pieces.items():
        bitboard = getattr(board, bitboardhelper)
        if where & bitboard and is_own_piece(board, where):
            if is_own_piece(board, to):
                print("Siirsit oman nappulasi päälle ja melkein rikoit pelin.")
                return
                    
            bitboard = bitboard & ~where
            bitboard = bitboard | to
            setattr(board, bitboardhelper, bitboard)
            board.WhiteTurn = not board.WhiteTurn
            break
    else:
        print("Sääntöjenvastainen siirto.")
        return

    board.update_board()
    print("debug")#debugggggg
    board.print_board(board.WhiteBoard)#debugggggg
    board.print_board(board.BlackBoard)#debugggggg
    board.print_gameboard()
