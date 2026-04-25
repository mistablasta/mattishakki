import moves
from movesets import checked

PIECE_VALUES = {
    'pawn': 100,
    'knight': 300,
    'bishop': 300,
    'rook': 500,
    'queen': 900,
    'king': 0
}

PIECE_LOCATION_VALUES = {
            "pawn" : [0,  0,  0,  0,  0,  0,  0,  0,
                    50, 50, 50, 50, 50, 50, 50, 50,
                    10, 10, 20, 30, 30, 20, 10, 10,
                    5,  5, 10, 25, 25, 10,  5,  5,
                    0,  0,  0, 20, 20,  0,  0,  0,
                    5, -5,-10,  0,  0,-10, -5,  5,
                    5, 10, 10,-20,-20, 10, 10,  5,
                    0,  0,  0,  0,  0,  0,  0,  0],

            "knight" : [-50,-40,-30,-30,-30,-30,-40,-50,
                        -40,-20,  0,  0,  0,  0,-20,-40,
                        -30,  0, 10, 15, 15, 10,  0,-30,
                        -30,  5, 15, 20, 20, 15,  5,-30,
                        -30,  0, 15, 20, 20, 15,  0,-30,
                        -30,  5, 10, 15, 15, 10,  5,-30,
                        -40,-20,  0,  5,  5,  0,-20,-40,
                        -50,-40,-30,-30,-30,-30,-40,-50],

            "bishop" : [-20,-10,-10,-10,-10,-10,-10,-20,
                        -10,  0,  0,  0,  0,  0,  0,-10,
                        -10,  0,  5, 10, 10,  5,  0,-10,
                        -10,  5,  5, 10, 10,  5,  5,-10,
                        -10,  0, 10, 10, 10, 10,  0,-10,
                        -10, 10, 10, 10, 10, 10, 10,-10,
                        -10,  5,  0,  0,  0,  0,  5,-10,
                        -20,-10,-10,-10,-10,-10,-10,-20],

            "rook" : [  0,  0,  0,  0,  0,  0,  0,  0,
                        5, 10, 10, 10, 10, 10, 10,  5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        0,  0,  0,  5,  5,  0,  0,  0],

            "queen" : [-20,-10,-10, -5, -5,-10,-10,-20,
                        -10,  0,  0,  0,  0,  0,  0,-10,
                        -10,  0,  5,  5,  5,  5,  0,-10,
                        -5,  0,  5,  5,  5,  5,  0, -5,
                        0,  0,  5,  5,  5,  5,  0, -5,
                        -10,  5,  5,  5,  5,  5,  0,-10,
                        -10,  0,  5,  0,  0,  0,  0,-10,
                        -20,-10,-10, -5, -5,-10,-10,-20],

            "king" : [-30,-40,-40,-50,-50,-40,-40,-30,
                    -30,-40,-40,-50,-50,-40,-40,-30,
                    -30,-40,-40,-50,-50,-40,-40,-30,
                    -30,-40,-40,-50,-50,-40,-40,-30,
                    -20,-30,-30,-40,-40,-30,-30,-20,
                    -10,-20,-20,-20,-20,-20,-20,-10,
                    20, 20,  0,  0,  0,  0, 20, 20,
                    20, 30, 10,  0,  0, 10, 30, 20]}

def get_piece_value(board, square):
    piece = board.pieces_location[square]

    if piece is None:
        return 0

    color, piece = piece.split("_")
    piecemap = PIECE_LOCATION_VALUES[piece]

    if color == "white":
        return piecemap[square ^ 56] + PIECE_VALUES[piece]
    return -(piecemap[square] + PIECE_VALUES[piece])

def get_board_score(board):
    """Palauttaa nykyisen laudantilan pisteet. Valkoiset positiivisena, mustat negatiivisena."""
    score = 0
    for square in range(64):
        score += get_piece_value(board, square)

    return score

def minimax(board, depth, alpha, beta, maximizing): #pylint: disable=too-many-statements
    """Hyvin yksinkertainen minimax AB karsinnalla.

    Args:
        depth: minimaxin syvyys
        alpha: paras arvo maksimoijalle
        beta: paras arvo minimoijalle
        maximizing: halutaanko painottaa mahdollisimman suuria positiivisia vai negatiivisia lukuja,

    Returns:
        laudan evaluaatio halutulla syvyydellä.
    """
    if checked(board):
        legal_moves = moves.get_legal_moves(board)
        if not legal_moves:
            return -1000000 if maximizing else 1000000
    else:
        if depth == 0:
            return get_board_score(board)

        legal_moves = moves.get_legal_moves(board)
        if not legal_moves:
            return 0

    if depth == 0:
        return get_board_score(board)

    def move_priority(board, move):
        """Järjestää nappulat AB karsintaa varten. Syötävän arvo - syöjän arvo on päämäärittäjä, 
        jos liike ei ole syövä niin liikkuvan nappulan arvoa prioritisoidaan."""
        where, to = move

        target = board.pieces_location[to]
        mover = board.pieces_location[where]

        if target is not None:
            target_piece = target.split("_")[1]
            mover_piece = mover.split("_")[1]
            return (2, PIECE_VALUES[target_piece], -PIECE_VALUES[mover_piece])

        if mover is not None:
            mover_piece = mover.split("_")[1]
            return (1, PIECE_VALUES[mover_piece])

        return (0,0)

    legal_moves.sort(key=lambda m: move_priority(board, m), reverse=True)

    if maximizing:
        max_eval = -float('inf')
        for move in legal_moves:
            board_copy = board.copy()
            moves.move_ai(board_copy, move[0], move[1])
            eval_score = minimax(board_copy, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval

    min_eval = float('inf')
    for move in legal_moves:
        board_copy = board.copy()
        moves.move_ai(board_copy, move[0], move[1])
        eval_score = minimax(board_copy, depth - 1, alpha, beta, True)
        min_eval = min(min_eval, eval_score)
        beta = min(beta, eval_score)
        if beta <= alpha:
            break
    return min_eval

def get_best_move(board, max_depth=4): #pylint: disable=too-many-statements
    """ Kertoo parhaan laillisen siirron nykyiselle pelaajalle minimaxilla.
    
    Returns:
        best_move: paras siirto pelaajalle.
    """
    legal_moves = moves.get_legal_moves(board)
    print("LEGAL MOVES:", legal_moves)
    if not legal_moves:
        return None

    depth = 1
    best_move = None

    for depth in range(1, max_depth + 1):
        if best_move is not None:
            ordered = [best_move] + [move for move in legal_moves if move != best_move]
        else:
            ordered = legal_moves

        ongoing_best = None
        alpha = -float('inf')
        beta = float('inf')

        if board.white_turn:
            best_val = -float('inf')
            for move in ordered:
                board_copy = board.copy()
                moves.move_ai(board_copy, move[0], move[1])
                val = minimax(board_copy, depth - 1, alpha, beta, False)
                if val > best_val:
                    best_val = val
                    ongoing_best = move
                alpha = max(alpha, val)
        else:
            best_val = float('inf')
            for move in ordered:
                board_copy = board.copy()
                moves.move_ai(board_copy, move[0], move[1])
                val = minimax(board_copy, depth - 1, alpha, beta, True)
                if val < best_val:
                    best_val = val
                    ongoing_best = move
                beta = min(beta, val)

        if ongoing_best is not None:
            best_move = ongoing_best
        else:
            break
        depth += 1
    return best_move
