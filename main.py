"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Richard Papež
email: richard.papez.ml@gmail.com¨
"""

# Knihovny
from copy import deepcopy
from colorama import init, Fore, Style
from time import sleep

# Funkce
def zobraz_uvod():
    """
    Tiskne úvod zkopírovaný ze zadání projektu.

    Bez vstupu či výstupu.
    """
    uvod_text = """Welcome to Tic Tac Toe
============================================
GAME RULES:
Each player can place one mark (or stone)
per turn on the 3x3 grid. The WINNER is
who succeeds in placing three of their
marks in a:
* horizontal,
* vertical or
* diagonal row
============================================
Let's start the game
--------------------------------------------"""

    print(uvod_text)

def ziskej_volbu(stav):
    """
    Ptá se hráče, na jaké pole chce umístit hrací kámen,
    kontroluje vstup a přepisuje stav hry:
        - připisuje položený kámen hráči
        - obsazuje pole
        - přičítá kolo

    :param stav: slovník obsahující aktuální stav hry
    :type stav: dict
    Bez návratové funkce.
    """
    oddelovac = "=" * 44
    pripustne_volby = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    print(oddelovac)
    zadane_policko = input(f"Player {stav['na tahu']} | Please enter your move number: ")
    while zadane_policko not in pripustne_volby or zadane_policko in stav["pole x"] or zadane_policko in stav["pole o"]:
        print(oddelovac)
        zadane_policko = input(Fore.RED + "Wrong input or occupied box." + Style.RESET_ALL + "\nPlease enter your move number: ")
    stav[f"pole {stav['na tahu']}"].append(zadane_policko)
    stav[f"pole {zadane_policko}"] = stav["na tahu"]
    stav["kolo"] += 1

def zmen_hrace(stav):
    """
    Mění aktuálně táhnoucího hráče. Pokud už někdo vyhrál, funkce rovnou skončí.

    :param stav: slovník obsahující aktuální stav hry
    :type stav: dict
    Bez návratové hodnoty.
    """
    if stav["dohrano"] == "ano":
        return
    if stav["na tahu"] == "o":
        stav["na tahu"] = "x"
    else: stav["na tahu"] = "o"

def vykresli_herni_plochu(stav):
    """
    Vykresluje aktuální hrací plochu.

    :param stav: slovník obsahující aktuální stav hry
    :type stav: dict
    Bez návratové funkce.
    """
    oddelovac = "=" * 44
    if stav["kolo"] != 1:
        print(oddelovac)
    print(
        f"""+---+---+---+
| {stav['pole 1']} | {stav['pole 2']} | {stav['pole 3']} |
+---+---+---+
| {stav['pole 4']} | {stav['pole 5']} | {stav['pole 6']} |
+---+---+---+
| {stav['pole 7']} | {stav['pole 8']} | {stav['pole 9']} |
+---+---+---+"""
    )

def vyhodnot_vyhru(stav):
    """
    Ověřuje, zda již někdo vyhrál, a přepisuje stav hry, pokud ano.

    :param stav: slovník obsahující aktuální stav hry
    :type stav: dict
    Bez návratové funkce.
    """
    overit = stav['na tahu']

    vyhra_1 = (stav["pole 1"] == overit, stav["pole 2"] == overit, stav["pole 3"] == overit)
    vyhra_2 = (stav["pole 4"] == overit, stav["pole 5"] == overit, stav["pole 6"] == overit)
    vyhra_3 = (stav["pole 7"] == overit, stav["pole 8"] == overit, stav["pole 9"] == overit)
    vyhra_4 = (stav["pole 1"] == overit, stav["pole 4"] == overit, stav["pole 7"] == overit)
    vyhra_5 = (stav["pole 2"] == overit, stav["pole 5"] == overit, stav["pole 8"] == overit)
    vyhra_6 = (stav["pole 3"] == overit, stav["pole 6"] == overit, stav["pole 9"] == overit)
    vyhra_7 = (stav["pole 1"] == overit, stav["pole 5"] == overit, stav["pole 9"] == overit)
    vyhra_8 = (stav["pole 3"] == overit, stav["pole 5"] == overit, stav["pole 7"] == overit)

    vitezne_kombinace = (all(vyhra_1), all(vyhra_2), all(vyhra_3), all(vyhra_4),
                         all(vyhra_5), all(vyhra_6), all(vyhra_7), all(vyhra_8),)

    oddelovac = "=" * 44
    if any(vitezne_kombinace):
        print(oddelovac + Fore.GREEN + f"\nCongratulations, the player {stav['na tahu']} WON!\n" + Style.RESET_ALL + oddelovac)
        stav["dohrano"] = "ano"

def dej_novou_hru(stav, stav_novy):
    """
    Ptá se hráče, jestli chce hrát další partii. Pokud ano, vynuluje stav hry. Pokud ne, ukončí aplikaci.

    :param stav: slovník obsahující aktuální stav hry
    :type stav: dict
    :return: slovník obsahující nový stav hry
    :rtype: dict
    """
    oddelovac = "=" * 44
    pripustne_volby = ["y", "n"]
    if stav["dohrano"] == "ne":
        nova_hra = input(oddelovac + Fore.YELLOW + "\nIt is a DRAW !!\n" + Style.RESET_ALL + oddelovac + "\nShall we play again? (y/n): ").lower()
    elif stav["dohrano"] == "ano":
        nova_hra = input("Shall we play again? (y/n): ").lower()
    while nova_hra not in pripustne_volby:
        nova_hra = input(Fore.RED + "Wrong input. Give me Yes or No." + Style.RESET_ALL + "\nShall we play again? (y/n): ").lower()
    if nova_hra == "y":
        print(Fore.BLUE + "\nLet's play a new one !\n" + Style.RESET_ALL)
        sleep(2)
        return stav_novy
    else:
        print("\nSee you next time...")
        sleep(2)
        exit()

# Hlavní funkce
def main():
    """
    Hlavní funkce. Definuje výchozí stav hry, inicializuje coloramu, obsahuje hlavní herní smyčku.
    Je tu víceméně jen proto, aby skript neobsahoval globální proměnné.

    Bez vstupu či výstupu.
    """
    stav_hry_novy = {"na tahu": "o",
            "pole x": list(),
            "pole o": list(),
            "kolo": 1, 
            "pole 1": " ",
            "pole 2": " ",
            "pole 3": " ",
            "pole 4": " ",
            "pole 5": " ",
            "pole 6": " ",
            "pole 7": " ",
            "pole 8": " ",
            "pole 9": " ",
            "dohrano": "ne"
            }
    
    init()

    stav_hry = deepcopy(stav_hry_novy)

    while True:
        if stav_hry["kolo"] == 1:
            zobraz_uvod()
            vykresli_herni_plochu(stav_hry)
        ziskej_volbu(stav_hry)
        vykresli_herni_plochu(stav_hry)
        vyhodnot_vyhru(stav_hry)
        zmen_hrace(stav_hry)
        if stav_hry["dohrano"] == "ano":
            stav_hry = deepcopy(dej_novou_hru(stav_hry, stav_hry_novy))
        elif stav_hry["kolo"] > 9:
            stav_hry = deepcopy(dej_novou_hru(stav_hry, stav_hry_novy))

# Aplikace
main()