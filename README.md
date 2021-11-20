# Kymmensormiharjoittelu
Sovelluksen avulla voit harjoitella kymmensormijärjestelmän käyttöä. Voit myös mitata edistymistäsi ja kisata muita käyttäjiä vastaan nopeustesteillä. 

## Sovelluksen ominaisuuksia
* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden käyttäjätunnuksen.
* Käyttäjä voi valita haluamansa tasoisia harjoituksia (esim. 1=aeloittelija, 10=ammattilainen). En ole vielä tässä vaiheessa varma kuinka monta tasoa ohjelmaan tulee.
* Kunkin tason sisällä on valittavana joukko erilaisia harjoituksia. Esim. tasolla 1 harjoitellaan yksittäisten sormien käyttöä. Seuraavilla tasoilla näiden yhdistelmiä. Vaikeimmalla tasolla kokonaisia lauseita, joissa on välimerkkejä ja isoja kirjaimia yms.
* Kuhunkin harjoitukseen liittyen käyttäjä näkee omat aiemmat suorituksensa: Päivämäärä, harjoitukseen kulunut aika, virheiden määrä ja paras suoritus.
* Harjoitus on hyväksytysti suoritettu, kun virheiden määrä on alle 5%. 
* Käyttäjä näkee tilaston kuinka monta harjoitusta hän on yhteensä tehnyt.
* Käyttäjä näkee myös kunkin harjoituksen high score-listan parhaimmista suorituksista. 
 
* Ylläpitäjä voi luoda uusia harjoituksia ja tasoja
* Ylläpitäjä voi poistaa harjoituksia ja tasoja
* Ylläpitäjä näkee kaikkien käyttäjien tilastot

## Status välipalautus 2
* Sovellus löytyy osoitteesta: https://type10trainer.herokuapp.com/
* Perustoiminnallisuus on koodausmielessä kasassa. Eli kaikki alkuperäisen vaatimusmäärittelyn vaatimukset toteutuvat.
* Enää puuttuu itse sisältö eli mielekkäät harjoitukset. :)
* Kysymys: Omaan toteutukseeni jäi lopulta vain ao. kolme tietokantataulua (ks. schema.sql) LISÄÄ HYPERLINKKI. a) Onko tämä ok näin? Vai yritänkö b) laajentaa sisältöä siten että tauluja tulee lisää (esim. mahdollisuus lisätä omia muistiinpanoja tms)? c) Vai pilkonko olemassa olemat taulut pienemmiksi?