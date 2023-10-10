import discord
from discord.ext import commands
import logging
import random
from source import * 
from dataclasses import *
from stats import *
from functools import cmp_to_key
#import numpy as np

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
bot = commands.Bot('!', intents=intents)



class Channels():
    def __init__(self) -> None:
        self.allowed = [ch1,ch2]

channels = Channels()
#cards = open("kenney_cards_large/cardClubs2.png",'rb').
    
# channels = Channels(1140997146234069063,1140997171622191165,1140997190819532810) #1st kanal to kanal do grania 

kolory = ["pik","trefl","karo","kier"]
wartosci = ["9","10","jopek","krolowa","krol","as"]
uklady = ["najwyzsza","para","straight","trojka","full","kolor","kareta","poker"]
wielkosci = ["maly","duzy"]


class Game():
    def __init__(self,liczba_graczy,gracze) -> None:
        self.max_cards = min(23//liczba_graczy,6)
        self.l_zywych_graczy = liczba_graczy
        self.gracze = gracze
        self.kolej = 0
        self.round = 1
        self.ostatni_bet = None
        self.on = 0

        self.deck = []
        for znak in kolory:
            for wartosc in wartosci:
                self.deck.append((wartosc,znak))

        self.curr_deck = self.deck #czego nie ma na stole
        self.stol = [] #polaczenie rak wszystkich graczy


gracze = {} #profil dicord -> (liczba kart,reka gracza)





# @bot.event
# async def on_ready():
#     serwer = bot.get_guild(id_serwera)


def utworz_rece():
    for gracz in game.gracze:
        gracze[gracz] = (1,None)


def custom_compare(x,y):
    if wartosci.index(x[0]) == wartosci.index(y[0]):
        if kolory.index(x[1]) > kolory.index(y[1]):
            return 1
        else:
            return -1
    else:
        if wartosci.index(x[0]) > wartosci.index(y[0]):
            return 1
        else:
            return -1
        
#await ctx.send(file = discord.File(open("kenney_cards_large/cardClubs2.png", 'rb')))
async def wyslij_png(cos,gracz):
    cos.sort(key = cmp_to_key(custom_compare))

    pom = []

    for mess in cos:
        #return f"{mess[0]}_{mess[1]}.png"
        await gracz.send(file = discord.File(open(f"kenney_cards_large/{mess[0]}_{mess[1]}.png", 'rb')))
        
    #pom.append(discord.File(open(f"kenney_cards_large/{mess[0]}_{mess[1]}.png", 'rb')))
    #await gracz.send(files = pom)

    #print(f"{mess[0]}_{mess[1]}.png")



def konwersja(cos):
    cos.sort(key = cmp_to_key(custom_compare))
    res = []
    for x in cos:
        res.append(' '.join(x))
    
    res2 = []

    res2 = '\n'.join(res)

    #print(cos)

    return '-----------------\n'+res2+'\n-----------------'
    #return konwersja_na_png(cos)

async def rozdaj_rece():
    game.stol.clear()
    for gracz in game.gracze:
        losuj = []
        for i in range(gracze[gracz][0]):
            krotka = random.choice(game.curr_deck)
            game.curr_deck.remove(krotka)
            losuj.append(krotka)
        
        #print(losuj)

        gracze[gracz] = (gracze[gracz][0],losuj)
        #game.curr_deck = [x for x in game.curr_deck if x not in losuj[:gracze[gracz][0]]]
        game.stol += losuj
    for gracz in game.gracze:
        #await gracz.send(konwersja(gracze[gracz][1]))
        #print(f"kenney_cards_large/{konwersja(gracze[gracz][1])}")
       # await gracz.send(file = discord.File(open(f"kenney_cards_large/{konwersja(gracze[gracz][1])}", 'rb')))
        await wyslij_png(gracze[gracz][1],gracz)



@bot.command()
async def start(ctx, *gracze_inp:discord.Member):
    global gracze
    global game
    if ctx.channel.id not in channels.allowed:
        await ctx.send(f"Write on a right channel")
        return

    #print(f"Gra {il_osob} osób!")
    gracze.clear()
    gracze_inp = list(gracze_inp)
    il_osob = len(gracze_inp)
    random.shuffle(gracze_inp) #później zamienic na bez komentarza
    #await ctx.send(gracze)
    game = Game(il_osob,gracze_inp)
    game.on = True
    random.shuffle(game.deck)
    if il_osob == 1:
        await ctx.send(f"Gra {il_osob} osoba!")
    elif il_osob <=4:
        await ctx.send(f"Grają {il_osob} osoby!")
    else:
        await ctx.send(f"Gra {il_osob} osób!")
    await ctx.send(f"Max cards on hand: {game.max_cards}")
    await ctx.send(f"ROUND {game.round}")
    await ctx.send(f"Player {game.gracze[game.kolej].name} turn")
    utworz_rece()
    await rozdaj_rece()
    #print(game.stol)
    # for gracz in game.gracze:
    #     await gracz.send(konwersja(gracze[gracz][1]))

def poprawny_bet(bet):
    if len(bet) == 2:
        if bet[0] in {"straight"}:
            if bet[1] in wielkosci:
                return True
        if bet[0] in {"najwyzsza","para","trojka","kareta"}:
            if bet[1] in wartosci:
                return True
        if bet[0] == "kolor":
            if bet[1] in kolory:
                return True
    if len(bet) == 3:
        if bet[0] == "full":
            if bet[1] in wartosci and bet[2] in wartosci and bet[1] != bet[2]:
                return True
        if bet[0] == "poker":
            if bet[1] in wielkosci and bet[2] in kolory:
                return True
        
        


    return False

def czy_wyzszy_bet(nowy_bet,stary_bet):
    nowy_ukl = nowy_bet[0]
    stary_ukl = stary_bet[0]

    nowy_cos = nowy_bet[1]
    stary_cos = stary_bet[1]

    if nowy_ukl == stary_ukl:
        if nowy_ukl in {"straight"}:
            return wielkosci.index(nowy_cos) > wielkosci.index(stary_cos)
        if nowy_ukl in {"najwyzsza","para","trojka","kareta"}:
            return wartosci.index(nowy_cos) > wartosci.index(stary_cos)
        if nowy_ukl == "kolor":
            return kolory.index(nowy_cos) > kolory.index(stary_cos)
        if nowy_ukl == "full":
            if wartosci.index(nowy_cos) > wartosci.index(stary_cos):
                return True
            elif wartosci.index(nowy_cos) == wartosci.index(stary_cos):
                return wartosci.index(nowy_bet[2]) > wartosci.index(stary_bet[2])
            else:
                return False
        if nowy_ukl == "poker":
            if wielkosci.index(nowy_cos) > wielkosci.index(stary_cos):
                return True
            elif wielkosci.index(nowy_cos) == wielkosci.index(stary_cos):
                return kolory.index(nowy_bet[2]) > kolory.index(stary_bet[2])
            else:   
                return False
    else:
        return uklady.index(nowy_ukl) > uklady.index(stary_ukl)


        # for i in range(len(uklady)):
        #     if uklady[i] == nowy_ukl:
        #         wart = i
        #         break
        # for i in range(len(uklady)):
        #      if uklady[i] == stary_ukl:
        #          if wart > i:
        #              return True
        #          else:
        #              return False

#uklady = ["najwyzsza","para","straight","trojka","full","kolor","kareta","poker"]
#wartosci = ["9","10","jopek","krolowa","krol","as"]



def alias(mess):

    for i in range(len(mess)):
        mess[i] = mess[i].lower()


    if mess[0] in {"n","naj"}:
        mess[0] = "najwyzsza"
    if mess[0] in {"p","par","pa"}:
        mess[0] = "para"
    if mess[0] in {"s","str"}:
        mess[0] = "straight"
    if mess[0] in {"t","tro"}:
        mess[0] = "trojka"
    if mess[0] in {"f","fool"}:
        mess[0] = "full"
    if mess[0] in {"ko","kol"}:
        mess[0] = "kolor"
    if mess[0] in {"ka","kar"}:
        mess[0] = "kareta"
    if mess[0] in {"po","pok"}:
        mess[0] = "poker"

    for i in range(1,len(mess)):
        if mess[i] in {"j","jop","walet","wal","w"}:
            mess[i] = "jopek"
        if mess[i] in {"q","dama","d","queen"}:
            mess[i] = "krolowa"
        if mess[i] in {"k","kr"}:
            mess[i] = "krol"
        if mess[i] in {"a"}:
            mess[i] = "as"
    return mess
    # if len(mess) == 3:
    #     if mess[2] in {"j","jop","walet","wal","w"}:
    #         mess[2] = "jopek"
    #     if mess[2] in {"q","dama","d","queen"}:
    #         mess[2] = "krolowa"
    #     if mess[2] in {"k","kr"}:
    #         mess[2] = "krol"
    #     if mess[2] in {"a"}:
    #         mess[2] = "as"
    


# @bot.command(aliases = ['u',"ukl"])
# async def uklad(ctx):

    
#def konwersja_beta



@bot.command(aliases = ['p'])
async def przebij(ctx,*message:str):
    if ctx.channel.id not in channels.allowed:
        await ctx.send(f"Write on a right channel")
        return
    if game.on == False:
        return
    message = list(message)
    message = alias(message)
    print(message)
    await ctx.send(f"Hand:\n {message}")

    if ctx.author == game.gracze[game.kolej]:
        if poprawny_bet(message):
            #await ctx.send("Poprawny uklad")

            if game.ostatni_bet == None:
                game.ostatni_bet = message
                game.kolej +=1
                game.kolej %= game.l_zywych_graczy
                await ctx.send(f"Player {game.gracze[game.kolej].name} turn")
            elif czy_wyzszy_bet(message,game.ostatni_bet):
                game.ostatni_bet = message
                game.kolej +=1
                game.kolej %= game.l_zywych_graczy
                await ctx.send(f"Player {game.gracze[game.kolej].name} turn")
            else:
                await ctx.send("This bet is too low bet")

            

            # uklad = message[0]
            # poprzedni_uklad = game.ostatni_bet[0]

            # for i in range(len(uklady)):


            # if uklad in uklady:
            #     if uklad. 
        else:
            await ctx.send("Wrong bet")
    else:
        await ctx.send("It is not your turn")




def konw_z_beta(bet):
    if len(bet) == 2:
        if bet[0] == "najwyzsza":
            return [bet[1]]
        if bet[0] == "para":
            return [bet[1]]*2
        if bet[0] == "straight":
            if bet[1] == "maly":
                return wartosci[:len(wartosci)-1]
            else:
                return wartosci[1:]
        if bet[0] == "trojka":
            return [bet[1]]*3
        if bet[0] == "kolor":
            return [bet[1]]*5
        if bet[0] == "kareta":
            return [bet[1]]*4
        
    if len(bet) == 3:
        if bet[0] == "full":
            return [bet[1]]*3 + [bet[2]]*2
            
def konw_ze_stolu(stol):
    res = []
    for x in stol:
        res.append(x[0])
        res.append(x[1])
    return res


@bot.command()
async def najwyzsza(ctx):
    if ctx.channel.id not in channels.allowed:
        await ctx.send(f"Write on a right channel")
        return
    if game.on == False:
        return

@bot.command(aliases = ["k"])
async def karty(ctx,kto:discord.Member):
    if game.on == False:
        return
    if gracze[kto][0] == 1:
        await ctx.send(f"{kto.name} has {gracze[kto][0]} card :)")
    elif gracze[kto][0] <=4:
        await ctx.send(f"{kto.name} has {gracze[kto][0]} cards :)")
    else:
        await ctx.send(f"{kto.name} has {gracze[kto][0]} cards  :)")
    #await ctx.send(f"{kto.name} ma {gracze[kto][0]} kart :)")



@bot.command()
async def send_png(ctx):
    await ctx.send(file = discord.File(open("kenney_cards_large/cardClubs2.png", 'rb')))


def spr_poker():
    obet = game.ostatni_bet
    bet = []
    if obet[1] == "maly":
        for i in range(len(wartosci)-1):
            bet.append((wartosci[i],obet[2]))
    else:
        for i in range(1,len(wartosci)):
            bet.append((wartosci[i],obet[2]))
    
    # print(bet)
    # print(game.stol)

    return all(element in game.stol for element in bet)

@bot.command(aliases = ['s'])
async def sprawdzam(ctx):
    if ctx.channel.id not in channels.allowed:
        await ctx.send(f"Write on a right channel")
        return
    if game.on == False:
        return

    if ctx.author == game.gracze[game.kolej]:
        if game.ostatni_bet == None:
            await ctx.send(f"There is no bet")
            return
        
        czy = True
        if game.ostatni_bet[0] != "poker":
            kbet = konw_z_beta(game.ostatni_bet)
            kstol = konw_ze_stolu(game.stol)
            # print(game.ostatni_bet)
            # print(game.stol)



            for x in kbet:
                if x in kstol:
                    kstol.remove(x)
                else:
                    czy = False

        else:
            czy = spr_poker()

        #await ctx.send(f"Na stole jest:\n{konwersja(game.stol)}")
        await ctx.send(f"Table:")
        #await ctx.send(file = discord.File(open(f"kenney_cards_large/{konwersja(game.stol)}", 'rb')))
        await wyslij_png(game.stol,ctx)
        if czy:
            await ctx.send("You lose")
        else:
            await ctx.send("You win")
            game.kolej -=1
            game.kolej %= game.l_zywych_graczy

        gracze[game.gracze[game.kolej]] = (gracze[game.gracze[game.kolej]][0]+1,gracze[game.gracze[game.kolej]][1])
        if gracze[game.gracze[game.kolej]][0] > game.max_cards:
            await ctx.send(f"Gracz {game.gracze[game.kolej].name} umiera")
            game.gracze.pop(game.kolej)
            game.l_zywych_graczy-=1
            game.max_cards = min(23//game.l_zywych_graczy,6)
            await ctx.send(f"Current max cards on hands {game.max_cards}")
            game.kolej -=1
            game.kolej %= game.l_zywych_graczy

            if len(game.gracze) == 1:
                await ctx.send(f"{game.gracze[0].name} wins!")
                await ctx.send(f"{game.gracze[0].name} wins!!")
                await ctx.send(f"{game.gracze[0].name} wins!!!")
                game.on = False
                return


        game.ostatni_bet = None
        game.round +=1
        game.curr_deck = game.deck.copy()
        await ctx.send(f"Round {game.round}")
        await ctx.send(f"Player {game.gracze[game.kolej].name} turn")
        await rozdaj_rece()


    else:
        await ctx.send("Not your round")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Command not found")
        #await ctx.send(insults[random.randrange(len(insults))])


bot.run(TOKEN)