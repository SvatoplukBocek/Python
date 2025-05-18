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
    uzemni_uroven = requests.get(WWW) #rozseká stránku s výsledky
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
                    mesta[nazev_mesta] = odkaz # 1, dostanu slovník s nazev_mesta, odkaz, v main dostanu url_okresu
    return mesta

def get_obce_z_okresu(url_okresu):
    response = requests.get(url_okresu) #rozseká url_okresu
    soup = BS(response.text, "html.parser")

    obce = []

    tabulky = soup.find_all("table")

    for tabulka in tabulky:
        rows = tabulka.find_all("tr")[2:]  # přeskočíme hlavičky
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                kod_obce = cells[0].get_text(strip=True)
                nazev_obce = cells[1].get_text(strip=True)
                odkaz_tag = cells[0].find("a")
                if odkaz_tag and odkaz_tag.has_attr("href"):
                    url_obce = BASE_URL + odkaz_tag["href"].replace("&amp;", "&")
                    obce.append((kod_obce, nazev_obce, url_obce)) # 3, dostanu list s kod_obce, nazev_obce, url_obce

    return obce

def ziskej_vysledky_z_url(kod, nazev, url):
    response = requests.get(url)
    soup = BS(response.text, "html.parser")

    data = {
        "kód obce": kod,
        "obec": nazev
    }

    # 1. Získání souhrnných údajů z první tabulky (účast, obálky, platné hlasy)
    tabulky = soup.find_all("table", class_="table")
    if len(tabulky) < 1:
        print(f"⚠️  Nenalezena tabulka souhrnu pro {nazev}")
        return data

    souhrn_radek = tabulky[0].find_all("tr")[-1]  # poslední řádek má celkové součty
    bunky = souhrn_radek.find_all("td")

    try:
        data["voliči v seznamu"] = int(bunky[3].text.replace("\xa0", "").replace(" ", ""))
        data["vydané obálky"] = int(bunky[4].text.replace("\xa0", "").replace(" ", ""))
        data["platné hlasy"] = int(bunky[7].text.replace("\xa0", "").replace(" ", ""))
    except (IndexError, ValueError):
        print(f"⚠️  Nepodařilo se načíst souhrnné údaje pro {nazev}")

    # 2. Získání hlasů pro strany (všechny tabulky po první obsahují strany)
    for tabulka in tabulky[1:]:
        rows = tabulka.find_all("tr")[2:]  # přeskočíme hlavičky
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 5:
                nazev_strany = cells[1].get_text(strip=True)
                hlasy = cells[2].get_text(strip=True).replace("\xa0", "").replace(" ", "")
                try:
                    data[nazev_strany] = int(hlasy)
                except ValueError:
                    data[nazev_strany] = 0

    return data

def main():
    if len(sys.argv) != 3:
        print("Použití: python3 election_scraper.py 'NázevOkresu' 'soubor.csv'")
        sys.exit(1)

    nazev_mesta = sys.argv[1]
    vystupni_soubor = sys.argv[2]

    mesta = get_uzemni_uroven()
    if nazev_mesta not in mesta:
        print("Neplatný první argument – okres nenalezen.")
        sys.exit(1)

    print(f"STAHUJI DATA PODLE VYBRANÉHO MĚSTA: {nazev_mesta}")
    print(f"VYTVÁŘÍM SOUBOR {vystupni_soubor}")

    url_okresu = mesta[nazev_mesta]
    obce = get_obce_z_okresu(url_okresu)

    radky = []
    for kod, nazev, odkaz in obce:
        print(f"Stahuji výsledky pro: {nazev}")
        vysledky = ziskej_vysledky_z_url(kod, nazev, odkaz)
        radky.append(vysledky)

    # 1. Zjistíme všechny unikátní klíče napříč obcemi
    vsechny_klice = {k for radek in radky for k in radek.keys()}

    # 2. Definujeme pevné pořadí základních sloupců
    hlavicky = ["kód obce", "obec", "platné hlasy", "voliči v seznamu", "vydané obálky"]

    # 3. Zbytek (strany) setřídíme abecedně a přidáme za základní sloupce
    strany = sorted(vsechny_klice - set(hlavicky))
    hlavicky += strany

    # 4. Zápis do CSV
    with open(vystupni_soubor, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=hlavicky)
        writer.writeheader()
        writer.writerows(radky)

    print(f"\n✅ Výsledky uloženy do souboru: {vystupni_soubor}")
    
if __name__ == "__main__":
    main()

