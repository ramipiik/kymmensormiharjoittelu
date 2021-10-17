# Kymmensormijärjestelmän harjoittelu

Sovelluksen avulla voit opetella ja harjoitella kymmensormijärjestelmän käyttöä. Voit myös mitata edistymistäsi ja kisata muita käyttäjiä vastaan nopeustesteillä. 

Sovelluksen ominaisuuksia:

* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden käyttäjätunnuksen.
* Käyttäjä voi valita haluamansa tason esim. 1-10 (1=ensikertalainen, 10=ammattilainen). En ole vielä tässä vaiheessa varma kuinka monta tasoa ohjelmaan tulee.
* Kunkin tason sisällä on valittavana joukko erilaisia harjoituksia. Esim. tasolla 1 harjoitellaan yksittäisten sormien käyttöä. Seuraavilla tasoilla näiden yhdistelmiä. Vaikeimmalla tasolla kokonaisia lauseita, joissa on välimerkkejä ja isoja kirjaimia yms.
* Kuhunkin harjoitukseen liittyen käyttäjä näkee omat aiemmat suorituksensa: Päivämäärä, harjoitukseen kulunut aika, virheiden määrä ja paras suoritus.
* Harjoitus on hyväksytysti suoritettu, kun virheiden määrä on alle 3%. Käyttäjä saa 1 op suoritusmerkinnän kun 90% harjoituksista on hyväksytysti suoritettu. SISU-integraatio on tulossa seuraavaan versioon. :)
* Käyttäjä näkee tilaston kuinka monta harjoitusta hän on yhteensä tehnyt.
* Käyttäjä näkee myös kunkin harjoituksen top10-listan parhaimmista suorituksista. Tähän pitää kehittää joku kaava miten virheiden määrä suhteutuu käytettyyn aikaan. Esim. niin, että kukin virhe lisää suoritusaikaa 3 sekuntia tai 3% tms.
 
* Ylläpitäjä voi luoda uusia harjoituksia ja tasoja
* Ylläpitäjä voi poistaa harjoituksia ja tasoja
* Ylläpitäjä näkee kaikkien käyttäjien tilastot
