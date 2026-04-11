# Toteutusdokumentti


## Ohjelman rakenne

### Shakkilauta
Shakkilauta toimii bitboardeilla, jotka sallivat nopean liikegeneraation ja siirtojen laillisuuden tarkistamisen. Bitboardit ovat yksinkertaisuudessaan 64-bittisiä binäärilukuja (shakkilaudassa on 64 ruutua), jossa numero 1 on laudalla oleva nappula, ja 0 on tyhjä ruutu. Jokaiselle nappulatyypille per väri on alustettu omat bitboardit, joita käytetään **movesets.py** tiedostossa erilaisissa operaatioissa. Ydinidea on tehdä erilaisia muunnoksia nappuloiden bitboardeille joko ennaltalaskettujen liikeratojen tai raycastin avulla liukunappuloiden tapauksessa. Esimerkiksi ratsun tapauksessa on ennaltalasketut liikeradat (L muodot jokaiseen suuntaan), jotka kerrotuna ritarin bitboardeihin ja pienen maskeerauksen jälkeen palauttaa ritarin nykyisestä ruudusta bitboardin sijainneista, johon ritari voi mennä. Tämän päälle tehdään erilaisia tarkistuksia (onko liikutettava nappi oma, meneekö siirto oman nappulan päälle, aiheuttaako siirto omalle kuninkaalle shakin) joka luo laillisen liikkeen perustan.