# Testausraportti
Testaus on toteutettu unittest kirjaston avulla. Testit ovat luokiteltuna omiin kategorioihin sijainnissa src/tests.\

Koodin laatua ylläpidetään pylintin avulla. pylint ja testit suoritetaan GitHubin actionsin avulla pilvessä automaattisesti, kun branchia päivitetään.

### moves_test.py
Testaa erilaisia liikkeitä laudalla, ja varmistaa, että nappulat liikkuvat, syövät ja mahdollisesti aiheuttaa shakin pelin sääntöjen mukaisesti.

**test_move_empty_square** - Yrittää liikuttaa tyhjän ruudun varattuun ruutuun.

**test_move_wrong_turn** - Liikuttaa väärällä vuorolla valkoisen, sekä mustan hevosen

**test_friendly_capture** - Yrittää syödä hevosella oman sotilaan

**test_pawn_move_and_capture** - Liikuttaa valkoisen, sekä mustan sotilaan kaksi askelta. Yrittää uudestaan, sen jälkeen syö mustan sotilaan valkoisella.

**test_fools_mate** - Testaa shakkimatin mahdollisimman nopeasti kuningattaren avulla.

**test_no_checkmate_at_start** - Tarkistaa, ettei ole shakkimattia alkutilanteessa

**test_initial_board_score** - Testaa laudan pisteytyksen alkutilanteessa.

**test_king_cannot_move_into_check** - Varmistaa, että kuningas ei voi liikkua shakkiin.

### Kattavuusraportti
[![codecov](https://codecov.io/gh/mistablasta/mattishakki/graph/badge.svg?token=OLBMUSIGFU)](https://codecov.io/gh/mistablasta/mattishakki)

### Testien suorittaminen
Testit voi suorittaa paikallisesti projektin ympäristössä komennoilla
```
pytest src
```
```
pylint src
```