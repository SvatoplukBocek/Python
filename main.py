"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Svatopluk Boček
email: svatopluk.bocek@gmail.com
"""

from random import randint

hadane_cislo = str(randint(1000, 9999))         #cislo nemuze zacinat nulou, podmínka, aby nezacinalo nulou je zbytecna
while len(set(hadane_cislo)) != 4:              #set zajistí unikátní prvky a len zajistí, aby byly 4
    hadane_cislo = str(randint(1000,9999))      #poznámka pro lektora: mě se zdá tvorba hádaného čísla na 3 řádky OK
                                                #v čem je lepší to zabalit do funkce? Díky
def kontrola_cisla(hadane_cislo, cislo):
    """
    Zkontroluje, kolik číslic a kolik pozic zadaného čísla se shoduje s hádaným číslem.
    
    Parametry:
    hadane_cislo (str) – tajné číslo
    cislo (str) – číslo, které uživatel zadal

    Návrat:
    (int, int) – počet správných číslic, počet správných pozic
    """
    stejna_pozice = 0

    stejna_cislice = 0

    for pozice in range(4):                                 #zkontroluje všechny číslice
        if hadane_cislo[pozice] == cislo[pozice]:           #a porovná jestli jsou na stejných pozicích stejné číslice
            stejna_pozice +=1
        elif hadane_cislo[pozice] in cislo:                 #pokud nejsou, tak porovná, jestli číslice z pozice je v čísle samotném
            stejna_cislice +=1
    return stejna_pozice, stejna_cislice

print("Hi there!\n"
"-----------------------------------------------\n"
"I've generated a random 4 digit number for you.\n"
"Let's play a bulls and cows game.\n"
"The number consists of 4 different digits\n"
"-----------------------------------------------\n"
"Enter a number:\n"
"-----------------------------------------------")
cislo = 0

pocet_pokusu = 0                      

while cislo != hadane_cislo:
    cislo = input()             #vse zadane pomoci input je string
    pocet_pokusu +=1            #pocitani, za jak dlouho uhodne
    while cislo.startswith("0") or len(set(cislo)) != 4 or not cislo.isdigit():     #set zajistí unikátní prvky a len zajistí, aby byly 4
        print("Number can`t start with zero and must have 4 different digits, please input different number:")
        cislo = input() 

    pozice, cislice = kontrola_cisla(hadane_cislo, cislo)

    if pozice == 0 or pozice == 1:                              #zde jen jednoduché rozdělení na bull/bulls 0-1 a 2-4
        print(f"Bull:{pozice}")
    else:
        print(f"Bulls:{pozice}")

    if cislice == 0 or cislice == 1:                            #zde jen jednoduché rozdělení na cow/cows 0-1 a 2-4
        print (f"Cow:{cislice}")
    else:
        print(f"Cows:{cislice}")

else:
    print("Correct, you've guessed the right number\n"          
          f"in {pocet_pokusu} guesses\n"
           "That`s amazing")