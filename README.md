## Nykyiset toiminnot
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään/ulos
* Käyttäjä pystyy lisäämään/muokkaaman/poistamaan omia kampanjoita
* Käyttäjä pystyy lisäämään/poistamaan kampanjaan kuvia
* Käyttäjä näkee sovellukseen lisätyt kampanjat
* Käyttäjä pystyy etsimään kampanjoita hakusanalla
* Käyttäjä pystyy lahjoittamaan kampanjoihin
* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät kampanjat
* Käyttäjä pystyy valitsemaan kampanjalle kategorian

## Sovelluksen asennus

Asenna `flask`-kirjasto

```
$ pip install flask
```

Luo  ja alusta tietokanta

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistää sovelluksen näin

```
$ flask run
```

# Joukkorahoitus

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan kampanjoita.
* Käyttäjä näkee sovellukseen lisätyt kampanjat.
* Käyttäjä pystyy etsimään kampanjoita hakusanalla, tavoitesummalla ja kategorialla.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät kampanjat.
* Käyttäjä pystyy valitsemaan kampanjalle yhden tai useamman luokittelun (esim. taivoitesumma, kategoria (kuten hyväntekeväisyys, taide, teknologia)).
* Käyttäjä pystyy lahjoittamaan kampanjoihin.
