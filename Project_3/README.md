ENGETO-pa-3-projekt

třetí projekt na Python akademii od Engeta

POPIS PROJEKTU

Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017 ze stránky https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

INSTALACE KNIHOVEN

Knihovny, které jsou použity v kódu jsou uložené v souboru requirements.txt. Pro instalaci doporučuji použít nové virtuální prostředí a s anainsatolvaným manažerem spustit následovně:

$ pip3 --version                    #ověříš verzi manažeru
$ pi3 install -r requirements.txt   # nainstalujeme knihovny

SPUŠTĚNÍ PROJEKTU

spuštění souboru elections_scraper.py v rámci příkazového řádku vyžaduje dva argumenty

python election_scraper <vybrane_mesto> <vysledny_soubor>

Následně se Vám stáhnou výsledky jako soubor s příponou .csv

UKÁZKA PROJEKTU

Výsledky hlasování pro okres Prostějov
1. argument Prostějov
2. argument vysledky_prostejov.csv

SPUŠTĚNÍ PROGRAMU
python election_scraper.py 'Prostějov' 'vysledky_prostejov.csv'

Průběh stahování:
STAHUJI DATA Z VYBRANÉHO MĚSTA: Prostějov
DATA JSOU NA URL: https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xnumnuts=7103
UKLADAM DO SOUBORU: vysledky_prostejov.csv
UKONCUJI election_scraper

Částečný výstup:
code, location, registered, envelopes, valid,...
506761, Alojzov, 205, 145, 144, 29, 0, 0, 9, 0