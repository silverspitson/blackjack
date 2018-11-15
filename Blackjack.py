#TODO
#Pygame või muu GUI sisse tuua, vb tkinter parem
#Bettimine teha

#from pygame import *
from random import randint

def ekraan():
    #jamasin natuke ekraani tekitamisega pygame abil; sittagi ei saa aru pmst
#    display.init()
    display.set_mode((1000,600))
    
    pilt = image.load("download.bmp")
#    pilt = pilt.convert()
    pilt = image.tostring(pilt, "RGBX")
    image.fromstring(pilt, (100,100), "RGBX")

#    font.init()
#    #print(font.get_fonts())
#    Font = font.SysFont("arial", 15)
#    tekst = font.Font(Font, 15)
#    font.Font.render(tekst)

def generator(): #genereerib random numbri vahemikus 0-51(kaardi indeksid listis)
    kaardiNr = randint(0, 51)
    return kaardiNr

#kontrollib, kas kaart on juba võetud(genereeritud) või mitte
def checker(nr):
#    global genereeritud
    if nr in genereeritud:
        return True
    return False

#võtab kaardi listist, veendudes, et seda pole veel võetud
def kaart():
    kaardiNr = generator()
    while checker(kaardiNr):
        kaardiNr = generator()
    kaart = kaardid[kaardiNr]
    genereeritud.append(kaart)
    return kaart

#annab ette antud kaardi väärtuse(arvestab ka kelle kaart see on, et käe summat jälgida)
def väärtus(kaart, omanik):
    global mSumma
    global dSumma
    if kaart in väärtused: #kui see pole äss, annab lihtsalt selle väärtuse sõnastiku abil
        väärtus = väärtused[kaart]
        return väärtus
    else: #kui see kaart on äss, siis olenevalt praegusest käe summast, määrab, kas 1 või 11
        if omanik == "D":
            if dSumma+11 > 21:
                väärtus = 1
            else:
                väärtus = 11
            return väärtus
        if omanik == "M":
            if mSumma+11 > 21:
                väärtus = 1
            else:
                väärtus = 11
            return väärtus

#algusfaas, annab mängijale 2 kaarti ja siis diilerile 2 kaarti
def algus():
    global mSumma
    global dSumma
    global dSumma_üksik
    card = kaart()
    mSumma += väärtus(card, "M")
    mKaardid.append(card)
    card = kaart()
    mSumma += väärtus(card, "M")
    mKaardid.append(card)

    card = kaart()
    dSumma += väärtus(card, "D")
    dSumma_üksik = dSumma
    dKaardid.append(card)
    card = kaart()
    dSumma += väärtus(card, "D")
    dKaardid.append(card)

    print("Mängija kaartide summa on: " + str(mSumma) + ". Mängija kaardid: " + str(mKaardid))
    print("Diileri kaartide summa on: " + str(dSumma_üksik) + ". Diileri kaardid: " + str(dKaardid[0]))
#kui mängija tahab kaarti juurde saada
def hit():
    global mSumma
    global mKaardid
    global dSumma_üksik
    global dKaardid

    card  = kaart()
    mKaardid.append(card)
    mSumma += väärtus(card, "M")
    print("Mängija kaartide summa on: " + str(mSumma) + ". Mängija kaardid: "+str(mKaardid))
    print("Diileri kaartide summa on: " + str(dSumma_üksik) + ". Diileri kaardid: " + str(dKaardid[0]))

    if mSumma == 21:
        print("Said blackjacki! Oled võitnud!")
        jätk()
    if mSumma > 21:
        print("Läksid lõhki. Kaotasid mängu.")
        jätk()
#kui mängija ei taha kaarti juurde
def stand():
    global dSumma
    global dKaardid
    global mSumma
    print("Diileri kaartide summa: " + str(dSumma) + ". Diileri kaardid: " + str(dKaardid))
    #diiler võtab kaarte kuni ta käe summa on vähemalt 17
    while dSumma<17:
        card = kaart()
        dSumma += väärtus(card, "D")
        dKaardid.append(card)
        print("Diileri kaartide summa: "+str(dSumma)+". Diileri kaardid: "+str(dKaardid))

    #võidu ja kaotamise tingimused
    if dSumma == 21:
        print("Diiler sai blackjacki. Kaotasid mängu.")
    if dSumma > 21:
        print("Diiler läks lõhki. Võitsid mängu!")
    if dSumma < 21:
        if dSumma < mSumma:
            print("Sinu käsi on diileri omast parem. Võitsid mängu!")
        if dSumma > mSumma:
            print("Diileri käsi on sinu omast parem. Kaotasid mängu.")
        if dSumma == mSumma:
            print("Jäid viiki")
    jätk()

#ksib peale mängu lõppu, kas mängija tahab uut mängu või mitte
def jätk():
    global running
    vastus = input("Tahad edasi mängida? Jah või ei: ")
    if vastus.lower().strip() == "jah":
        running = False
    if vastus.lower().strip() == "ei":
        exit()

#algsed listid
kaardid = ["Poti 2","Ärtu 2","Risti 2","Ruutu 2","Poti 3","Ärtu 3","Risti 3","Ruutu 3","Poti 4","Ärtu 4","Risti 4","Ruutu 4","Poti 5","Ärtu 5","Risti 5","Ruutu 5","Poti 6","Ärtu 6","Risti 6","Ruutu 6","Poti 7","Ärtu 7","Risti 7","Ruutu 7","Poti 8","Ärtu 8","Risti 8","Ruutu 8","Poti 9","Ärtu 9","Risti 9","Ruutu 9","Poti 10","Ärtu 10","Risti 10","Ruutu 10","Poti poiss","Ärtu poiss","Risti poiss","Ruutu poiss","Poti emand","Ärtu emand","Risti emand","Ruutu emand","Poti kuningas","Ärtu kuningas","Risti kuningas","Ruutu kuningas","Poti äss","Ärtu äss","Risti äss","Ruutu äss"]
väärtused = {"Poti 2": 2,"Ärtu 2": 2,"Risti 2": 2,"Ruutu 2": 2,"Poti 3": 3,"Ärtu 3": 3,"Risti 3": 3,"Ruutu 3": 3,"Poti 4": 4,"Ärtu 4": 4,"Risti 4": 4,"Ruutu 4": 4,"Poti 5": 5,"Ärtu 5": 5,"Risti 5": 5,"Ruutu 5": 5,"Poti 6": 6,"Ärtu 6": 6,"Risti 6": 6,"Ruutu 6": 6,"Poti 7": 7,"Ärtu 7": 7,"Risti 7": 7,"Ruutu 7": 7,"Poti 8": 8,"Ärtu 8": 8,"Risti 8": 8,"Ruutu 8": 8,"Poti 9": 9,"Ärtu 9": 9,"Risti 9": 9,"Ruutu 9": 9,"Poti 10": 10,"Ärtu 10": 10,"Risti 10": 10,"Ruutu 10": 10,"Poti poiss": 10,"Ärtu poiss": 10,"Risti poiss": 10,"Ruutu poiss": 10,"Poti emand": 10,"Ärtu emand": 10,"Risti emand": 10,"Ruutu emand": 10,"Poti kuningas": 10,"Ärtu kuningas": 10,"Risti kuningas": 10,"Ruutu kuningas": 10}
mKaardid = [] #mängija kaardid
dKaardid = [] #diileri kaardid
kaardiNr = []
genereeritud = [] #juba võetud kaartide numbrid

#kogu mängu tsükkel, jookseb kuni programm töötab
while True:
    #enne mängu algust tehtav faas(algfaas)
    running = True
    dSumma = 0
    mSumma = 0
    dSumma_üksik = 0
    dKaardid.clear()
    mKaardid.clear()
    algus()

    if mSumma == 21:
        print("Said naturaalse blackjacki, oled võitnud!")
        jätk()
    if dSumma == 21:
        print("Diiler sai naturaalse blackjacki, oled kaotanud.")
        jätk()

    #kui mäng niiöelda käib
    while running:
        vastus = input("Mida tahad edasi teha? hit või stand: ")
        if vastus.lower().strip() == "hit":
            hit()
        if vastus.lower().strip() == "stand":
            stand()
