# Kaikki ruudut paitsi oikea reuna, ja vasen reuna.
# Käytetään maskeina, jotta nappulat eivät hyppää reunasta reunaan.
NOT_A_FILE = 0xfefefefefefefefe
NOT_H_FILE = 0x7f7f7f7f7f7f7f7f

# Sijainnit jotka määrittelee, voiko sotilaat liikkua kaksi ruutua.
WHITE_PAWN_RANK = 0x000000000000ff00
BLACK_PAWN_RANK = 0x00ff000000000000

# Bitboardit kaikista sallituista liikkeistä liikegeneraatiota varten.
# -------------------------------------------------------------------------------------------
KNIGHT_BITBOARD = [None] * 64
for i in range(64):

    bitboard = 1 << i

    moves = (bitboard & NOT_H_FILE) << 17                                  # Ylös-oikealle
    moves |= ((bitboard & NOT_A_FILE) << 15)                               # Ylös-vasemmalle

    moves |= ((bitboard & NOT_A_FILE) >> 17)                               # Alas-vasemmalle
    moves |= ((bitboard & NOT_H_FILE) >> 15)                               # Alas-oikealle

    moves |= ((bitboard & NOT_H_FILE) << 10)                               # Oikealle-ylös
    moves |= ((bitboard & NOT_A_FILE) << 6)                                # Vasemmalle-ylös

    moves |= ((bitboard & NOT_H_FILE) >> 10)                               # Oikealle-alas
    moves |= ((bitboard & NOT_A_FILE) >> 6)                                # Vasemmalle-alas

    KNIGHT_BITBOARD[i] = moves
# -------------------------------------------------------------------------------------------
KING_BITBOARD = [None] * 64
for i in range(64):

    bitboard = 1 << i

    moves = bitboard << 8                                                    # Ylös
    moves |= (bitboard >> 8)                                                 # Alas

    moves |= ((bitboard & NOT_H_FILE) << 1)                                  # Oikea
    moves |= ((bitboard & NOT_A_FILE) >> 1)                                  # Vasen

    moves |= ((bitboard & NOT_H_FILE) << 9)                                  # Koillinen
    moves |= ((bitboard & NOT_A_FILE) >> 9)                                  # Lounas

    moves |= ((bitboard & NOT_A_FILE) << 7)                                  # Luode
    moves |= ((bitboard & NOT_H_FILE) >> 7)

    KING_BITBOARD[i] = moves
# -------------------------------------------------------------------------------------------
WHITE_PAWN_ATTACKS_BITBOARD = [None] * 64
for i in range(64):
    bitboard = 1 << i
    moves = (bitboard & NOT_H_FILE) << 9        # Syö koillinen
    moves |= ((bitboard & NOT_A_FILE) << 7)       # Syö luode
    WHITE_PAWN_ATTACKS_BITBOARD[i] = moves

BLACK_PAWN_ATTACKS_BITBOARD = [None] * 64
for i in range(64):
    bitboard = 1 << i
    moves = (bitboard & NOT_H_FILE) >> 9          # Syö kaakko
    moves |= ((bitboard & NOT_A_FILE) >> 7)         # Syö lounas
    BLACK_PAWN_ATTACKS_BITBOARD[i] = moves
# -------------------------------------------------------------------------------------------
ROOK_DIRECTIONS = [8, -8, 1, -1]
BISHOP_DIRECTIONS = [9, -9, 7, -7]
QUEEN_DIRECTIONS = ROOK_DIRECTIONS + BISHOP_DIRECTIONS




def knight_moves(board):
    """Palauttaa kaikki ratsun pseudolailliset liikkeet kyseisellä vuorolla.
    
    Args:
        board: lauta
    """
    movelist = []
    if board.white_turn:
        knights = board.white_knight
        own_board = board.white_board
    else:
        knights = board.black_knight
        own_board = board.black_board

    piece_bitboard = knights
    while piece_bitboard:
        lsb = piece_bitboard & -piece_bitboard
        where = lsb.bit_length() - 1
        targets = KNIGHT_BITBOARD[where] & ~own_board

        target_bitboard = targets
        while target_bitboard:
            lsb = target_bitboard & -target_bitboard
            to = lsb.bit_length() - 1
            movelist.append((where, to))
            target_bitboard &= target_bitboard - 1
        piece_bitboard &= piece_bitboard - 1

    return movelist


def king_moves(board):
    """Palauttaa kaikki kuninkaan pseudolailliset liikkeet kyseisellä vuorolla.
    
    Args:
        board: lauta
    """
    movelist = []
    if board.white_turn:
        kings = board.white_king
        own_board = board.white_board
    else:
        kings = board.black_king
        own_board = board.black_board

    piece_bitboard = kings
    while piece_bitboard:
        lsb = piece_bitboard & -piece_bitboard
        where = lsb.bit_length() - 1
        targets = KING_BITBOARD[where] & ~own_board

        target_bitboard = targets
        while target_bitboard:
            lsb = target_bitboard & -target_bitboard
            to = lsb.bit_length() - 1
            movelist.append((where, to))
            target_bitboard &= target_bitboard - 1
        piece_bitboard &= piece_bitboard - 1

    return movelist


def pawn_moves(board): #pylint: disable=too-many-statements
    """Palauttaa kaikki sotilaan pseudolailliset liikkeet kyseisellä vuorolla.
    
    Args:
        board: lauta
    """
    movelist = []
    empty = ~board.combined_board

    if board.white_turn:
        pawns = board.white_pawn
        opponent_board = board.black_board

        pawn_attacks = WHITE_PAWN_ATTACKS_BITBOARD
        single_move = (pawns << 8) & empty
        double_move = ((pawns & WHITE_PAWN_RANK) << 8) & empty
        double_move = (double_move << 8) & empty
        direction = 8
    else:
        pawns = board.black_pawn
        opponent_board = board.white_board

        pawn_attacks = BLACK_PAWN_ATTACKS_BITBOARD
        single_move = (pawns >> 8) & empty
        double_move = ((pawns & BLACK_PAWN_RANK) >> 8) & empty
        double_move = (double_move >> 8) & empty
        direction = -8

    # Hyökkäyslogiikka
    piece_bitboard = pawns
    while piece_bitboard:
        lsb = piece_bitboard & -piece_bitboard
        where = lsb.bit_length() - 1
        targets = pawn_attacks[where] & opponent_board

        target_bitboard = targets
        while target_bitboard:
            lsb = target_bitboard & -target_bitboard
            to = lsb.bit_length() - 1
            movelist.append((where, to))
            target_bitboard &= target_bitboard - 1
        piece_bitboard &= piece_bitboard - 1

    # Liikkumislogiikka
    piece_bitboard = single_move
    while piece_bitboard:
        lsb = piece_bitboard & -piece_bitboard
        to = lsb.bit_length() - 1
        where = to - direction
        movelist.append((where, to))
        piece_bitboard &= piece_bitboard - 1

    piece_bitboard = double_move
    while piece_bitboard:
        lsb = piece_bitboard & -piece_bitboard
        to = lsb.bit_length() - 1
        where = to - direction * 2
        movelist.append((where, to))
        piece_bitboard &= piece_bitboard - 1

    return movelist


def rook_moves(board):
    """Palauttaa kaikki tornin pseudolailliset liikkeet kyseisellä vuorolla.
    
    Args:
        board: lauta
    """
    movelist = []
    if board.white_turn:
        rooks = board.white_rook
        own_board = board.white_board
        opponent_board = board.black_board
    else:
        rooks = board.black_rook
        own_board = board.black_board
        opponent_board = board.white_board

    piece_bitboard = rooks
    while piece_bitboard:
        lsb = piece_bitboard & -piece_bitboard
        where = lsb.bit_length() - 1

        sliding_pieces(where, ROOK_DIRECTIONS, own_board, opponent_board, movelist)

        piece_bitboard &= piece_bitboard - 1

    return movelist


def bishop_moves(board):
    """Palauttaa kaikki lähetin pseudolailliset liikkeet kyseisellä vuorolla.
    
    Args:
        board: lauta
    """
    movelist = []
    if board.white_turn:
        bishops = board.white_bishop
        own_board = board.white_board
        opponent_board = board.black_board
    else:
        bishops = board.black_bishop
        own_board = board.black_board
        opponent_board = board.white_board

    piece_bitboard = bishops
    while piece_bitboard:
        lsb = piece_bitboard & -piece_bitboard
        where = lsb.bit_length() - 1

        sliding_pieces(where, BISHOP_DIRECTIONS, own_board, opponent_board, movelist)

        piece_bitboard &= piece_bitboard - 1

    return movelist


def queen_moves(board):
    """Palauttaa kaikki kuningattaren pseudolailliset liikkeet kyseisellä vuorolla.
    
    Args:
        board: lauta
    """
    movelist = []
    if board.white_turn:
        queens = board.white_queen
        own_board = board.white_board
        opponent_board = board.black_board
    else:
        queens = board.black_queen
        own_board = board.black_board
        opponent_board = board.white_board

    piece_bitboard = queens
    while piece_bitboard:
        lsb = piece_bitboard & -piece_bitboard
        where = lsb.bit_length() - 1

        sliding_pieces(where, QUEEN_DIRECTIONS, own_board, opponent_board, movelist)

        piece_bitboard &= piece_bitboard - 1

    return movelist


def sliding_pieces(where, directions, own_board, opponent_board, movelist): #pylint: disable=too-many-statements
    """Generoi annetulle liukuvalle nappulatyypille kaikki pseudolailliset liikeet.

    args:
        where: lähtöruutu
        directions: nappulan suunnat (torni, lähetti vai kuningatar)
        own_board: oman laudan bitboard
        opponent_board: vastustajan laudan bitboard
        movelist: lista, joka pitää kirjaa sallituista liikkeistä.
    
    """
    for direction in directions:
        current = where
        while True:
            file = current % 8
            if direction == 1 and file == 7:
                break
            if direction == -1 and file == 0:
                break
            if direction == 9 and file == 7:
                break
            if direction == -9 and file == 0:
                break
            if direction == 7 and file == 0:
                break
            if direction == -7 and file == 7:
                break

            current += direction
            if current < 0 or current >= 64:
                break

            target = 1 << current
            if target & own_board:
                break

            movelist.append((where, current))

            if target & opponent_board:
                break


def sliding_attacks_check(where, directions, own_board, opponent_board, combined_board): #pylint: disable=too-many-statements
    """Kertoo, maalaako joku liukuva nappula ruutua. Käytetään shakin tarkastamisessa."""
    for direction in directions:
        current = where
        while True:
            file = current % 8
            if direction == 1 and file == 7:
                break
            if direction == -1 and file == 0:
                break
            if direction == 9 and file == 7:
                break
            if direction == -9 and file == 0:
                break
            if direction == 7 and file == 0:
                break
            if direction == -7 and file == 7:
                break

            current += direction
            if current < 0 or current >= 64:
                break

            target = 1 << current
            if target & own_board:
                break

            if target & opponent_board:
                return True

            if target & combined_board:
                break
    return False


def checked(board): #pylint: disable=too-many-statements
    if board.white_turn:
        friendly_king = board.white_king
        own_board = board.white_board

        opponent_knights = board.black_knight
        opponent_king = board.black_king
        opponent_queen = board.black_queen
        opponent_rooks = board.black_rook
        opponent_bishops = board.black_bishop
        opponent_pawns = board.black_pawn
        pawn_attacks = BLACK_PAWN_ATTACKS_BITBOARD
    else:
        friendly_king = board.black_king
        own_board = board.black_board

        opponent_knights = board.white_knight
        opponent_king = board.white_king
        opponent_queen = board.white_queen
        opponent_rooks = board.white_rook
        opponent_bishops = board.white_bishop
        opponent_pawns = board.white_pawn
        pawn_attacks = WHITE_PAWN_ATTACKS_BITBOARD

    combined_board = board.combined_board
    king_square = (friendly_king & -friendly_king).bit_length() - 1

    if KNIGHT_BITBOARD[king_square] & opponent_knights:
        return True
    if KING_BITBOARD[king_square] & opponent_king:
        return True
    if pawn_attacks[king_square] & opponent_pawns:
        return True
    if sliding_attacks_check(king_square, ROOK_DIRECTIONS, own_board, opponent_rooks | opponent_queen, combined_board): #pylint: disable=line-too-long
        return True
    if sliding_attacks_check(king_square, BISHOP_DIRECTIONS, own_board, opponent_bishops | opponent_queen, combined_board): #pylint: disable=line-too-long
        return True
    return False
