import math
from random import randrange
import tkinter as tk
from tkinter import *
from tkinter import ttk
import os

root = Tk()
root.title("Santorini")

canvas = Canvas(root, height=665, width=665, bg="#173c4f")
canvas.pack()

komande = Label(root, height=100, width=665)
komande.pack()

def clickMe():
    global AIP1
    global AIP2
    global AIP1difficulty
    global AIP2difficulty
    global korak
    global naPotezu

    if P1choice.get() == '' and P2choice.get() == '':
        print('Greska! Niste izabrali igrace.')
        korak = 99

    if P1choice.get() == 'Player 1':
        AIP1 = False
        korak = 0
    if P1choice.get() == 'AI Easy':
        AIP1 = True
        AIP1difficulty = 'Easy'
        initAI(Igrac1.figura1)
        initAI(Igrac1.figura2)
        korak = 0
    if P1choice.get() == 'AI Medium':
        AIP1 = True
        AIP1difficulty = 'Medium'
        initAI(Igrac1.figura1)
        initAI(Igrac1.figura2)
        korak = 0
    if P1choice.get() == 'AI Hard':
        AIP1 = True
        AIP1difficulty = 'Hard'
        initAI(Igrac1.figura1)
        initAI(Igrac1.figura2)
        korak = 0
    if P2choice.get() == 'Player 2':
        AIP2 = False
        korak = 0
    if P2choice.get() == 'AI Easy':
        AIP2 = True
        AIP2difficulty = 'Easy'
    if P2choice.get() == 'AI Medium':
        AIP2 = True
        AIP2difficulty = 'Medium'
    if P2choice.get() == 'AI Hard':
        AIP2 = True
        AIP2difficulty = 'Hard'

def zavrsiIgru():
    global korak
    print('Igrica zaustavljena!')

    korak = 99


P1choice = StringVar()
P2choice = StringVar()

comboP1 = ttk.Combobox(komande, width=15, state="readonly", textvariable=P1choice, values=("Player 1", "AI Easy", "AI Medium", "AI Hard")).grid(column=0, row=0)
lbl1 = Label(komande, width="7", height="5").grid(column=1, row=0)
comboP2 = ttk.Combobox(komande, width=15, state="readonly", textvariable=P2choice, values=("Player 2", "AI Easy", "AI Medium", "AI Hard")).grid(column=2, row=0)
lbl2 = Label(komande, width="7", height="5").grid(column=3, row=0)
proba2 = Button(komande, text="Igraj!", padx=20, pady=10, bg="#173c4f", fg="white", command=clickMe).grid(column=4, row=0)
lbl3 = Label(komande, width="7", height="5").grid(column=5, row=0)
krajDugme = Button(komande, text="Zavrsi!", padx=20, pady=10, bg="red", fg="white", command=zavrsiIgru).grid(column=6, row=0)

tabla = Frame(root, bg="white")
tabla.place(relx=0.05, rely=0.05)

# Slike
# polja bez igraca
pp = PhotoImage(file=r"../assets/praznopolje.gif")
jp = PhotoImage(file=r"../assets/1plocica.gif")
dp = PhotoImage(file=r"../assets/2plocice.gif")
tp = PhotoImage(file=r"../assets/3plocice.gif")
kp = PhotoImage(file=r"../assets/kupola.gif")

# P1
p1pp = PhotoImage(file=r"../assets/0p1.gif")
p1jp = PhotoImage(file=r"../assets/1p1.gif")
p1dp = PhotoImage(file=r"../assets/2p1.gif")
p1tp = PhotoImage(file=r"../assets/3p1.gif")

# P2
p2pp = PhotoImage(file=r"../assets/0p2.gif")
p2jp = PhotoImage(file=r"../assets/1p2.gif")
p2dp = PhotoImage(file=r"../assets/2p2.gif")
p2tp = PhotoImage(file=r"../assets/3p2.gif")

# Highlight
pph = PhotoImage(file=r"../assets/pph.gif")
jph = PhotoImage(file=r"../assets/jph.gif")
dph = PhotoImage(file=r"../assets/dph.gif")
tph = PhotoImage(file=r"../assets/tph.gif")
p2pph = PhotoImage(file=r"../assets/p2pph.gif")
p2jph = PhotoImage(file=r"../assets/p2jph.gif")
p2dph = PhotoImage(file=r"../assets/p2dph.gif")
p2tph = PhotoImage(file=r"../assets/p2tph.gif")


###### KLASA TABLA ######
class Tabla(object):

    def __init__(self):
        self.tabla = self.kreiraj_tablu()

    def kreiraj_tablu(self):
        tabla = []  # ovo ce da bude zapravo matrica jer je niz nizova. U njoj ce da se nalazi 25 objekata klase Polje

        # ovo je ugnijezdena petlja koja pravi 25 objekata klase polje i smesta ih u tabla[]
        for row in range(5):
            vrsta = []
            for col in range(5):
                vrsta.append(Polje(row, col))
            tabla.append(vrsta)
        return tabla


###### KLASA POLJE ######
class Polje(object):

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.izgradjenost = 0
        self.naPolju = None
        self.btn = Button(tabla, image=pp, command=lambda: Play(self))
        self.btn.grid(row=self.row, column=self.col)

    def gradi(self):
        if self.izgradjenost < 4:
            self.izgradjenost += 1
            if self.izgradjenost == 1:
                self.btn.config(image=jp)
            if self.izgradjenost == 2:
                self.btn.config(image=dp)
            if self.izgradjenost == 3:
                self.btn.config(image=tp)
            if self.izgradjenost == 4:
                self.btn.config(image=kp)

    def pomeriFiguru(self, figura):

        # Ako jos nisu postavljene figure na tablu
        if figura.trPolje is None and self.naPolju is None:
            figura.trPolje = self
            self.naPolju = figura
            if figura.vlasnik == Igrac1.ime:
                self.btn.config(image=p1pp)
            if figura.vlasnik == Igrac2.ime:
                self.btn.config(image=p2pp)

        # Kada regularno pomera figuru
        elif self.naPolju is None:
            self.resetHighlight()
            figura.trPolje.naPolju = None
            figura.trPolje = self
            self.naPolju = figura

            # crta figuru na pomerenom polju
            if naPotezu == Igrac1.ime:
                if self.izgradjenost == 0:
                    self.btn.config(image=p1pp)
                if self.izgradjenost == 1:
                    self.btn.config(image=p1jp)
                if self.izgradjenost == 2:
                    self.btn.config(image=p1dp)
                if self.izgradjenost == 3:
                    self.btn.config(image=p1tp)
            elif naPotezu == Igrac2.ime:
                if self.izgradjenost == 0:
                    self.btn.config(image=p2pp)
                if self.izgradjenost == 1:
                    self.btn.config(image=p2jp)
                if self.izgradjenost == 2:
                    self.btn.config(image=p2dp)
                if self.izgradjenost == 3:
                    self.btn.config(image=p2tp)

    def fillBtn(self, string):
        if string == 'pyimage1':
            return pp
        if string == 'pyimage2':
            return jp
        if string == 'pyimage3':
            return dp
        if string == 'pyimage4':
            return tp

    def highlight(self, korak):
        for nr in range(5):
            for nc in range(5):
                # higlhight za pomeranje
                if korak == 1:
                    if abs(nr - self.row) <= 1 and abs(nc - self.col) <= 1 and (proba.tabla[nr][nc].izgradjenost - self.izgradjenost) <= 1 and proba.tabla[nr][nc].naPolju is None:
                        self.setHighlight(nr, nc)

                # highlight za gradnju
                elif korak == 2:
                    if abs(nr - self.row) <= 1 and abs(nc - self.col) <= 1 and proba.tabla[nr][nc].naPolju is None:
                        self.setHighlight(nr, nc)

    def setHighlight(self, nr, nc):
        if naPotezu == Igrac1.ime:
            if proba.tabla[nr][nc].izgradjenost == 0:
                proba.tabla[nr][nc].btn.config(image=pph)
            if proba.tabla[nr][nc].izgradjenost == 1:
                proba.tabla[nr][nc].btn.config(image=jph)
            if proba.tabla[nr][nc].izgradjenost == 2:
                proba.tabla[nr][nc].btn.config(image=dph)
            if proba.tabla[nr][nc].izgradjenost == 3:
                proba.tabla[nr][nc].btn.config(image=tph)
        if naPotezu == Igrac2.ime:
            if proba.tabla[nr][nc].izgradjenost == 0:
                proba.tabla[nr][nc].btn.config(image=p2pph)
            if proba.tabla[nr][nc].izgradjenost == 1:
                proba.tabla[nr][nc].btn.config(image=p2jph)
            if proba.tabla[nr][nc].izgradjenost == 2:
                proba.tabla[nr][nc].btn.config(image=p2dph)
            if proba.tabla[nr][nc].izgradjenost == 3:
                proba.tabla[nr][nc].btn.config(image=p2tph)

    def resetHighlight(self):
        for row in range(5):
            for col in range(5):
                if proba.tabla[row][col].naPolju is None:
                    if proba.tabla[row][col].izgradjenost == 0:
                        proba.tabla[row][col].btn.config(image=pp)
                    if proba.tabla[row][col].izgradjenost == 1:
                        proba.tabla[row][col].btn.config(image=jp)
                    if proba.tabla[row][col].izgradjenost == 2:
                        proba.tabla[row][col].btn.config(image=dp)
                    if proba.tabla[row][col].izgradjenost == 3:
                        proba.tabla[row][col].btn.config(image=tp)


    # dozvola za kretanje/gradnju
    def dozvolaAkcije(self, izFigura):
        if self.naPolju != None:    #proverava da li ima neko na polju - ako ima ne daje dozvolu
                return False
        elif abs(izFigura.trPolje.row - self.row) > 1 or abs(izFigura.trPolje.col - self.col) > 1:  # proverava da li je u dozvoljenom domenu
            return False
        elif korak == 1 and self.izgradjenost - izFigura.trPolje.izgradjenost > 1:  # proverava da li je u fazi izgradnje ili pomeranja - ako gradi onda dopusta akciju i na poljima cija je razlika u stepenu izgradjenosti i veca od 1
            return False
        elif korak == 2 and self.izgradjenost == 4:
            return False
        else:   # ako sve uslove ispunjava - dobija dozovlu za akciju
            return True

    def pokretan(self, figura):
        for row in range(5):
            for col in range(5):
                if abs(row - figura.trPolje.row) <= 1 and abs(col - figura.trPolje.col) <=1 and (proba.tabla[row][col].izgradjenost - figura.trPolje.izgradjenost) <= 1 and proba.tabla[row][col].naPolju is None:
                    return True
        return False

    def checkForWinner(self):
        global korak
        if self.izgradjenost == 3 and self.naPolju is not None:
            korak = 7
            print('!!!Pobedio je ' + naPotezu + '!!!')
        else:
            if Igrac1.ime == naPotezu:
                if not(self.pokretan(Igrac2.figura1)) and not(self.pokretan(Igrac2.figura2)):
                    korak = 7
                    print('Pobedio je: ' + Igrac1.ime)
                elif not(self.pokretan(Igrac1.figura1)) and not(self.pokretan(Igrac1.figura2)):
                    korak = 7
                    print('Pobedio je: ' + Igrac2.ime)
            elif Igrac2.ime == naPotezu:
                if not(self.pokretan(Igrac1.figura1)) and not(self.pokretan(Igrac1.figura2)):
                    korak = 7
                    print('Pobedio je: ' + Igrac2.ime)
                elif not(self.pokretan(Igrac2.figura1)) and not(self.pokretan(Igrac2.figura2)):
                    korak = 7
                    print('Pobedio je: ' + Igrac1.ime)

###### KLASA IGRAC ######
class Igrac(object):

    def __init__(self, ime):
        self.ime = ime
        self.figura1 = Figura(self.ime, 1)
        self.figura2 = Figura(self.ime, 2)


###### KLASA FIGURA ######
class Figura(object):

    def __init__(self, ime, rb):
        self.vlasnik = ime
        self.rb = rb
        self.trPolje = None

##### AI STVARI ######
class Potez(object):

    def __init__(self, figura, pR, pC, gR, gC):
        # koordinate pomeranja
        self.pR = pR
        self.pC = pC

        # koordinate gradnje
        self.gR = gR
        self.gC = gC

        # figura koja obavlja potez
        self.figura = figura


def moguciPotezi(igrac):
    mogPotezi = []
    f1 = igrac.figura1
    f2 = igrac.figura2

    # za figuru 1
    for row in range(5):
        for col in range(5):
            # proverava pomeranje
            if proba.tabla[row][col].naPolju is None and abs(row - f1.trPolje.row) <= 1 and abs(col - f1.trPolje.col) <= 1 and (proba.tabla[row][col].izgradjenost - f1.trPolje.izgradjenost) <= 1:
                tempR = row
                tempC = col
                for rrow in range(5):
                    for ccol in range(5):
                        # na kojim poljima pomerena figura moze da gradi
                        if proba.tabla[rrow][ccol].izgradjenost < 4:
                            if proba.tabla[rrow][ccol].naPolju is None and not(rrow == tempR and ccol == tempC) or proba.tabla[rrow][ccol].naPolju == f1:
                                if abs(rrow - tempR) <= 1 and abs(ccol - tempC) <= 1:
                                    mogPotezi.append(Potez(f1, tempR, tempC, rrow, ccol))
    # za figuru 2
    for row in range(5):
        for col in range(5):
            # proverava pomeranje
            if proba.tabla[row][col].naPolju is None and abs(row - f2.trPolje.row) <= 1 and abs(col - f2.trPolje.col) <= 1 and (proba.tabla[row][col].izgradjenost - f2.trPolje.izgradjenost) <= 1:
                tempR = row
                tempC = col
                for rrow in range(5):
                    for ccol in range(5):
                        # na kojim poljima pomerena figura moze da gradi
                        if proba.tabla[rrow][ccol].izgradjenost < 4:
                            if proba.tabla[rrow][ccol].naPolju is None and not(rrow == tempR and ccol == tempC) or proba.tabla[rrow][ccol].naPolju == f2: # prva dva uslova proveravaju da na polju nema nikoga a drugi da li je na polju f2 (ali on vise nije tu jer se pomerio)
                                if abs(rrow - tempR) <= 1 and abs(ccol - tempC) <= 1:
                                    mogPotezi.append(Potez(f2, tempR, tempC, rrow, ccol))
    return mogPotezi


def heuristika(potez):
    f = 0
    m = 0
    l = 0

    if (potez.figura.vlasnik == Igrac1.ime):
        igracNaPotezu = Igrac1
        drIgrac = Igrac2
    elif (potez.figura.vlasnik == Igrac2.ime):
        igracNaPotezu = Igrac2
        drIgrac = Igrac1


    pomeranje = proba.tabla[potez.pR][potez.pC]
    gradnja = proba.tabla[potez.gR][potez.gC]

    rastojanjeSopstvenih = math.sqrt(math.pow(igracNaPotezu.figura1.trPolje.col - potez.gC, 2) + math.pow(igracNaPotezu.figura1.trPolje.row - potez.gR, 2)) + math.sqrt(math.pow(igracNaPotezu.figura2.trPolje.col - potez.gC, 2) + math.pow(igracNaPotezu.figura2.trPolje.row - potez.gR, 2))
    rastojanjeProtivnickih = math.sqrt(math.pow(drIgrac.figura1.trPolje.col - potez.gC, 2) + math.pow(drIgrac.figura1.trPolje.row - potez.gR, 2)) + math.sqrt(math.pow(drIgrac.figura2.trPolje.col - potez.gC, 2) + math.pow(drIgrac.figura2.trPolje.row - potez.gR, 2))

    m = pomeranje.izgradjenost
    l = gradnja.izgradjenost*(rastojanjeProtivnickih - rastojanjeSopstvenih)

    f = m + l
    return f

def heuristikaHard(potez):
    f = 0
    m = 0
    l = 0

    if (potez.figura.vlasnik == Igrac1.ime):
        igracNaPotezu = Igrac1
        drIgrac = Igrac2
    elif (potez.figura.vlasnik == Igrac2.ime):
        igracNaPotezu = Igrac2
        drIgrac = Igrac1


    m = igracNaPotezu.figura1.trPolje.izgradjenost*igracNaPotezu.figura1.trPolje.izgradjenost + igracNaPotezu.figura2.trPolje.izgradjenost*igracNaPotezu.figura2.trPolje.izgradjenost
    l = drIgrac.figura1.trPolje.izgradjenost*drIgrac.figura1.trPolje.izgradjenost + drIgrac.figura2.trPolje.izgradjenost*drIgrac.figura2.trPolje.izgradjenost

    f = m - l
    return f

### samo proba simulacija pokreta
def simPotez(potez):
    fig = potez.figura  # figura koja treba da izvrsi potez
    pNaPolje = proba.tabla[potez.pR][potez.pC]  # polje na koje treba da se pomeri
    gNaPolje = proba.tabla[potez.gR][potez.gC]  # polje na koje treba da gradi posle pomeranja

    # KRETNJA
    fig.trPolje.naPolju = None  # uklanja figuru sa trenutnog polja
    fig.trPolje = pNaPolje      # stavlja trenutno polje figure da je izabrano polje za kretnju, tj pomera figuru
    pNaPolje.naPolju = fig      # stavlja da je na tom polju ta figura

    # GRADNJA
    if gNaPolje.izgradjenost < 4:   # bespotreban uslov ja msm jer u mogucipotezi on proverava da l tu uopste moze da gradi
        gNaPolje.izgradjenost += 1


# MINIMAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def miniMaxEasy(dubina, isMaximizing):

    # AKO JE MAXIMIZER
    if isMaximizing:
        maxScore = -1000
        if dubina == 2:     # ako je dubina 2 pa ne mora da simulira potez vec samo da mu odredi heuristiku
            if AIP2:
                pPotezi = moguciPotezi(Igrac2)
            elif AIP1:
                pPotezi = moguciPotezi(Igrac1)
            if len(pPotezi) == 0:           # ne znam ovde sta treba da radi.. koja vrednost treba da se vrati ako nema vise mogucih poteza
                return -1000
            for i in range(len(pPotezi)):
                score = heuristika(pPotezi[i])
                maxScore = max(score, maxScore)
            return maxScore
        else:
            if AIP2:
                potezi = moguciPotezi(Igrac2)
            elif AIP1:
                potezi = moguciPotezi(Igrac1)
            najPotez = potezi[0]
            if potezi is None:
                return -1000
            for i in range(len(potezi)):
                # ovde treba da se postave pocetne vrednosti table i figure pre nego sto se simulira
                backupFigura = potezi[i].figura
                backupTrPolje = backupFigura.trPolje

                poljeGradnje = proba.tabla[potezi[i].gR][potezi[i].gC]
                backupIzgradjenosti = poljeGradnje.izgradjenost

                #simulacija
                simPotez(potezi[i])
                score = miniMaxEasy(dubina+1, False)
                if score > maxScore:
                    maxScore = max(score, maxScore)
                    najPotez = potezi[i]

                #undo pokreta
                backupFigura.trPolje.naPolju = None         # atribut polja
                backupFigura.trPolje = backupTrPolje        # atribut figure
                backupFigura.trPolje.naPolju = backupFigura    # atribut polja

                #undo gradnje
                poljeGradnje.izgradjenost = backupIzgradjenosti

            return najPotez

    # AKO JE MINIMIZER
    else:
        minScore = 1000
        if AIP2:
            potezi = moguciPotezi(Igrac1)
        elif AIP1:
            potezi = moguciPotezi(Igrac2)

        if len(potezi) == 0:
            return 1000

        for i in range(len(potezi)):
            # ovde treba da se postave pocetne vrednosti table i figure pre nego sto se simulira
            backupFigura = potezi[i].figura
            backupTrPolje = backupFigura.trPolje
            poljeGradnje = proba.tabla[potezi[i].gR][potezi[i].gC]
            backupIzgradjenosti = poljeGradnje.izgradjenost

            # simulacija
            if proba.tabla[potezi[i].pR][potezi[i].pC].izgradjenost == 3:
                score = -1000
            else:
                simPotez(potezi[i])
                score = miniMaxEasy(dubina+1, True)
            minScore = min(score, minScore)

            # undo pokreta
            backupFigura.trPolje.naPolju = None  # atribut polja
            backupFigura.trPolje = backupTrPolje  # atribut figure
            backupFigura.trPolje.naPolju = backupFigura  # atribut polja

            # undo gradnje
            poljeGradnje.izgradjenost = backupIzgradjenosti
        return minScore

def miniMaxMedium(dubina, isMaximizing, alfa, beta):
    # AKO JE MAXIMIZER
    if isMaximizing:
        if dubina == 2:     # ako je dubina 2 pa ne mora da simulira potez vec samo da mu odredi heuristiku
            maxScore = -1000
            if AIP2:
                pPotezi = moguciPotezi(Igrac2)
            elif AIP1:
                pPotezi = moguciPotezi(Igrac1)
            if len(pPotezi) == 0:           # ne znam ovde sta treba da radi.. koja vrednost treba da se vrati ako nema vise mogucih poteza
                return -1000
            for i in range(len(pPotezi)):
                score = heuristika(pPotezi[i])
                maxScore = max(score, maxScore)
                alfa = max(alfa, maxScore)
                if beta <= alfa:
                    break
            return maxScore
        if dubina == 0:
            maxScore = -1000
            if AIP2:
                potezi = moguciPotezi(Igrac2)
            elif AIP1:
                potezi = moguciPotezi(Igrac1)
            najPotez = potezi[0]
            if potezi is None:
                return -1000
            for i in range(len(potezi)):
                # ovde treba da se postave pocetne vrednosti table i figure pre nego sto se simulira
                backupFigura = potezi[i].figura
                backupTrPolje = backupFigura.trPolje

                poljeGradnje = proba.tabla[potezi[i].gR][potezi[i].gC]
                backupIzgradjenosti = poljeGradnje.izgradjenost

                #simulacija
                simPotez(potezi[i])
                score = miniMaxMedium(dubina+1, False, alfa, beta)
                if score > maxScore:
                    maxScore = max(score, maxScore)
                    najPotez = potezi[i]
                alfa = max(alfa, maxScore)

                #undo pokreta
                backupFigura.trPolje.naPolju = None         # atribut polja
                backupFigura.trPolje = backupTrPolje        # atribut figure
                backupFigura.trPolje.naPolju = backupFigura    # atribut polja

                #undo gradnje
                poljeGradnje.izgradjenost = backupIzgradjenosti

                if beta <= alfa:
                    break

            return najPotez

    # AKO JE MINIMIZER
    else:
        minScore = 1000
        if AIP2:
            potezi = moguciPotezi(Igrac1)
        elif AIP1:
            potezi = moguciPotezi(Igrac2)

        if len(potezi) == 0:
            return 1000

        for i in range(len(potezi)):
            # ovde treba da se postave pocetne vrednosti table i figure pre nego sto se simulira
            backupFigura = potezi[i].figura
            backupTrPolje = backupFigura.trPolje
            poljeGradnje = proba.tabla[potezi[i].gR][potezi[i].gC]
            backupIzgradjenosti = poljeGradnje.izgradjenost

            # simulacija
            if proba.tabla[potezi[i].pR][potezi[i].pC].izgradjenost == 3:
                score = -1000
            else:
                simPotez(potezi[i])
                score = miniMaxMedium(dubina+1, True, alfa, beta)
            minScore = min(score, minScore)
            beta = min(minScore, beta)

            # undo pokreta
            backupFigura.trPolje.naPolju = None  # atribut polja
            backupFigura.trPolje = backupTrPolje  # atribut figure
            backupFigura.trPolje.naPolju = backupFigura  # atribut polja

            # undo gradnje
            poljeGradnje.izgradjenost = backupIzgradjenosti

            if beta <= alfa:
                break
        return minScore

def miniMaxHard(dubina, isMaximizing, alfa, beta):

    # AKO JE MAXIMIZER
    if isMaximizing:
        if dubina == 4:     # ako je dubina 2 pa ne mora da simulira potez vec samo da mu odredi heuristiku
            maxScore = -1000
            if AIP2:
                pPotezi = moguciPotezi(Igrac2)
            elif AIP1:
                pPotezi = moguciPotezi(Igrac1)
            if len(pPotezi) == 0:           # ne znam ovde sta treba da radi.. koja vrednost treba da se vrati ako nema vise mogucih poteza
                return -1000
            for i in range(len(pPotezi)):
                score = heuristikaHard(pPotezi[i])
                maxScore = max(score, maxScore)
                alfa = max(alfa, maxScore)
                if beta <= alfa:
                    break
            return maxScore

        if dubina == 0:
            maxScore = -1000
            if AIP2:
                potezi = moguciPotezi(Igrac2)
            elif AIP1:
                potezi = moguciPotezi(Igrac1)
            najPotez = potezi[0]
            if potezi is None:
                return -1000
            for i in range(len(potezi)):
                # ovde treba da se postave pocetne vrednosti table i figure pre nego sto se simulira
                backupFigura = potezi[i].figura
                backupTrPolje = backupFigura.trPolje

                poljeGradnje = proba.tabla[potezi[i].gR][potezi[i].gC]
                backupIzgradjenosti = poljeGradnje.izgradjenost

                #simulacija
                if proba.tabla[potezi[i].pR][potezi[i].pC].izgradjenost == 3:
                    score = 1000
                else:
                    simPotez(potezi[i])
                    score = miniMaxHard(dubina+1, False, alfa, beta)
                if score > maxScore:
                    maxScore = max(score, maxScore)
                    najPotez = potezi[i]
                alfa = max(alfa, maxScore)

                #undo pokreta
                backupFigura.trPolje.naPolju = None         # atribut polja
                backupFigura.trPolje = backupTrPolje        # atribut figure
                backupFigura.trPolje.naPolju = backupFigura    # atribut polja

                #undo gradnje
                poljeGradnje.izgradjenost = backupIzgradjenosti

                if beta <= alfa:
                    break
            return najPotez

        if dubina == 2:
            maxScore = -1000
            if AIP2:
                potezi = moguciPotezi(Igrac2)
            elif AIP1:
                potezi = moguciPotezi(Igrac1)
            if potezi is None:
                return -1000
            for i in range(len(potezi)):
                # ovde treba da se postave pocetne vrednosti table i figure pre nego sto se simulira
                backupFigura = potezi[i].figura
                backupTrPolje = backupFigura.trPolje

                poljeGradnje = proba.tabla[potezi[i].gR][potezi[i].gC]
                backupIzgradjenosti = poljeGradnje.izgradjenost

                #simulacija
                if proba.tabla[potezi[i].pR][potezi[i].pC].izgradjenost == 3:
                    score = 1000
                else:
                    simPotez(potezi[i])
                    score = miniMaxHard(dubina+1, False, alfa, beta)
                maxScore = max(maxScore, score)
                alfa = max(alfa, maxScore)

                #undo pokreta
                backupFigura.trPolje.naPolju = None         # atribut polja
                backupFigura.trPolje = backupTrPolje        # atribut figure
                backupFigura.trPolje.naPolju = backupFigura    # atribut polja

                #undo gradnje
                poljeGradnje.izgradjenost = backupIzgradjenosti

                if beta <= alfa:
                    break

            return maxScore

    # AKO JE MINIMIZER
    else:
        if dubina == 1:
            minScore = 1000
            if AIP2:
                potezi = moguciPotezi(Igrac1)
            elif AIP1:
                potezi = moguciPotezi(Igrac2)

            if len(potezi) == 0:
                return 1000

            for i in range(len(potezi)):
                # ovde treba da se postave pocetne vrednosti table i figure pre nego sto se simulira
                backupFigura = potezi[i].figura
                backupTrPolje = backupFigura.trPolje
                poljeGradnje = proba.tabla[potezi[i].gR][potezi[i].gC]
                backupIzgradjenosti = poljeGradnje.izgradjenost

                # simulacija
                if proba.tabla[potezi[i].pR][potezi[i].pC].izgradjenost == 3:
                    score = -1000
                else:
                    simPotez(potezi[i])
                    score = miniMaxHard(dubina+1, True, alfa, beta)
                minScore = min(score, minScore)
                beta = min(minScore, beta)

                # undo pokreta
                backupFigura.trPolje.naPolju = None  # atribut polja
                backupFigura.trPolje = backupTrPolje  # atribut figure
                backupFigura.trPolje.naPolju = backupFigura  # atribut polja

                # undo gradnje
                poljeGradnje.izgradjenost = backupIzgradjenosti

                if beta <= alfa:
                    break
            return minScore

        if dubina == 3:
            minScore = 1000
            if AIP2:
                potezi = moguciPotezi(Igrac1)
            elif AIP1:
                potezi = moguciPotezi(Igrac2)

            if len(potezi) == 0:
                return 1000

            for i in range(len(potezi)):
                # ovde treba da se postave pocetne vrednosti table i figure pre nego sto se simulira
                backupFigura = potezi[i].figura
                backupTrPolje = backupFigura.trPolje
                poljeGradnje = proba.tabla[potezi[i].gR][potezi[i].gC]
                backupIzgradjenosti = poljeGradnje.izgradjenost

                # simulacija
                if proba.tabla[potezi[i].pR][potezi[i].pC].izgradjenost == 3:
                    score = -1000
                else:
                    simPotez(potezi[i])
                    score = miniMaxHard(dubina + 1, True, alfa, beta)
                minScore = min(score, minScore)
                beta = min(minScore, beta)

                # undo pokreta
                backupFigura.trPolje.naPolju = None  # atribut polja
                backupFigura.trPolje = backupTrPolje  # atribut figure
                backupFigura.trPolje.naPolju = backupFigura  # atribut polja

                # undo gradnje
                poljeGradnje.izgradjenost = backupIzgradjenosti

                if beta <= alfa:
                    break
            return minScore

def initAI(figura):
    rR = randrange(4)
    rC = randrange(4)

    if proba.tabla[rR][rC].naPolju == None:
        proba.tabla[rR][rC].pomeriFiguru(figura)
    else:
        initAI(figura)

### GAME START
korak = 99
counter = 0
proba = Tabla()
Igrac1 = Igrac('Zeleni')
Igrac2 = Igrac('Lila')
naPotezu = Igrac1.ime
izabranaFigura = None
AIP1 = BooleanVar()
AIP2 = BooleanVar()
AIP1difficulty = StringVar()
AIP2difficulty = StringVar()

################################ Play funkcija
def Play(polje):
    global counter
    global korak
    global izabranaFigura
    global naPotezu
    global proba

    # Postavljanje figura pri pocetku igre
    if korak == 0:
        if not AIP1:
            if Igrac1.figura1.trPolje is None:
                polje.pomeriFiguru(Igrac1.figura1)
            elif Igrac1.figura2.trPolje is None:
                polje.pomeriFiguru(Igrac1.figura2)
                if AIP2 and Igrac1.figura2.trPolje is not None:
                    initAI(Igrac2.figura1)
                    initAI(Igrac2.figura2)
                    korak = 1

        if Igrac2.figura1.trPolje is None:
            polje.pomeriFiguru(Igrac2.figura1)
        elif Igrac2.figura2.trPolje is None:
            polje.pomeriFiguru(Igrac2.figura2)
            if Igrac2.figura2.trPolje is not None:
                korak = 1
                if AIP1:
                    ### AI IGRA ###
                    if AIP1difficulty == 'Easy':
                        pAI = miniMaxEasy(0, True)
                    elif AIP1difficulty == 'Medium':
                        pAI = miniMaxMedium(0, True, -1000, 1000)
                    elif AIP1difficulty == 'Hard':
                        pAI = miniMaxHard(0, True, -1000, 1000)

                    poljeTrenutnoAI = proba.tabla[pAI.figura.trPolje.row][pAI.figura.trPolje.col]
                    poljePomeranjaAI = proba.tabla[pAI.pR][pAI.pC]
                    poljeGradnjeAI = proba.tabla[pAI.gR][pAI.gC]

                    poljePomeranjaAI.pomeriFiguru(pAI.figura)
                    poljePomeranjaAI.checkForWinner()
                    poljePomeranjaAI.resetHighlight()

                    poljeGradnjeAI.gradi()
                    poljeGradnjeAI.resetHighlight()
                    poljeGradnjeAI.checkForWinner()

                    naPotezu = Igrac2.ime

                    # PRINTANJE
                    print('Figura je bila na: ' + str(poljeTrenutnoAI.row) + 'x' + str(poljeTrenutnoAI.col))
                    print('Pomerio je na: ' + str(pAI.pR) + 'x' + str(pAI.pC))
                    print('Gradio je na: ' + str(pAI.gR) + 'x' + str(pAI.gC))
                    print('/////////////////////////')

    # Biranje figure za akciju
    elif korak == 1:
        if polje.naPolju != None and polje.naPolju.vlasnik == naPotezu: # ako je izabrao polje na kome neko ima i ako je ta figura zapravo njegova figura
            izabranaFigura = polje.naPolju
            polje.resetHighlight()
            polje.highlight(korak)
        if izabranaFigura != None and polje.dozvolaAkcije(izabranaFigura):
            polje.pomeriFiguru(izabranaFigura)
            korak = 2
            polje.checkForWinner()
            polje.resetHighlight()
            polje.highlight(korak)

    # Gradnja
    elif korak == 2:
        if polje.dozvolaAkcije(izabranaFigura):
            polje.gradi()
            polje.resetHighlight()
            izabranaFigura = None
            korak = 1
            polje.checkForWinner()
            if naPotezu == Igrac1.ime:
                naPotezu = Igrac2.ime

                if AIP2:
                    ### AI IGRA ###
                    if AIP2difficulty == 'Easy':
                        pAI = miniMaxEasy(0, True)
                    elif AIP2difficulty == 'Medium':
                        pAI = miniMaxMedium(0, True, -1000, 1000)
                    elif AIP2difficulty == 'Hard':
                        pAI = miniMaxHard(0, True, -1000, 1000)

                    poljeTrenutnoAI = proba.tabla[pAI.figura.trPolje.row][pAI.figura.trPolje.col]
                    poljePomeranjaAI = proba.tabla[pAI.pR][pAI.pC]
                    poljeGradnjeAI = proba.tabla[pAI.gR][pAI.gC]

                    poljePomeranjaAI.pomeriFiguru(pAI.figura)
                    poljePomeranjaAI.checkForWinner()
                    poljePomeranjaAI.resetHighlight()

                    poljeGradnjeAI.gradi()
                    poljeGradnjeAI.resetHighlight()
                    poljeGradnjeAI.checkForWinner()

                    naPotezu = Igrac1.ime

                    # PRINTANJE
                    print('Figura je bila na: ' + str(poljeTrenutnoAI.row) + 'x' + str(poljeTrenutnoAI.col))
                    print('Pomerio je na: ' + str(pAI.pR) + 'x' + str(pAI.pC))
                    print('Gradio je na: ' + str(pAI.gR) + 'x' + str(pAI.gC))
                    print('/////////////////////////')

            elif naPotezu == Igrac2.ime:
                naPotezu = Igrac1.ime

                if AIP1:
                    ### AI IGRA ###
                    if AIP1difficulty == 'Easy':
                        pAI = miniMaxEasy(0, True)
                    elif AIP1difficulty == 'Medium':
                        pAI = miniMaxMedium(0, True, -1000, 1000)
                    elif AIP1difficulty == 'Hard':
                        pAI = miniMaxHard(0, True, -1000, 1000)
                    poljeTrenutnoAI = proba.tabla[pAI.figura.trPolje.row][pAI.figura.trPolje.col]
                    poljePomeranjaAI = proba.tabla[pAI.pR][pAI.pC]
                    poljeGradnjeAI = proba.tabla[pAI.gR][pAI.gC]

                    poljePomeranjaAI.pomeriFiguru(pAI.figura)
                    poljePomeranjaAI.checkForWinner()
                    poljePomeranjaAI.resetHighlight()

                    poljeGradnjeAI.gradi()
                    poljeGradnjeAI.resetHighlight()
                    poljeGradnjeAI.checkForWinner()

                    naPotezu = Igrac2.ime

                    # PRINTANJE
                    print('Figura je bila na: ' + str(poljeTrenutnoAI.row) + 'x' + str(poljeTrenutnoAI.col))
                    print('Pomerio je na: ' + str(pAI.pR) + 'x' + str(pAI.pC))
                    print('Gradio je na: ' + str(pAI.gR) + 'x' + str(pAI.gC))
                    print('/////////////////////////')

root.mainloop()