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
            print("Launch the program with the --ai flag to play against a virtual opponent.")
            print("The depth of the AI can be changed in the main.py file at line 24. Default 3")
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


def move_leaves_king_in_check(board, where, to):
    """Tarkistaa, onko siirron tekijä shakissa siirron jälkeen.
    
    Args:
        where: lähtöruutu
        to: tavoiteruutu

    Returns:
        True jos siirto ei johda shakkiin, False jos johtaa.
    """
    board_copy = board.copy()
    target = board_copy.pieces_location[where]
    if target is None:
        return False

    if board_copy.pieces_location[to] is not None:
        captured_piece = board_copy.pieces_location[to]
        bitboard_captured = getattr(board_copy, captured_piece)
        bitboard_captured &= ~(1 << to)
        setattr(board_copy, captured_piece, bitboard_captured)
        board_copy.pieces_location[to] = None

    bitboard = getattr(board_copy, target)
    bitboard &= ~(1 << where)
    bitboard |= (1 << to)
    setattr(board_copy, target, bitboard)
    board_copy.pieces_location[where] = None
    board_copy.pieces_location[to] = target

    board_copy.update_board()
    return not movesets.checked(board_copy)

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
    """Liikkuminen käyttäjän syötteellä."""
    where, to = input_to_coordinates()
    move(board, where, to, silent=False)

def move_ai(board, where, to):
    """Liikkuminen laudan koordinaateilla."""
    return move(board, where, to, silent=True)

def move(board, where, to, silent=False): #pylint: disable=too-many-statements
    """Liikkuminen laudalla, poistaa lähtöruudusta nappulan ja lisää tavoiteruutuun
    
    Args:
        where: lähtöruutu
        to: tavoiteruutu
        silent: Tulostetaanko pelilauta ja huomiot laittomista liikkeistä.
    """
    target = board.pieces_location[where]

    if not check_legality(board, where, to):
        if not silent:
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

    if not silent:
        board.print_gameboard()
        if movesets.checked(board):
            if is_checkmate(board):
                winner = "BLACK" if board.white_turn else "WHITE"
                print("CHECKMATE!", winner, "WINS!")
            else:
                print("CHECK!")

    return True

def check_legality(board, where, to): #pylint: disable=too-many-return-statements
    """Tarkistaa siirron pseudolaillisuuden.
    
    Args:
        where: lähtöruutu
        to: tavoiteruutu

    Returns:
        True jos siirto on pseudolaillinen, False jos ei.
    """
    target = board.pieces_location[where]

    if target is None:
        return False

    if not is_own_piece(board, where):
        return False

    if "knight" in target:
        moves = movesets.knight_moves(board)
    elif "king" in target:
        moves = movesets.king_moves(board)
    elif "pawn" in target:
        moves = movesets.pawn_moves(board)
    elif "rook" in target:
        moves = movesets.rook_moves(board)
    elif "bishop" in target:
        moves = movesets.bishop_moves(board)
    elif "queen" in target:
        moves = movesets.queen_moves(board)
    else:
        return False

    if (where, to) not in moves:
        return False

    return move_leaves_king_in_check(board, where, to)


def get_legal_moves(board):  #pylint: disable=too-many-statements
    """Palauttaa kaikki lailliset siirrot.
    
    Returns:
        legal_moves: Kaikki lailliset siirrot.
    """

    legal_moves = []
    for where in range(64):
        piece = board.pieces_location[where]
        if piece is None or not is_own_piece(board, where):
            continue

        if "knight" in piece:
            moves = movesets.knight_moves(board)
        elif "king" in piece:
            moves = movesets.king_moves(board)
        elif "pawn" in piece:
            moves = movesets.pawn_moves(board)
        elif "rook" in piece:
            moves = movesets.rook_moves(board)
        elif "bishop" in piece:
            moves = movesets.bishop_moves(board)
        elif "queen" in piece:
            moves = movesets.queen_moves(board)
        else:
            continue

        for w, t in moves:
            if w == where and move_leaves_king_in_check(board, w, t):
                legal_moves.append((w, t))
    return legal_moves

def is_checkmate(board):
    """Kertoo, onko pelissä shakkimatti"""
    if not movesets.checked(board):
        return False
    return len(get_legal_moves(board)) == 0
