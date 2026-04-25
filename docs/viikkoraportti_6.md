# Viikkoraportti 6

Käytin viikon algoritmin optimointiin, jotta se pystyy pyörimään edes jollakin tasolla syvyydellä viisi. Zoom keskustelussa ohjaajan kanssa sain vinkkejä testaamiseen ja minimaxin parantamiseen, joista paljon tuli käyttöön. Ensimmäisenä on iteratiivinen syventyminen, jossa esimerkiksi syvyyteen viisi mennessä algoritmi käy ensiksi läpi syvyydet 1-4 ja pitää niistää parhaimman liikkeen kärjessä mahdollista karsintaa varten joka syvyydellä. Pienemmillä syvyyksillä vaikutti, että suoritusajat nousevat mutta korkeammilla syvyyksillä sain parannuksia aikoihin. Liikkeiden järjestäminen oli myös toinen keskusteltu aihe, mistä sain paljon implementoitua. Nyt liikkeet järjestetään parhaiten syöntien mukaan (syönnit, jotka aiheuttavat eniten vahinkoa vähimmällä omalla nappula-arvolla), jonka jälkeen ei-syövät liikkeet järjestetään nappula-arvon mukaan, eli kuningattaresta alaspäin. Huomasin näistä myös paljon nopeutumista, sillä nyt AB karsinta alkoi vasta oikeasti toimimaan.

Minimaxin optimoinnin lisäksi aloitin itse algoritmin testailun, ne ovat tällä hetkellä melko alkeellisia testejä, missä käydään läpi pakotettuja pelin lopetuksia kahdella ja kolmella liikkeellä.

Seuraavaksi tavoitteena on itse projektin viimeistely, eli koodin parempi dokukmentointi, dokumentaatiotiedostojen tekeminen ja algoritmiin liittyvien testien tekemistä. Uskon myös, että aikaa vielä riittää algoritmien paranteluun, jotta saisin vitossyvyyden vielä nopeammaksi. Zoom keskustelussa suunnitelmana oli sijoittaa shakin aiheuttavat liikeet kärkeen, jota en vain ehtinyt tehdä tällä viikolla. Heuristiikka on myös aika heikko, jota voi mahdollisesti parannella.

Perjantai 24.4 5h - Bugien etsimistä, iteratiivinen syventyminen

Lauantai 25.4 6h - Likkeiden järjestäminen, testit, dokumentaatio