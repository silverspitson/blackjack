from random import randint
from tkinter import *
import time

#Kogu graafiline liides
class GUI:
    def __init__(self, master):
        frame_master = Frame(master,bg="#acff7c")
        frame_master.pack(fill="both",side=TOP,anchor=CENTER, expand=YES)

        self.mängija = Label(frame_master,text="MÄNGIJA",font=("Bahnschrift",24),bg="#acff7c")
        self.mängija.grid(row=0,columnspan=2)
        self.diiler = Label(frame_master, text="DIILER",font=("Bahnschrift",24),bg="#acff7c")
        self.diiler.grid(row=5,columnspan=2)

        self.kaardid_d = Label(frame_master, text="Diileri kaardid: ",font=("Bahnschrift",12),bg="#acff7c")
        self.kaardid_d.grid(row=6,sticky=W,columnspan=2)
        self.summa_d = Label(frame_master, text="Diileri kaartide summa: ",font=("Bahnschrift",12),bg="#acff7c")
        self.summa_d.grid(row=7,sticky=W,columnspan=2)
        self.kaardid_m = Label(frame_master, text="Mängija kaardid: ",font=("Bahnschrift",12),bg="#acff7c")
        self.kaardid_m.grid(row=1,sticky=W,columnspan=2)
        self.summa_m = Label(frame_master, text="Mängija kaartide summa: ",font=("Bahnschrift",12),bg="#acff7c")
        self.summa_m.grid(row=2,sticky=W,columnspan=2)
        self.raha = Label(frame_master, text="Praegune raha: "+str(rahakott),font=("Bahnschrift",12),bg="#acff7c")
        self.raha.grid(row=3,sticky=W,columnspan=2)

        self.teade = Label(frame_master,text="",font=("Bahnschrift",12),bg="#acff7c")
        self.teade.grid(row=8,column=0, columnspan=2)
        self.nupp_hit = Button(frame_master,text="Hit",command=self.cmd1,font=("Bahnschrift"),bg="#fcba20",padx=100)
        self.nupp_hit.grid(row=9,column=0,sticky=W+E)
        self.nupp_stand = Button(frame_master,text="Stand",command=self.cmd2,font=("Bahnschrift"),bg="#fcba20",padx=100)
        self.nupp_stand.grid(row=9,column=1,sticky=W+E)
        self.nupp_bet = Button(frame_master,text="Panusta",command=self.cmd3,font=("Bahnschrift"),bg="#fcba20")
        self.nupp_bet.grid(row=10,column=0,sticky=W+E)
        self.e = Entry(frame_master)
        self.e.grid(row=10,column=1,sticky=W+E)

        #infobox
        global readme
        readme = Toplevel(root)
        readme.title("Info")
        readme.geometry("500x115")
        self.tekst = Label(readme,text="Mõned märkused reeglite ja mängu kohta:\n"
                                       "Diiler võtab kaarte seni, kuni ta käe väärtus on vähemalt 17\n"
                                       "Enne mängu algust, pead panustama ehk vajutama nuppu \"Panusta\"\n"
                                       "Panuse võitmisel saad selle kahekordselt tagasi",font=("Bahnschrift"))
        self.tekst.grid()
        self.nupp = Button(readme,text="Ok",command=self.ok,font=("Bahnschrift"))
        self.nupp.grid()

    def cmd1(self): #hit
        if bet_made == False:
            return
        hit()
    def cmd2(self): #stand
        if bet_made == False:
            return
        stand()
    def cmd3(self): #panustamine
        global bet_made
        global panus
        global rahakott
        try:
            panus = int(graafika.e.get())
        except:
            return
        if panus <= 0 or panus > rahakott:
            return
        graafika.e.delete(0, END)
        bet_made = True
    def uus_aken(self): #Peale mängu jätkamise küsimus
        global aken
        aken = Toplevel(root)
        self.tekst = Label(aken, text="Kas tahad alustada uut mängu?",font=("Bahnschrift"))
        self.tekst.grid(columnspan=2)
        self.yes = Button(aken,text="Jah",command=self.jah,font=("Bahnschrift"))
        self.yes.grid(row=1)
        self.no = Button(aken,text="Ei",command=self.ei,font=("Bahnschrift"))
        self.no.grid(row=1,column=1)

    def jah(self):
        global running
        global aken
        running = False
        aken.destroy()
    def ei(self):
        root.destroy()
        exit()
    def ok(self):
        global readme
        readme.destroy()

#uuendab kõiki tekste graafilisel liidesel uute andmetega
def GUI_update():
    graafika.kaardid_d.config(text="Diileri kaardid: " + str(dKaardid))
    graafika.summa_d.config(text="Diileri kaartide summa: " + str(dSumma))
    graafika.kaardid_m.config(text="Mängija kaardid: " + str(mKaardid))
    graafika.summa_m.config(text="Mängija kaartide summa: " + str(mSumma))
    graafika.raha.config(text="Praegune raha: "+str(rahakott))

def generator(): #genereerib random numbri vahemikus 0-51(kaardi indeksid listis)
    kaardiNr = randint(0, 51)
    return kaardiNr

#kontrollib, kas kaart on juba võetud(genereeritud) või mitte
def checker(nr):
    global genereeritud
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
    global panus
    global rahakott
    if rahakott <= 0:
        graafika.teade.config(text="Sul sai raha otsa, mine koju")

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

#kui mängija tahab kaarti juurde saada
def hit():
    global mSumma
    global mKaardid
    global dSumma_üksik
    global dKaardid
    global panus
    global rahakott
    card  = kaart()
    mKaardid.append(card)
    mSumma += väärtus(card, "M")

    if mSumma == 21:
        rahakott += panus
        GUI_update()
        graafika.teade.config(text="Said blackjacki! Oled võitnud!")
        jätk()

    if mSumma > 21:
        rahakott -= panus
        GUI_update()
        graafika.teade.config(text="Läksid lõhki. Kaotasid mängu.")
        jätk()

#kui mängija ei taha kaarti juurde
def stand():
    global dSumma
    global dKaardid
    global mSumma
    global panus
    global rahakott
    GUI_update()

    #diiler võtab kaarte kuni ta käe summa on vähemalt 17
    while dSumma<17:
        card = kaart()
        dSumma += väärtus(card, "D")
        dKaardid.append(card)
        GUI_update()

    #võidu ja kaotamise tingimused
    if dSumma == 21:
        rahakott -= panus
        GUI_update()
        graafika.teade.config(text="Diiler sai blackjacki. Kaotasid mängu.")
    if dSumma > 21:
        rahakott += panus
        GUI_update()
        graafika.teade.config(text="Diiler läks lõhki. Võitsid mängu!")
    if dSumma < 21:
        if dSumma < mSumma:
            rahakott += panus
            GUI_update()
            graafika.teade.config(text="Sinu käsi on diileri omast parem. Võitsid mängu!")
        if dSumma > mSumma:
            rahakott -= panus
            GUI_update()
            graafika.teade.config(text="Diileri käsi on sinu omast parem. Kaotasid mängu.")
        if dSumma == mSumma:
            GUI_update()
            graafika.teade.config(text="Jäid viiki")
    jätk()

#küsib peale mängu lõppu, kas mängija tahab uut mängu või mitte
def jätk():
    graafika.uus_aken()

#algsed listid
kaardid = ["Poti 2","Ärtu 2","Risti 2","Ruutu 2","Poti 3","Ärtu 3","Risti 3","Ruutu 3","Poti 4","Ärtu 4","Risti 4","Ruutu 4","Poti 5","Ärtu 5","Risti 5","Ruutu 5","Poti 6","Ärtu 6","Risti 6","Ruutu 6","Poti 7","Ärtu 7","Risti 7","Ruutu 7","Poti 8","Ärtu 8","Risti 8","Ruutu 8","Poti 9","Ärtu 9","Risti 9","Ruutu 9","Poti 10","Ärtu 10","Risti 10","Ruutu 10","Poti poiss","Ärtu poiss","Risti poiss","Ruutu poiss","Poti emand","Ärtu emand","Risti emand","Ruutu emand","Poti kuningas","Ärtu kuningas","Risti kuningas","Ruutu kuningas","Poti äss","Ärtu äss","Risti äss","Ruutu äss"]
väärtused = {"Poti 2": 2,"Ärtu 2": 2,"Risti 2": 2,"Ruutu 2": 2,"Poti 3": 3,"Ärtu 3": 3,"Risti 3": 3,"Ruutu 3": 3,"Poti 4": 4,"Ärtu 4": 4,"Risti 4": 4,"Ruutu 4": 4,"Poti 5": 5,"Ärtu 5": 5,"Risti 5": 5,"Ruutu 5": 5,"Poti 6": 6,"Ärtu 6": 6,"Risti 6": 6,"Ruutu 6": 6,"Poti 7": 7,"Ärtu 7": 7,"Risti 7": 7,"Ruutu 7": 7,"Poti 8": 8,"Ärtu 8": 8,"Risti 8": 8,"Ruutu 8": 8,"Poti 9": 9,"Ärtu 9": 9,"Risti 9": 9,"Ruutu 9": 9,"Poti 10": 10,"Ärtu 10": 10,"Risti 10": 10,"Ruutu 10": 10,"Poti poiss": 10,"Ärtu poiss": 10,"Risti poiss": 10,"Ruutu poiss": 10,"Poti emand": 10,"Ärtu emand": 10,"Risti emand": 10,"Ruutu emand": 10,"Poti kuningas": 10,"Ärtu kuningas": 10,"Risti kuningas": 10,"Ruutu kuningas": 10}
mKaardid = [] #mängija kaardid
dKaardid = [] #diileri kaardid
kaardiNr = []
genereeritud = [] #juba võetud kaartide numbrid
panus = 0
rahakott = 1000

#GUI initializing faas
root = Tk()
root.geometry("600x310")
root.title("Blackjack")
graafika = GUI(root)

#kogu mängu tsükkel, jookseb kuni programm töötab
while True:

    #enne mängu algust tehtav faas(algfaas)
    running = True
    bet_made = False
    dSumma = 0
    mSumma = 0
    dSumma_üksik = 0
    dKaardid.clear()
    mKaardid.clear()

    graafika.kaardid_d.config(text="Diileri kaardid: " )
    graafika.summa_d.config(text="Diileri kaartide summa: ")
    graafika.kaardid_m.config(text="Mängija kaardid: " )
    graafika.summa_m.config(text="Mängija kaartide summa: ")
    graafika.teade.config(text="")

    algus()
    #kuni pole panustatud, ei lähe edasi(ehk ei näita kaarte ega käe summasid)
    while bet_made == False:
        root.update_idletasks()
        root.update()
        continue

    #paneb ekraanile diileri ühe avaliku kaardi ja selle väärtuse
    graafika.kaardid_d.config(text="Diileri kaardid: " + str(dKaardid[0]))
    graafika.summa_d.config(text="Diileri kaartide summa: " + str(dSumma_üksik))

    if mSumma == 21:
        rahakott += panus
        GUI_update()
        graafika.teade.config(text="Said naturaalse blackjacki, oled võitnud!")
        jätk()
    if dSumma == 21:
        rahakott -= panus
        GUI_update()
        graafika.teade.config(text="Diiler sai naturaalse blackjacki, oled kaotanud.")
        jätk()

    #kui mäng niiöelda käib
    while running:
        root.update_idletasks()
        root.update()

        graafika.kaardid_m.config(text="Mängija kaardid: " + str(mKaardid))
        graafika.summa_m.config(text="Mängija kaartide summa: " + str(mSumma))