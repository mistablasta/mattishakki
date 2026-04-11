# Viikkoraportti 4

Viikko meni refaktorointiin ja itse varhaisen minimax tekoälyn implementoimiseen. movesets.py sai paljon siistimistä, ja osa auttajafunktioista siirrettiin utils.py tiedostoon, jotta projekti on organisoidumpi. Sain myös shakkimatin havaitsemisen toimimaan, joka itsessään vaati funktion, joka havaitsee aiheuttaako oma siirto omalle kuninkaalle shakin. Tämän jälkeen pystyin generoimaan laillisia liikkeitä, joita hyödynnetään varhaisessa minimax-tekoälyvastustajassa. Aika alkoi loppumaan, joten minimaxin heuristiikkana on tällä hetkellä ainoastaan nappuloiden arvot, eikä minimaxissa ole AB karsintaa. Tekoälyvastustajan toimimiseksi liikefunktiota muutettiin hieman. Testejä en ehtinyt tällä viikolla parannella. Koodissa oli myös pari bugia joiden debuggaamiseen meni huomattavasti aikaa, sillä tekoälyvastustaja teki sotureilla täysin laittomia liikkeitä.

Opin paljon minimaxista, shakkiheuristiikasta ja ab-karsinnasta vaikka en ehtinyt kaikkea implementoida. 

Ensi viikon suunnitelmana on taas pientä refaktorointia, mutta pääfokus on minimaxin kehittämisessä ja niihin liittyvien testien luomisessa. Suunnitelmana on tuoda lisää heuristiikkaa liikkeiden parantamiseksi sekä ab-karsinnan lisääminen. Testauksessa voidaan verrata tiedettyjä parhaita siirtoja tekoälyn tekemiin siirtoihin, ja ylipäätäänsä vertailla, valitseeko tekoäly pisteellisesti parhaimpia siirtoja.

### Käytetyt tunnit
Lauantai 11.4 9h - Kaikki yllämainitut