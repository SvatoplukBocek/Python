# Vstupní text
text = "Toto je testovací text. Jak často se zde vyskytují slova různých délek?"

# Inicializace slovníku pro počítání četností slov podle délky
cetnosti = {}

# Rozdělení textu na slova a odstranění interpunkce
slova = text.split()

# Procházení slov a počítání jejich délek
for slovo in slova:
    delka = len(slovo)  # Zjištění délky slova
    if delka in cetnosti:
        cetnosti[delka] += 1  # Zvýšení počtu slov této délky
    else:
        cetnosti[delka] = 1  # První výskyt této délky

# Výstup
for delka in sorted(cetnosti):  # Seřazení podle délky slova
    print(f"Slova s {delka} písmeny: {cetnosti[delka]}x")
