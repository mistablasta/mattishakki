# Viikkoraportti 3
Viikko meni liikkeiden generaation laajentamiseen liikkuvia nappuloita varten, sekä aikaisemmin tehtyjen nappuloiden optimointiin, jotta myöhemmin algoritmi voi saada kaikki sallitut liikkeet kerralla. Peli myös nyt huomaa, kun kuningas on shakissa. Uutena asiana opin optimaalisen tavan iteroida bitboardeja least signifigant bitin (lsb) avulla, muulloin kyseessä oli valmiin koodin muotoilua.

Ensi viikon suunnitelma on refaktoroida movesets.py, sillä se on todella sotkuinen tällä hetkellä. Toistuvaa koodia on jatkuvasti jotka saa helposti karsittua pois, sekä tällä hetkellä sammutetut pylint varoitukset pitää korjata. Refaktoroinnin jälkeen puuttuu vielä shakkimatti. Sen jälkeen voin aloittaa ohjelmoida minimax algoritmia täysin voimin. Uskon, että ensi viikolla saan ensimmäisen pelattavan tekoälyvastustajan valmiiksi, vaikka se ei olisi kovin tehokas. Myös testejä pitää toteutaa enemmän.

### Käytetyt tunnit
Perjantai 27.3 3h - Kuninkaan, sotilaan ja ratsun refaktorointia.

Lauantai 28.3 4h - Liukuvat nappulat, shakin tarkastaminen, movesets.py refaktorointia. Raportointi.

