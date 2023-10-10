import os
import random

folder_path = 'C:/Users/Jan/Desktop/discord_bot/blef/kenney_cards_large'

# Pobierz listę wszystkich elementów (plików i folderów) w folderze
items = os.listdir(folder_path)


def f(item):
    res = "nic" + str(random.randrange(99999999))
    item = str(item)
    if item[4] == 'C':
        if '9' in item:
            res = "9"
        if '10' in item:
            res = "10"
        if 'J' in item:
            res = "jopek"
        if 'Q' in item:
            res = "krolowa"
        if 'K' in item:
            res = "krol"
        if 'A' in item:
            res = "as"

        res+="_trefl"

    if item[4] == 'D':
        
        if '9' in item:
            res = "9"
        if '10' in item:
            res = "10"
        if 'J' in item:
            res = "jopek"
        if 'Q' in item:
            res = "krolowa"
        if 'K' in item:
            res = "krol"
        if 'A' in item:
            res = "as"


        res+="_karo"
    if item[4] == 'H':
        
        if '9' in item:
            res = "9"
        if '10' in item:
            res = "10"
        if 'J' in item:
            res = "jopek"
        if 'Q' in item:
            res = "krolowa"
        if 'K' in item:
            res = "krol"
        if 'A' in item:
            res = "as"


        res+="_kier"
    if item[4] == 'S':
        if '9' in item:
            res = "9"
        if '10' in item:
            res = "10"
        if 'J' in item:
            res = "jopek"
        if 'Q' in item:
            res = "krolowa"
        if 'K' in item:
            res = "krol"
        if 'A' in item:
            res = "as"
        

        res+="_pik"
    return res

# Iteruj się po elementach i wybierz tylko pliki
for item in items:
    item_path = os.path.join(folder_path, item)
    if os.path.isfile(item_path):
        os.rename(item, f(item))
        #print(item)