def lsb_helper(piece_bitboard, move_bitboard, own_board, movelist):
    """Käy läpi bitboardeja least signifigant bitin avulla nopeasti.
     Args:
        piece_bitboard: bitboard, joka sisältää kaikki kyseisen nappulatyypin nappulat
        move_bitboard: liikebitboard
        own_board: bitboard omista nappuloista
        movelist: lista, johon lisätään löydetyt liikkeet (where, to) muodossa
    """
    while piece_bitboard:
        lsb = piece_bitboard & -piece_bitboard
        where = lsb.bit_length() - 1
        targets = move_bitboard[where] & own_board
        target_bitboard = targets
        while target_bitboard:
            lsb_to = target_bitboard & -target_bitboard
            to = lsb_to.bit_length() - 1
            movelist.append((where, to))
            target_bitboard &= target_bitboard - 1
        piece_bitboard &= piece_bitboard - 1


def check_edges(current, direction):
    """Tarkistaa liukunappuloiden tapauksessa ollaanko reunalla. Estää laudan yli liikkumisen.
    Args:
        current: nykyinen sijainti
        direction: nappulan suunnat (torni, lähetti vai kuningatar)

    Returns:
        True, jos ruudusta ei voi liikkua reunan ylityksen seurauksena.
    """
    file = current % 8
    return (
        (direction == 1 and file == 7) or
        (direction == -1 and file == 0) or
        (direction == 9 and file == 7) or
        (direction == -9 and file == 0) or
        (direction == 7 and file == 0) or
        (direction == -7 and file == 7)
    )


def sliding_pieces(where, directions, own_board, opponent_board, movelist):
    """Generoi annetulle liukuvalle nappulatyypille kaikki pseudolailliset liikeet.

    Args:
        where: lähtöruutu
        directions: nappulan suunnat (torni, lähetti vai kuningatar)
        own_board: oman laudan bitboard
        opponent_board: vastustajan laudan bitboard
        movelist: lista, joka pitää kirjaa sallituista liikkeistä.

    """
    for direction in directions:
        current = where
        while True:

            if check_edges(current, direction):
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


def sliding_attacks_check(where, directions, own_board, opponent_board, combined_board):
    """Kertoo, maalaako joku liukuva nappula valittua ruutua. Käytetään shakin tarkastamisessa."""
    for direction in directions:
        current = where
        while True:

            if check_edges(current, direction):
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
