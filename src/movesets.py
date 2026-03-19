# Kaikki ruudut paitsi oikea reuna, ja vasen reuna.
# Käytetään maskeina, jotta nappulat eivät hyppää reunasta reunaan.
NOT_A_FILE = 0xfefefefefefefefe
NOT_H_FILE = 0x7f7f7f7f7f7f7f7f

# Sijainnit jotka määrittelee, voiko sotilaat liikkua kaksi ruutua.
WHITE_PAWN_RANK = 0x000000000000ff00
BLACK_PAWN_RANK = 0x00ff000000000000

def knight_moves(knight_bitboard, own_bitboard):
    """Ritarin sallitut liikkeet"""
    moves = (knight_bitboard & NOT_H_FILE) << 17                                  # Ylös-oikealle
    moves |= ((knight_bitboard & NOT_A_FILE) << 15)                               # Ylös-vasemmalle

    moves |= ((knight_bitboard & NOT_A_FILE) >> 17)                               # Alas-vasemmalle
    moves |= ((knight_bitboard & NOT_H_FILE) >> 15)                               # Alas-oikealle

    moves |= ((knight_bitboard & NOT_H_FILE) << 10)                               # Oikealle-ylös
    moves |= ((knight_bitboard & NOT_A_FILE) << 6)                                # Vasemmalle-ylös

    moves |= ((knight_bitboard & NOT_H_FILE) >> 10)                               # Oikealle-alas
    moves |= ((knight_bitboard & NOT_A_FILE) >> 6)                                # Vasemmalle-alas

    legal = moves & ~ own_bitboard
    return legal

def king_moves(king_bitboard, own_bitboard):
    """Kuninkaan sallitut liikkeet"""
    moves = king_bitboard << 8                                                    # Ylös
    moves |= (king_bitboard >> 8)                                                 # Alas

    moves |= ((king_bitboard & NOT_H_FILE) << 1)                                  # Oikea
    moves |= ((king_bitboard & NOT_A_FILE) >> 1)                                  # Vasen

    moves |= ((king_bitboard & NOT_H_FILE) << 9)                                  # Koillinen
    moves |= ((king_bitboard & NOT_A_FILE) >> 9)                                  # Lounas

    moves |= ((king_bitboard & NOT_A_FILE) << 7)                                  # Luode
    moves |= ((king_bitboard & NOT_H_FILE) >> 7)                                  # Kaakko

    legal = moves & ~ own_bitboard
    return legal

def pawn_moves(pawn_bitboard, own_bitboard, opponent_bitboard, direction_up):
    empty_bitboard = ~ (own_bitboard | opponent_bitboard)

    if direction_up:
        moves = (pawn_bitboard << 8) & empty_bitboard                              # Ylös yksi
        moves |= ((pawn_bitboard & WHITE_PAWN_RANK) << 16 ) & empty_bitboard       # Ylös kaksi

        moves |= ((pawn_bitboard & NOT_H_FILE) << 9) & opponent_bitboard           # Syö koillinen
        moves |= ((pawn_bitboard & NOT_A_FILE) << 7) & opponent_bitboard           # Syö luode
    else:
        moves = (pawn_bitboard >> 8) & empty_bitboard                              # Alas yksi
        moves |= ((pawn_bitboard & BLACK_PAWN_RANK) >> 16 ) & empty_bitboard       # Alas kaksi

        moves |= ((pawn_bitboard & NOT_H_FILE) >> 9) & opponent_bitboard           # Syö kaakko
        moves |= ((pawn_bitboard & NOT_A_FILE) >> 7) & opponent_bitboard           # Syö lounas

    legal = moves
    return legal
