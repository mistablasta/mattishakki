# Määrittelydokumentti

Tietojenkäsittelytieteen kandidaattiohjelman Algoritmit ja tekoäly -kurssin harjoitustyö.\
Dokumentaatio toteutetaan suomeksi.\
Toteutus- ja vertaisarviointikieli on Python.

## Aihe

Harjoitustyön aiheena on luoda sääntöihin perustuva alusta shakin pelaamiseen, ja itse **ytimenä** toteuttaa siihen **minimax-algoritmia** sekä **alpha-beta karsintaa** hyödyntävä tekoälyvastustaja. Algoritmin heuristiikkana käytetään nappulakohtaisia materiaaliarvoja, sekä jokaiselle nappulatyypille ominaisia karttoja, jotka määrittelevät nappuloille suosituimmat sijainnit pelilaudalla.

Ohjelma alkaa alustetulla shakkilaudalla komentokehotteessa, johon pelaaja syöttää komentona haluamansa siirron (mistä-mihin, esim: e2e4). Pelaajan siirron jälkeen tekoälyllä toimiva vastustaja analysoi laudan tilan tiettyyn syvyyteen asti ja valitsee saadusta datasta parhaan mahdollisen siirron. Laudan tila esitetään useina [bitboardeina](https://www.chessprogramming.org/Bitboards), joka helpottaa itse pelilogiikan kehitystä, sekä nopeuttaa minimax-algoritmin lukuisten eri pelitilojen analyyseja.

## Aika- ja tilavaativuudet

Aikavaativuus O(b^d) ja tilavaativuus O(bd), missä b on haarautumistekijä ja d on syvyys. Alpha-beta karsinta voi pudottaa aikavaativuuden tasolle O(b^(d/2)).

Shakin haarautumistekijän keskiarvo on n. 35 ja se perustuu jokaisella kierroksella olevaan laillisten siirtojen määrään. Loppupelissä tekijä on paljon pienempi, kun taas pelin keskellä paljon suurempi.

## Lähteet

[Chess Programming](https://www.chessprogramming.org) - Päälähde, laajasti tietoa koko aihealueeseen liittyen.

[Wikipedia - Minimax](https://en.wikipedia.org/wiki/Minimax)

[Wikipedia - Alpha-Beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)

