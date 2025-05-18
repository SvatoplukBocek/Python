"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Svatopluk Boček
email: svatopluk.bocek@gmail.com
"""
import requests
import bs4
from requests import get
from bs4 import BeautifulSoup as BS
import csv
import sys

WWW = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
BASE_URL = "https://www.volby.cz/pls/ps2017nss/"

def get_uzemni_uroven():
    uzemni_uroven = requests.get(WWW)
    vytah = BS(uzemni_uroven.text, "html.parser")

    tabulky = vytah.find_all("table", class_="table")
    mesta = {}
    for tabulka in tabulky:
        rows = tabulka.find_all("tr")[2:]  # přeskočíme hlavičky
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 4:
                nazev_mesta = cells[1].get_text(strip=True)
                odkaz_tag = cells[3].find("a")
                if odkaz_tag and odkaz_tag.has_attr("href"):
                    odkaz = BASE_URL + odkaz_tag["href"].replace("&amp;", "&")
                    mesta[nazev_mesta] = odkaz
    return mesta

def main():
    if len(sys.argv) != 3:
        sys.exit(1)
    nazev_mesta = sys.argv[1]
    vystupni_soubor = sys.argv[2]
    mesta = get_uzemni_uroven()
    if nazev_mesta not in mesta:
        print("Neplatný první argument, ukončuji program")
        sys.exit(1)
    print (f"STAHUJI DATA PODLE VYBRANÉHO MĚSTA: {nazev_mesta}")
    print (f"VYTVÁŘÍM SOUBOR {vystupni_soubor}")

if __name__ == "__main__":
    main()

