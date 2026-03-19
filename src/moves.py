import movesets

def is_own_piece(board, square):
    """Kertoo, onko ruudussa olevan nappulan väri sama kuin vuorossa olevan pelaajan väri.
        
    Args:
        square: Ruutu, jota tutkitaan.

    Returns:
        True, jos ruudussa olevan nappulan väri on oma väri, muuten False.
    """
    square = 1 << square
    if board.white_turn:
        return bool(square & board.white_board)
    return bool(square & board.black_board)

def input_to_coordinates():
    """Kääntää käyttäjän syötteen ruutuihin.

    Returns:
        where: lähtöruutu
        to: tavoiteruutu
    """
    ranks = "abcdefgh"
    error_message = "Incorrect command."
    while True:
        moveinput = input("Make your move: ")
        if moveinput.lower() == "help":
            print("Moving a piece example command: e2e4")
            continue
        if len(moveinput) != 4:
            print(error_message)
            continue
        if moveinput[0] not in ranks or moveinput[2] not in ranks:
            print(error_message)
            continue
        if not moveinput[1].isdigit() or not moveinput[3].isdigit():
            print(error_message)
            continue
        where = ranks.find(moveinput[0]) + (int(moveinput[1]) -1) * 8
        to = ranks.find(moveinput[2]) + (int(moveinput[3]) -1) * 8
        return where, to

def capture(board, to):
    """Poistaa kohdesijainnista nappulan, tehdään ennen siirtoa.
    
    Args:
        square: Ruutu, josta poistetaan
    """
    target = board.pieces_location[to]
    bitboard = getattr(board, target)
    bitboard &= ~ (1 << to)
    setattr(board, target, bitboard)
    board.pieces_location[to] = None

def move_manual(board):
    """Liikkuminen käyttäjän syötteellä"""
    where, to = input_to_coordinates()
    move(board, where, to)

def move(board, where, to):
    """Liikkuminen laudalla, poistaa lähtöruudusta nappulan ja lisää tavoiteruutuun
    
    Args:
        where: lähtöruutu
        to: tavoiteruutu
    """
    target = board.pieces_location[where]

    if not check_legality(board, where, to):
        print("Illegal move.")
        return False

    if board.pieces_location[to] is not None:
        capture(board, to)

    bitboard = getattr(board, target)
    bitboard &= ~ (1 << where)
    bitboard |= (1 << to)
    setattr(board, target, bitboard)

    board.pieces_location[where] = None
    board.pieces_location[to] = target

    board.white_turn = not board.white_turn

    board.update_board()
    board.print_gameboard()

    return True

def check_legality(board, where, to):
    """Tarkistaa siirron laillisuuden.
    
    Args:
        where: lähtöruutu
        to: tavoiteruutu
    """
    target = board.pieces_location[where]
    target_bitboard = 1 << where

    if board.white_turn:
        friendly_bitboard = board.white_board
        opponent_bitboard = board.black_board
    else:
        friendly_bitboard = board.black_board
        opponent_bitboard = board.white_board

    if target is None:
        return False

    if not is_own_piece(board, where):
        return False

    if "knight" in target:
        moves = movesets.knight_moves(target_bitboard, friendly_bitboard)
        return bool(moves & (1 << to))

    if "king" in target:
        moves = movesets.king_moves(target_bitboard, friendly_bitboard)
        return bool(moves & (1 << to))

    if "pawn" in target:
        moves = movesets.pawn_moves(target_bitboard, friendly_bitboard,
                                    opponent_bitboard, board.white_turn)
        return bool(moves & (1 << to))
    return False
