# Toteutusdokumentti


## Ohjelman rakenne

### Shakkilauta
Shakkilauta toimii bitboardeilla, jotka sallivat nopean liikegeneraation ja siirtojen laillisuuden tarkistamisen. Bitboardit ovat yksinkertaisuudessaan 64-bittisiä binäärilukuja (shakkilaudassa on 64 ruutua), jossa numero 1 on laudalla oleva nappula, ja 0 on tyhjä ruutu. Jokaiselle nappulatyypille per väri on alustettu omat bitboardit, joita käytetään **movesets.py** tiedostossa erilaisissa operaatioissa. Ydinidea on tehdä erilaisia muunnoksia nappuloiden bitboardeille joko ennaltalaskettujen liikeratojen tai raycastin avulla liukunappuloiden tapauksessa. Esimerkiksi ratsun tapauksessa on ennaltalasketut liikeradat (L muodot jokaiseen suuntaan), jotka kerrotuna ritareiden bitboardiin ja pienen maskeerauksen (jotta ritari ei hyppää laudan reunasta reunaan) jälkeen palauttaa ritareiden nykyisistä ruuduista bitboardin sijainneista, johon ritarit voivat mennä. Tämän päälle tehdään erilaisia tarkistuksia (onko liikutettava nappi oma, meneekö siirto oman nappulan päälle, aiheuttaako siirto omalle kuninkaalle shakin) joka luo laillisen liikkeen perustan.

Shakkilaudan koodi on jaettu seuraaviin osiin

board.py - Laudan alustaminen ja tulostaminen.

moves.py - Liikkeiden hallitseminen, laillisuuden tarkistaminen.

movesets.py - Bittioperaatiot, siirtojen generointi.

utils.py - Auttajafunktiot.

### Algoritmi
Shakin vastustajana on minimax algoritmi. Algoritmi yksinkertaisuudessaan painottaa tilanteita, missä huonoin mahdollinen tapahtuma aiheuttaa vähiten vahinkoa. Shakin tilanteessa tapahtumia painotetaan nappuloiden ominaisarvoilla, sekä vaihtuvalla pisteytyksellä riippuen nappulan sijainnista. Algoritmi käy läpi kaikki pelilaudan lailliset siirrot ja valitsee niistä parhaimman. Korkeammilla syvyyksillä analysoituja laudantiloja käydään läpi rekursiivisesti haluttuun syvyteen asti, jolloin algoritmi "ajattelee eteenpäin". Siirtojen määrät kasvavat nopeasti pienilläkin syvyyksillä, joten algoritmi käyttää Alpha-Beta karsintaa pelitilojen leikkaamiseksi. Karsinnan avulla algoritmi ei ota huomioon siirtoja, jotka ovat jo varmasti huonompia kuin jo siihen mennessä löydetty paras siirto.

Karsinnan parantamiseksi laillisten liikkeiden listaa on syytä pitää järjestettynä siten, että parhaimpia siirtoja tutkiaan ensimmäisenä. Projektissa siihen käytetään MVV-LVA (Most Valuable Victim, Least Valuable Attacker) syövissä siirroissa. Jos siirto ei ole syövä, järjestetään ne nappuloiden arvojen mukaan kuningattaresta alaspäin. Iteratiivisella syvenemisellä laillisten siirtojen listan kärjessä on aina yhden aiemman syvyyden löytämä paras siirto. Itse iteratiivinen syveneminen on sitä, että haluttuun syvyyteen mentäessä käydään kaikki alemmat syvyydet lävitse.

Algoritmin koodi löytyy ai.py tiedostosta kokonaisuudessaan

## Saavutetut aika- ja tilavaativuudet
**Shakin logiikka**
get_legal_moves funktio käy läpi kaikki laudan 64 ruutua ja generoi jokaiselle nappulatyypille lailliset siirrot. Ratsu, kuningas- ja sotilasbitboardit ovat ennalta laskettuja, mutta liukuvien nappuloiden tapauksessa ruutuja tutkitaan yksittäin korkeintaan seitsemään askeleen asti jokaiseen neljään mahdolliseen suuntaan. Pseudolaillisten liikkeiden generoinnin jälkeen liikkeet vielä tarkistetaan move_leaves_king_in_check funktion avulla, jossa laudan tila kopioidaan ja shakki tarkistetaan. Shakissa laillisia siirtoja voi olla maksimissaan 218, mutta keskiarvo on 35. Operaatioiden aikavaativuus on O(1) laudan kiinteän koon vuoksi.

**Algoritmi**
Minimaxin aikavaativuus on pahimmillaan O(b^d) ja parhaimmillaan O(b^(d/2)) missä b on haarautumistekijä ja d on syvyys. Huonoimpaan tapaukseen päästään, kun liikkeiden järjestely ei tue alpha-beta karsintaa jolloin kaikki mahdolliset siirrot tulee tutkittavaksi. Paras tapaus on toinen ääripää, missä liikkeet ovat järjestetty täydellisesti tukien tehokasta karsintaa. Tilavaativuus on algoritmille O(bd).

## Puutteet ja parannusehdotukset
Shakkilogiikasta puutuu en passant ja tornitus. Tasapeli aiheutuu vain liikkeiden puutteesta eikä toistuvista liikkeistä, joka voi johtaa loputtomaan liikkeiden toistokierteeseen, kun tekoälyjä laitetaan vastakkain. Sotilas ylennetään automaattisesti kuningattareen, joka voi harvoissa tilanteissa olla huonompi vaihtoehto kuin hevonen.

Shakkilogiikan suorituskyky ei ole paras. Raskain osio lienee laudan jatkuva kopiointi, jonka voisi vaihtaa tee liike/peru liike logiikkaan, jolloin jatkuvaa kopiointia vältetään. Liukuvilla nappuloilla voisi käyttää magic bitboardeja laillisten liikkeiden generaatioon. Iteratiivisesta syvenemisestä voisi repiä enemmän tietoa irti myöhempiin iteraatioihin AB karsinnan parantamiseksi, nykytilanteessa ainoastaan yksi paras liike siirretään laillisten liikkeiden kärkeen.

## Laajojen kielimallien käyttö
Laajaa kielimallia (DeepSeek) on käytetty bitboardien ja bittioperaatioiden havainnollistamiseen sekä yleisiin optimisaatiovinkkeihin shakin ydinlogiikassa, kuten deepcopyn välttäminen projektin alkuvaiheessa.

## Käytety lähteet
https://www.chessprogramming.org/Main_Page, ylivoimaisesti hyödyllisin lähde. 

https://en.wikipedia.org/wiki/Minimax, https://stackoverflow.com/questions/59608390/python-deep-copy-in-minimax-function

https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning