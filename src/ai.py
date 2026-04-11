import moves

PIECE_VALUES = {
    'pawn': 1,
    'knight': 3,
    'bishop': 3,
    'rook': 5,
    'queen': 9,
    'king': 0
}

def get_board_score(board):
    """Palauttaa nykyisen laudantilan pisteet. Valkoiset positiivisena, mustat negatiivisena."""
    score = 0
    for color, score_type in [('white', 1), ('black', -1)]:
        for piece, value in PIECE_VALUES.items():
            bitboard = getattr(board, color + '_' + piece)
            count = bin(bitboard).count('1')
            score += score_type * count * value
    return score

def minimax(board, depth, maximizing):
    """Hyvin yksinkertainen minimax ilman AB-karsintaa

    Args:
        depth: minimaxin syvyys
        maximizing: halutaanko painottaa mahdollisimman suuria positiivisia vai negatiivisia lukuja,

    Returns:
        laudan evaluaatio halutulla syvyydellä.
    """
    if depth == 0 or moves.is_checkmate(board):
        return get_board_score(board)

    legal_moves = moves.get_legal_moves(board)
    if not legal_moves:
        return 0

    if maximizing:
        max_eval = -float('inf')
        for move in legal_moves:
            board_copy = board.copy()
            moves.move_ai(board_copy, move[0], move[1])
            eval_score = minimax(board_copy, depth - 1, False)
            max_eval = max(max_eval, eval_score)
        return max_eval

    min_eval = float('inf')
    for move in legal_moves:
        board_copy = board.copy()
        moves.move_ai(board_copy, move[0], move[1])
        eval_score = minimax(board_copy, depth - 1, True)
        min_eval = min(min_eval, eval_score)
    return min_eval

def get_best_move(board, depth=5):
    """ Kertoo parhaan laillisen siirron nykyiselle pelaajalle minimaxilla.
    
    Returns:
        best_move: paras siirto pelaajalle.
    """
    legal_moves = moves.get_legal_moves(board)
    if not legal_moves:
        return None

    best_move = None
    if board.white_turn:
        best_val = -float('inf')
        for move in legal_moves:
            board_copy = board.copy()
            moves.move_ai(board_copy, move[0], move[1])
            val = minimax(board_copy, depth - 1, False)
            if val > best_val:
                best_val = val
                best_move = move
    else:
        best_val = float('inf')
        for move in legal_moves:
            board_copy = board.copy()
            moves.move_ai(board_copy, move[0], move[1])
            val = minimax(board_copy, depth - 1, True)
            if val < best_val:
                best_val = val
                best_move = move
    return best_move
