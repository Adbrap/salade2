# ----- initialisation des modules -----#
import pandas as pd
import numpy
from tkinter import Tk
from tkinter import messagebox
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import requests
import datetime
from numpy import *
from matplotlib.pyplot import *
import colorama
from colorama import Fore
import os
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
from multiprocessing import Process
import math
#from playsound import playsound
import webbrowser
import random
# ----- initialisation des modules -----#
activ = False
activactiv = False
antholemuscler = False
compteurjson = 1

def confirmer(event,arg1,placeA,data,url):
    global compteurjson
    arg1 = arg1.drop(range(0, placeA - 1))
    arg1 = arg1.reset_index(drop=True)
    arg1.to_json(f'json_recent/{compteurjson}.json')
    #webbrowser.open(url)

def Indicateurs(event):
    global antholemuscler
    antholemuscler = True
# ----- initialisation des fonctions lies au boutons -----#

# ----- initialisation des couleurs du modules pystyle -----#
class bcolors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR
    PURPLE = '\033[35m'  # PURPLE

w = Fore.WHITE
b = Fore.BLACK
g = Fore.LIGHTGREEN_EX
y = Fore.LIGHTYELLOW_EX
m = Fore.LIGHTMAGENTA_EX
c = Fore.LIGHTCYAN_EX
lr = Fore.LIGHTRED_EX
lb = Fore.LIGHTBLUE_EX
# ----- initialisation des couleurs du modules pystyle -----#

# ----- initialisation des temps de recherches -----#
date = datetime.datetime.now()
my_lock = threading.RLock()
#end = str(pd.Timestamp.today() + pd.DateOffset(5))[0:10]
start_5m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_15m = str(pd.Timestamp.today() + pd.DateOffset(-15000))[0:10]
start_30m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_1h = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_6h = str(pd.Timestamp.today() + pd.DateOffset(-20))[0:10]
start_1d = str(pd.Timestamp.today() + pd.DateOffset(-50))[0:10]
start_1week = str(pd.Timestamp.today() + pd.DateOffset(-120))[0:10]
start_1month = str(pd.Timestamp.today() + pd.DateOffset(-240))[0:10]
# ----- initialisation des temps de recherches -----#

# ----- initialisation de l'API key et ticker -----#
api_key = '1KsqKOh1pTAJyWZx6Qm9pvnaNcpKVh_8'
#api_key = 'q5li8Y5ldvlF7eP8YI7XdMWbyOA3scWJ'
# ----- initialisation de l'API key et ticker -----#

# ----- fonction pour trouver les point intersection de la ligne de coup et de la Courbe -----#
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('les courbes ne se coupent pas')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
# ----- fonction pour trouver les point intersection de la ligne de coup et de la Courbe -----#

# ----- fonction Principale -----#
def Finder_IETE(time1, time_name1, start, end, start2, TETE, lettre):
    global ticker
    global antholemuscler
    global compteurjson
    # while True:
    i = 0
    fa = 0
    fb = 1
    fc = 1
    fd = 2
    fe = 2
    ff = 3
    fg = 3
    compteur = 0
    compteur2 = 0
    compteur3 = 0
    a = 0
    # ----- Appel des données Polygon.io OHLC et creation du DF -----#
    while i != 1:

        with my_lock:

            # api_url_OHLC = f'http://api.polygon.io/v2/aggs/ticker/{ticker}/range/15/minute/2022-07-01/2022-07-15?adjusted=true&sort=asc&limit=30000&apiKey={api_key}'
            api_url_OHLC = f'http://api.polygon.io/v2/aggs/ticker/{ticker}/range/{time1}/{time_name1}/{start}/{end}?adjusted=true&limit=50000&apiKey={api_key}'
            data = requests.get(api_url_OHLC).json()
            df = pd.DataFrame(data['results'])

            api_url_OHLC2 = f'http://api.polygon.io/v2/aggs/ticker/{ticker}/range/{time1}/{time_name1}/{start2}/{end}?adjusted=true&limit=50000&apiKey={api_key}'
            data2 = requests.get(api_url_OHLC2).json()
            df2 = pd.DataFrame(data2['results'])


        # ----- creation des locals(min/max) -----#
        local_max = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
        local_min = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]
        local_max1 = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
        local_min1 = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]

        local_max2 = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
        local_min2 = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]
        # ----- creation des locals(min/max) -----#

        # ----- suppression des points morts de la courbe -----#
        test_min = []
        test_max = []

        # if local_min[0] > local_max[0]:
        #        local_max = local_max[1:]
        #        print('On a supprimer le premier point')
        #
        q = 0
        p = 0

        len1 = len(local_min)
        len2 = len(local_max)
        while p < len1 - 5 or p < len2 - 5:
            if local_min[p + 1] < local_max[p]:
                test_min.append(local_min[p])
                local_min = np.delete(local_min, p)

                p = p - 1
            if local_max[p + 1] < local_min[p + 1]:
                test_max.append(local_max[p])
                local_max = np.delete(local_max, p)

                p = p - 1
            p = p + 1

            len1 = len(local_min)
            len2 = len(local_max)

        highs = df.iloc[local_max, :]
        lows = df.iloc[local_min, :]
        highs1 = df.iloc[test_max, :]
        lows1 = df.iloc[test_min, :]

        decalage = 0
        # ----- suppression des points morts de la courbe -----#

        # ----- initialisation des pointeurs de la figure -----#
        print(len(df.iloc[local_max, :]))
        while i != 1:
            if ((len(df.iloc[local_max, :])) - (ff)) > 1 and ((len(df.iloc[local_min, :])) - (ff)) > 1:

                A = float(highs['c'].iloc[fa])
                B = float(lows['c'].iloc[fb])
                C = float(highs['c'].iloc[fc])
                D = float(lows['c'].iloc[fd])
                E = float(highs['c'].iloc[fe])
                F = float(lows['c'].iloc[ff])
                G = float(highs['c'].iloc[fg])

                data_A = []
                data_B = []
                data_C = []
                data_D = []
                data_E = []
                data_F = []
                data_G = []
                # ----- initialisation des pointeurs de la figure -----#

                # ----- determination du 'PAS' de la pente de la LDC pour la prolonger plus loins que C et E -----#
                if C > E:
                    differ = (C - E)
                    pas = (local_max[fe] - local_max[fc])
                    suite = differ / pas
                if C < E:
                    differ = (E - C)
                    pas = (local_max[fe] - local_max[fc])
                    suite = differ / pas
                # ----- determination du 'PAS' de la pente de la LDC pour la prolonger plus loins que C et E -----#

                # ----- PRINT affichage dans la console -----#
                Write.Print(f"  >> RECHERCHE IETE:", Colors.white, interval=0.000)
                Write.Print(f"  {ticker}", Colors.green, interval=0.000)
                Write.Print(f"  {time1} {time_name1} {start}", Colors.cyan, interval=0.000)
                Write.Print("  <<", Colors.white, interval=0.000)
                print('')
                # ----- PRINT affichage dans la console -----#

                # ----- creation des differentes courbe: rouge(surlignage figure), vert(ligne de coup), bleu(la figure en zoomer)-----#
                rouge = []
                vert = []
                bleu = []

                rouge.append(local_max[fa])
                rouge.append(local_min[fb])
                rouge.append(local_max[fc])
                rouge.append(local_min[fd])
                rouge.append(local_max[fe])
                rouge.append(local_min[ff])
                rouge.append(local_max[fg])

                vert.append(local_max[fa])
                vert.append(local_max[fc])
                vert.append(local_max[fe])
                vert.append(local_max[fg])

                i = 0
                for i in range(local_min[fa]-1, len(df)):
                    bleu.append(i)


                mirande2 = df.iloc[vert, :]
                mirande = df.iloc[rouge, :]
                mirande3 = df.iloc[bleu, :]

                local_max_pp = argrelextrema(mirande3['c'].values, np.greater, order=1, mode='clip')[0]
                local_min_pp = argrelextrema(mirande3['c'].values, np.less, order=1, mode='clip')[0]

                # ----- creation des differentes courbe: rouge(surlignage figure), vert(ligne de coup), bleu(la figure en zoomer)-----#

                # ----- determiner la direction pente LDC et allongement apres E et C -----#
                if activ == True:
                    fig1 = plt.figure(figsize=(10, 7))
                    plt.plot([], [], " ")
                    fig1.patch.set_facecolor('#17DE17')
                    fig1.patch.set_alpha(0.3)
                    plt.title(f'IETE : {ticker} {start} | {end}', fontweight="bold", color='black')
                    mirande3['c'].plot(color=['blue'], label='Clotures')
                    mirande['c'].plot(color=['red'], label='Clotures', alpha=0.3)
                    plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='red', wrap=True)
                    plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='red', wrap=True)
                    plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='red', wrap=True)
                    plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='red', wrap=True)
                    plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='red', wrap=True)
                    plt.text(local_min[ff], F, "F", ha='left', style='normal', size=10.5, color='red', wrap=True)
                    plt.text(local_max[fg], G, f"G {round(G,5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
                    #mirande2['c'].plot(color=['green'], linestyle='--', label='Ligne de coup')
                    plt.scatter(local_max[fa], A, color='blue')
                    plt.scatter(local_min[fb], B, color='blue')
                    plt.scatter(local_max[fc], C, color='blue')
                    plt.scatter(local_min[fd], D, color='blue')
                    plt.scatter(local_max[fe], E, color='blue')
                    plt.scatter(local_min[ff], F, color='blue')
                    plt.scatter(local_max[fg], G, color='blue')
                    plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)

                    # plt.scatter(x=low.index, y=low["c"])
                    plt.show()








                if E > C:
                    mirande2['c'].values[0] = mirande2['c'].values[1] - ((suite * (local_max[fc] - local_max[fa])))
                    mirande2['c'].values[3] = mirande2['c'].values[2] + ((suite * (local_max[fg] - local_max[fe])))
                if E < C:
                    mirande2['c'].values[0] = mirande2['c'].values[1] + ((suite * (local_max[fc] - local_max[fa])))
                    mirande2['c'].values[3] = mirande2['c'].values[2] - ((suite * (local_max[fg] - local_max[fe])))
                if E == C:
                    mirande2['c'].values[0] = df['c'].values[local_max[fc]]
                    mirande2['c'].values[3] = df['c'].values[local_max[fe]]
                # ----- determiner la direction pente LDC et allongement apres E et C -----#

                # ----- transformer le tableau en DF avec les donnée du DF reel -----#
                vert1 = {'c': vert}
                vert2 = pd.DataFrame(data=vert1)
                rouge1 = {'c': rouge}
                rouge2 = pd.DataFrame(data=rouge1)
                bleu1 = {'c': bleu}
                bleu2 = pd.DataFrame(data=bleu1)
                # ----- transformer le tableau en DF avec les donnée du DF reel -----#

                # ----- preparation des deux courbes pour determiner intersection de I et J -----#
                # --- premiere droite cotée gauche ---#
                AI = [local_max[fa], mirande2['c'].iloc[0]]
                BI = [local_max[fc], mirande2['c'].iloc[1]]
                # --- premiere droite coté gauche ---#

                # --- deuxieme droite coté gauche ---#
                CI = [local_max[fa], A]
                DI = [local_min[fb], B]
                # I = line_intersection((AI, BI), (CI, DI))
                # --- deuxieme droite coté gauche ---#

                # --- premiere droite cotée droit ---#
                AJ = [local_max[fe], mirande2['c'].iloc[2]]
                BJ = [local_max[fg], mirande2['c'].iloc[3]]
                # --- premiere droite cotée droit ---#

                # --- deuxieme droite coté droit ---#
                CJ = [local_max[fg], G]
                DJ = [local_min[ff], F]
                # J = line_intersection((AJ, BJ), (CJ, DJ))
                # --- deuxieme droite coté droit ---#
                # ----- preparation des deux courbes pour determiner intersection de I et J -----#

                # ----- verification qu'il n'y est pas de point mort dans la figure -----# ------------------- VERIFIER !!
                pop = 0
                verif = 0

                for pop in range(0, len(test_min)):
                    if test_min[pop] > local_max[fa] and test_min[pop] < local_max[fg]:
                        verif = verif + 1
                pop = 0
                for pop in range(0, len(test_max)):
                    if test_max[pop] > local_max[fa] and test_max[pop] < local_max[fg]:
                        verif = verif + 1
                # ----- verification qu'il n'y est pas de point mort dans la figure -----# ------------------- VERIFIER !!


                # ----- condition pour que l'ordre des point de la figure soit respecter -----#
                ordre = False
                if local_max[fa] < local_min[fb] < local_max[fc] < local_min[fd] < local_max[fe] < local_min[ff]:
                    ordre = True
                # ----- condition pour que l'ordre des point de la figure soit respecter -----#

                # ----- condition pour que la tete fasse au minimum 2.8% -----#
                mini_pourcent = False
                if ((((C + E) / 2) - D) * 100) / D >= 2.8:
                    mini_pourcent = True
                # ----- condition pour que la tete fasse au minimum 2.8% -----#

                # ----- condition pour garantir la forme de l'iete  -----#
                if (C - B) < (C - D) and (C - B) < (E - D) and (E - F) < (E - D) and (E - F) < (C - D) and B > D and F > D and B < C and F < E and A >= mirande2['c'].iloc[0] and verif == 0 and ordre == True and mini_pourcent == True:
                # ----- condition pour garantir la forme de l'iete  -----#

                    # ----- essaye de determiner les point d'intersection de la LDC -----#
                    try:
                        J = line_intersection((AJ, BJ), (CJ, DJ))
                        I = line_intersection((AI, BI), (CI, DI))
                        moyenne_tete = ((C - D) + (E - D)) / 2
                        moyenne_epaule1 = ((I[1] - B) + (C - B)) / 2
                        moyenne_epaule2 = ((E - F) + (J[1] - F)) / 2
                        moyenne_des_epaule = ((E - F) + (J[1] - F)) + ((E - F) + (J[1] - F)) / 4
                        accept = True
                    except:
                        accept = False
                        # ----- essaye de determiner les point d'intersection de la LDC -----#
                    trouver = False
                    if accept == True:
                        if I[1] > B and J[1] > F and moyenne_epaule1 <= moyenne_tete / 2 and moyenne_epaule2 <= moyenne_tete / 2 and moyenne_epaule1 >= moyenne_tete / 4 and moyenne_epaule2 >= moyenne_tete / 4 and G >= 1 and accept == True:
                            for i in range(local_min[ff] + 1, local_max[fg]):
                                if df['c'].iloc[i] >= J[1] and df['c'].iloc[i] <= J[1] + (moyenne_tete) / 4 and trouver == False:
                                    # if df['c'].iloc[i] > df['c'].iloc[local_min[ff]] and df['c'].iloc[i] <= J[1] + (moyenne_tete) / 4 and trouver == False:
                                    placejaune = i
                                    trouver = True
                            if trouver == True:
                                local_max89 = argrelextrema(mirande3['c'].values, np.greater, order=1, mode='clip')[0]
                                local_min89 = argrelextrema(mirande3['c'].values, np.less, order=1, mode='clip')[0]

                                highs89 = mirande3.iloc[local_max89, :]
                                lows89 = mirande3.iloc[local_min89, :]


                                compteur2 = compteur2 +1
                                fig1 = plt.figure(figsize=(10, 7))
                                plt.plot([], [], " ")
                                fig1.patch.set_facecolor('#17DE17')
                                fig1.patch.set_alpha(0.3)
                                plt.title(f'IETE : {ticker}', fontweight="bold", color='black')
                                mirande3['c'].plot(color=['blue'], label='Clotures')
                                mirande['c'].plot(color=['red'], label='Clotures', alpha=0.3)
                                plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                plt.text(local_min[ff], F, "F", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                plt.text(local_max[fg], G, "G", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                mirande2['c'].plot(color=['green'], linestyle='--', label='Ligne de coup')
                                plt.scatter(local_max[fa], A, color='blue')
                                plt.scatter(local_min[fb], B, color='blue')
                                plt.scatter(local_max[fc], C, color='blue')
                                plt.scatter(local_min[fd], D, color='blue')
                                plt.scatter(local_max[fe], E, color='blue')
                                plt.scatter(local_min[ff], F, color='blue')
                                plt.scatter(local_max[fg], G, color='blue')
                                plt.scatter(I[0], I[1], color='green')
                                plt.scatter(J[0], J[1], color='green')
                                plt.scatter(placejaune, df['c'].values[placejaune], color='orange', label='BUY')
                                plt.axhline(y=J[1] + moyenne_tete, linestyle='--', alpha=0.3, color='red',
                                            label='100% objectif')
                                plt.axhline(y=J[1] + (((moyenne_tete) / 2) + ((moyenne_tete) / 4)), linestyle='--', alpha=0.3,
                                            color='black', label='75% objectif')
                                plt.axhline(y=J[1] + (moyenne_tete) / 2, linestyle='--', alpha=0.3, color='orange',
                                            label='50% objectif')
                                plt.axhline(y=J[1] + (moyenne_tete) / 4, linestyle='--', alpha=0.3, color='black',
                                            label='25% objectif')
                                plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)
                                #plt.scatter(x=highs89.index, y=highs89['c'], alpha=0.5)
                                #plt.scatter(x=lows89.index, y=lows89['c'], alpha=0.5)
                                button_width = 0.2
                                button_height = 0.075
                                button_space = 0.05
                                # Création du bouton pour acheter
                                button_ax = plt.axes([0.9 - button_width, 0.001, button_width, button_height], facecolor='none')
                                button = plt.Button(button_ax, 'Confirmer', color='white', hovercolor='lightgray')
                                button.on_clicked(lambda event: confirmer(event,df,local_max[fa],data,api_url_OHLC))

                                button_ax2 = plt.axes([0.125, 0.001, button_width, button_height],facecolor='none')
                                button2 = plt.Button(button_ax2, 'Indicateurs', color='white', hovercolor='lightgray')
                                button2.on_clicked(Indicateurs)


                                # plt.scatter(x=low.index, y=low["c"])
                                if activactiv == True:
                                    plt.show()
                                if activactiv == False:
                                    compteurjson = compteurjson + 1
                                    arg1 = df.drop(range(0, local_max[fa] - 1))
                                    arg1 = arg1.reset_index(drop=True)
                                    arg1.to_json(f'json_recent/{lettre}{random.randint(10**11, (10**12)-1)}.json')

                                # ----- creation variable des moyennes de la tete et epaules  pour les prochaines conditions-----#
                                if accept == True:
                                    moyenne_epaule1 = ((I[1] - B) + (C - B)) / 2
                                    moyenne_epaule2 = ((E - F) + (J[1] - F)) / 2
                                    moyenne_des_epaule = ((E - F) + (J[1] - F)) + ((E - F) + (J[1] - F)) / 4
                                    moyenne_tete = ((C - D) + (E - D)) / 2
                                # ----- creation variable des moyennes de la tete et epaules  pour les prochaines conditions-----#

                                    tuche = 0
                                    noo = 0
                                    place_pc = 0
                                    point_max = J[0] + ((J[0] - I[0]))
                                    point_max = int(round(point_max, 0))

                                    # ----- creation de la fonction Moyenne mobile  -----#
                                    def sma(data, window):
                                        sma = data.rolling(window=window).mean()
                                        return sma

                                    df['sma_20'] = sma(df['c'], 20)
                                    df['sma_50'] = sma(df['c'], 50)
                                    df['sma_100'] = sma(df['c'], 100)
                                    df.tail()
                                    # ----- creation de la fonction Moyenne mobile  -----#
                                    # ----- creation de la fonction RSI  -----#

                                    def rsi(df, periods=14, ema=True):

                                        close_delta = df['c'].diff()

                                        # Make two series: one for lower closes and one for higher closes
                                        up = close_delta.clip(lower=0)
                                        down = -1 * close_delta.clip(upper=0)

                                        if ema == True:
                                            # Use exponential moving average
                                            ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
                                            ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
                                        else:
                                            # Use simple moving average
                                            ma_up = up.rolling(window=periods, adjust=False).mean()
                                            ma_down = down.rolling(window=periods, adjust=False).mean()

                                        rsi = ma_up / ma_down
                                        rsi = 100 - (100 / (1 + rsi))
                                        return rsi

                                    df2['rsi'] = rsi(df2)
                                    df['rsi'] = rsi(df)

                                    def bb(data, sma, window):
                                        std = data.rolling(window=window).std()
                                        upper_bb = sma + std * 2
                                        lower_bb = sma - std * 2
                                        return upper_bb, lower_bb

                                    df['upper_bb'], df['lower_bb'] = bb(df['c'], df['sma_20'], 20)
                                    df.tail()

                                    def createMACD(df):
                                        df['e26'] = pd.Series.ewm(df['c'], span=26).mean()
                                        df['e12'] = pd.Series.ewm(df['c'], span=12).mean()
                                        df['MACD'] = df['e12'] - df['e26']
                                        df['e9'] = pd.Series.ewm(df['MACD'], span=9).mean()
                                        df['HIST'] = df['MACD'] - df['e9']

                                    createMACD(df)

                                    # ----- creation de la fonction RSI  -----#
                                    trouver = False
                                    for i in range(local_min[ff]+1,local_max[fg]+5):
                                        if df['c'].iloc[i] >= J[1] and df['c'].iloc[i] <= J[1] + (moyenne_tete) / 4 and trouver == False:
                                        #if df['c'].iloc[i] > df['c'].iloc[local_min[ff]] and df['c'].iloc[i] <= J[1] + (moyenne_tete) / 4 and trouver == False:
                                            placejaune = i
                                            trouver = True
                                # ----- condition pour filtrer iete  -----#
                                if I[1] > B :#and J[1] > F and moyenne_epaule1 <= moyenne_tete / 2 and moyenne_epaule2 <= moyenne_tete / 2 and moyenne_epaule1 >= moyenne_tete / 4 and moyenne_epaule2 >= moyenne_tete / 4 and accept == True and G >= J[1] and trouver == True:# and df['c'].values[-2] <= J[1] + (moyenne_tete) / 4 and df['c'].values[-2] >= J[1] and df['c'].values[-1] <= J[1] + (moyenne_tete) / 4 and df['c'].values[-1] >= J[1]:
                                # ----- condition pour filtrer iete  -----#
                                    if antholemuscler == True:
                                        compteur3 = compteur3 +1
                                        # ----- systeme de notation des iete en fonction de la beaute et de la perfection de realisation  -----#
                                        note = 0
                                        pourcentage_10_tete = (10 * (local_max[fe] - local_max[fc]))/100
                                        pourcentage_10_ep1 = (20 * (local_max[fc] - I[0])) / 100
                                        pourcentage_10_ep2 = (20 * (J[0] - local_max[fe])) / 100
                                        pourcentage_20_moy_epaule = (30 * moyenne_des_epaule) / 100

                                        debugage = []
                                        if local_min[fd] < (local_max[fc] + local_max[fe])/2 + pourcentage_10_tete and local_min[fd] > (local_max[fc] + local_max[fe])/2 - pourcentage_10_tete : # D doit etre au millieu (10% de marge)
                                            note = note + 3
                                            debugage.append(1)

                                        if local_min[fb] < (I[0] + local_max[fc])/2 + pourcentage_10_ep1 and local_min[fb] > (I[0] + local_max[fc])/2 - pourcentage_10_ep1: # B doit etre au millieu (10% de marge)
                                            note = note + 1
                                            debugage.append(2)

                                        if local_min[ff] < (J[0] + local_max[fe])/2 + pourcentage_10_ep2 and local_min[ff] > (J[0] + local_max[fe])/2 - pourcentage_10_ep2: # F doit etre au millieu (10% de marge)
                                            note = note + 1
                                            debugage.append(3)

                                        if moyenne_epaule1 < moyenne_des_epaule + pourcentage_20_moy_epaule and moyenne_epaule1 > moyenne_des_epaule - pourcentage_20_moy_epaule and moyenne_epaule2 < moyenne_des_epaule + pourcentage_20_moy_epaule and moyenne_epaule2 > moyenne_des_epaule - pourcentage_20_moy_epaule : # les epaules doivent etre de presque meme hauteur
                                            note = note + 1
                                            debugage.append(4)

                                        if B < F :
                                            if (((F - B) *100) / moyenne_tete) <= 30:
                                                note = note + 2
                                                debugage.append(5)


                                        if B > F:
                                            if (((B - F) *100) / moyenne_tete) <= 30:
                                                note = note + 2
                                                debugage.append(5)

                                        if B == F:
                                            note = note + 2
                                            debugage.append(5)

                                        if (local_max[fe] - local_max[fc]) > local_max[fc] - I[0] and (local_max[fe] - local_max[fc]) > J[0] - local_max[fe]: # tete plus large que les 2 epaules
                                            note = note + 0.5
                                            debugage.append(6)

                                        debugage1 = 'NULL'
                                        if debugage == True:
                                            debugage1 = 'Atteint en Volatilitée'
                                        if debugage == False:
                                            debugage1 = 'Pas atteint en Volatilitée'

                                        #if il y a pas de bruit:
                                            #note = note + 1.5
                                # --    --- systeme de notation des iete en fonction de la beaute et de la perfection de realisation  -----#

                                        # ----- initialisation des données d'aide -----#
                                        #playsound('note.wav')
                                        moins50p = J[1] - ((moyenne_tete) / 2)
                                        plus_grand = round((J[1] + (moyenne_tete) / 2), 5)
                                        plus_petit = round(df['c'].iloc[placejaune], 5)
                                        pourcent_chercher = ((plus_grand - plus_petit) / plus_petit)*100
                                        pourcent_chercher = round(pourcent_chercher, 2)
                                        pourcent_perdu = ((round(G, 5)-round(F, 5))*100)/round(G, 5)
                                        pourcent_perdu = round(pourcent_perdu, 2)
                                        pertenet = 0.005 * G
                                        if pertenet < 1:
                                            pertenet = 1
                                        pertenet = pertenet * 2  # 2 fois puisque maker et taker
                                        pertenet_pourcent = (pertenet * 100) / 500
                                        pourcent_chercher2 = pourcent_chercher - pertenet_pourcent
                                        pourcent_chercher2 = round(pourcent_chercher2, 2)

                                        pourcent_perdu = pourcent_perdu - pertenet_pourcent
                                        pourcent_perdu = round(pourcent_perdu, 2)
                                        # ----- initialisation des données d'aide -----#



                                        # ----- creer la figure et l'affichage MATPLOTLIB -----#
                                        fig = plt.figure(figsize=(10, 7))
                                        # fig.patch.set_facecolor('#17abde'
                                        plt.plot([], [], ' ')
                                        time_name2 = time_name1
                                        duree_figure = (placejaune - local_max[fa])*time1
                                        if duree_figure >= 75 and time_name1 == 'minute':
                                            duree_figure = duree_figure /60
                                            time_name2 = 'heure'


                                        if duree_figure >= 1440 and time_name1 == 'hour':
                                            duree_figure = duree_figure /24
                                            time_name2 = 'jour'

                                        trouver2 = False
                                        trouver3 = False
                                        duree_achat = 0
                                        for i in range(placejaune, mirande3.index[-1]):
                                            if df['c'].iloc[i] < F and trouver3 == False and trouver2 == False:
                                                placerouge = i
                                                trouver3 = True
                                                duree_achat = (placerouge - placejaune) * time1

                                            if df['h'].iloc[i] >= J[1] + (((moyenne_tete) / 2)) and trouver2 == False and trouver3 == False:
                                                placevert = i
                                                trouver2 = True
                                                duree_achat = (placevert - placejaune) * time1




                                        time_name3 = time_name1
                                        if duree_achat >= 75 and time_name1 == 'minute':
                                            duree_achat = duree_achat / 60
                                            time_name3 = 'heure'


                                        if duree_achat >= 1440 and time_name1 == 'hour':
                                            duree_achat = duree_achat / 24
                                            time_name3 = 'jour'

                                        noir = []
                                        for i in range(placejaune - 1, mirande3.index[-1]):
                                            noir.append(i)
                                        mirande4 = df.iloc[noir, :]
                                        noir1 = {'c': noir}
                                        noir2 = pd.DataFrame(data=noir1)

                                        plt.title(f'IETE : {ticker} | {time1} {time_name1}  | +{pourcent_chercher}% BRUT | +{pourcent_chercher2}% NET | -{pourcent_perdu}% NET | {duree_figure} {time_name2} | {duree_achat} {time_name3} |', fontweight="bold", color='black')
                                        mirande3['c'].plot(color=['blue'], label='Clotures')
                                        mirande4['h'].plot(color=['green'], alpha=0.3, label='Highs')
                                        mirande4['l'].plot(color=['red'], alpha=0.3, label='Lows')
                                        #df['sma_20'].plot(label='Ema 20', linestyle='-', linewidth=1.2, color='green')
                                        #df['sma_50'].plot(label='Ema 50', linestyle='-', linewidth=1.2, color='red')
                                        #df['sma_100'].plot(label='Ema 100', linestyle='-', linewidth=1.2, color='blue')
                                        # mirande['c'].plot(color=['#FF0000'])
                                        mirande2['c'].plot(color=['green'], linestyle='--', label='Ligne de coup')
                                        plt.axhline(y=J[1] + moyenne_tete, linestyle='--', alpha=0.3, color='red', label='100% objectif')
                                        plt.axhline(y=J[1] + (((moyenne_tete) / 2) + ((moyenne_tete) / 4)), linestyle='--', alpha=0.3, color='black', label='75% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 2, linestyle='--', alpha=0.3, color='orange', label='50% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 4, linestyle='--', alpha=0.3, color='black', label='25% objectif')
                                        plt.axhline(y=moins50p, linestyle='--', alpha=0.3, color='purple', label='-50% objectif')
                                        plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)
                                        taille_diviser = (local_max[fe] - local_max[fc]) / (local_min[fd] - local_max[fc])
                                        # point_max = J[0]+((J[0] - I[0])/taille_diviser)
                                        point_max = J[0] + ((J[0] - I[0]))
                                        point_max = int(round(point_max, 0))
                                        # plt.scatter(point_max, df['c'].values[int(round(point_max, 0))], color='red',label='Max temps realisation')
                                        plt.legend()
                                        plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(J[0], J[1] + (moyenne_tete) / 2, f"{round((J[1] + (moyenne_tete) / 2), 5)}", ha='left', style='normal', size=10.5, color='orange', wrap=True)
                                        plt.text(J[0], moins50p, f"{round(moins50p, 5)}", ha='left',style='normal', size=10.5, color='purple', wrap=True)
                                        plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_min[fd], D, f"D {round(D, 5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_min[ff], F, f"F  {round(F, 5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        #plt.text(local_max[fg], G, f"G", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(placejaune, df['c'].iloc[placejaune], f"  BUY  {round(df['c'].iloc[placejaune], 5)}", ha='left', style='normal', size=10.5, color='red',
                                         wrap=True)
                                        plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
                                        plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
                                        # test_valeur = df['c'].iloc[round(J[0]) + 1]
                                        # plt.text(round(J[0]), df['c'].iloc[round(J[0])], f"J+1 {test_valeur}", ha='left',style='normal', size=10.5, color='#00FF36', wrap=True)
                                        #plt.scatter(len(df['c']) - 1, df['c'].values[-1], color='blue', label='liveprice')
                                        plt.scatter(placejaune, df['c'].values[placejaune], color='orange', label='BUY')
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['h'].values[placevert], color='green', label='SELL')

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['c'].values[placerouge], color='red', label='SELL')
                                        plt.scatter(local_max[fa], A, color='blue')
                                        plt.scatter(local_min[fb], B, color='blue')
                                        plt.scatter(local_max[fc], C, color='blue')
                                        plt.scatter(local_min[fd], D, color='blue')
                                        plt.scatter(local_max[fe], E, color='blue')
                                        plt.scatter(local_min[ff], F, color='blue')
                                        plt.savefig(f'/home/mat/Bureau/musculage/0.png')
                                        plt.show()
                                        fig = plt.figure(figsize=(10, 7))
                                        # fig.patch.set_facecolor('#17abde'
                                        plt.plot([], [], ' ')
                                        plt.title(f'IETE : {ticker} | {time1} {time_name1} | +{pourcent_chercher}% | {duree_figure} {time_name2} | {duree_achat} {time_name3} |', fontweight="bold", color='black')
                                        plt.bar(df['v'][(mirande3.index[0]):(mirande3.index[-1]) + 1].index, df['v'].values[(mirande3.index[0]):(mirande3.index[-1]) + 1])
                                        plt.scatter(placejaune, df['v'].values[placejaune], color='orange', label='BUY')
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['v'].values[placevert], color='green', label='SELL')

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['v'].values[placerouge], color='red', label='SELL')

                                        plt.text(local_max[fa], df['v'].values[local_max[fa]], "A", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_min[fb], df['v'].values[local_min[fb]], "B", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_max[fc], df['v'].values[local_max[fc]], "C", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_min[fd], df['v'].values[local_min[fd]], "D", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_max[fe], df['v'].values[local_max[fe]], "E", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_min[ff], df['v'].values[local_min[ff]], "F", ha='left', style='normal', size=10.5, color='red',
                                         wrap=True)
                                        plt.savefig(f'/home/mat/Bureau/musculage/1.png')
                                        plt.show()
                                        #----- creer la figure et l'affichage MATPLOTLIB -----#


                                        # -----------------------lire et connaitre nom de image et enregistrer image (pour remplacer le plt.show)--------------------------#
                                        # file = open('/home/mat/Bureau/logi3_direct/compteur_images.txt', 'r')
                                        # compteur_nombre_image = int(file.read())
                                        # file.close()
                                        # file = open('/home/mat/Bureau/logi3_direct/compteur_images.txt', 'w')
                                        # compteur_nombre_image = compteur_nombre_image + 1
                                        # file.write(f'{compteur_nombre_image}')
                                        # file.close()
                                        # plt.savefig(f'images/figure_{compteur_nombre_image}.png'
                                        # -----------------------lire et connaitre nom de image et enregistrer image (pour remplacer le plt.show)--------------------------#

                                        fig = plt.figure(figsize=(10, 7))
                                        # fig.patch.set_facecolor('#17abde'
                                        plt.plot([], [], ' ')
                                        plt.subplot(2, 1, 1)
                                        plt.title(f'IETE : {ticker} | {time1} {time_name1} | +{pourcent_chercher}% | {duree_figure} {time_name2} | {duree_achat} {time_name3} |', fontweight="bold", color='black')
                                        df['rsi'].iloc[(local_min[fa] - 1):(local_max[ff] + 5)].plot(color=['purple'], alpha=0.6)
                                        plt.axhline(y=30, alpha=0.3, color='black')
                                        plt.axhline(y=70, alpha=0.3, color='black')
                                        plt.axhline(y=50, linestyle='--', alpha=0.3, color='grey')
                                        plt.legend(['Rsi'])

                                        plt.text(local_max[fa], df['rsi'].iloc[local_max[fa]], "A", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_min[fb], df['rsi'].iloc[local_min[fb]], "B", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_max[fc], df['rsi'].iloc[local_max[fc]], "C", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_min[fd], df['rsi'].iloc[local_min[fd]], "D", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_max[fe], df['rsi'].iloc[local_max[fe]], "E", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_min[ff], df['rsi'].iloc[local_min[ff]], "F", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_max[fg], df['rsi'].iloc[local_max[fg]], "G", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.scatter(placejaune, df['rsi'].values[placejaune], color='orange', label='BUY')
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['rsi'].values[placevert], color='green', label='SELL')

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['rsi'].values[placerouge], color='red', label='SELL')
                                        a2 = plt.subplot(2, 1, 2)

                                        mirande3['c'].plot(color=['blue'], alpha=0.3, label='Clotures')
                                        mirande2['c'].plot(color=['green'], alpha=0.3, linestyle='--', label='Ligne de coup')
                                        plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[ff], F, "F", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fg], G, "G", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='black', wrap=True)
                                        plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='black', wrap=True)
                                        plt.axhline(y=J[1] + moyenne_tete, linestyle='--', alpha=0.3, color='red', label='100% objectif')
                                        plt.axhline(y=J[1] + (((moyenne_tete) / 2) + ((moyenne_tete) / 4)), linestyle='--', alpha=0.3,
                                                    color='black', label='75% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 2, linestyle='--', alpha=0.3, color='orange',
                                                    label='50% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 4, linestyle='--', alpha=0.3, color='black', label='25% objectif')
                                        plt.axhline(y=moins50p, linestyle='--', alpha=0.3, color='purple', label='-50% objectif')
                                        plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)

                                        plt.scatter(placejaune, df['c'].values[placejaune], color='orange', label='BUY')
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['c'].values[placevert], color='green', label='SELL')

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['c'].values[placerouge], color='red', label='SELL')

                                        plt.legend()
                                        plt.savefig(f'/home/mat/Bureau/musculage/2.png')
                                        plt.show()


                                        fig = plt.figure(figsize=(10, 7))

                                        #fig.patch.set_facecolor('#17abde')


                                        plt.plot([], [], ' ')

                                        plt.title(f'IETE : {ticker} | {time1} {time_name1} | +{pourcent_chercher}% | {duree_figure} {time_name2} | {duree_achat} {time_name3} |', fontweight="bold", color='black')
                                        mirande3['c'].plot(color=['blue'], alpha=0.3, label ='Clotures')
                                        mirande2['c'].plot(color=['green'], alpha=0.3, linestyle='--', label ='Ligne de coup')
                                        plt.axhline(y=J[1] + moyenne_tete, linestyle='--', alpha=0.3, color='red', label='100% objectif')
                                        plt.axhline(y=J[1] + (((moyenne_tete) / 2) + ((moyenne_tete) / 4)), linestyle='--', alpha=0.3,
                                            color='black', label='75% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 2, linestyle='--', alpha=0.3, color='orange',
                                            label='50% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 4, linestyle='--', alpha=0.3, color='black', label='25% objectif')
                                        plt.axhline(y=moins50p, linestyle='--', alpha=0.3, color='purple', label='-50% objectif')
                                        plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)



                                        width = .4
                                        width2 = .05

                                        #define up and down prices
                                        up = mirande3[mirande3.c >= mirande3.o]
                                        down = mirande3[mirande3.c < mirande3.o]

                                        #define colors to use
                                        col1 = 'green'
                                        col2 = 'red'

                                        #plot up prices9
                                        plt.bar(up.index, up.c - up.o, width, bottom=up.o, color=col1, label ='Bougies Japonnaises')
                                        plt.bar(up.index, up.h - up.c, width2, bottom=up.c, color=col1)
                                        plt.bar(up.index, up.l - up.o, width2, bottom=up.o, color=col1)

                                        #plot down prices
                                        plt.bar(down.index, down.c - down.o, width, bottom=down.o, color=col2)
                                        plt.bar(down.index, down.h - down.o, width2, bottom=down.o, color=col2)
                                        plt.bar(down.index, down.l - down.c, width2, bottom=down.c, color=col2)
                                        plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='black',
                                                wrap=True)
                                        plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='black',
                                                wrap=True)
                                        plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='black',
                                                wrap=True)
                                        plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='black',
                                                wrap=True)
                                        plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='black',
                                                wrap=True)
                                        plt.text(local_min[ff], F, "F", ha='left', style='normal', size=10.5, color='black',
                                                wrap=True)
                                        plt.text(local_max[fg], G, "G", ha='left', style='normal', size=10.5, color='black',
                                                wrap=True)
                                        plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='black', wrap=True)
                                        plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='black', wrap=True)

                                        plt.scatter(placejaune, df['c'].values[placejaune], color='orange', label='BUY', s=100)
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['c'].values[placevert], color='green', label='SELL', s=100)

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['c'].values[placerouge], color='red', label='SELL', s=100)


                                        plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)
                                        plt.legend()
                                        plt.savefig(f'/home/mat/Bureau/musculage/3.png')
                                        plt.show()
#-------------------            ----    --------------------------------------------------- boolinger--------------------------------------------------------#
                                        fig = plt.figure(figsize=(10, 7))

                                        # fig.patch.set_facecolor('#17abde')

                                        plt.plot([], [], ' ')

                                        plt.title(f'IETE : {ticker} | {time1} {time_name1} | {start} | {end} | {start2} |', fontweight="bold", color='black')
                                        mirande3['c'].plot(color=['blue'], alpha=0.3, label='Clotures')
                                        mirande2['c'].plot(color=['green'], alpha=0.3, linestyle='--', label='Ligne de coup')
                                        plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[ff], F, "F", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fg], G, "G", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='black', wrap=True)
                                        plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='black', wrap=True)

                                        df['upper_bb'].iloc[(local_max[fa] - 1):(local_max[fg]) + 5].plot(label='Haut Band', linestyle='--', linewidth=1, color='red')
                                        df['sma_20'].iloc[(local_max[fa]-1):(local_max[fg]) + 5].plot(label='Ema 20', linestyle='-', linewidth=1.2, color='grey')
                                        df['lower_bb'].iloc[(local_max[fa]-1):(local_max[fg]) + 5].plot(label='Bas Band', linestyle='--', linewidth=1, color='green')
                                        plt.axhline(y=J[1] + moyenne_tete, linestyle='--', alpha=0.3, color='red', label='100% objectif')
                                        plt.axhline(y=J[1] + (((moyenne_tete) / 2) + ((moyenne_tete) / 4)), linestyle='--', alpha=0.3,
                                            color='black', label='75% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 2, linestyle='--', alpha=0.3, color='orange',
                                            label='50% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 4, linestyle='--', alpha=0.3, color='black', label='25% objectif')
                                        plt.axhline(y=moins50p, linestyle='--', alpha=0.3, color='purple', label='-50% objectif')
                                        plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)
                                        plt.scatter(placejaune, df['c'].values[placejaune], color='orange', label='BUY')
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['c'].values[placevert], color='green', label='SELL')

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['c'].values[placerouge], color='red', label='SELL')

                                        plt.legend()
                                        plt.savefig(f'/home/mat/Bureau/musculage/4.png')
                                        plt.show()
# ------------------            ----    ---------------------------------------------------- boolinger--------------------------------------------------------#

                                        fig = plt.figure(figsize=(10, 7))

                                        # fig.patch.set_facecolor('#17abde')

                                        plt.plot([], [], ' ')
                                        plt.subplot(2, 1, 1)
                                        plt.title(f'IETE : {ticker} | {time1} {time_name1} | +{pourcent_chercher}% | {duree_figure} {time_name2} | {duree_achat} {time_name3} |', fontweight="bold", color='black')
                                        plt.bar(df['HIST'][(local_max[fa]-2):(local_max[fg]) + 7].index,df['HIST'].values[(local_max[fa]-2):(local_max[fg]) + 7], color='purple', alpha=0.6)
                                        df['MACD'].iloc[(local_max[fa] - 2):(local_max[fg] + 7)].plot(color=['blue'], alpha=0.6)
                                        df['e9'].iloc[(local_max[fa] - 2):(local_max[fg] + 7)].plot(color=['red'], alpha=0.6)
                                        plt.text(local_max[fa], df['HIST'].iloc[(local_max[fa])], "A", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_min[fb], df['HIST'].iloc[(local_min[fb])], "B", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_max[fc], df['HIST'].iloc[(local_max[fc])], "C", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_min[fd], df['HIST'].iloc[(local_min[fd])], "D", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_max[fe], df['HIST'].iloc[(local_max[fe])], "E", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_min[ff], df['HIST'].iloc[(local_min[ff])], "F", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_max[fg], df['HIST'].iloc[(local_max[fg])], "G", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        #plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
                                        #plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
                                        plt.scatter(placejaune, df['HIST'].values[placejaune], color='orange', label='BUY')
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['HIST'].values[placevert], color='green', label='SELL')

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['HIST'].values[placerouge], color='red', label='SELL')




                                        plt.legend(['Macd','Signal','histogramme'])
                                        a2 = plt.subplot(2, 1, 2)

                                        mirande3['c'].plot(color=['blue'], alpha=0.3, label='Clotures')
                                        mirande2['c'].plot(color=['green'], alpha=0.3, linestyle='--', label='Ligne de coup')
                                        plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[ff], F, "F", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fg], G, "G", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='black', wrap=True)
                                        plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='black', wrap=True)
                                        plt.axhline(y=J[1] + moyenne_tete, linestyle='--', alpha=0.3, color='red', label='100% objectif')
                                        plt.axhline(y=J[1] + (((moyenne_tete) / 2) + ((moyenne_tete) / 4)), linestyle='--', alpha=0.3,
                                            color='black', label='75% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 2, linestyle='--', alpha=0.3, color='orange',
                                            label='50% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 4, linestyle='--', alpha=0.3, color='black', label='25% objectif')
                                        plt.axhline(y=moins50p, linestyle='--', alpha=0.3, color='purple', label='-50% objectif')
                                        plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)

                                        plt.scatter(placejaune, df['c'].values[placejaune], color='orange', label='BUY')
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['c'].values[placevert], color='green', label='SELL')

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['c'].values[placerouge], color='red', label='SELL')

                                        plt.legend()
                                        plt.savefig(f'/home/mat/Bureau/musculage/5.png')
                                        plt.show()

                # --            ---     enregister des données inutiles -----#
                                        data_A.append(A)
                                        data_B.append(B)
                                        data_C.append(C)
                                        data_D.append(D)
                                        data_E.append(E)
                                        data_F.append(F)
                                        data_F.append(G)
                                        data_A_ = pd.DataFrame(data_A, columns=['A'])
                                        data_B_ = pd.DataFrame(data_B, columns=['B'])
                                        data_C_ = pd.DataFrame(data_C, columns=['C'])
                                        data_D_ = pd.DataFrame(data_D, columns=['D'])
                                        data_E_ = pd.DataFrame(data_E, columns=['E'])
                                        data_F_ = pd.DataFrame(data_E, columns=['F'])
                                        data_G_ = pd.DataFrame(data_E, columns=['G'])
                                        df_IETE = pd.concat([data_A_, data_B_, data_C_, data_D_, data_E_, data_F_, data_G_], axis=1)
                                        # ----- enregister des données inutiles -----#
                                        antholemuscler = False

                fa = fa + 1
                fb = fb + 1
                fc = fc + 1
                fd = fd + 1
                fe = fe + 1
                ff = ff + 1
                fg = fg + 1
                print(f'{compteur} iete on etaient trouvés')
                print(f'{compteur2} reussite')
                print(f'{compteur3} big reussite')
                print('----------------------------------------------------------------------', flush=True)
            else:
                print('pas assez de place pour continuer')
                i = 1
# ----- fonction Principale -----#

# ----- traduction francais anglais pour appel polygon -----#
minute = "minute"
heure = "hour"
jour = "day"
# ----- traduction francais anglais pour appel polygon -----#
TETE = 2.909
#databax = ['A', 'AA', 'AAA', 'AAAU', 'AAC', 'AACG', 'AACI', 'AACIU', 'AADI', 'AADR', 'AAIC', 'AAIC', 'AAIC', 'AAIN', 'AAL', 'AAMC', 'AAME', 'AAN', 'AAOI', 'AAON', 'AAP', 'AAPL', 'AAT', 'AAU', 'AAWW', 'AAXJ', 'AB', 'ABB', 'ABBV', 'ABC', 'ABCB', 'ABCL', 'ABCM', 'ABEO', 'ABEQ', 'ABEV', 'ABG', 'ABIO', 'ABM', 'ABNB', 'ABOS', 'ABR', 'ABSI', 'ABST', 'ABT', 'ABUS', 'ABVC', 'AC', 'ACA', 'ACAB', 'ACACU', 'ACAD', 'ACAH', 'ACAHU', 'ACAQ', 'ACAX', 'ACAXR', 'ACAXU', 'ACB', 'ACBA', 'ACBAU', 'ACCD', 'ACCO', 'ACEL', 'ACER', 'ACES', 'ACET', 'ACGL', 'ACGLN', 'ACGLO', 'ACHC', 'ACHL', 'ACHR', 'ACHV', 'ACI', 'ACIO', 'ACIU', 'ACIW', 'ACLS', 'ACLX', 'ACM', 'ACMR', 'ACN', 'ACNB', 'ACON', 'ACOR', 'ACP', 'ACQR', 'ACQRU', 'ACR', 'ACRE', 'ACRO', 'ACRS', 'ACRX', 'ACSI', 'ACST', 'ACT', 'ACTG', 'ACTV','ACU', 'ACV', 'ACVA', 'ACVF', 'ACWI', 'ACWV', 'ACWX', 'ACXP', 'ADAG', 'ADAL', 'ADALU', 'ADAP', 'ADBE', 'ADC', 'ADCT', 'ADER', 'ADERU', 'ADES', 'ADEX', 'ADFI', 'ADI', 'ADIL', 'ADIV', 'ADM', 'ADMA', 'ADME', 'ADMP', 'ADN', 'ADNT', 'ADOC', 'ADOCR', 'ADP', 'ADPT', 'ADRE', 'ADRT', 'ADSE', 'ADSK', 'ADT', 'ADTH', 'ADTN', 'ADTX', 'ADUS', 'ADV', 'ADVM', 'ADX', 'ADXN', 'AE', 'AEAE', 'AEAEU', 'AEE', 'AEF', 'AEFC', 'AEG', 'AEHL', 'AEHR', 'AEI', 'AEIS', 'AEL', 'AEM', 'AEMB', 'AEMD', 'AENZ', 'AEO', 'AEP', 'AEPPZ', 'AER', 'AES', 'AESC', 'AESR', 'AEVA', 'AEY', 'AEYE', 'AEZS', 'AFAR', 'AFARU', 'AFB', 'AFBI', 'AFCG', 'AFG', 'AFGB', 'AFGC', 'AFGD', 'AFGE', 'AFIB', 'AFIF', 'AFK', 'AFL', 'AFLG', 'AFMC', 'AFMD', 'AFRI', 'AFRM', 'AFSM', 'AFT', 'AFTR', 'AFTR', 'AFTY', 'AFYA', 'AG', 'AGAC', 'AGAC', 'AGBA', 'AGCO', 'AGD', 'AGE', 'AGEN', 'AGFS', 'AGFY', 'AGG', 'AGGH', 'AGGR', 'AGGRU', 'AGGY', 'AGI', 'AGIH', 'AGIL', 'AGIO', 'AGL', 'AGLE', 'AGM', 'AGMH', 'AGNC', 'AGNCM', 'AGNCN', 'AGNCO', 'AGNCP', 'AGNG', 'AGO', 'AGOV', 'AGOX', 'AGQ', 'AGR', 'AGRH', 'AGRI', 'AGRO', 'AGRX', 'AGS', 'AGTI', 'AGX', 'AGYS', 'AGZ', 'AGZD', 'AHCO', 'AHG', 'AHH', 'AHHX', 'AHI', 'AHOY', 'AHRN', 'AHRNU', 'AHT','AHYB', 'AI', 'AIA', 'AIB', 'AIBBR', 'AIBBU', 'AIC', 'AIEQ', 'AIF', 'AIG', 'AIH', 'AIHS', 'AILG', 'AILV', 'AIM', 'AIMBU', 'AIMC', 'AIMD', 'AIN', 'AINC', 'AIO', 'AIP', 'AIQ', 'AIR', 'AIRC', 'AIRG', 'AIRI', 'AIRR', 'AIRS', 'AIRT', 'AIRTP', 'AIT', 'AIU', 'AIV', 'AIVI', 'AIVL', 'AIZ', 'AIZN', 'AJG', 'AJRD', 'AJX', 'AJXA', 'AKA', 'AKAM', 'AKAN', 'AKBA', 'AKR', 'AKRO', 'AKTS', 'AKTX', 'AKU', 'AKYA', 'AL', 'ALB', 'ALC', 'ALCC', 'ALCO', 'ALDX', 'ALE', 'ALEC', 'ALEX', 'ALG', 'ALGM', 'ALGN', 'ALGS', 'ALGT', 'ALHC', 'ALIM', 'ALIT', 'ALK', 'ALKS', 'ALKT', 'ALL', 'ALLE', 'ALLG', 'ALLK', 'ALLO', 'ALLR', 'ALLT', 'ALLY', 'ALNY', 'ALOR', 'ALORU', 'ALOT', 'ALPA', 'ALPAU', 'ALPN', 'ALPP', 'ALR', 'ALRM', 'ALRN', 'ALRS', 'ALSA', 'ALSAR', 'ALSAU', 'ALSN', 'ALT', 'ALTG', 'ALTL', 'ALTO', 'ALTR', 'ALTU', 'ALTUU', 'ALTY', 'ALV', 'ALVO', 'ALVR', 'ALX', 'ALXO', 'ALYA', 'ALZN', 'AM', 'AMAL', 'AMAM', 'AMAO', 'AMAT', 'AMAX', 'AMBA', 'AMBC', 'AMBO', 'AMBP', 'AMC', 'AMCR', 'AMCX', 'AMD', 'AME', 'AMED', 'AMEH', 'AMG', 'AMGN', 'AMH', 'AMJ', 'AMK', 'AMKR', 'AMLP', 'AMLX', 'AMN', 'AMNB', 'AMND', 'AMOM', 'AMOT', 'AMOV', 'AMP', 'AMPE', 'AMPG', 'AMPH', 'AMPL', 'AMPS', 'AMPY', 'AMR', 'AMRC', 'AMRK', 'AMRN', 'AMRS', 'AMRX', 'AMS', 'AMSC', 'AMSF', 'AMST', 'AMSWA', 'AMT', 'AMTB', 'AMTD', 'AMTI', 'AMTX', 'AMUB', 'AMWD', 'AMWL', 'AMX', 'AMYT', 'AMZA', 'AMZN', 'AN', 'ANAB', 'ANDE', 'ANEB', 'ANET', 'ANEW', 'ANF', 'ANGH', 'ANGI', 'ANGL', 'ANGN', 'ANGO', 'ANIK', 'ANIP', 'ANIX', 'ANNX', 'ANPC', 'ANSS', 'ANTE', 'ANTX', 'ANVS', 'ANY', 'ANZU', 'ANZUU', 'AOA', 'AOD', 'AOGO', 'AOK', 'AOM', 'AOMR', 'AON', 'AOR', 'AORT', 'AOS', 'AOSL', 'AOTG', 'AOUT', 'AP', 'APA', 'APAC', 'APACU', 'APAM', 'APCA', 'APCX', 'APD', 'APDN', 'APEI', 'APEN', 'APG', 'APGB', 'APH', 'API', 'APLD', 'APLE', 'APLS', 'APLT', 'APM', 'APMI', 'APMIU', 'APO', 'APOG', 'APP', 'APPF', 'APPH', 'APPN', 'APPS', 'APRE', 'APRN', 'APRZ', 'APT', 'APTM', 'APTMU', 'APTO', 'APTV', 'APTX', 'APVO', 'APWC', 'APXI','APXIU', 'APYX', 'AQB', 'AQGX', 'AQMS', 'AQN', 'AQNA', 'AQNB', 'AQNU', 'AQST', 'AQUA', 'AQWA', 'AR', 'ARAV', 'ARAY', 'ARB', 'ARBE', 'ARBG', 'ARBK', 'ARBKL', 'ARC', 'ARCB', 'ARCC', 'ARCE', 'ARCH', 'ARCM', 'ARCO', 'ARCT', 'ARDC', 'ARDS', 'ARDX', 'ARE', 'AREB', 'AREC', 'AREN', 'ARES', 'ARGD', 'ARGO', 'ARGT', 'ARGX', 'ARHS', 'ARI', 'ARIS', 'ARIZ', 'ARIZR', 'ARKF', 'ARKG', 'ARKK', 'ARKO', 'ARKQ', 'ARKR', 'ARKW', 'ARKX', 'ARL', 'ARLO', 'ARLP', 'ARMK', 'ARMP', 'ARMR', 'ARNC', 'AROC', 'AROW', 'ARQQ', 'ARQT', 'ARR', 'ARRW', 'ARRWU', 'ARRY', 'ARTE', 'ARTEU', 'ARTL', 'ARTNA', 'ARTW', 'ARVL', 'ARVN', 'ARW', 'ARWR', 'ARYD', 'ARYE', 'ASA', 'ASAI', 'ASAN', 'ASB', 'ASC', 'ASCA', 'ASCAR', 'ASCAU', 'ASCB', 'ASCBR', 'ASCBU', 'ASEA', 'ASET', 'ASG', 'ASGI', 'ASGN', 'ASH', 'ASHR', 'ASHS', 'ASHX', 'ASIX', 'ASLE', 'ASLN', 'ASM', 'ASMB', 'ASML', 'ASND', 'ASNS', 'ASO', 'ASPA', 'ASPN', 'ASPS', 'ASPU', 'ASPY', 'ASR', 'ASRT', 'ASRV', 'ASTC', 'ASTE', 'ASTI', 'ASTL', 'ASTR', 'ASTS', 'ASUR', 'ASX', 'ASXC', 'ASYS', 'ATAI', 'ATAK', 'ATAKR', 'ATAKU', 'ATAQ', 'ATCO', 'ATCOL', 'ATCX', 'ATEC', 'ATEK', 'ATEN', 'ATER', 'ATEX', 'ATFV', 'ATGE', 'ATHA', 'ATHE', 'ATHM', 'ATHX', 'ATI', 'ATIF', 'ATIP', 'ATKR', 'ATLC', 'ATLCL', 'ATLCP', 'ATLO', 'ATMP', 'ATNF', 'ATNI', 'ATNM', 'ATNX', 'ATO', 'ATOM', 'ATOS', 'ATR', 'ATRA', 'ATRC', 'ATRI', 'ATRO', 'ATSG', 'ATTO', 'ATUS', 'ATVI', 'ATXI', 'ATXS', 'ATY', 'AU', 'AUB', 'AUBN', 'AUD', 'AUDC', 'AUGX', 'AUGZ', 'AUID', 'AUMN', 'AUPH', 'AUR', 'AURA', 'AURC', 'AUSF', 'AUST', 'AUTL', 'AUUD', 'AUVI', 'AUVIP', 'AUY', 'AVA', 'AVAC', 'AVACU', 'AVAH', 'AVAL', 'AVAV', 'AVB', 'AVD', 'AVDE', 'AVDL', 'AVDV', 'AVDX', 'AVEM', 'AVES', 'AVGO', 'AVGR', 'AVHI', 'AVHIU', 'AVID', 'AVIG', 'AVIR', 'AVIV', 'AVK', 'AVLV', 'AVMU', 'AVNS', 'AVNT', 'AVNW', 'AVO', 'AVPT', 'AVRE', 'AVRO', 'AVSC', 'AVSD', 'AVSE', 'AVSF', 'AVSU', 'AVT', 'AVTE', 'AVTR', 'AVTX', 'AVUS', 'AVUV', 'AVXL', 'AVY', 'AWAY', 'AWF', 'AWH', 'AWI', 'AWK', 'AWP', 'AWR', 'AWRE', 'AWX', 'AWYX', 'AX', 'AXAC','AXDX', 'AXGN', 'AXL', 'AXLA', 'AXNX', 'AXON', 'AXP', 'AXR', 'AXS', 'AXSM', 'AXTA', 'AXTI', 'AY', 'AYI', 'AYRO', 'AYTU', 'AYX', 'AZ', 'AZEK', 'AZN', 'AZO', 'AZPN', 'AZRE', 'AZTA', 'AZUL', 'AZYO', 'AZZ', 'B', 'BA', 'BAB', 'BABA', 'BAC', 'BACA', 'BAD', 'BAFN', 'BAH', 'BAK', 'BAL', 'BALL', 'BALT', 'BALY', 'BAM', 'BANC', 'BAND', 'BANF', 'BANFP', 'BANR', 'BANX', 'BAOS', 'BAP', 'BAPR', 'BAR', 'BARK', 'BASE', 'BATL', 'BATRA', 'BATRK', 'BATT', 'BAUG', 'BAX', 'BB', 'BBAI', 'BBAR', 'BBAX', 'BBBY', 'BBC', 'BBCA', 'BBCP', 'BBD', 'BBDC', 'BBDO', 'BBEU', 'BBGI', 'BBH', 'BBIG', 'BBIN', 'BBIO', 'BBJP', 'BBLG', 'BBLN', 'BBMC', 'BBN', 'BBP', 'BBRE', 'BBSA', 'BBSC', 'BBSI', 'BBU', 'BBUC', 'BBUS', 'BBVA', 'BBW', 'BBWI', 'BBY', 'BC', 'BCAB', 'BCAN', 'BCAT', 'BCBP', 'BCC', 'BCD', 'BCDA', 'BCE', 'BCEL', 'BCH', 'BCI', 'BCIM', 'BCLI', 'BCM', 'BCML', 'BCO', 'BCOV', 'BCOW', 'BCPC', 'BCRX', 'BCS', 'BCSA', 'BCSAU', 'BCSF', 'BCTX', 'BCV', 'BCX', 'BCYC', 'BDC', 'BDCX', 'BDCZ', 'BDEC', 'BDJ', 'BDL', 'BDN', 'BDRY', 'BDSX', 'BDTX', 'BDX', 'BDXB', 'BE', 'BEAM', 'BEAT', 'BECN', 'BECO', 'BEDU', 'BEDZ', 'BEEM', 'BEKE', 'BELFA', 'BELFB', 'BEN', 'BEP', 'BEPC', 'BEPH', 'BEPI', 'BERY', 'BERZ', 'BEST', 'BETZ', 'BFAC', 'BFAM', 'BFC', 'BFEB', 'BFH', 'BFI', 'BFIN', 'BFIT', 'BFIX', 'BFK', 'BFLY', 'BFOR', 'BFRI', 'BFS', 'BFST', 'BFTR', 'BFZ', 'BG', 'BGB', 'BGCP', 'BGFV', 'BGH', 'BGI', 'BGLD', 'BGNE', 'BGR', 'BGRN', 'BGRY', 'BGS', 'BGSF', 'BGSX', 'BGT', 'BGX', 'BGXX', 'BGY', 'BH', 'BHAC', 'BHACU', 'BHAT', 'BHB', 'BHC', 'BHE', 'BHF', 'BHFAL', 'BHFAM', 'BHFAN', 'BHFAO', 'BHFAP', 'BHG', 'BHIL', 'BHK', 'BHLB', 'BHP', 'BHR', 'BHV', 'BHVN', 'BIB', 'BIBL', 'BICK', 'BIDS', 'BIDU', 'BIG', 'BIGC', 'BIGZ', 'BIIB', 'BIL', 'BILI', 'BILL', 'BILS', 'BIMI', 'BIO', 'BIOC', 'BIOL', 'BIOR', 'BIOS', 'BIOX', 'BIP', 'BIPC', 'BIPH', 'BIPI', 'BIRD', 'BIS', 'BIT', 'BITE', 'BITF', 'BITI', 'BITO', 'BITQ', 'BITS', 'BIV', 'BIVI', 'BIZD', 'BJ', 'BJAN', 'BJDX']


databaxA = ['BJK', 'BJRI', 'BJUL', 'BJUN', 'BK', 'BKAG', 'BKCC', 'BKCH', 'BKCI', 'BKD', 'BKE', 'BKEM', 'BKES', 'BKF', 'BKH', 'BKHY', 'BKI', 'BKIE', 'BKIS', 'BKKT', 'BKLC', 'BKLN', 'BKMC', 'BKN', 'BKNG', 'BKR', 'BKSB', 'BKSC',
 'BKSE', 'BKSY', 'BKT', 'BKTI', 'BKU', 'BKUI', 'BKUS', 'BKYI', 'BL', 'BLBD', 'BLBX', 'BLCM', 'BLCN', 'BLCO', 'BLD', 'BLDE', 'BLDG', 'BLDP', 'BLDR', 'BLE', 'BLES', 'BLEU', 'BLEUR', 'BLEUU', 'BLFS', 'BLFY', 'BLHY',
 'BLI', 'BLIN', 'BLK', 'BLKB', 'BLKC', 'BLMN', 'BLND', 'BLNG', 'BLNGU', 'BLNK', 'BLOK', 'BLPH', 'BLRX', 'BLTE', 'BLU', 'BLUA', 'BLUE', 'BLV', 'BLW', 'BLX', 'BLZE', 'BMA', 'BMAC', 'BMAQ', 'BMAQR', 'BMAQU', 'BMAR',
 'BMAY', 'BMBL', 'BME', 'BMEA', 'BMED', 'BMEZ', 'BMI', 'BMO', 'BMRA', 'BMRC', 'BMRN', 'BMTX', 'BMY', 'BND', 'BNDC', 'BNDD', 'BNDW', 'BNDX', 'BNE', 'BNED', 'BNGE', 'BNGO', 'BNIX', 'BNIXR', 'BNKD', 'BNKU', 'BNL',
 'BNNR', 'BNNRU', 'BNO', 'BNOV', 'BNOX', 'BNR', 'BNRG', 'BNS', 'BNSO', 'BNTC', 'BNTX', 'BNY', 'BOAC', 'BOAT', 'BOC', 'BOCN', 'BOCNU', 'BOCT', 'BODY', 'BOE', 'BOH', 'BOIL', 'BOKF', 'BOLT', 'BON', 'BOND', 'BOOM',
 'BOOT', 'BORR', 'BOSC', 'BOSS', 'BOTJ', 'BOTZ', 'BOUT', 'BOWL', 'BOX', 'BOXD', 'BOXL', 'BP', 'BPAC', 'BPACU', 'BPMC', 'BPOP', 'BPOPM', 'BPRN', 'BPT', 'BPTH', 'BPTS', 'BPYPM', 'BPYPN', 'BPYPO', 'BPYPP', 'BQ',
 'BR', 'BRAC', 'BRACR', 'BRACU', 'BRAG', 'BRBR', 'BRBS', 'BRC', 'BRCC', 'BRD', 'BRDG', 'BRDS', 'BREZ', 'BREZR', 'BRF', 'BRFH', 'BRFS', 'BRID', 'BRIV', 'BRIVU', 'BRKH', 'BRKHU', 'BRKL', 'BRKR', 'BRKY', 'BRLI',
 'BRLT', 'BRMK', 'BRN', 'BRO', 'BROG', 'BROS', 'BRP', 'BRQS', 'BRSP', 'BRT', 'BRTX', 'BRW', 'BRX', 'BRY', 'BRZE', 'BRZU', 'BSAC', 'BSAQ', 'BSBK', 'BSBR', 'BSCE', 'BSCN', 'BSCO', 'BSCP', 'BSCQ', 'BSCR', 'BSCS',
 'BSCT', 'BSCU', 'BSCV', 'BSDE', 'BSEA', 'BSEP', 'BSET', 'BSFC', 'BSGA', 'BSGAR', 'BSGAU', 'BSGM', 'BSIG', 'BSJN', 'BSJO', 'BSJP', 'BSJQ', 'BSJR', 'BSJS', 'BSJT', 'BSL', 'BSM', 'BSMN', 'BSMO', 'BSMP', 'BSMQ',
 'BSMR', 'BSMS', 'BSMT', 'BSMU', 'BSMV', 'BSMX', 'BSQR', 'BSRR', 'BST', 'BSTP', 'BSTZ', 'BSV', 'BSVN', 'BSX', 'BSY', 'BTA', 'BTAI', 'BTAL', 'BTB', 'BTBD', 'BTBT', 'BTCM', 'BTCS', 'BTCY', 'BTEC', 'BTEK', 'BTF',
 'BTG', 'BTHM', 'BTI', 'BTMD', 'BTO', 'BTOG', 'BTT', 'BTTR', 'BTTX', 'BTU', 'BTWN', 'BTWNU', 'BTZ', 'BUD', 'BUFB', 'BUFD', 'BUFF', 'BUFG', 'BUFQ', 'BUFR', 'BUFT', 'BUG', 'BUI', 'BUL', 'BULZ', 'BUR', 'BURL',
 'BUSE', 'BUYZ', 'BUZZ', 'BV', 'BVH', 'BVN', 'BVS', 'BVXV', 'BW', 'BWA', 'BWAC', 'BWACU', 'BWAQR', 'BWAQU', 'BWAY', 'BWB', 'BWBBP', 'BWC', 'BWCAU', 'BWEN', 'BWFG', 'BWG', 'BWMN', 'BWMX', 'BWNB', 'BWSN', 'BWV',
 'BWX', 'BWXT', 'BWZ', 'BX', 'BXC', 'BXMT', 'BXMX', 'BXP', 'BXRX', 'BXSL', 'BY', 'BYD', 'BYFC', 'BYLD', 'BYM', 'BYN', 'BYND', 'BYNO', 'BYNOU', 'BYRN', 'BYSI', 'BYTE', 'BYTS', 'BYTSU', 'BZ', 'BZFD', 'BZH', 'BZQ',
 'BZUN', 'C', 'CAAP', 'CAAS', 'CABA', 'CABO', 'CAC', 'CACC', 'CACG', 'CACI', 'CADE', 'CADL', 'CAE', 'CAF', 'CAG', 'CAH', 'CAKE', 'CAL', 'CALB', 'CALF', 'CALM', 'CALT', 'CALX', 'CAMP', 'CAMT', 'CAN', 'CANE', 'CANF',
 'CANG', 'CANO', 'CAPE', 'CAPL', 'CAPR', 'CAR', 'CARA', 'CARE', 'CARG', 'CARR', 'CARS', 'CARV', 'CARZ', 'CASA', 'CASH', 'CASI', 'CASS', 'CASY', 'CAT', 'CATC', 'CATH', 'CATO', 'CATY', 'CB', 'CBAN', 'CBAT', 'CBAY',
 'CBD', 'CBFV', 'CBH', 'CBIO', 'CBL', 'CBLS', 'CBNK', 'CBOE', 'CBON', 'CBRE', 'CBRG', 'CBRGU', 'CBRL', 'CBSE', 'CBSH', 'CBT', 'CBU', 'CBZ', 'CC', 'CCAI', 'CCAIU', 'CCAP', 'CCB', 'CCBG', 'CCCC', 'CCCS', 'CCD',
 'CCEL', 'CCEP', 'CCF', 'CCI', 'CCJ', 'CCK', 'CCL', 'CCLP', 'CCM', 'CCNE', 'CCNEP', 'CCO', 'CCOI', 'CCOR', 'CCRD', 'CCRN', 'CCRV', 'CCS', 'CCSI', 'CCTS', 'CCU', 'CCV', 'CCVI', 'CCZ', 'CD', 'CDAK', 'CDAQ', 'CDAQU',
 'CDAY', 'CDC', 'CDE', 'CDL', 'CDLX', 'CDMO', 'CDNA', 'CDNS', 'CDRE', 'CDRO', 'CDTX', 'CDW', 'CDX', 'CDXC', 'CDXS', 'CDZI', 'CDZIP', 'CE', 'CEAD', 'CEE', 'CEF', 'CEFA', 'CEFD', 'CEFS', 'CEG', 'CEI', 'CEIX',
 'CELC', 'CELH', 'CELU', 'CELZ', 'CEM', 'CEMB', 'CEMI', 'CEN', 'CENN', 'CENT', 'CENTA', 'CENX', 'CEPU', 'CEQP', 'CERE', 'CERS', 'CERT', 'CET', 'CETX', 'CETXP', 'CEV', 'CEVA', 'CEW', 'CF', 'CFA', 'CFB', 'CFBK',
 'CFCV', 'CFFE', 'CFFI', 'CFFN', 'CFFS', 'CFG', 'CFIV', 'CFIVU', 'CFLT', 'CFMS', 'CFO', 'CFR', 'CFRX', 'CFSB', 'CG', 'CGA', 'CGABL', 'CGAU', 'CGBD', 'CGC', 'CGCP', 'CGDV', 'CGEM', 'CGEN', 'CGGO', 'CGGR',
 'CGNT', 'CGNX', 'CGO', 'CGRN', 'CGTX', 'CGUS', 'CGW', 'CGXU', 'CHAA', 'CHAU', 'CHB', 'CHCI', 'CHCO', 'CHCT', 'CHD', 'CHDN', 'CHE', 'CHEA', 'CHEAU', 'CHEF', 'CHEK', 'CHGG', 'CHGX', 'CHH', 'CHI', 'CHIC',
 'CHIE', 'CHIH', 'CHII', 'CHIK', 'CHIM', 'CHIQ', 'CHIR', 'CHIS', 'CHIU', 'CHIX', 'CHK', 'CHKP', 'CHMG', 'CHMI', 'CHN', 'CHNA', 'CHNR', 'CHPT', 'CHRA', 'CHRB', 'CHRD', 'CHRS', 'CHRW', 'CHS', 'CHSCL', 'CHSCM',
 'CHSCN', 'CHSCO', 'CHSCP', 'CHT', 'CHTR', 'CHUY', 'CHW', 'CHWY', 'CHX', 'CHY', 'CI', 'CIA', 'CIB', 'CIBR', 'CID', 'CIDM', 'CIEN', 'CIF', 'CIFR', 'CIG', 'CIGI', 'CIH', 'CII', 'CIIG', 'CIIGU', 'CIK', 'CIL',
 'CIM', 'CINF', 'CING', 'CINT', 'CIO', 'CION', 'CIR', 'CISO', 'CITE', 'CITEU', 'CIVB', 'CIVI', 'CIX', 'CIZ', 'CIZN', 'CJJD', 'CKPT', 'CKX', 'CL', 'CLAA', 'CLAR', 'CLAY', 'CLAYU', 'CLB', 'CLBK', 'CLBR',
 'CLBT', 'CLDL', 'CLDT', 'CLDX', 'CLEU', 'CLF', 'CLFD', 'CLGN', 'CLH', 'CLIN', 'CLINR', 'CLINU', 'CLIR', 'CLIX', 'CLLS', 'CLM', 'CLMT', 'CLNE', 'CLNN', 'CLNR', 'CLOE', 'CLOER', 'CLOEU', 'CLOI', 'CLOU',
 'CLOV', 'CLPR', 'CLPS', 'CLPT', 'CLRB', 'CLRC', 'CLRCR', 'CLRCU', 'CLRG', 'CLRO', 'CLS', 'CLSA', 'CLSC', 'CLSD', 'CLSE', 'CLSK', 'CLSM', 'CLST', 'CLTL', 'CLVR', 'CLVT', 'CLW', 'CLWT', 'CLX', 'CLXT', 'CM',
 'CMA', 'CMAX', 'CMBM', 'CMBS', 'CMC', 'CMCA', 'CMCAU', 'CMCL', 'CMCM', 'CMCO', 'CMCSA', 'CMCT', 'CMDY', 'CME', 'CMF', 'CMG', 'CMI', 'CMLS', 'CMMB', 'CMP', 'CMPO', 'CMPR', 'CMPS', 'CMPX', 'CMRA', 'CMRE',
 'CMRX', 'CMS', 'CMSA', 'CMSC', 'CMSD', 'CMT', 'CMTG', 'CMTL', 'CMU', 'CN', 'CNA', 'CNBS', 'CNC', 'CNCR', 'CNDA', 'CNDB', 'CNDT', 'CNET', 'CNEY', 'CNF', 'CNFR', 'CNFRL', 'CNGL', 'CNGLU', 'CNHI', 'CNI', 'CNK',
 'CNM', 'CNMD', 'CNNE', 'CNO', 'CNOB', 'CNOBP', 'CNP', 'CNQ', 'CNRG', 'CNS', 'CNSL', 'CNSP', 'CNTA', 'CNTB', 'CNTG', 'CNTX', 'CNTY', 'CNX', 'CNXA', 'CNXC', 'CNXN', 'CNXT', 'CNYA', 'CO', 'COCO', 'COCP', 'CODA',
 'CODI', 'CODX', 'COE', 'COEP', 'COF', 'COFS', 'COGT', 'COHN', 'COHU', 'COIN', 'COKE', 'COLB', 'COLD', 'COLL', 'COLM', 'COM', 'COMB', 'COMM', 'COMP', 'COMS', 'COMSP', 'COMT', 'CONN', 'CONX', 'CONXU', 'COO',
 'COOK', 'COOL', 'COOLU', 'COOP', 'COP', 'COPX', 'CORN', 'CORP', 'CORR', 'CORS', 'CORT', 'COSM', 'COST', 'COTY', 'COUR', 'COW', 'COWZ', 'CP', 'CPA', 'CPAA', 'CPAAU', 'CPAC', 'CPB', 'CPE', 'CPER', 'CPF',
 'CPG', 'CPHC', 'CPHI', 'CPI', 'CPII', 'CPIX', 'CPK', 'CPLP', 'CPNG', 'CPOP', 'CPRI', 'CPRT', 'CPRX', 'CPS', 'CPSH', 'CPSI', 'CPSS', 'CPT', 'CPTK', 'CPTN', 'CPUH', 'CPZ', 'CQP', 'CQQQ', 'CR', 'CRAI', 'CRAK',
 'CRBN', 'CRBP', 'CRBU', 'CRC', 'CRCT', 'CRDF', 'CRDL', 'CRDO', 'CREC', 'CRECU', 'CREG', 'CRESY', 'CREX', 'CRF', 'CRGE', 'CRGY', 'CRH', 'CRI', 'CRIS', 'CRIT', 'CRK', 'CRKN', 'CRL', 'CRM', 'CRMD', 'CRMT',
 'CRNC', 'CRNT', 'CRNX', 'CRON', 'CROX', 'CRPT', 'CRS', 'CRSP', 'CRSR', 'CRT', 'CRTO', 'CRUS', 'CRUZ', 'CRVL', 'CRVS', 'CRWD', 'CRWS', 'CRYP', 'CRZN', 'CRZNU', 'CS', 'CSA', 'CSAN', 'CSB', 'CSBR', 'CSCO',
 'CSD', 'CSF', 'CSGP', 'CSGS', 'CSH', 'CSII', 'CSIQ', 'CSL', 'CSLM', 'CSLMR', 'CSM', 'CSML', 'CSPI', 'CSQ', 'CSR', 'CSSE', 'CSSEN', 'CSSEP', 'CSTA', 'CSTE', 'CSTL', 'CSTM', 'CSTR', 'CSV', 'CSWC', 'CSWI',
 'CSX', 'CTA', 'CTAS', 'CTBB', 'CTBI', 'CTDD', 'CTEC', 'CTEX', 'CTG', 'CTGO', 'CTHR', 'CTIB', 'CTIC', 'CTKB', 'CTLP', 'CTLT', 'CTMX', 'CTO', 'CTOS', 'CTR', 'CTRA', 'CTRE', 'CTRM', 'CTRN', 'CTS', 'CTSH',
 'CTSO', 'CTV', 'CTVA', 'CTXR', 'CUBA', 'CUBB', 'CUBE', 'CUBI', 'CUBS', 'CUE', 'CUEN', 'CUK', 'CULL', 'CULP', 'CURE', 'CURI', 'CURO', 'CURV', 'CUT', 'CUTR', 'CUZ', 'CVAC', 'CVAR', 'CVBF', 'CVCO', 'CVCY',
 'CVE', 'CVEO', 'CVGI', 'CVGW', 'CVI', 'CVII', 'CVLG', 'CVLT', 'CVLY', 'CVM', 'CVNA', 'CVR', 'CVRX', 'CVS', 'CVT', 'CVV', 'CVX', 'CVY', 'CW', 'CWAN', 'CWB', 'CWBC', 'CWBR', 'CWCO', 'CWEB', 'CWEN', 'CWH',
 'CWI', 'CWK', 'CWS', 'CWST', 'CWT', 'CX', 'CXAC', 'CXDO', 'CXE', 'CXH', 'CXM', 'CXSE', 'CXW', 'CYA', 'CYAD', 'CYAN', 'CYB', 'CYBN', 'CYBR', 'CYCC', 'CYCCP', 'CYCN', 'CYD', 'CYH', 'CYN', 'CYRX', 'CYT',
 'CYTH', 'CYTK', 'CYTO', 'CYXT', 'CZA', 'CZFS', 'CZNC', 'CZOO', 'CZR', 'CZWI', 'D', 'DAC', 'DADA', 'DAIO', 'DAKT', 'DAL', 'DALI', 'DALN', 'DALS', 'DALT', 'DAM', 'DAN', 'DAO', 'DAPP', 'DAPR', 'DAR', 'DARE',
 'DASH', 'DAT', 'DATS', 'DAUG', 'DAVA', 'DAVE', 'DAWN', 'DAX', 'DB', 'DBA', 'DBAW', 'DBB', 'DBC', 'DBD', 'DBE', 'DBEF', 'DBEH', 'DBEM', 'DBEU', 'DBEZ', 'DBGI', 'DBGR', 'DBI', 'DBJA', 'DBJP', 'DBL', 'DBMF',
 'DBND', 'DBO', 'DBOC', 'DBP', 'DBRG', 'DBTX', 'DBVT', 'DBX', 'DC', 'DCBO', 'DCF', 'DCFC', 'DCGO', 'DCI', 'DCO', 'DCOM', 'DCOMP', 'DCP', 'DCPH', 'DCT', 'DCTH', 'DD', 'DDD', 'DDEC', 'DDF', 'DDI', 'DDIV',
 'DDL', 'DDLS', 'DDM', 'DDOG', 'DDS', 'DDT', 'DDWM', 'DE', 'DEA', 'DECA', 'DECAU', 'DECK', 'DECZ', 'DEED', 'DEEF', 'DEEP', 'DEF', 'DEHP', 'DEI', 'DELL', 'DEM', 'DEMZ', 'DEN', 'DENN', 'DEO', 'DERM', 'DES',
 'DESP', 'DEUS', 'DEW', 'DEX', 'DFAC', 'DFAE', 'DFAI', 'DFAR', 'DFAS', 'DFAT', 'DFAU', 'DFAX', 'DFCF', 'DFE', 'DFEB', 'DFEM', 'DFEN', 'DFEV', 'DFFN', 'DFH', 'DFHY', 'DFIC', 'DFIN', 'DFIP', 'DFIS', 'DFIV',
 'DFJ', 'DFND', 'DFNL', 'DFNM', 'DFNV', 'DFP', 'DFRA', 'DFS', 'DFSD', 'DFSV', 'DFUS', 'DFUV', 'DG', 'DGHI', 'DGICA', 'DGICB', 'DGII', 'DGIN', 'DGLY', 'DGNU', 'DGP', 'DGRE', 'DGRO', 'DGRS', 'DGRW', 'DGS',
 'DGT', 'DGX', 'DGZ', 'DH', 'DHAC', 'DHACU', 'DHC', 'DHCA', 'DHCAU', 'DHCNI', 'DHCNL', 'DHF', 'DHHC', 'DHHCU', 'DHI', 'DHIL', 'DHR', 'DHS', 'DHT', 'DHX', 'DHY', 'DIA', 'DIAL', 'DIAX', 'DIBS', 'DICE', 'DIG',
 'DIHP', 'DIM', 'DIN', 'DINO', 'DINT', 'DIOD', 'DIS', 'DISA', 'DISAU', 'DISH', 'DISV', 'DIT', 'DIV', 'DIVB', 'DIVO', 'DIVS', 'DIVZ', 'DJAN', 'DJCB', 'DJCO', 'DJD', 'DJIA', 'DJP', 'DJUL', 'DJUN', 'DK',
 'DKDCA', 'DKDCU', 'DKL', 'DKNG', 'DKS', 'DLA', 'DLB', 'DLHC', 'DLN', 'DLNG', 'DLO', 'DLPN', 'DLR', 'DLS', 'DLTH', 'DLTR', 'DLX', 'DLY', 'DM', 'DMA', 'DMAC', 'DMAQ', 'DMAQR', 'DMAR', 'DMAT', 'DMAY',
 'DMB', 'DMCY', 'DMF', 'DMLP', 'DMO', 'DMRC', 'DMS', 'DMTK', 'DMXF', 'DMYS', 'DNA', 'DNAB', 'DNAD', 'DNB', 'DNL', 'DNLI', 'DNMR', 'DNN', 'DNOV', 'DNOW', 'DNP', 'DNUT', 'DO', 'DOC', 'DOCN', 'DOCS',
 'DOCT', 'DOCU', 'DOG', 'DOGZ', 'DOL', 'DOLE', 'DOMA', 'DOMO', 'DON', 'DOOO', 'DOOR', 'DORM', 'DOUG', 'DOV', 'DOW', 'DOX', 'DOYU', 'DPCS', 'DPCSU', 'DPG', 'DPRO', 'DPSI', 'DPST', 'DPZ', 'DQ', 'DRCT',
 'DRD', 'DRH', 'DRI', 'DRIO', 'DRIP', 'DRIV', 'DRMA', 'DRN', 'DRQ', 'DRRX', 'DRSK', 'DRTS', 'DRTT', 'DRUG', 'DRV', 'DRVN', 'DSCF', 'DSEP', 'DSEY', 'DSGN', 'DSGR', 'DSGX', 'DSI', 'DSJA', 'DSKE', 'DSL',
 'DSM', 'DSOC', 'DSP', 'DSS', 'DSTL', 'DSTX', 'DSU', 'DSWL', 'DSX', 'DT', 'DTB', 'DTC', 'DTD', 'DTE', 'DTEA', 'DTEC', 'DTF', 'DTG', 'DTH', 'DTIL', 'DTM', 'DTOC', 'DTOCU', 'DTSS', 'DTST', 'DTW', 'DUDE',
 'DUET', 'DUETU', 'DUG', 'DUHP', 'DUK', 'DUKB', 'DUNE', 'DUNEU', 'DUO', 'DUOL', 'DUOT', 'DURA', 'DUSA', 'DUSL', 'DUST', 'DV', 'DVA', 'DVAX', 'DVLU', 'DVN', 'DVOL', 'DVY', 'DVYA', 'DVYE', 'DWAC', 'DWACU',
 'DWAS', 'DWAT', 'DWAW', 'DWCR', 'DWEQ', 'DWLD', 'DWM', 'DWMC', 'DWMF', 'DWSH', 'DWSN', 'DWUS', 'DWX', 'DX', 'DXC', 'DXCM', 'DXD', 'DXF', 'DXGE', 'DXJ', 'DXJS', 'DXLG', 'DXPE', 'DXR', 'DXYN', 'DY', 'DYAI',
 'DYLD', 'DYN', 'DYNF', 'DYNT', 'DZSI', 'DZZ', 'E', 'EA', 'EAC', 'EACPU', 'EAD', 'EAF', 'EAFD', 'EAGG', 'EAI', 'EAOA', 'EAOK', 'EAOM', 'EAOR', 'EAPR', 'EAR', 'EARN', 'EASG', 'EAST', 'EAT', 'EATV', 'EATZ',
 'EB', 'EBAY', 'EBC', 'EBET', 'EBF', 'EBIX', 'EBIZ', 'EBLU', 'EBMT', 'EBND', 'EBON', 'EBR', 'EBS', 'EBTC', 'EC', 'ECAT', 'ECC', 'ECCC', 'ECCV', 'ECCW', 'ECCX', 'ECF', 'ECH', 'ECL', 'ECLN', 'ECNS', 'ECON',
 'ECOR', 'ECOW', 'ECOZ', 'ECPG', 'ECVT', 'ED', 'EDAP', 'EDBL', 'EDC', 'EDD', 'EDEN', 'EDF', 'EDI', 'EDIT', 'EDIV', 'EDN', 'EDOC', 'EDOG', 'EDOW', 'EDR', 'EDRY', 'EDSA', 'EDTK', 'EDTX', 'EDTXU', 'EDU',
 'EDUC', 'EDUT', 'EDV', 'EDZ', 'EE', 'EEA', 'EEFT', 'EEIQ', 'EELV', 'EEM', 'EEMA', 'EEMD', 'EEMO', 'EEMS', 'EEMV', 'EEMX', 'EES', 'EET', 'EEV', 'EEX', 'EFA', 'EFAD', 'EFAS', 'EFAV', 'EFAX', 'EFC', 'EFG',
 'EFIV', 'EFIX', 'EFNL', 'EFO', 'EFOI', 'EFR', 'EFSC', 'EFSCP', 'EFSH', 'EFT', 'EFTR', 'EFU', 'EFV', 'EFX', 'EFZ', 'EGAN', 'EGBN', 'EGF', 'EGGF', 'EGHT', 'EGIO', 'EGIS', 'EGLE', 'EGLX', 'EGO', 'EGP', 'EGPT',
 'EGRX', 'EGY', 'EH', 'EHAB', 'EHC', 'EHI', 'EHTH', 'EIC', 'EICA', 'EIDO', 'EIG', 'EIGR', 'EIM', 'EINC', 'EIRL', 'EIS', 'EIX', 'EJAN', 'EJH', 'EJUL', 'EKG', 'EKSO', 'EL', 'ELA', 'ELAN', 'ELBM', 'ELC', 'ELD',
 'ELDN', 'ELEV', 'ELF', 'ELLO', 'ELMD', 'ELOX', 'ELP', 'ELS', 'ELSE', 'ELTK', 'ELV', 'ELYM', 'ELYS', 'EM', 'EMAN', 'EMB', 'EMBC', 'EMBD', 'EMBK', 'EMCB', 'EMCR', 'EMD', 'EMDV', 'EME', 'EMF', 'EMFM', 'EMFQ',
 'EMGD', 'EMGF', 'EMHC', 'EMHY', 'EMIF', 'EMKR', 'EML', 'EMLC', 'EMLD', 'EMLDU', 'EMLP', 'EMMF', 'EMN', 'EMNT', 'EMO', 'EMP', 'EMQQ', 'EMR', 'EMSG', 'EMTL', 'EMTY', 'EMX', 'EMXC', 'EMXF', 'ENB', 'ENBA',
 'ENCP', 'ENCPU', 'ENER', 'ENERR', 'ENERU', 'ENFN', 'ENFR', 'ENG', 'ENIC', 'ENJ', 'ENLC', 'ENLV', 'ENO', 'ENOB', 'ENOR', 'ENOV', 'ENPH', 'ENR', 'ENS', 'ENSC', 'ENSG', 'ENSV', 'ENTA', 'ENTF', 'ENTFU', 'ENTG',
 'ENTR', 'ENTX', 'ENV', 'ENVA', 'ENVB', 'ENVX', 'ENX', 'ENZ', 'ENZL', 'EOCT', 'EOCW', 'EOD', 'EOG', 'EOI', 'EOLS', 'EOS', 'EOSE', 'EOT', 'EP', 'EPAC', 'EPAM', 'EPC', 'EPD', 'EPHE', 'EPI', 'EPIX', 'EPM',
 'EPOL', 'EPP', 'EPR', 'EPRF', 'EPRT', 'EPS', 'EPSN', 'EPU', 'EPV', 'EQ', 'EQAL', 'EQBK', 'EQC', 'EQH', 'EQIX', 'EQL', 'EQNR', 'EQOP', 'EQR', 'EQRR', 'EQRX', 'EQS', 'EQT', 'EQUL', 'EQWL', 'EQX', 'ERAS',
 'ERC', 'ERES', 'ERESU', 'ERF', 'ERH', 'ERIC', 'ERIE', 'ERII', 'ERJ', 'ERM', 'ERO', 'ERSX', 'ERTH', 'ERX', 'ERY', 'ERYP', 'ES', 'ESAB', 'ESAC', 'ESACU', 'ESBA', 'ESCA', 'ESE', 'ESEA', 'ESEB', 'ESG', 'ESGA',
 'ESGD', 'ESGE', 'ESGG', 'ESGN', 'ESGR', 'ESGRO', 'ESGRP', 'ESGS', 'ESGU', 'ESGV', 'ESGY', 'ESHY', 'ESI', 'ESIX', 'ESLT', 'ESM', 'ESML', 'ESMT', 'ESMV', 'ESNT', 'ESOA', 'ESP', 'ESPO', 'ESPR', 'ESQ', 'ESRT',
 'ESS', 'ESSA', 'ESTA', 'ESTC', 'ESTE', 'ET', 'ETB', 'ETD', 'ETG', 'ETHO', 'ETJ', 'ETN', 'ETNB', 'ETO', 'ETON', 'ETR', 'ETRN', 'ETSY', 'ETV', 'ETW', 'ETWO', 'ETX', 'ETY', 'EUCR', 'EUCRU', 'EUDG', 'EUDV',
 'EUFN', 'EUM', 'EUO', 'EURL', 'EURN', 'EUSA', 'EUSB', 'EUSC', 'EVA', 'EVAX', 'EVBG', 'EVBN', 'EVC', 'EVCM', 'EVE', 'EVEN', 'EVER', 'EVEX', 'EVF', 'EVG', 'EVGN', 'EVGO', 'EVGR', 'EVH', 'EVI', 'EVLO', 'EVLV',
 'EVM', 'EVMT', 'EVN', 'EVNT', 'EVO', 'EVOJ', 'EVOJU', 'EVOK', 'EVOP', 'EVR', 'EVRG', 'EVRI', 'EVT', 'EVTC', 'EVTL', 'EVTV', 'EVV', 'EVX', 'EW', 'EWA', 'EWBC', 'EWC', 'EWCO', 'EWCZ', 'EWD', 'EWEB', 'EWG', 'EWGS',
 'EWH', 'EWI', 'EWJ', 'EWJV', 'EWK', 'EWL', 'EWM', 'EWMC', 'EWN', 'EWO', 'EWP', 'EWQ', 'EWRE', 'EWS', 'EWSC', 'EWT', 'EWTX', 'EWU', 'EWUS', 'EWV', 'EWW', 'EWX', 'EWY', 'EWZ', 'EWZS', 'EXAI', 'EXAS', 'EXC', 'EXD',
 'EXEL', 'EXFY', 'EXG', 'EXI', 'EXK', 'EXLS', 'EXP', 'EXPD', 'EXPE', 'EXPI', 'EXPO', 'EXPR', 'EXR', 'EXTR', 'EYE', 'EYEN', 'EYLD', 'EYPT', 'EZA', 'EZFL', 'EZGO', 'EZJ', 'EZM', 'EZPW', 'EZU', 'F', 'FA', 'FAAR',
 'FAB', 'FACT', 'FAD', 'FAF', 'FAIL', 'FALN', 'FAM', 'FAMI', 'FAN', 'FANG', 'FANH', 'FAPR', 'FARM', 'FARO', 'FAS', 'FAST', 'FAT', 'FATBB', 'FATBP', 'FATE', 'FATH', 'FATP', 'FATPU', 'FAUG', 'FAX', 'FAZ', 'FBCG',
 'FBCV', 'FBGX', 'FBIO', 'FBIOP', 'FBIZ', 'FBK', 'FBMS', 'FBNC', 'FBND', 'FBP', 'FBRT', 'FBRX', 'FBT', 'FBZ', 'FC', 'FCA', 'FCAL', 'FCAP', 'FCBC', 'FCCO', 'FCEF', 'FCEL', 'FCF', 'FCFS', 'FCG', 'FCLD', 'FCN',
 'FCNCA', 'FCNCO', 'FCNCP', 'FCO', 'FCOM', 'FCOR', 'FCPI', 'FCPT', 'FCRD', 'FCRX', 'FCSH', 'FCT', 'FCTR', 'FCUV', 'FCVT', 'FCX', 'FDBC', 'FDD', 'FDEC', 'FDEM', 'FDEU', 'FDEV', 'FDG', 'FDHT', 'FDHY', 'FDIG',
 'FDIS', 'FDL', 'FDLO', 'FDM', 'FDMO', 'FDMT', 'FDN', 'FDNI', 'FDP', 'FDRR', 'FDRV', 'FDS', 'FDT', 'FDTS', 'FDUS', 'FDVV', 'FDWM', 'FDX', 'FE', 'FEAM', 'FEBZ', 'FEDL', 'FEDM', 'FEDU', 'FEHY', 'FEI', 'FEIG',
 'FEIM', 'FELE', 'FEM', 'FEMB', 'FEMS', 'FEMY', 'FEN', 'FENC', 'FENG', 'FENY', 'FEP', 'FERG', 'FET', 'FEUS', 'FEUZ', 'FEX', 'FEXD', 'FEXDR', 'FEXDU', 'FEZ', 'FF', 'FFA', 'FFBC', 'FFC', 'FFEB', 'FFHG', 'FFIC',
 'FFIE', 'FFIN', 'FFIU', 'FFIV', 'FFND', 'FFNW', 'FFSG', 'FFTG', 'FFTI', 'FFTY', 'FFWM', 'FGB', 'FGBI', 'FGBIP', 'FGD', 'FGEN', 'FGF', 'FGFPP', 'FGI', 'FGLD', 'FGM', 'FGMC', 'FGMCU', 'FGRO', 'FHB', 'FHI',
 'FHLC', 'FHLT', 'FHLTU', 'FHN', 'FHTX', 'FHYS', 'FIAC', 'FIACU', 'FIBK', 'FIBR', 'FICO', 'FICS', 'FICV', 'FICVU', 'FID', 'FIDI', 'FIDU', 'FIEE', 'FIF', 'FIG', 'FIGB', 'FIGS', 'FILL', 'FINS', 'FINV', 'FINW',
 'FINX', 'FIS', 'FISI', 'FISK', 'FISR', 'FISV', 'FITB', 'FITBI', 'FITBO', 'FITBP', 'FITE', 'FIVA', 'FIVE', 'FIVG', 'FIVN', 'FIVR', 'FIW', 'FIX', 'FIXD', 'FIXX', 'FIZZ', 'FJAN', 'FJP', 'FJUL', 'FJUN', 'FKU',
 'FKWL', 'FL', 'FLAG', 'FLAU', 'FLAX', 'FLBL', 'FLBR', 'FLC', 'FLCA', 'FLCB', 'FLCH', 'FLCO', 'FLDR', 'FLDZ', 'FLEE', 'FLEH', 'FLEX', 'FLFR', 'FLFVU', 'FLGB', 'FLGC', 'FLGR', 'FLGT', 'FLGV', 'FLHK', 'FLHY',
 'FLIA', 'FLIC', 'FLIN', 'FLIY', 'FLJH', 'FLJP', 'FLKR', 'FLL', 'FLLA', 'FLLV', 'FLMB', 'FLME', 'FLMI', 'FLMX', 'FLN', 'FLNC', 'FLNG', 'FLNT', 'FLO', 'FLOT', 'FLQL', 'FLQM', 'FLQS', 'FLR', 'FLRG', 'FLRN',
 'FLRT', 'FLS', 'FLSA', 'FLSP', 'FLSW', 'FLT', 'FLTB', 'FLTN', 'FLTR', 'FLTW', 'FLUD', 'FLUX', 'FLV', 'FLWS', 'FLXS', 'FLYD', 'FLYU', 'FLYW', 'FLZA', 'FM', 'FMAG', 'FMAO', 'FMAR', 'FMAT', 'FMAY', 'FMB',
 'FMBH', 'FMC', 'FMCX', 'FMET', 'FMF', 'FMHI', 'FMIL', 'FMIV', 'FMIVU', 'FMN', 'FMNB', 'FMNY', 'FMQQ', 'FMS', 'FMX', 'FMY', 'FN', 'FNA', 'FNB', 'FNCB', 'FNCH', 'FNCL', 'FND', 'FNDA', 'FNDB', 'FNDC', 'FNDE',
 'FNDF', 'FNDX', 'FNF', 'FNGD', 'FNGG', 'FNGO', 'FNGR', 'FNGS', 'FNGU', 'FNK', 'FNKO', 'FNLC', 'FNOV', 'FNV', 'FNVT', 'FNVTU', 'FNWB', 'FNWD', 'FNX', 'FNY', 'FOA', 'FOCS', 'FOCT', 'FOF', 'FOLD', 'FONR',
 'FOR', 'FORA', 'FORD', 'FORG', 'FORH', 'FORM', 'FORR', 'FORTY', 'FOSL', 'FOSLL', 'FOUR', 'FOVL', 'FOX', 'FOXA', 'FOXF', 'FPA', 'FPAG', 'FPAY', 'FPE', 'FPEI', 'FPF', 'FPFD', 'FPH', 'FPI', 'FPL', 'FPRO',
 'FPX', 'FPXE', 'FPXI', 'FQAL', 'FR', 'FRA', 'FRAF', 'FRBA', 'FRBK', 'FRBN', 'FRBNU', 'FRC', 'FRD', 'FRDM', 'FREE', 'FREL', 'FREQ', 'FREY', 'FRG', 'FRGAP', 'FRGE', 'FRGI', 'FRGT', 'FRHC', 'FRI', 'FRLN',
 'FRME', 'FRMEP', 'FRNW', 'FRO', 'FROG', 'FRON', 'FRONU', 'FRPH', 'FRPT', 'FRSH', 'FRST', 'FRSX', 'FRT', 'FRTY', 'FRXB', 'FSBC', 'FSBD', 'FSBW', 'FSD', 'FSEA', 'FSEC', 'FSEP', 'FSFG', 'FSI', 'FSIG',
 'FSK', 'FSLD', 'FSLR', 'FSLY', 'FSM', 'FSMB', 'FSMD', 'FSMO', 'FSNB', 'FSP', 'FSR', 'FSRX', 'FSRXU', 'FSS', 'FSST', 'FSTA', 'FSTR', 'FSV', 'FSYD', 'FSZ', 'FT', 'FTA', 'FTAG', 'FTAI', 'FTAIN', 'FTAIO',
 'FTAIP', 'FTC', 'FTCH', 'FTCI', 'FTCS', 'FTDR', 'FTDS', 'FTEC', 'FTEK', 'FTF', 'FTFT', 'FTGC', 'FTHI', 'FTHM', 'FTHY', 'FTI', 'FTII', 'FTK', 'FTLS', 'FTNT', 'FTPA', 'FTPAU', 'FTQI', 'FTRI', 'FTS', 'FTSD',
 'FTSL', 'FTSM', 'FTV', 'FTXG', 'FTXH', 'FTXL', 'FTXN', 'FTXO', 'FTXR', 'FUBO', 'FUL', 'FULC', 'FULT', 'FULTP', 'FUMB', 'FUN', 'FUNC', 'FUND', 'FUNL', 'FURY', 'FUSB', 'FUSN', 'FUTU', 'FUTY', 'FUV', 'FV',
 'FVAL', 'FVC', 'FVCB', 'FVD', 'FVRR', 'FWAC', 'FWBI', 'FWONA', 'FWONK', 'FWRD', 'FWRG', 'FXA', 'FXB', 'FXC', 'FXCO', 'FXCOR', 'FXD', 'FXE', 'FXF', 'FXG', 'FXH', 'FXI', 'FXL', 'FXLV', 'FXN', 'FXNC', 'FXO',
 'FXP', 'FXR', 'FXU', 'FXY', 'FXZ', 'FYBR', 'FYC', 'FYLD', 'FYT', 'FYX', 'FZT', 'FZT', 'G', 'GAA', 'GAB', 'GABC', 'GABF', 'GAIA', 'GAIN', 'GAINN', 'GAINZ', 'GAL', 'GALT', 'GAM', 'GAMB', 'GAMC', 'GAME',
 'GAMR', 'GAN', 'GANX', 'GAQ', 'GASS', 'GATE', 'GATEU', 'GATO', 'GATX', 'GAU', 'GAZ', 'GB', 'GBAB', 'GBBK', 'GBBKR', 'GBCI', 'GBDC', 'GBF', 'GBIL', 'GBIO', 'GBLD', 'GBLI', 'GBNH', 'GBNY', 'GBR', 'GBRG',
 'GBRGR', 'GBRGU', 'GBTG', 'GBUY', 'GBX', 'GCBC', 'GCC', 'GCI', 'GCLN', 'GCMG', 'GCO', 'GCOR', 'GCOW', 'GCTK', 'GCV', 'GD', 'GDDY', 'GDE', 'GDEN', 'GDIV', 'GDL', 'GDMA', 'GDMN', 'GDNR', 'GDNRU', 'GDO',
 'GDOC', 'GDOT', 'GDRX', 'GDS', 'GDST', 'GDSTR', 'GDSTU', 'GDV', 'GDVD', 'GDX', 'GDXD', 'GDXJ', 'GDXU', 'GDYN', 'GE', 'GECC', 'GECCM', 'GECCN', 'GECCO', 'GEEX', 'GEEXU', 'GEF', 'GEG', 'GEGGL', 'GEHI',
 'GEL', 'GEM', 'GEMD', 'GENC', 'GENE', 'GENI', 'GENQ', 'GENQU', 'GENY', 'GEO', 'GEOS', 'GER', 'GERM', 'GERN', 'GES', 'GEVO', 'GF', 'GFAI', 'GFF', 'GFGD', 'GFGDR', 'GFGDU', 'GFGF', 'GFI', 'GFL', 'GFLU',
 'GFOF', 'GFOR', 'GFS', 'GFX', 'GGAA', 'GGAAU', 'GGAL', 'GGB', 'GGE', 'GGG', 'GGN', 'GGR', 'GGRW', 'GGT', 'GGZ', 'GH', 'GHC', 'GHG', 'GHIX', 'GHIXU', 'GHL', 'GHLD', 'GHM', 'GHRS', 'GHSI', 'GHY', 'GHYB',
 'GHYG', 'GIA', 'GIB', 'GIC', 'GIFI', 'GIGB', 'GIGM', 'GII', 'GIII', 'GIL', 'GILD', 'GILT', 'GIM', 'GINN', 'GIPR', 'GIS', 'GJH', 'GJO', 'GJP', 'GJR', 'GJS', 'GJT', 'GK', 'GKOS', 'GL', 'GLAD', 'GLBE', 'GLBS',
 'GLBZ', 'GLCN', 'GLD', 'GLDB', 'GLDD', 'GLDG', 'GLDI', 'GLDM', 'GLDX', 'GLG', 'GLIN', 'GLL', 'GLLI', 'GLLIR', 'GLLIU', 'GLMD', 'GLNG', 'GLO', 'GLOB', 'GLOP', 'GLOV', 'GLP', 'GLPG', 'GLPI', 'GLQ', 'GLRE',
 'GLRY', 'GLS', 'GLSI', 'GLT', 'GLTA', 'GLTO', 'GLTR', 'GLU', 'GLUE', 'GLV', 'GLW', 'GLYC', 'GM', 'GMAB', 'GMBL', 'GMBLP', 'GMDA', 'GME', 'GMED', 'GMET', 'GMF', 'GMFI', 'GMGI', 'GMOM', 'GMRE', 'GMS',
 'GMVD', 'GNE', 'GNFT', 'GNK', 'GNL', 'GNLN', 'GNMA', 'GNOM', 'GNPX', 'GNR', 'GNRC', 'GNS', 'GNSS', 'GNT', 'GNTA', 'GNTX', 'GNTY', 'GNUS', 'GNW', 'GO', 'GOAU', 'GOCO', 'GOEV', 'GOEX', 'GOF', 'GOGL',
 'GOGN', 'GOGO', 'GOL', 'GOLD', 'GOLF', 'GOOD', 'GOODN', 'GOODO', 'GOOG', 'GOOGL', 'GOOS', 'GORO', 'GOSS', 'GOTU', 'GOVT', 'GOVX', 'GOVZ', 'GP', 'GPAC', 'GPACU', 'GPAL', 'GPC', 'GPI', 'GPJA', 'GPK',
 'GPMT', 'GPN', 'GPOR', 'GPP', 'GPRE', 'GPRK', 'GPRO', 'GPS', 'GQRE', 'GRAB', 'GRAY', 'GRBK', 'GRC', 'GRCL', 'GRCY', 'GRCYU', 'GREE', 'GREEL', 'GREI', 'GREK', 'GRES', 'GRF', 'GRFS', 'GRID', 'GRIL',
 'GRIN', 'GRMN', 'GRN', 'GRNA', 'GRNB', 'GRNQ', 'GRNR', 'GROM', 'GROV', 'GROW', 'GROY', 'GRPH', 'GRPN', 'GRRR', 'GRTS', 'GRTX', 'GRVY', 'GRWG', 'GRX', 'GRZZ', 'GS', 'GSAT', 'GSBC', 'GSBD', 'GSEE',
 'GSEU', 'GSEW', 'GSFP', 'GSG', 'GSHD', 'GSID', 'GSIE', 'GSIG', 'GSIT', 'GSJY', 'GSK', 'GSL', 'GSLC', 'GSM', 'GSMG', 'GSP', 'GSPY', 'GSQB', 'GSRM', 'GSRMR', 'GSRMU', 'GSSC', 'GSST', 'GSUN', 'GSUS',
 'GSY', 'GT', 'GTAC', 'GTACU', 'GTBP', 'GTE', 'GTEC', 'GTEK', 'GTES', 'GTH', 'GTHX', 'GTIM', 'GTIP', 'GTLB', 'GTLS', 'GTN', 'GTO', 'GTR', 'GTX', 'GTXAP', 'GTY', 'GUG', 'GUNR', 'GURE', 'GURU', 'GUSH']

databaxB =  ['GVA', 'GVAL', 'GVCI', 'GVCIU', 'GVI', 'GVIP', 'GVLU', 'GVP', 'GWAV', 'GWH', 'GWII', 'GWRE', 'GWRS', 'GWW', 'GWX', 'GXC', 'GXG', 'GXII', 'GXIIU', 'GXO', 'GXTG', 'GYLD', 'GYRO', 'H', 'HA', 'HACK',
 'HAE', 'HAFC', 'HAIA', 'HAIAU', 'HAIL', 'HAIN', 'HAL', 'HALL', 'HALO', 'HAP', 'HAPP', 'HAPY', 'HARP', 'HART', 'HAS', 'HASI', 'HAUS', 'HAUZ', 'HAWX', 'HAYN', 'HAYW', 'HBAN', 'HBANM', 'HBANP', 'HBB', 'HBCP',
 'HBI', 'HBIO', 'HBM', 'HBNC', 'HBT', 'HCA', 'HCAT', 'HCC', 'HCCI', 'HCDI', 'HCDIP', 'HCI', 'HCKT', 'HCM', 'HCMA', 'HCMAU', 'HCNE', 'HCNEU', 'HCOM', 'HCP', 'HCRB', 'HCSG', 'HCTI', 'HCVI', 'HCVIU', 'HCWB',
 'HCXY', 'HD', 'HDAW', 'HDB', 'HDEF', 'HDG', 'HDGE', 'HDLB', 'HDMV', 'HDRO', 'HDSN', 'HDV', 'HE', 'HEAR', 'HEDJ', 'HEEM', 'HEES', 'HEET', 'HEFA', 'HEGD', 'HEI', 'HELE', 'HELX', 'HEP', 'HEPA', 'HEPS', 'HEQ',
 'HEQT', 'HERD', 'HERO', 'HES', 'HESM', 'HEWC', 'HEWG', 'HEWJ', 'HEWU', 'HEXO', 'HEZU', 'HFBL', 'HFFG', 'HFGO', 'HFRO', 'HFWA', 'HFXI', 'HGBL', 'HGEN', 'HGER', 'HGLB', 'HGTY', 'HGV', 'HHC', 'HHGC', 'HHGCR',
 'HHLA', 'HHS', 'HI', 'HIBB', 'HIBL', 'HIBS', 'HIE', 'HIFS', 'HIG', 'HIHO', 'HII', 'HILS', 'HIMS', 'HIMX', 'HIO', 'HIPO', 'HIPS', 'HISF', 'HITI', 'HIVE', 'HIW', 'HIX', 'HJEN', 'HKD', 'HKND', 'HL', 'HLAL',
 'HLBZ', 'HLF', 'HLGN', 'HLI', 'HLIO', 'HLIT', 'HLLY', 'HLMN', 'HLNE', 'HLT', 'HLTH', 'HLVX', 'HLX', 'HMA', 'HMC', 'HMN', 'HMNF', 'HMOP', 'HMPT', 'HMST', 'HMY', 'HNDL', 'HNI', 'HNNA', 'HNNAZ', 'HNRA', 'HNRG',
 'HNST', 'HNVR', 'HNW', 'HOFT', 'HOFV', 'HOG', 'HOLD', 'HOLI', 'HOLX', 'HOM', 'HOMB', 'HOMZ', 'HON', 'HONE', 'HOOD', 'HOOK', 'HOPE', 'HORI', 'HORIU', 'HOTH', 'HOTL', 'HOUR', 'HOUS', 'HOV', 'HOVNP', 'HOWL', 'HP',
 'HPE', 'HPF', 'HPI', 'HPK', 'HPLT', 'HPLTU', 'HPP', 'HPQ', 'HPS', 'HQH', 'HQI', 'HQL', 'HQY', 'HR', 'HRB', 'HRI', 'HRL', 'HRMY', 'HROW', 'HROWL', 'HRT', 'HRTG', 'HRTX', 'HRZN', 'HSBC', 'HSC', 'HSCS', 'HSCZ',
 'HSDT', 'HSIC', 'HSII', 'HSKA', 'HSMV', 'HSON', 'HSRT', 'HST', 'HSTM', 'HSTO', 'HSUN', 'HSY', 'HT', 'HTAB', 'HTBI', 'HTBK', 'HTCR', 'HTD', 'HTEC', 'HTFB', 'HTFC', 'HTGC', 'HTGM', 'HTH', 'HTHT', 'HTIA',
 'HTIBP', 'HTLD', 'HTLF', 'HTLFP', 'HTOO', 'HTRB', 'HTUS', 'HTY', 'HTZ', 'HUBB', 'HUBG', 'HUBS', 'HUDI', 'HUGE', 'HUIZ', 'HUM', 'HUMA', 'HUN', 'HURC', 'HURN', 'HUSA', 'HUSV', 'HUT', 'HUYA', 'HVAL', 'HVBC',
 'HVT', 'HWBK', 'HWC', 'HWCPZ', 'HWEL', 'HWKN', 'HWKZ', 'HWM', 'HXL', 'HY', 'HYB', 'HYBB', 'HYBL', 'HYD', 'HYDB', 'HYDR', 'HYDW', 'HYEM', 'HYFM', 'HYG', 'HYGH', 'HYGI', 'HYGV', 'HYHG', 'HYI', 'HYIN', 'HYLB',
 'HYLD', 'HYLN', 'HYLS', 'HYMB', 'HYMC', 'HYMU', 'HYPR', 'HYRM', 'HYS', 'HYT', 'HYTR', 'HYUP', 'HYW', 'HYXF', 'HYXU', 'HYZD', 'HYZN', 'HZNP', 'HZO', 'HZON', 'IAA', 'IAC', 'IAE', 'IAF', 'IAG', 'IAGG', 'IAI',
 'IAK', 'IAPR', 'IART', 'IAS', 'IAT', 'IAU', 'IAUF', 'IAUM', 'IAUX', 'IBA', 'IBB', 'IBBQ', 'IBCE', 'IBCP', 'IBD', 'IBDD', 'IBDO', 'IBDP', 'IBDQ', 'IBDR', 'IBDS', 'IBDT', 'IBDU', 'IBDV', 'IBDW', 'IBDX', 'IBET',
 'IBEX', 'IBHC', 'IBHD', 'IBHE', 'IBHF', 'IBHG', 'IBHH', 'IBHI', 'IBIO', 'IBKR', 'IBLC', 'IBM', 'IBML', 'IBMM', 'IBMN', 'IBMO', 'IBMP', 'IBMQ', 'IBN', 'IBND', 'IBOC', 'IBP', 'IBRX', 'IBTD', 'IBTE', 'IBTF',
 'IBTG', 'IBTH', 'IBTI', 'IBTJ', 'IBTK', 'IBTL', 'IBTM', 'IBTX', 'IBUY', 'ICAD', 'ICAP', 'ICCC', 'ICCH', 'ICCM', 'ICD', 'ICE', 'ICF', 'ICFI', 'ICHR', 'ICL', 'ICLK', 'ICLN', 'ICLR', 'ICMB', 'ICNC', 'ICOW',
 'ICPT', 'ICSH', 'ICUI', 'ICVT', 'ICVX', 'ID', 'IDA', 'IDAI', 'IDAT', 'IDBA', 'IDCC', 'IDE', 'IDEV', 'IDEX', 'IDHD', 'IDHQ', 'IDLB', 'IDLV', 'IDME', 'IDMO', 'IDN', 'IDNA', 'IDOG', 'IDR', 'IDRV', 'IDT',
 'IDU', 'IDV', 'IDW', 'IDX', 'IDXX', 'IDYA', 'IE', 'IEDI', 'IEF', 'IEFA', 'IEI', 'IEMG', 'IEO', 'IEP', 'IESC', 'IETC', 'IEUR', 'IEUS', 'IEV', 'IEX', 'IEZ', 'IFBD', 'IFED', 'IFF', 'IFGL', 'IFIN', 'IFN',
 'IFRA', 'IFRX', 'IFS', 'IFV', 'IG', 'IGA', 'IGBH', 'IGC', 'IGD', 'IGE', 'IGEB', 'IGF', 'IGHG', 'IGI', 'IGIB', 'IGIC', 'IGLB', 'IGLD', 'IGM', 'IGMS', 'IGN', 'IGOV', 'IGR', 'IGRO', 'IGSB', 'IGT', 'IGTA',
 'IGTAR', 'IGTAU', 'IGV', 'IH', 'IHAK', 'IHD', 'IHDG', 'IHE', 'IHF', 'IHG', 'IHI', 'IHIT', 'IHRT', 'IHS', 'IHT', 'IHTA', 'IHY', 'IHYF', 'IIF', 'IIGD', 'IIGV', 'III', 'IIIN', 'IIIV', 'IIM', 'IINN', 'IIPR',
 'IIVI', 'IJAN', 'IJH', 'IJJ', 'IJK', 'IJR', 'IJS', 'IJT', 'IJUL', 'IKNA', 'IKT', 'ILAG', 'ILCB', 'ILCG', 'ILCV', 'ILDR', 'ILF', 'ILMN', 'ILPT', 'ILTB', 'IMAB', 'IMAQ', 'IMAQR', 'IMAQU', 'IMAX', 'IMBI',
 'IMBIL', 'IMCB', 'IMCC', 'IMCG', 'IMCR', 'IMCV', 'IMFL', 'IMGN', 'IMH', 'IMKTA', 'IMMP', 'IMMR', 'IMMX', 'IMNM', 'IMO', 'IMOM', 'IMOS', 'IMPL', 'IMPP', 'IMPPP', 'IMRN', 'IMRX', 'IMTB', 'IMTE', 'IMTM',
 'IMTX', 'IMUX', 'IMV', 'IMVT', 'IMXI', 'INAB', 'INAQ', 'INBK', 'INBKZ', 'INBX', 'INCO', 'INCR', 'INCY', 'INDA', 'INDB', 'INDF', 'INDI', 'INDL', 'INDO', 'INDP', 'INDS', 'INDT', 'INDY', 'INFA', 'INFI',
 'INFL', 'INFN', 'INFU', 'INFY', 'ING', 'INGN', 'INGR', 'INKA', 'INKAU', 'INKM', 'INKT', 'INLX', 'INM', 'INMB', 'INMD', 'INMU', 'INN', 'INNO', 'INNV', 'INO', 'INOD', 'INPX', 'INQQ', 'INSE', 'INSG',
 'INSI', 'INSM', 'INSP', 'INST', 'INSW', 'INT', 'INTA', 'INTC', 'INTE', 'INTEU', 'INTF', 'INTG', 'INTR', 'INTT', 'INTU', 'INTZ', 'INUV', 'INVA', 'INVE', 'INVH', 'INVO', 'INVZ', 'INZY', 'IOAC', 'IOACU',
 'IOBT', 'IOCT', 'IONM', 'IONQ', 'IONR', 'IONS', 'IOO', 'IOR', 'IOSP', 'IOT', 'IOVA', 'IP', 'IPA', 'IPAC', 'IPAR', 'IPAY', 'IPB', 'IPDN', 'IPDP', 'IPG', 'IPGP', 'IPHA', 'IPI', 'IPKW', 'IPO', 'IPOS',
 'IPPP', 'IPSC', 'IPVF', 'IPVI', 'IPVIU', 'IPW', 'IPWR', 'IPX', 'IQ', 'IQDE', 'IQDF', 'IQDG', 'IQDY', 'IQI', 'IQIN', 'IQLT', 'IQM', 'IQMD', 'IQMDU', 'IQSI', 'IQSU', 'IQV', 'IR', 'IRBA', 'IRBO', 'IRBT',
 'IRDM', 'IREN', 'IRIX', 'IRM', 'IRMD', 'IRNT', 'IROQ', 'IRRX', 'IRS', 'IRT', 'IRTC', 'IRVH', 'IRWD', 'ISCB', 'ISCF', 'ISCG', 'ISCV', 'ISD', 'ISDR', 'ISDX', 'ISEE', 'ISEM', 'ISHG', 'ISHP', 'ISIG', 'ISMD',
 'ISO', 'ISPC', 'ISPO', 'ISRA', 'ISRG', 'ISSC', 'ISTB', 'ISTR', 'ISUN', 'ISVL', 'ISWN', 'ISZE', 'IT', 'ITA', 'ITAN', 'ITAQ', 'ITAQU', 'ITB', 'ITCB', 'ITCI', 'ITEQ', 'ITGR', 'ITI', 'ITIC', 'ITM', 'ITOS',
 'ITOT', 'ITP', 'ITRG', 'ITRI', 'ITRM', 'ITRN', 'ITT', 'ITUB', 'ITW', 'IUS', 'IUSB', 'IUSG', 'IUSS', 'IUSV', 'IVA', 'IVAC', 'IVAL', 'IVCA', 'IVCAU', 'IVCB', 'IVCBU', 'IVCP', 'IVCPU', 'IVDA', 'IVDG',
 'IVE', 'IVEG', 'IVES', 'IVH', 'IVLC', 'IVLU', 'IVOG', 'IVOL', 'IVOO', 'IVOV', 'IVR', 'IVRA', 'IVSG', 'IVT', 'IVV', 'IVW', 'IVZ', 'IWB', 'IWC', 'IWD', 'IWDL', 'IWF', 'IWFG', 'IWFH', 'IWFL', 'IWIN', 'IWL',
 'IWLG', 'IWM', 'IWML', 'IWN', 'IWO', 'IWP', 'IWR', 'IWS', 'IWV', 'IWX', 'IWY', 'IX', 'IXAQ', 'IXAQU', 'IXC', 'IXG', 'IXHL', 'IXJ', 'IXN', 'IXP', 'IXSE', 'IXUS', 'IYC', 'IYE', 'IYF', 'IYG', 'IYH', 'IYJ',
 'IYK', 'IYLD', 'IYM', 'IYR', 'IYT', 'IYW', 'IYY', 'IYZ', 'IZEA', 'IZRL', 'J', 'JAAA', 'JACK', 'JAGX', 'JAKK', 'JAMF', 'JAN', 'JANX', 'JANZ', 'JAQC', 'JAQCU', 'JATT', 'JAVA', 'JAZZ', 'JBBB', 'JBGS', 'JBHT',
 'JBI', 'JBK', 'JBL', 'JBLU', 'JBSS', 'JBT', 'JCE', 'JCI', 'JCPB', 'JCPI', 'JCSE', 'JCTCF', 'JCTR', 'JD', 'JDST', 'JEF', 'JELD', 'JEMA', 'JEPI', 'JEPQ', 'JEQ', 'JETS', 'JFIN', 'JFR', 'JFU', 'JFWD', 'JG',
 'JGGC', 'JGGCR', 'JGGCU', 'JGH', 'JHAA', 'JHCB', 'JHEM', 'JHG', 'JHI', 'JHMB', 'JHMD', 'JHML', 'JHMM', 'JHPI', 'JHS', 'JHSC', 'JHX', 'JIB', 'JIDA', 'JIG', 'JILL', 'JIRE', 'JJA','JJC', 'JJE', 'JJG', 'JJM',
 'JJN', 'JJP', 'JJS', 'JJSF', 'JJT', 'JJU', 'JKHY', 'JKS', 'JLL', 'JLS', 'JMAC', 'JMACU', 'JMBS', 'JMEE', 'JMIA', 'JMM', 'JMOM', 'JMSB', 'JMST', 'JMUB', 'JNCE', 'JNJ', 'JNK', 'JNPR', 'JNUG', 'JO', 'JOAN',
 'JOB', 'JOBY', 'JOE', 'JOET', 'JOF', 'JOJO', 'JOUT', 'JPC', 'JPEM', 'JPI', 'JPIB', 'JPIE', 'JPIN', 'JPM', 'JPMB', 'JPME', 'JPRE', 'JPS', 'JPSE', 'JPST', 'JPT', 'JPUS', 'JPXN', 'JQC', 'JQUA', 'JRE', 'JRI',
 'JRNY', 'JRO', 'JRS', 'JRSH', 'JRVR', 'JSCP', 'JSD', 'JSM', 'JSMD', 'JSML', 'JSPR', 'JSTC', 'JT', 'JUGG', 'JUGGU', 'JULZ', 'JUN', 'JUNZ', 'JUPW', 'JUSA', 'JUST', 'JVA', 'JVAL', 'JWAC', 'JWACR', 'JWEL',
 'JWN', 'JWSM', 'JXI', 'JXN', 'JYNT', 'JZRO', 'JZXN', 'K', 'KACL', 'KACLR', 'KACLU', 'KAI', 'KAL', 'KALA', 'KALL', 'KALU', 'KALV', 'KAMN', 'KAPR', 'KAR', 'KARO', 'KARS', 'KAVL', 'KB', 'KBA', 'KBAL', 'KBE',
 'KBH', 'KBND', 'KBNT', 'KBR', 'KBUY', 'KBWB', 'KBWD', 'KBWP', 'KBWR', 'KBWY', 'KC', 'KCCA', 'KCE', 'KCGI', 'KD', 'KDNY', 'KDP', 'KDRN', 'KE', 'KEJI', 'KELYA', 'KELYB', 'KEMQ', 'KEMX', 'KEN', 'KEP', 'KEQU',
 'KERN', 'KESG', 'KEUA', 'KEX', 'KEY', 'KEYS', 'KF', 'KFFB', 'KFRC', 'KFS', 'KFVG', 'KFY', 'KFYP', 'KGC', 'KGHG', 'KGRN', 'KGRO', 'KHC', 'KHYB', 'KIDS', 'KIE', 'KIM', 'KIND', 'KINS', 'KINZ', 'KINZU', 'KIO',
 'KIQ', 'KIRK', 'KJAN', 'KJUL', 'KKR', 'KKRS', 'KLAC', 'KLDW', 'KLIC', 'KLNE', 'KLR', 'KLTR', 'KLXE', 'KMB', 'KMDA', 'KMED', 'KMF', 'KMI', 'KMLM', 'KMPB', 'KMPR', 'KMT', 'KMX', 'KN', 'KNDI', 'KNG', 'KNGS',
 'KNOP', 'KNSA', 'KNSL', 'KNSW', 'KNTE', 'KNTK', 'KNX', 'KO', 'KOCG', 'KOCT', 'KOD', 'KODK', 'KOF', 'KOIN', 'KOKU', 'KOLD', 'KOMP', 'KONG', 'KOP', 'KOPN', 'KORE', 'KORP', 'KORU', 'KOS', 'KOSS', 'KPLT',
 'KPRX', 'KPTI', 'KR', 'KRBN', 'KRBP', 'KRC', 'KRE', 'KREF', 'KRG', 'KRKR', 'KRMA', 'KRMD', 'KRNL', 'KRNLU', 'KRNT', 'KRNY', 'KRO', 'KRON', 'KROP', 'KROS', 'KRP', 'KRT', 'KRTX', 'KRUS', 'KRYS', 'KSA', 'KSCP',
 'KSET', 'KSI', 'KSICU', 'KSM', 'KSPN', 'KSS', 'KSTR', 'KT', 'KTB', 'KTCC', 'KTEC', 'KTF', 'KTH', 'KTN', 'KTOS', 'KTRA', 'KTTA', 'KUKE', 'KULR', 'KURA', 'KURE', 'KVHI', 'KVLE', 'KVSA', 'KVSC', 'KW', 'KWEB',
 'KWR', 'KWT', 'KXI', 'KXIN', 'KYCH', 'KYCHR', 'KYCHU', 'KYMR', 'KYN', 'KZIA', 'KZR', 'L', 'LAB', 'LABD', 'LABP', 'LABU', 'LAC', 'LAD', 'LADR', 'LAKE', 'LAMR', 'LANC', 'LAND', 'LANDM', 'LANDO', 'LARK', 'LASR',
 'LATG', 'LATGU', 'LAUR', 'LAW', 'LAZ', 'LAZR', 'LAZY', 'LBAI', 'LBAY', 'LBBBR', 'LBBBU', 'LBC', 'LBPH', 'LBRDA', 'LBRDK', 'LBRDP', 'LBRT', 'LBTYA', 'LBTYB', 'LBTYK', 'LC', 'LCA', 'LCAA', 'LCAAU', 'LCAHU',
 'LCFY', 'LCG', 'LCI', 'LCID', 'LCII', 'LCNB', 'LCR', 'LCTD', 'LCTU', 'LCTX', 'LCUT', 'LCW', 'LD', 'LDEM', 'LDHA', 'LDHAU', 'LDI', 'LDOS', 'LDP', 'LDSF', 'LDUR', 'LE', 'LEA', 'LEAD', 'LECO', 'LEDS', 'LEE',
 'LEG', 'LEGA', 'LEGAU', 'LEGH', 'LEGN', 'LEGR', 'LEJU', 'LEMB', 'LEN', 'LEO', 'LESL', 'LETB', 'LEU', 'LEV', 'LEVI', 'LEXI', 'LEXX', 'LFAC', 'LFACU', 'LFEQ', 'LFLY', 'LFMD', 'LFMDP', 'LFST', 'LFT', 'LFUS',
 'LFVN', 'LGH', 'LGHL', 'LGI', 'LGIH', 'LGL', 'LGLV', 'LGMK', 'LGND', 'LGO', 'LGOV', 'LGST', 'LGSTU', 'LGVC', 'LGVN', 'LH', 'LHC', 'LHX', 'LI', 'LIAN', 'LIBY', 'LIBYU', 'LICY', 'LIDR', 'LIFE', 'LII', 'LILA',
 'LILAK', 'LILM', 'LIN', 'LINC', 'LIND', 'LINK', 'LIQT', 'LIT', 'LITB', 'LITE', 'LITM', 'LITT', 'LIVB', 'LIVBU', 'LIVE', 'LIVN', 'LIXT', 'LIZI', 'LKCO', 'LKFN', 'LKOR', 'LKQ', 'LL', 'LLAP', 'LLY', 'LMAT',
 'LMB', 'LMBS', 'LMDX', 'LMFA', 'LMND', 'LMNL', 'LMNR', 'LMST', 'LMT', 'LNC', 'LND', 'LNG', 'LNKB', 'LNN', 'LNSR', 'LNT', 'LNTH', 'LNW', 'LOAN', 'LOB', 'LOCC', 'LOCL', 'LOCO', 'LODE', 'LOGI', 'LOMA', 'LONZ',
 'LOOP', 'LOPE', 'LOPP', 'LOUP', 'LOV', 'LOVE', 'LOW', 'LPCN', 'LPG', 'LPL', 'LPLA', 'LPRO', 'LPSN', 'LPTH', 'LPTV', 'LPTX', 'LPX', 'LQD', 'LQDA', 'LQDB', 'LQDH', 'LQDI', 'LQDT', 'LQIG', 'LRCX', 'LRFC', 'LRGE',
 'LRGF', 'LRMR', 'LRN', 'LRND', 'LRNZ', 'LSAF', 'LSAK', 'LSAT', 'LSBK', 'LSCC', 'LSEA', 'LSF', 'LSI', 'LSPD', 'LSST', 'LSTR', 'LSXMA', 'LSXMB', 'LSXMK', 'LTBR', 'LTC', 'LTCH', 'LTH', 'LTHM', 'LTL', 'LTPZ', 'LTRN',
 'LTRPA', 'LTRPB', 'LTRX', 'LTRY', 'LU', 'LUCD', 'LULU', 'LUMN', 'LUMO', 'LUNA', 'LUNG', 'LUV', 'LVAC', 'LVACU', 'LVHD', 'LVHI', 'LVLU', 'LVO', 'LVOL', 'LVOX', 'LVRA', 'LVRAU', 'LVS', 'LVTX', 'LW', 'LWAY', 'LWLG',
 'LX', 'LXEH', 'LXFR', 'LXP', 'LXRX', 'LXU', 'LYB', 'LYEL', 'LYFE', 'LYFT', 'LYG', 'LYLT', 'LYRA', 'LYT', 'LYTS', 'LYV', 'LZ', 'LZB', 'M', 'MA', 'MAA', 'MAAX', 'MAC', 'MACA', 'MACAU', 'MACK', 'MAG', 'MAGA', 'MAIN',
 'MAKX', 'MAMB', 'MAN', 'MANH', 'MANU', 'MAPS', 'MAQC', 'MAQCU', 'MAR', 'MARA', 'MARB', 'MARK', 'MARPS', 'MARZ', 'MAS', 'MASI', 'MASS', 'MAT', 'MATV', 'MATW', 'MATX', 'MAV', 'MAX', 'MAXN', 'MAXR', 'MAYS', 'MAYZ',
 'MBAC', 'MBB', 'MBBB', 'MBCC', 'MBCN', 'MBI', 'MBIN', 'MBINN', 'MBINO', 'MBINP', 'MBIO', 'MBND', 'MBNE', 'MBNKP', 'MBOT', 'MBOX', 'MBRX', 'MBSC', 'MBSD', 'MBTC', 'MBTCR', 'MBTCU', 'MBUU', 'MBWM', 'MC', 'MCAA',
 'MCAAU', 'MCAC', 'MCACR', 'MCACU', 'MCAF', 'MCAFR', 'MCAFU', 'MCAG', 'MCAGR', 'MCB', 'MCBC', 'MCBS', 'MCD', 'MCFT', 'MCG', 'MCH', 'MCHI', 'MCHP', 'MCHX', 'MCI', 'MCK', 'MCLD', 'MCN', 'MCO', 'MCR', 'MCRB', 'MCRI',
 'MCS', 'MCVT', 'MCW', 'MCY', 'MD', 'MDB', 'MDC', 'MDCP', 'MDEV', 'MDGL', 'MDGS', 'MDIA', 'MDIV', 'MDJH', 'MDLZ', 'MDNA', 'MDRR', 'MDRRP', 'MDRX', 'MDT', 'MDU', 'MDV', 'MDVL', 'MDWD', 'MDWT', 'MDXG', 'MDXH', 'MDY',
 'MDYG', 'MDYV', 'ME', 'MEAR', 'MEC', 'MED', 'MEDP', 'MEDS', 'MEG', 'MEGI', 'MEI', 'MEIP', 'MEKA', 'MELI', 'MEM', 'MEME', 'MEOA', 'MEOAU', 'MEOH', 'MERC', 'MESA', 'MESO', 'MET', 'META', 'METC', 'METCL', 'METV',
 'METX', 'MEXX', 'MF', 'MFA', 'MFC', 'MFD', 'MFDX', 'MFEM', 'MFG', 'MFH', 'MFIN', 'MFLX', 'MFM', 'MFUL', 'MFUS', 'MFV', 'MG', 'MGA', 'MGC', 'MGEE', 'MGF', 'MGI', 'MGIC', 'MGK', 'MGLD', 'MGM', 'MGMT', 'MGNI',
 'MGNX', 'MGPI', 'MGR', 'MGRB', 'MGRC', 'MGRD', 'MGTA', 'MGTX', 'MGU', 'MGV', 'MGY', 'MGYR', 'MHD', 'MHF', 'MHH', 'MHI', 'MHK', 'MHLA', 'MHLD', 'MHN', 'MHNC', 'MHO', 'MHUA', 'MICS', 'MID', 'MIDD', 'MIDE', 'MIDU',
 'MIG', 'MIGI', 'MILN', 'MIMO', 'MIN', 'MINC', 'MIND', 'MINDP', 'MINM', 'MINN', 'MINO', 'MINT', 'MINV', 'MIO', 'MIR', 'MIRM', 'MIRO', 'MIST', 'MITA', 'MITAU', 'MITK', 'MITQ', 'MITT', 'MIXT', 'MIY', 'MJ', 'MJUS',
 'MKC', 'MKFG', 'MKL', 'MKSI', 'MKTW', 'MKTX', 'ML', 'MLAB', 'MLAC', 'MLACU', 'MLCO', 'MLI', 'MLKN', 'MLM', 'MLN', 'MLNK', 'MLP', 'MLPA', 'MLPB', 'MLPO', 'MLPR', 'MLPX', 'MLR', 'MLSS', 'MLTX', 'MLVF', 'MMAT', 'MMC',
 'MMCA', 'MMD', 'MMI', 'MMIN', 'MMIT', 'MMLG', 'MMLP', 'MMM', 'MMMB', 'MMP', 'MMS', 'MMSC', 'MMSI', 'MMT', 'MMTM', 'MMU', 'MMYT', 'MNA', 'MNBD', 'MNDO', 'MNDY', 'MNKD', 'MNM', 'MNMD', 'MNOV', 'MNP', 'MNPR',
 'MNRO', 'MNSB', 'MNSBP', 'MNSO', 'MNST', 'MNTK', 'MNTN', 'MNTS', 'MNTV', 'MNTX', 'MO', 'MOAT', 'MOBQ', 'MOD', 'MODD', 'MODN', 'MODV', 'MOFG', 'MOGO', 'MOGU', 'MOH', 'MOHR', 'MOLN', 'MOMO', 'MOO', 'MOOD',
 'MOON', 'MOR', 'MORF', 'MORN', 'MORT', 'MOS', 'MOTE', 'MOTG', 'MOTI', 'MOTO', 'MOTS', 'MOV', 'MOVE', 'MOXC', 'MP', 'MPA', 'MPAA', 'MPAY', 'MPB', 'MPC', 'MPLN', 'MPLX', 'MPRA', 'MPRAU', 'MPRO', 'MPV',
 'MPW', 'MPWR', 'MPX', 'MQ', 'MQT', 'MQY', 'MRAD', 'MRAI', 'MRAM', 'MRBK', 'MRC', 'MRCC', 'MRCY', 'MREO', 'MRGR', 'MRIN', 'MRK', 'MRKR', 'MRM', 'MRNA', 'MRND', 'MRNS', 'MRO', 'MRSK', 'MRSN', 'MRTN', 'MRTX',
 'MRUS', 'MRVI', 'MRVL', 'MS', 'MSA', 'MSB', 'MSBI', 'MSC', 'MSCI', 'MSD', 'MSDA', 'MSDAU', 'MSEX', 'MSFT', 'MSGE', 'MSGM', 'MSGR', 'MSGS', 'MSI', 'MSM', 'MSMR', 'MSN', 'MSOS', 'MSSA', 'MSSAR', 'MSTB',
 'MSTQ', 'MSTR', 'MSVB', 'MSVX', 'MT', 'MTA', 'MTAC', 'MTACU', 'MTAL', 'MTB', 'MTC', 'MTCH', 'MTCN', 'MTD', 'MTDR', 'MTEK', 'MTEM', 'MTEX', 'MTG', 'MTGP', 'MTH', 'MTLS', 'MTN', 'MTNB', 'MTP', 'MTR',
 'MTRN', 'MTRX', 'MTRY', 'MTRYU', 'MTSI', 'MTTR', 'MTUL', 'MTUM', 'MTVC', 'MTVR', 'MTW', 'MTX', 'MTZ', 'MU', 'MUA', 'MUB', 'MUC', 'MUE', 'MUFG', 'MUI', 'MUJ', 'MULN', 'MUNI', 'MUR', 'MURF', 'MURFU',
 'MUSA', 'MUSI', 'MUST', 'MUX', 'MVBF', 'MVF', 'MVIS', 'MVO', 'MVPS', 'MVRL', 'MVST', 'MVT', 'MVV', 'MWA', 'MX', 'MXC', 'MXCT', 'MXE', 'MXF', 'MXI', 'MXL', 'MYD', 'MYE', 'MYFW', 'MYGN', 'MYI', 'MYMD',
 'MYN', 'MYNA', 'MYNZ', 'MYO', 'MYOV', 'MYPS', 'MYRG', 'MYSZ', 'MYTE', 'MYY', 'MZZ', 'NA', 'NAAS', 'NABL', 'NAC', 'NACP', 'NAD', 'NAII', 'NAIL', 'NAK', 'NAN', 'NANR', 'NAOV', 'NAPA', 'NAPR', 'NARI',
 'NAT', 'NATH', 'NATI', 'NATR', 'NAUT', 'NAVB', 'NAVI', 'NAZ', 'NBB', 'NBCC', 'NBDS', 'NBH', 'NBHC', 'NBIX', 'NBN', 'NBO', 'NBR', 'NBRV', 'NBSE', 'NBST', 'NBSTU', 'NBTB', 'NBTX', 'NBW', 'NBXG', 'NBY',
 'NC', 'NCA', 'NCAC', 'NCACU', 'NCLH', 'NCMI', 'NCNA', 'NCNO', 'NCPL', 'NCR', 'NCRA', 'NCSM', 'NCTY', 'NCV', 'NCZ', 'NDAQ', 'NDJI', 'NDLS', 'NDMO', 'NDP', 'NDRA', 'NDSN', 'NDVG', 'NE', 'NEA', 'NEAR',
 'NECB', 'NEE', 'NEGG', 'NEM', 'NEN', 'NEO', 'NEOG', 'NEON', 'NEOV', 'NEP', 'NEPH', 'NEPT', 'NERD', 'NERV', 'NESR', 'NET', 'NETC', 'NETI', 'NETL', 'NETZ', 'NEU', 'NEWP', 'NEWR', 'NEWT', 'NEWTL', 'NEWTZ',
 'NEX', 'NEXA', 'NEXI', 'NEXT', 'NFBK', 'NFE', 'NFG', 'NFGC', 'NFJ', 'NFLT', 'NFLX', 'NFNT', 'NFRA', 'NFTY', 'NFYS', 'NG', 'NGC', 'NGD', 'NGE', 'NGG', 'NGL', 'NGM', 'NGMS', 'NGS', 'NGVC', 'NGVT', 'NH',
 'NHC', 'NHI', 'NHIC', 'NHICU', 'NHS', 'NHTC', 'NHWK', 'NI', 'NIB', 'NIC', 'NICE', 'NICK', 'NID', 'NIE', 'NIM', 'NIMC', 'NINE', 'NIO', 'NIQ', 'NISN', 'NIU', 'NIWM', 'NJAN', 'NJR', 'NJUL', 'NKE', 'NKEL',
 'NKEQ', 'NKG', 'NKLA', 'NKSH', 'NKTR', 'NKTX', 'NKX', 'NL', 'NLR', 'NLS', 'NLSP', 'NLTX', 'NLY', 'NM', 'NMAI', 'NMCO', 'NMFC', 'NMG', 'NMI', 'NMIH', 'NML', 'NMM', 'NMR', 'NMRD', 'NMRK', 'NMS', 'NMT',
 'NMTC', 'NMTR', 'NMZ', 'NN', 'NNBR', 'NNDM', 'NNI', 'NNN', 'NNOX', 'NNVC', 'NNY', 'NOA', 'NOAH', 'NOBL', 'NOC', 'NOCT', 'NODK', 'NOG', 'NOK', 'NOM', 'NOMD', 'NORW', 'NOTV', 'NOV', 'NOVA', 'NOVN',
 'NOVT', 'NOVV', 'NOVVR', 'NOVZ', 'NOW', 'NPAB', 'NPABU', 'NPCE', 'NPCT', 'NPFD', 'NPK', 'NPO', 'NPV', 'NQP', 'NR', 'NRAC', 'NRACU', 'NRBO', 'NRC', 'NRDS', 'NRDY', 'NREF', 'NRG', 'NRGD', 'NRGU', 'NRGV',
 'NRGX', 'NRIM', 'NRIX', 'NRK', 'NRO', 'NRP', 'NRSN', 'NRT', 'NRUC', 'NRXP', 'NS', 'NSA', 'NSC', 'NSCS', 'NSIT', 'NSL', 'NSP', 'NSPI', 'NSPR', 'NSPY', 'NSS', 'NSSC', 'NSTB', 'NSTC', 'NSTD', 'NSTG', 'NSTS',
 'NSYS', 'NTAP', 'NTB', 'NTCO', 'NTCT', 'NTES', 'NTG', 'NTGR', 'NTIC', 'NTIP', 'NTKI', 'NTLA', 'NTNX', 'NTR', 'NTRA', 'NTRB', 'NTRS', 'NTRSO', 'NTSE', 'NTSI', 'NTST', 'NTSX', 'NTWK', 'NTZ', 'NTZG', 'NU',
 'NUAG', 'NUBD', 'NUBI', 'NUBIU', 'NUDM', 'NUDV', 'NUE', 'NUEM', 'NUGO', 'NUGT', 'NUHY', 'NULC', 'NULG', 'NULV', 'NUMG', 'NUMV', 'NUO', 'NURE', 'NURO', 'NUS', 'NUSA', 'NUSC', 'NUSI', 'NUTX', 'NUV', 'NUVA',
 'NUVB', 'NUVL', 'NUW', 'NUWE', 'NUZE', 'NVAC', 'NVACR', 'NVAX', 'NVCN', 'NVCR', 'NVCT', 'NVDA', 'NVDS', 'NVEC', 'NVEE', 'NVEI', 'NVFY', 'NVG', 'NVGS', 'NVIV', 'NVMI', 'NVNO', 'NVO', 'NVOS', 'NVQ', 'NVR',
 'NVRO', 'NVS', 'NVST', 'NVT', 'NVTA', 'NVTS', 'NVVE', 'NVX', 'NWBI', 'NWE', 'NWFL', 'NWG', 'NWL', 'NWLG', 'NWLI', 'NWN', 'NWPX', 'NWS', 'NWSA', 'NX', 'NXC', 'NXDT', 'NXE', 'NXGL', 'NXGN', 'NXJ', 'NXN',
 'NXP', 'NXPI', 'NXPL', 'NXRT', 'NXST', 'NXTC', 'NXTG', 'NXTP', 'NYC', 'NYCB', 'NYF', 'NYMT', 'NYMTL', 'NYMTM', 'NYMTN', 'NYMTZ', 'NYMX', 'NYT', 'NYXH', 'NZAC', 'NZF', 'NZUS', 'O', 'OACP', 'OAIE', 'OALC',
 'OB', 'OBE', 'OBLG', 'OBND', 'OBNK', 'OBOR', 'OBSV', 'OBT', 'OC', 'OCAX', 'OCAXU', 'OCC', 'OCCI', 'OCCIN', 'OCCIO', 'OCEN', 'OCFC', 'OCFCP', 'OCFT', 'OCG', 'OCGN', 'OCIO', 'OCN', 'OCSL', 'OCTZ', 'OCUL',
 'OCUP', 'OCX', 'ODC', 'ODDS', 'ODFL', 'ODP', 'ODV', 'OEC', 'OEF', 'OESX', 'OEUR', 'OFC', 'OFED', 'OFG', 'OFIX', 'OFLX', 'OFS', 'OFSSH', 'OGCP', 'OGE', 'OGEN', 'OGI', 'OGIG', 'OGN', 'OGS', 'OHAA', 'OHI',
 'OI', 'OIA', 'OIH', 'OII', 'OIL', 'OILD', 'OILK', 'OILU', 'OIS', 'OKE', 'OKTA', 'OKYO', 'OLB', 'OLED', 'OLIT', 'OLITU', 'OLK', 'OLLI', 'OLMA', 'OLN', 'OLO', 'OLP', 'OLPX', 'OM', 'OMAB', 'OMC', 'OMCL', 'OMER',
 'OMEX', 'OMF', 'OMFL', 'OMFS', 'OMGA', 'OMI', 'OMIC', 'OMQS', 'ON', 'ONB', 'ONBPO', 'ONBPP', 'ONCR', 'ONCS', 'ONCT', 'ONCY', 'OND', 'ONDS', 'ONEO', 'ONEQ', 'ONEV', 'ONEW', 'ONEY', 'ONG', 'ONL', 'ONLN', 'ONOF',
 'ONON', 'ONTF', 'ONTO', 'ONTX', 'ONVO', 'ONYX', 'ONYXU', 'OOMA', 'OOTO', 'OP', 'OPA', 'OPAD', 'OPBK', 'OPCH', 'OPEN', 'OPER', 'OPFI', 'OPGN', 'OPHC', 'OPI', 'OPINL', 'OPK', 'OPOF', 'OPP', 'OPPX', 'OPRA', 'OPRT',
 'OPRX', 'OPT', 'OPTN', 'OPTT', 'OPY', 'OR', 'ORA', 'ORAN', 'ORC', 'ORCC', 'ORCL', 'ORFN', 'ORGN', 'ORGO', 'ORGS', 'ORI', 'ORIA', 'ORIAU', 'ORIC', 'ORLA', 'ORLY', 'ORMP', 'ORN', 'ORRF', 'ORTX', 'OSBC', 'OSCR',
 'OSCV', 'OSG', 'OSH', 'OSI', 'OSIS', 'OSK', 'OSPN', 'OSS', 'OST', 'OSTK', 'OSUR', 'OSW', 'OTEC', 'OTECU', 'OTEX', 'OTIS', 'OTLK', 'OTLY', 'OTMO', 'OTRK', 'OTRKP', 'OTTR', 'OUNZ', 'OUSA', 'OUSM', 'OUST', 'OUT',
 'OVB', 'OVBC', 'OVF', 'OVID', 'OVL', 'OVLH', 'OVLY', 'OVM', 'OVS', 'OVT', 'OVV', 'OWL', 'OWLT', 'OWNS', 'OXAC', 'OXBR', 'OXLC', 'OXLCL', 'OXLCM', 'OXLCN', 'OXLCO', 'OXLCP', 'OXLCZ', 'OXM', 'OXSQ', 'OXSQG',
 'OXSQL', 'OXSQZ', 'OXUS', 'OXUSU', 'OXY', 'OZ', 'OZK', 'OZKAP', 'PAA', 'PAAS', 'PABU', 'PAC', 'PACB', 'PACI', 'PACK', 'PACW', 'PACWP', 'PAG', 'PAGP', 'PAGS', 'PAHC', 'PAI', 'PAK', 'PALC', 'PALI', 'PALL', 'PALT',
 'PAM', 'PAMC', 'PANA', 'PANL', 'PANW', 'PAPR', 'PAR', 'PARA', 'PARAA', 'PARAP', 'PARR', 'PASG', 'PATH', 'PATI', 'PATK', 'PAUG', 'PAVE', 'PAVM', 'PAWZ', 'PAX', 'PAXS', 'PAY', 'PAYC', 'PAYO', 'PAYS', 'PAYX', 'PB',
 'PBA', 'PBAX', 'PBAXU', 'PBBK', 'PBD', 'PBDM', 'PBE', 'PBEE', 'PBF', 'PBFS', 'PBH', 'PBHC', 'PBI', 'PBJ', 'PBLA', 'PBND', 'PBP', 'PBPB', 'PBR', 'PBS', 'PBSM', 'PBT', 'PBTP', 'PBTS', 'PBUS', 'PBW', 'PBYI', 'PCAR',
 'PCB', 'PCCT', 'PCEF', 'PCF', 'PCG', 'PCGU', 'PCH', 'PCK', 'PCM', 'PCN', 'PCOR', 'PCQ', 'PCRX', 'PCSA', 'PCT', 'PCTI', 'PCTTU', 'PCTY', 'PCVX', 'PCY', 'PCYG', 'PCYO', 'PD', 'PDBC', 'PDCE', 'PDCO', 'PDD', 'PDEC',
 'PDEX', 'PDFS', 'PDI', 'PDLB', 'PDM', 'PDN', 'PDO', 'PDOT', 'PDP', 'PDS', 'PDSB', 'PDT', 'PEAK', 'PEAR', 'PEB', 'PEBK', 'PEBO', 'PECO', 'PED', 'PEG', 'PEGA', 'PEGR', 'PEGRU', 'PEGY', 'PEJ', 'PEN', 'PENN', 'PEO',
 'PEP', 'PEPG', 'PEPL', 'PEPLU', 'PERI', 'PESI', 'PETQ', 'PETS', 'PETV', 'PETZ', 'PEV', 'PEX', 'PEXL', 'PEY', 'PEZ', 'PFBC', 'PFC', 'PFD', 'PFE', 'PFEB', 'PFEL', 'PFES', 'PFF', 'PFFA', 'PFFD', 'PFFL', 'PFFR',
 'PFFV', 'PFG', 'PFGC', 'PFH', 'PFI', 'PFIE', 'PFIG', 'PFIN', 'PFIS', 'PFIX', 'PFL', 'PFLD', 'PFLT', 'PFM', 'PFMT', 'PFN', 'PFO', 'PFRL', 'PFS', 'PFSI', 'PFSW', 'PFTA', 'PFTAU', 'PFUT', 'PFX', 'PFXF', 'PFXNZ',
 'PG', 'PGAL', 'PGC', 'PGEN', 'PGF', 'PGHY', 'PGJ', 'PGM', 'PGNY', 'PGP', 'PGR', 'PGRE', 'PGRO', 'PGRU', 'PGRW', 'PGRWU', 'PGSS', 'PGTI', 'PGX', 'PGY', 'PGZ', 'PH', 'PHAR', 'PHAT', 'PHB', 'PHCF', 'PHD', 'PHDG',
 'PHG', 'PHGE', 'PHI', 'PHIO', 'PHK', 'PHM', 'PHO', 'PHR', 'PHT', 'PHUN', 'PHVS', 'PHX', 'PHYL', 'PHYS', 'PHYT', 'PI', 'PIAI', 'PICB', 'PICK', 'PID', 'PIE', 'PIFI', 'PII', 'PIII', 'PIK', 'PILL', 'PIM', 'PIN',
 'PINC', 'PINE', 'PINK', 'PINS', 'PIO', 'PIPR', 'PIRS', 'PIXY', 'PIZ', 'PJAN', 'PJP', 'PJT', 'PJUL', 'PJUN', 'PK', 'PKB', 'PKBK', 'PKE', 'PKG', 'PKI', 'PKOH', 'PKW', 'PKX', 'PL', 'PLAB', 'PLAG', 'PLAO', 'PLAOU']



databaxC = ['PLXP', 'PLXS', 'PLYA', 'PLYM', 'PM', 'PMAR', 'PMAY', 'PMCB', 'PMD', 'PMF', 'PMGM', 'PMGMU', 'PML', 'PMM', 'PMN', 'PMO', 'PMT', 'PMTS', 'PMVP', 'PMX', 'PNAC', 'PNACR', 'PNACU', 'PNBK', 'PNC', 'PNF', 'PNFP',
 'PNFPP', 'PNI', 'PNM', 'PNNT', 'PNOV', 'PNQI', 'PNR', 'PNRG', 'PNT', 'PNTG', 'PNTM', 'PNW', 'POAI', 'POCT', 'PODD', 'POET', 'POLA', 'POOL', 'POR', 'PORT', 'POST', 'POTX', 'POWI', 'POWL', 'POWW', 'POWWP',
 'PPA', 'PPBI', 'PPBT', 'PPC', 'PPG', 'PPH', 'PPHP', 'PPHPR', 'PPHPU', 'PPI', 'PPIH', 'PPL', 'PPLT', 'PPSI', 'PPT', 'PPTA', 'PPTY', 'PPYA', 'PPYAU', 'PQDI', 'PRA', 'PRAA', 'PRAX', 'PRAY', 'PRCH', 'PRCT',
 'PRDO', 'PRDS', 'PRE', 'PREF', 'PRF', 'PRFT', 'PRFX', 'PRFZ', 'PRG', 'PRGO', 'PRGS', 'PRI', 'PRIM', 'PRK', 'PRLB', 'PRLD', 'PRLH', 'PRLHU', 'PRM', 'PRMW', 'PRN', 'PRNT', 'PRO', 'PROC', 'PROF', 'PROK',
 'PROV', 'PRPC', 'PRPH', 'PRPL', 'PRPO', 'PRQR', 'PRS', 'PRSO', 'PRSR', 'PRSRU', 'PRT', 'PRTA', 'PRTC', 'PRTG', 'PRTH', 'PRTK', 'PRTS', 'PRU', 'PRVA', 'PRVB', 'PSA', 'PSC', 'PSCC', 'PSCD', 'PSCE', 'PSCF',
 'PSCH', 'PSCI', 'PSCJ', 'PSCM', 'PSCQ', 'PSCT', 'PSCU', 'PSCW', 'PSCX', 'PSDN', 'PSEC', 'PSEP', 'PSET', 'PSF', 'PSFD', 'PSFE', 'PSFF', 'PSFJ', 'PSFM', 'PSFO', 'PSHG', 'PSI', 'PSIL', 'PSJ', 'PSK', 'PSL',
 'PSLV', 'PSMB', 'PSMC', 'PSMD', 'PSMG', 'PSMJ', 'PSMM', 'PSMO', 'PSMR', 'PSMT', 'PSN', 'PSNL', 'PSNY', 'PSO', 'PSP', 'PSPC', 'PSQ', 'PSR', 'PST', 'PSTG', 'PSTL', 'PSTP', 'PSTV', 'PSTX', 'PSX', 'PSYK',
 'PT', 'PTA', 'PTBD', 'PTC', 'PTCT', 'PTE', 'PTEN', 'PTEU', 'PTF', 'PTGX', 'PTH', 'PTIN', 'PTIX', 'PTLC', 'PTLO', 'PTMC', 'PTMN', 'PTN', 'PTNQ', 'PTOC', 'PTOCU', 'PTON', 'PTPI', 'PTRA', 'PTRB', 'PTRS',
 'PTSI', 'PTVE', 'PTY', 'PUBM', 'PUCK', 'PUCKU', 'PUI', 'PUK', 'PULM', 'PULS', 'PUMP', 'PUNK', 'PUTW', 'PUYI', 'PVAL', 'PVBC', 'PVH', 'PVI', 'PVL', 'PW', 'PWB', 'PWC', 'PWFL', 'PWOD', 'PWP', 'PWR', 'PWS',
 'PWSC', 'PWUP', 'PWUPU', 'PWV', 'PWZ', 'PX', 'PXD', 'PXE', 'PXF', 'PXH', 'PXI', 'PXJ', 'PXLW', 'PXQ', 'PXS', 'PXSAP', 'PXUS', 'PY', 'PYCR', 'PYN', 'PYPD', 'PYPE', 'PYPL', 'PYPS', 'PYPT', 'PYR', 'PYT',
 'PYXS', 'PYZ', 'PZA', 'PZC', 'PZG', 'PZT', 'PZZA', 'QABA', 'QAI', 'QARP', 'QAT', 'QCLN', 'QCLR', 'QCOM', 'QCON', 'QCRH', 'QD', 'QDEC', 'QDEF', 'QDEL', 'QDF', 'QDIV', 'QDPL', 'QDYN', 'QEFA', 'QEMM', 'QFIN',
 'QFTA', 'QGEN', 'QGRO', 'QH', 'QID', 'QINT', 'QIPT', 'QJUN', 'QLC', 'QLD', 'QLGN', 'QLI', 'QLTA', 'QLV', 'QLVD', 'QLVE', 'QLYS', 'QMAR', 'QMCO', 'QMOM', 'QNRX', 'QNST', 'QPFF', 'QPX', 'QQC', 'QQD', 'QQEW',
 'QQH', 'QQJG', 'QQMG', 'QQQ', 'QQQA', 'QQQE', 'QQQJ', 'QQQM', 'QQQN', 'QQQX', 'QQXT', 'QRFT', 'QRHC', 'QRMI', 'QRTEA', 'QRTEB', 'QRTEP', 'QRVO', 'QS', 'QSI', 'QSPT', 'QSR', 'QSWN', 'QTAP', 'QTEC', 'QTEK',
 'QTJA', 'QTJL', 'QTOC', 'QTR', 'QTRX', 'QTT', 'QTUM', 'QTWO', 'QUAD', 'QUAL', 'QUBT', 'QUIK', 'QULL', 'QUOT', 'QURE', 'QUS', 'QVAL', 'QVCC', 'QVCD', 'QVML', 'QVMM', 'QVMS', 'QWLD', 'QYLD', 'QYLG', 'R', 'RA',
 'RAAS', 'RAAX', 'RACE', 'RACY', 'RACYU', 'RAD', 'RADI', 'RAFE', 'RAIL', 'RAIN', 'RAM', 'RAMMU', 'RAMP', 'RAND', 'RANI', 'RAPT', 'RARE', 'RAVE', 'RAVI', 'RAYC', 'RAYD', 'RAYE', 'RAYS', 'RBA', 'RBB', 'RBBN',
 'RBCAA', 'RBKB', 'RBLX', 'RBND', 'RBOT', 'RC', 'RCA', 'RCAC', 'RCACU', 'RCAT', 'RCB', 'RCC', 'RCD', 'RCEL', 'RCFA', 'RCG', 'RCI', 'RCKT', 'RCKY', 'RCL', 'RCLF', 'RCLFU', 'RCM', 'RCMT', 'RCON', 'RCRT', 'RCS',
 'RCUS', 'RDCM', 'RDFI', 'RDFN', 'RDHL', 'RDI', 'RDIB', 'RDIV', 'RDMX', 'RDN', 'RDNT', 'RDOG', 'RDVT', 'RDVY', 'RDW', 'RDWR', 'RDY', 'RE', 'REAL', 'REAX', 'RECS', 'REE', 'REET', 'REFI', 'REFR', 'REG',
 'REGL', 'REGN', 'REI', 'REIT', 'REK', 'REKR', 'RELI', 'RELL', 'RELX', 'RELY', 'REM', 'REMG', 'REMX', 'RENE', 'RENEU', 'RENN', 'RENT', 'RENW', 'REPL', 'REPX', 'RERE', 'RES', 'RESD', 'RESE', 'RESI', 'RESP',
 'RETA', 'RETL', 'RETO', 'REVB', 'REVE', 'REVEU', 'REVG', 'REVS', 'REW', 'REX', 'REXR', 'REYN', 'REZ', 'REZI', 'RF', 'RFAC', 'RFACR', 'RFACU', 'RFCI', 'RFDA', 'RFDI', 'RFEM', 'RFEU', 'RFFC', 'RFG', 'RFI',
 'RFIL', 'RFL', 'RFM', 'RFMZ', 'RFV', 'RGA', 'RGC', 'RGCO', 'RGEN', 'RGF', 'RGI', 'RGLD', 'RGLS', 'RGNX', 'RGP', 'RGR', 'RGS', 'RGT', 'RGTI', 'RH', 'RHE', 'RHI', 'RHP', 'RHRX', 'RHS', 'RHTX', 'RIBT', 'RICK',
 'RIDE', 'RIET', 'RIG', 'RIGL', 'RIGS', 'RILY', 'RILYG', 'RILYK', 'RILYL', 'RILYM', 'RILYN', 'RILYO', 'RILYP', 'RILYT', 'RILYZ', 'RINF', 'RING', 'RIO', 'RIOT', 'RISN', 'RISR', 'RITA', 'RIV', 'RIVN', 'RJAC',
 'RJF', 'RKDA', 'RKLB', 'RKT', 'RKTA', 'RL', 'RLAY', 'RLGT', 'RLI', 'RLJ', 'RLMD', 'RLTY', 'RLX', 'RLY', 'RLYB', 'RM', 'RMAX', 'RMBI', 'RMBL', 'RMBS', 'RMCF', 'RMD', 'RMED', 'RMGC', 'RMGCU', 'RMI', 'RMM',
 'RMMZ', 'RMNI', 'RMR', 'RMT', 'RMTI', 'RNA', 'RNAZ', 'RNDM', 'RNDV', 'RNEM', 'RNG', 'RNGR', 'RNLC', 'RNLX', 'RNMC', 'RNP', 'RNR', 'RNRG', 'RNSC', 'RNST', 'RNW', 'RNXT', 'ROAD', 'ROAM', 'ROBO', 'ROBT',
 'ROC', 'ROCAR', 'ROCAU', 'ROCC', 'ROCG', 'ROCGU', 'ROCI', 'ROCK', 'ROCL', 'ROCLU', 'RODE', 'RODM', 'ROG', 'ROIC', 'ROIV', 'ROK', 'ROKT', 'ROKU', 'ROL', 'ROM', 'ROMO', 'RONI', 'ROOF', 'ROOT', 'ROP', 'RORO',
 'ROSC', 'ROSE', 'ROSEU', 'ROSS', 'ROST', 'ROUS', 'ROVR', 'RPAR', 'RPAY', 'RPD', 'RPG', 'RPHM', 'RPHS', 'RPID', 'RPM', 'RPRX', 'RPT', 'RPTX', 'RPV', 'RQI', 'RRAC', 'RRBI', 'RRC', 'RRGB', 'RRH', 'RRR', 'RRX',
 'RS', 'RSEE', 'RSF', 'RSG', 'RSI', 'RSKD', 'RSLS', 'RSP', 'RSPE', 'RSPY', 'RSSS', 'RSVR', 'RTAI', 'RTH', 'RTL', 'RTLPO', 'RTLPP', 'RTM', 'RTX', 'RTYD', 'RUFF', 'RULE', 'RUN', 'RUSHA', 'RUSHB', 'RUTH', 'RVLP',
 'RVLV', 'RVMD', 'RVNC', 'RVNU', 'RVP', 'RVPH', 'RVSB', 'RVSN', 'RVT', 'RWAY', 'RWJ', 'RWK', 'RWL', 'RWLK', 'RWM', 'RWO', 'RWOD', 'RWODU', 'RWR', 'RWT', 'RWX', 'RXD', 'RXDX', 'RXI', 'RXL', 'RXRX', 'RXST',
 'RXT', 'RY', 'RYAAY', 'RYAM', 'RYAN', 'RYE', 'RYF', 'RYH', 'RYI', 'RYJ', 'RYLD', 'RYN', 'RYT', 'RYTM', 'RYU', 'RZB', 'RZG', 'RZLT', 'RZV', 'S', 'SA', 'SAA', 'SABR', 'SABRP', 'SABS', 'SACC', 'SACH', 'SAEF',
 'SAFE', 'SAFT', 'SAGA', 'SAGAR', 'SAGAU', 'SAGE', 'SAGP', 'SAH', 'SAI', 'SAIA', 'SAIC', 'SAL', 'SALM', 'SAM', 'SAMA', 'SAMAU', 'SAMG', 'SAMT', 'SAN', 'SANA', 'SAND', 'SANG', 'SANM', 'SANW', 'SAP', 'SAR',
 'SARK', 'SASI', 'SASR', 'SAT', 'SATL', 'SATO', 'SATS', 'SAVA', 'SAVE', 'SAVN', 'SB', 'SBAC', 'SBB', 'SBBA', 'SBCF', 'SBET', 'SBEV', 'SBFG', 'SBFM', 'SBGI', 'SBH', 'SBI', 'SBIG', 'SBIO', 'SBLK', 'SBNY',
 'SBNYP', 'SBOW', 'SBR', 'SBRA', 'SBS', 'SBSI', 'SBSW', 'SBT', 'SBUX', 'SCAQ', 'SCAQU', 'SCC', 'SCCB', 'SCCC', 'SCCD', 'SCCE', 'SCCF', 'SCCO', 'SCD', 'SCDL', 'SCHA', 'SCHB', 'SCHC', 'SCHD', 'SCHE', 'SCHF',
 'SCHG', 'SCHH', 'SCHI', 'SCHJ', 'SCHK', 'SCHL', 'SCHM', 'SCHN', 'SCHO', 'SCHP', 'SCHQ', 'SCHR', 'SCHV', 'SCHW', 'SCHX', 'SCHY', 'SCHZ', 'SCI', 'SCJ', 'SCKT', 'SCL', 'SCM', 'SCO', 'SCOR', 'SCPH', 'SCPL',
 'SCRD', 'SCRM', 'SCRMU', 'SCS', 'SCSC', 'SCTL', 'SCU', 'SCUA', 'SCVL', 'SCWO', 'SCWX', 'SCX', 'SCYX', 'SCZ', 'SD', 'SDAC', 'SDACU', 'SDC', 'SDCI', 'SDD', 'SDEF', 'SDEI', 'SDEM', 'SDG', 'SDGR', 'SDHY',
 'SDIG', 'SDIV', 'SDOG', 'SDOW', 'SDP', 'SDPI', 'SDS', 'SDVY', 'SDY', 'SE', 'SEA', 'SEAC', 'SEAS', 'SEAT', 'SEB', 'SECO', 'SECT', 'SEDA', 'SEDG', 'SEE', 'SEED', 'SEEL', 'SEER', 'SEF', 'SEIC', 'SEIM', 'SEIQ',
 'SEIV', 'SEIX', 'SELB', 'SELF', 'SELV', 'SEM', 'SEMI', 'SEMR', 'SENEA', 'SENEB', 'SENS', 'SENT', 'SEPZ', 'SERA', 'SES', 'SEV', 'SEVN', 'SF', 'SFB', 'SFBC', 'SFBS', 'SFE', 'SFIG', 'SFIX', 'SFL', 'SFM', 'SFNC',
 'SFST', 'SFT', 'SFY', 'SFYF', 'SFYX', 'SG', 'SGA', 'SGBX', 'SGC', 'SGDJ', 'SGDM', 'SGEN', 'SGFY', 'SGG', 'SGH', 'SGHC', 'SGHL', 'SGHLU', 'SGHT', 'SGII', 'SGIIU', 'SGLY', 'SGMA', 'SGML', 'SGMO', 'SGOL', 'SGOV',
 'SGRP', 'SGRY', 'SGTX', 'SGU', 'SH', 'SHAG', 'SHAK', 'SHAP', 'SHBI', 'SHC', 'SHCR', 'SHE', 'SHEL', 'SHEN', 'SHG', 'SHIP', 'SHLS', 'SHM', 'SHO', 'SHOO', 'SHOP', 'SHPP', 'SHPW', 'SHUAU', 'SHUS', 'SHV', 'SHW',
 'SHY', 'SHYD', 'SHYF', 'SHYG', 'SHYL', 'SI', 'SIBN', 'SID', 'SIDU', 'SIEB', 'SIEN', 'SIF', 'SIFI', 'SIFY', 'SIG', 'SIGA', 'SIGI', 'SIGIP', 'SIHY', 'SII', 'SIJ', 'SIL', 'SILC', 'SILJ', 'SILK', 'SILO', 'SILV',
 'SILX', 'SIM', 'SIMO', 'SIMS', 'SINT', 'SIOX', 'SIRE', 'SIRI', 'SISI', 'SITC', 'SITE', 'SITM', 'SIVB', 'SIVBP', 'SIVR', 'SIX', 'SIXA', 'SIXH', 'SIXJ', 'SIXL', 'SIXO', 'SIXS', 'SIZE', 'SJ', 'SJB', 'SJM', 'SJNK',
 'SJR', 'SJT', 'SJW', 'SKE', 'SKF', 'SKGRU', 'SKIL', 'SKIN', 'SKLZ', 'SKM', 'SKOR', 'SKT', 'SKX', 'SKY', 'SKYA', 'SKYAU', 'SKYH', 'SKYT', 'SKYU', 'SKYW', 'SKYX', 'SKYY', 'SLAB', 'SLAC', 'SLAM', 'SLAMU', 'SLB',
 'SLCA', 'SLDB', 'SLDP', 'SLF', 'SLG', 'SLGC', 'SLGG', 'SLGL', 'SLGN', 'SLI', 'SLM', 'SLMBP', 'SLN', 'SLNG', 'SLNH', 'SLNHP', 'SLNO', 'SLP', 'SLQD', 'SLQT', 'SLRC', 'SLRX', 'SLS', 'SLV', 'SLVM', 'SLVO', 'SLVP',
 'SLVR', 'SLVRU', 'SLX', 'SLY', 'SLYG', 'SLYV', 'SM', 'SMAP', 'SMAPU', 'SMAR', 'SMB', 'SMBC', 'SMBK', 'SMCI', 'SMCP', 'SMDD', 'SMDV', 'SMFG', 'SMFL', 'SMG', 'SMH', 'SMHB', 'SMHI', 'SMI', 'SMID', 'SMIG', 'SMIH',
 'SMIHU', 'SMIN', 'SMLE', 'SMLF', 'SMLP', 'SMLR', 'SMLV', 'SMMD', 'SMMF', 'SMMT', 'SMMU', 'SMMV', 'SMN', 'SMOG', 'SMP', 'SMPL', 'SMR', 'SMRT', 'SMSI', 'SMTC', 'SMTI', 'SMWB', 'SNA', 'SNAP', 'SNAX', 'SNBR', 'SNCE',
 'SNCR', 'SNCRL', 'SNCY', 'SND', 'SNDA', 'SNDL', 'SNDR', 'SNDX', 'SNES', 'SNEX', 'SNFCA', 'SNGX', 'SNLN', 'SNMP', 'SNN', 'SNOA', 'SNOW', 'SNPE', 'SNPO', 'SNPS', 'SNPX', 'SNRH', 'SNRHU', 'SNSE', 'SNSR', 'SNT',
 'SNTG', 'SNTI', 'SNV', 'SNX', 'SNY', 'SO', 'SOBR', 'SOCL', 'SOFI', 'SOFO', 'SOGU', 'SOHO', 'SOHOB', 'SOHON',
 'SOHOO', 'SOHU', 'SOI', 'SOJC', 'SOJD', 'SOJE', 'SOL', 'SOLO', 'SOLR', 'SON', 'SOND', 'SONM', 'SONN', 'SONO', 'SONX', 'SONY', 'SOPA', 'SOPH', 'SOR', 'SOS', 'SOTK', 'SOUN', 'SOVO', 'SOXL', 'SOXQ', 'SOXS',
 'SOXX', 'SOYB', 'SP', 'SPAB', 'SPAX', 'SPB', 'SPBC', 'SPBO', 'SPC', 'SPCB', 'SPCE', 'SPCM', 'SPCMU', 'SPCX', 'SPCZ', 'SPD', 'SPDN', 'SPDV', 'SPDW', 'SPE', 'SPEM', 'SPEU', 'SPFF', 'SPFI', 'SPG', 'SPGI',
 'SPGM', 'SPGP', 'SPH', 'SPHB', 'SPHD', 'SPHQ', 'SPHY', 'SPI', 'SPIB', 'SPIP', 'SPIR', 'SPKB', 'SPKBU', 'SPLB', 'SPLG', 'SPLK', 'SPLP', 'SPLV', 'SPMB', 'SPMD', 'SPMO', 'SPMV', 'SPNS', 'SPNT', 'SPOK', 'SPOT',
 'SPPI', 'SPPP', 'SPR', 'SPRB', 'SPRC', 'SPRE', 'SPRO', 'SPRX', 'SPSB', 'SPSC', 'SPSK', 'SPSM', 'SPT', 'SPTI', 'SPTL', 'SPTM', 'SPTN', 'SPTS', 'SPUC', 'SPUS', 'SPUU', 'SPVM', 'SPVU', 'SPWH', 'SPWR', 'SPXB',
 'SPXC', 'SPXE', 'SPXL', 'SPXN', 'SPXS', 'SPXT', 'SPXU', 'SPXV', 'SPXX', 'SPY', 'SPYC', 'SPYD', 'SPYG', 'SPYV', 'SPYX', 'SQ', 'SQEW', 'SQFT', 'SQFTP', 'SQL', 'SQLV', 'SQM', 'SQNS', 'SQQQ', 'SQSP', 'SQZ', 'SR',
 'SRAD', 'SRC', 'SRCE', 'SRCL', 'SRDX', 'SRE', 'SREA', 'SRET', 'SRG', 'SRGA', 'SRI', 'SRL', 'SRLN', 'SRPT', 'SRRK', 'SRS', 'SRT', 'SRTS', 'SRTY', 'SRV', 'SRVR', 'SRZN', 'SSB', 'SSBI', 'SSBK', 'SSD', 'SSFI',
 'SSG', 'SSIC', 'SSKN', 'SSL', 'SSNC', 'SSNT', 'SSO', 'SSP', 'SSPX', 'SSPY', 'SSRM', 'SSSS', 'SSSSL', 'SST', 'SSTI', 'SSTK', 'SSU', 'SSUS', 'SSXU', 'SSY', 'SSYS', 'ST', 'STAA', 'STAF', 'STAG', 'STAR', 'STBA',
 'STC', 'STCN', 'STE', 'STEM', 'STEP', 'STER', 'STET', 'STEW', 'STG', 'STGF', 'STGW', 'STIM', 'STIP', 'STK', 'STKL', 'STKS', 'STLA', 'STLD', 'STLG', 'STLV', 'STM', 'STN', 'STNC', 'STNE', 'STNG', 'STOK', 'STOT',
 'STPZ', 'STR', 'STRA', 'STRC', 'STRE', 'STRL', 'STRM', 'STRO', 'STRR', 'STRRP', 'STRS', 'STRT', 'STSA', 'STSS', 'STT', 'STTK', 'STVN', 'STWD', 'STX', 'STXS', 'STZ', 'SU', 'SUAC', 'SUB', 'SUBS', 'SUI', 'SUM',
 'SUMO', 'SUN', 'SUNL', 'SUNW', 'SUP', 'SUPL', 'SUPN', 'SUPV', 'SURF', 'SURG', 'SUSA', 'SUSB', 'SUSC', 'SUSL', 'SUZ', 'SVAL', 'SVC', 'SVFB', 'SVFD', 'SVIX', 'SVM', 'SVNA', 'SVNAU', 'SVOL', 'SVRA', 'SVRE', 'SVT',
 'SVVC', 'SVXY', 'SWAG', 'SWAN', 'SWAR', 'SWAV', 'SWBI', 'SWEB', 'SWI', 'SWIM', 'SWK', 'SWKH', 'SWKS', 'SWN', 'SWSS', 'SWSSU', 'SWTX', 'SWVL', 'SWX', 'SWZ', 'SXC', 'SXI', 'SXQG', 'SXT', 'SXTC', 'SXUS', 'SY',
 'SYBT', 'SYBX', 'SYF', 'SYK', 'SYLD', 'SYM', 'SYNA', 'SYNH', 'SYPR', 'SYRS', 'SYTA', 'SYUS', 'SYY', 'SZK', 'SZNE', 'SZZL', 'SZZLU', 'T', 'TA', 'TAC', 'TACK', 'TACT', 'TAGG', 'TAGS', 'TAIL', 'TAIT', 'TAK',
 'TAL', 'TALK', 'TALO', 'TALS', 'TAN', 'TANH', 'TANNI', 'TANNL', 'TANNZ', 'TAOP', 'TAP', 'TARA', 'TARK', 'TARO', 'TARS', 'TASK', 'TAST', 'TATT', 'TAXF', 'TAYD', 'TBB', 'TBBK', 'TBC', 'TBCP', 'TBCPU', 'TBF',
 'TBI', 'TBJL', 'TBLA', 'TBLD', 'TBLT', 'TBNK', 'TBPH', 'TBSA', 'TBSAU', 'TBT', 'TBUX', 'TBX', 'TC', 'TCBC', 'TCBI', 'TCBIO', 'TCBK', 'TCBP', 'TCBS', 'TCBX', 'TCFC', 'TCHI', 'TCHP', 'TCI', 'TCMD', 'TCN',
 'TCOA', 'TCOM', 'TCON', 'TCPC', 'TCRR', 'TCRT', 'TCRX', 'TCS', 'TCVA', 'TCX', 'TD', 'TDC', 'TDCX', 'TDF', 'TDG', 'TDIV', 'TDOC', 'TDS', 'TDSA', 'TDSB', 'TDSC', 'TDSD', 'TDSE', 'TDTF', 'TDTT', 'TDUP', 'TDV',
 'TDVG', 'TDW', 'TDY', 'TEAF', 'TEAM', 'TECB', 'TECH', 'TECK', 'TECL', 'TECS', 'TECTP', 'TEDU', 'TEF', 'TEI', 'TEL', 'TELA', 'TELL', 'TELZ', 'TEMP', 'TENB', 'TENX', 'TEO', 'TEQI', 'TER', 'TERN', 'TESS',
 'TETC', 'TETCU', 'TETE', 'TETEU', 'TEVA', 'TEX', 'TFC', 'TFFP', 'TFI', 'TFII', 'TFJL', 'TFLO', 'TFSA', 'TFSL', 'TFX', 'TG', 'TGAA', 'TGAAU', 'TGAN', 'TGB', 'TGH', 'TGI', 'TGIF', 'TGLS', 'TGNA', 'TGR',
 'TGRW', 'TGS', 'TGT', 'TGTX', 'TGVC', 'TGVCU', 'TH', 'THC', 'THCP', 'THCPU', 'THCX', 'THD', 'THFF', 'THG', 'THM', 'THMO', 'THNQ', 'THO', 'THQ', 'THR', 'THRM', 'THRN', 'THRX', 'THRY', 'THS', 'THTX', 'THW',
 'THY', 'TIG', 'TIGO', 'TIGR', 'TIL', 'TILE', 'TILL', 'TILT', 'TIMB', 'TIME', 'TINT', 'TINY', 'TIOA', 'TIP', 'TIPD', 'TIPL', 'TIPT', 'TIPX', 'TIPZ', 'TIRX', 'TISI', 'TITN', 'TIVC', 'TIXT', 'TJX', 'TK',
 'TKAT', 'TKC', 'TKLF', 'TKNO', 'TKR', 'TLGA', 'TLGY', 'TLGYU', 'TLH', 'TLIS', 'TLK', 'TLRY', 'TLS', 'TLSA', 'TLT', 'TLTD', 'TLTE', 'TLYS', 'TM', 'TMAT', 'TMBR', 'TMC', 'TMCI', 'TMDI', 'TMDV', 'TMDX',
 'TME', 'TMF', 'TMFC', 'TMFE', 'TMFG', 'TMFM', 'TMFS', 'TMFX', 'TMHC', 'TMKR', 'TMKRU', 'TMO', 'TMP', 'TMQ', 'TMST', 'TMUS', 'TMV', 'TNA', 'TNC', 'TNDM', 'TNET', 'TNGX', 'TNK', 'TNL', 'TNON', 'TNP', 'TNXP',
 'TNYA', 'TOAC', 'TOACU', 'TOI', 'TOK', 'TOKE', 'TOL', 'TOLZ', 'TOMZ', 'TOP', 'TOPS', 'TOST', 'TOTL', 'TOTR', 'TOUR', 'TOWN', 'TPB', 'TPC', 'TPG', 'TPH', 'TPHD', 'TPHE', 'TPHS', 'TPIC', 'TPIF', 'TPL', 'TPLC',
 'TPLE', 'TPOR', 'TPR', 'TPSC', 'TPST', 'TPTA', 'TPVG', 'TPX', 'TPYP', 'TPZ', 'TQQQ', 'TR', 'TRAQ', 'TRC', 'TRCA', 'TRDA', 'TREE', 'TREX', 'TRFM', 'TRGP', 'TRHC', 'TRI', 'TRIB', 'TRIN', 'TRIP', 'TRIS', 'TRKA',
 'TRMB', 'TRMD', 'TRMK', 'TRMR', 'TRN', 'TRND', 'TRNO', 'TRNS', 'TRON', 'TRONU', 'TROO', 'TROW', 'TROX', 'TRP', 'TRPL', 'TRS', 'TRST', 'TRT', 'TRTL', 'TRTN', 'TRTX', 'TRTY', 'TRU', 'TRUE', 'TRUP', 'TRV', 'TRVG',
 'TRVI', 'TRVN', 'TRX', 'TS', 'TSAT', 'TSBK', 'TSCO', 'TSE', 'TSEM', 'TSHA', 'TSI', 'TSJA', 'TSLA', 'TSLQ', 'TSLX', 'TSM', 'TSN', 'TSOC', 'TSP', 'TSPA', 'TSQ', 'TSRI', 'TSVT', 'TT', 'TTAC', 'TTAI', 'TTC', 'TTCF',
 'TTD', 'TTE', 'TTEC', 'TTEK', 'TTGT', 'TTI', 'TTMI', 'TTNP', 'TTOO', 'TTP', 'TTSH', 'TTT', 'TTWO', 'TU', 'TUG', 'TUGN', 'TUP', 'TUR', 'TURN', 'TUSK', 'TUYA', 'TV', 'TVC', 'TVE', 'TVTX', 'TW', 'TWCB', 'TWCBU',
 'TWI', 'TWIN', 'TWIO', 'TWKS', 'TWLO', 'TWLV', 'TWLVU', 'TWM', 'TWN', 'TWNI', 'TWNK', 'TWO', 'TWOA', 'TWOU', 'TWST', 'TX', 'TXG', 'TXMD', 'TXN', 'TXRH', 'TXT', 'TY', 'TYA', 'TYD', 'TYDE', 'TYG', 'TYL', 'TYO',
 'TYRA', 'TZA', 'TZOO', 'U', 'UA', 'UAA', 'UAE', 'UAL', 'UAMY', 'UAN', 'UAPR', 'UAUG', 'UAV', 'UAVS', 'UBA', 'UBCP', 'UBER', 'UBFO', 'UBOT', 'UBP', 'UBR', 'UBS', 'UBSI', 'UBT', 'UBX', 'UCBI', 'UCBIO', 'UCC',
 'UCIB', 'UCL', 'UCO', 'UCON', 'UCTT', 'UCYB', 'UDEC', 'UDMY', 'UDN', 'UDOW', 'UDR', 'UE', 'UEC', 'UEIC', 'UEVM', 'UFAB', 'UFCS', 'UFEB', 'UFI', 'UFO', 'UFPI', 'UFPT', 'UG', 'UGA', 'UGE', 'UGI', 'UGIC', 'UGL',
 'UGP', 'UGRO', 'UHAL', 'UHS', 'UHT', 'UI', 'UIHC', 'UIS', 'UITB', 'UIVM', 'UJAN', 'UJB', 'UJUL', 'UJUN', 'UK', 'UL', 'ULBI', 'ULCC', 'ULE', 'ULH', 'ULST', 'ULTA', 'ULTR', 'ULVM', 'UMAR', 'UMAY', 'UMBF', 'UMC',
 'UMDD', 'UMH', 'UMI', 'UMMA', 'UNAM', 'UNB', 'UNCY', 'UNF', 'UNFI', 'UNG', 'UNH', 'UNIT', 'UNL', 'UNM', 'UNMA', 'UNOV', 'UNP', 'UNTY', 'UNVR', 'UOCT', 'UONE', 'UONEK', 'UP', 'UPAR', 'UPC', 'UPH', 'UPLD', 'UPRO',
 'UPS', 'UPST', 'UPTD', 'UPTDU', 'UPV', 'UPW', 'UPWK', 'URA', 'URBN', 'URE', 'URG', 'URGN', 'URI', 'URNM', 'UROY', 'URTH', 'URTY', 'USA', 'USAC', 'USAI', 'USAP', 'USAS', 'USAU', 'USB', 'USCB', 'USCI', 'USCT', 'USCTU',
 'USD', 'USDP', 'USDU', 'USEA', 'USEG', 'USEP', 'USEQ', 'USFD', 'USFR', 'USHY', 'USIG', 'USIO', 'USL', 'USLB', 'USLM', 'USM', 'USMC', 'USMF', 'USML', 'USMV', 'USNA', 'USNZ', 'USO', 'USOI', 'USPH', 'USRT', 'USSG',
 'UST', 'USTB', 'USVM', 'USVT', 'USX', 'USXF', 'UTAA', 'UTAAU', 'UTES', 'UTF', 'UTG', 'UTHR', 'UTI', 'UTL', 'UTMD', 'UTME', 'UTRN', 'UTRS', 'UTSI', 'UTSL', 'UTZ', 'UUP', 'UUU', 'UUUU', 'UVDV', 'UVE', 'UVIX',
 'UVSP', 'UVV', 'UVXY', 'UWM', 'UWMC', 'UXI', 'UXIN', 'UYG', 'UYM', 'UZD', 'UZE', 'UZF', 'V', 'VABK', 'VABS', 'VAC', 'VACC', 'VAL', 'VALE', 'VALN', 'VALQ', 'VALT', 'VALU', 'VAMO', 'VAPO', 'VAQC', 'VATE',
 'VAW', 'VAXX', 'VB', 'VBF', 'VBFC', 'VBIV', 'VBK', 'VBLT', 'VBND', 'VBNK', 'VBOC', 'VBOCU', 'VBR', 'VBTX', 'VC', 'VCAR', 'VCEB', 'VCEL', 'VCIF', 'VCIT', 'VCLN', 'VCLO', 'VCLT', 'VCNX', 'VCR', 'VCSA', 'VCSH',
 'VCTR', 'VCV', 'VCXA', 'VCXAU', 'VCXB', 'VCYT', 'VDC', 'VDE', 'VDNI', 'VEA', 'VECO', 'VECT', 'VEDU', 'VEEE', 'VEEV', 'VEGA', 'VEGI', 'VEGN', 'VEL', 'VEON', 'VERA', 'VERB', 'VERI', 'VERO', 'VERS', 'VERU',
 'VERV', 'VERX', 'VERY', 'VET', 'VEU', 'VEV', 'VFC', 'VFF', 'VFH', 'VFL', 'VFMF', 'VFMO', 'VFMV', 'VFQY', 'VFVA', 'VGI', 'VGIT', 'VGK', 'VGLT', 'VGM', 'VGR', 'VGSH', 'VGT', 'VGZ', 'VHAQ', 'VHC', 'VHI', 'VHNA',
 'VHT', 'VIA', 'VIAO', 'VIASP', 'VIAV', 'VICE', 'VICI', 'VICR', 'VIDI', 'VIEW', 'VIG', 'VIGI', 'VIGL', 'VII', 'VINC', 'VINE', 'VINO', 'VINP', 'VIOG', 'VIOO', 'VIOT', 'VIOV', 'VIPS', 'VIR', 'VIRC', 'VIRI',
 'VIRS', 'VIRT', 'VIRX', 'VIS', 'VISL', 'VIST', 'VITL', 'VIV', 'VIVK', 'VIXM', 'VIXY', 'VJET', 'VKI', 'VKQ', 'VKTX', 'VLAT', 'VLATU', 'VLCN', 'VLD', 'VLGEA', 'VLN', 'VLO', 'VLON', 'VLRS', 'VLT', 'VLTA', 'VLU',
 'VLUE', 'VLY', 'VLYPO', 'VLYPP', 'VMAR', 'VMBS', 'VMC', 'VMCA', 'VMCAU', 'VMD', 'VMEO', 'VMGA', 'VMGAU', 'VMI', 'VMO', 'VMOT', 'VMW', 'VNAM', 'VNCE', 'VNDA', 'VNET', 'VNLA', 'VNM', 'VNO', 'VNOM', 'VNQ',
 'VNQI', 'VNRX', 'VNSE', 'VNT', 'VNTR', 'VO', 'VOC', 'VOD', 'VOE', 'VONE', 'VONG', 'VONV', 'VOO', 'VOOG', 'VOOV', 'VOR', 'VORB', 'VOT', 'VOTE', 'VOX', 'VOXX', 'VOYA', 'VPC', 'VPCB', 'VPCBU', 'VPG', 'VPL',
 'VPN', 'VPU', 'VPV', 'VQS', 'VR', 'VRA', 'VRAI', 'VRAR', 'VRAY', 'VRCA', 'VRDN', 'VRE', 'VREX', 'VRIG', 'VRM', 'VRME', 'VRNA', 'VRNS', 'VRNT', 'VRP', 'VRPX', 'VRRM', 'VRSK', 'VRSN', 'VRT', 'VRTS', 'VRTV',
 'VRTX', 'VS', 'VSAC', 'VSACU', 'VSAT', 'VSCO', 'VSDA', 'VSEC', 'VSGX', 'VSH', 'VSLU', 'VSMV', 'VSS', 'VST', 'VSTA', 'VSTM', 'VSTO', 'VT', 'VTC', 'VTEB', 'VTEX', 'VTGN', 'VTHR', 'VTI', 'VTIP', 'VTN', 'VTNR',
 'VTOL', 'VTR', 'VTRS', 'VTRU', 'VTSI', 'VTV', 'VTVT', 'VTWG', 'VTWO', 'VTWV', 'VTYX', 'VUG', 'VUSB', 'VUSE', 'VUZI', 'VV', 'VVI', 'VVNT', 'VVOS', 'VVPR', 'VVR', 'VVV', 'VVX', 'VWE', 'VWID', 'VWO', 'VWOB', 'VXF',
 'VXRT', 'VXUS', 'VXX', 'VXZ', 'VYGR', 'VYM', 'VYMI', 'VYNE', 'VYNT', 'VZ', 'VZIO', 'VZLA', 'W', 'WAB', 'WABC', 'WAFD', 'WAFDP', 'WAFU', 'WAL', 'WALD', 'WANT', 'WASH', 'WAT', 'WATT', 'WAVC', 'WAVD', 'WAVE', 'WAVS',
 'WAVSU', 'WB', 'WBA', 'WBAT', 'WBD', 'WBIF', 'WBIG', 'WBIL', 'WBIY', 'WBND', 'WBS', 'WBX', 'WCBR', 'WCC', 'WCLD', 'WCN', 'WD', 'WDAY', 'WDC', 'WDFC', 'WDH', 'WDI', 'WDIV', 'WDNA', 'WDS', 'WE', 'WEA', 'WEAT',
 'WEAV', 'WEBL', 'WEBS', 'WEC', 'WEED', 'WEJO', 'WEL', 'WELL', 'WEN', 'WERN', 'WES', 'WETG', 'WEX', 'WEYS', 'WF', 'WFC', 'WFCF', 'WFG', 'WFH', 'WFHY', 'WFIG', 'WFRD', 'WGMI', 'WGO', 'WGRO', 'WH', 'WHD', 'WHF',
 'WHG', 'WHLM', 'WHLR', 'WHLRD', 'WHLRL', 'WHLRP', 'WHR', 'WIA', 'WILC', 'WIMI', 'WINA', 'WINC', 'WING', 'WINN', 'WINT', 'WINV', 'WINVR', 'WINVU', 'WIP', 'WIRE', 'WISA', 'WISH', 'WIT', 'WIW', 'WIX', 'WIZ', 'WK',
 'WKEY', 'WKHS', 'WKLY', 'WKME', 'WKSP', 'WLDN', 'WLDR', 'WLFC', 'WLK', 'WLKP', 'WLMS', 'WLTG', 'WLTH', 'WLY', 'WLYB', 'WM', 'WMB', 'WMC', 'WMG', 'WMK', 'WMPN', 'WMS', 'WMT', 'WNC', 'WNDY', 'WNEB', 'WNNR', 'WNS',
 'WNW', 'WOLF', 'WOMN', 'WOOD', 'WOOF', 'WOR', 'WORX', 'WOW', 'WPC', 'WPCA', 'WPCB', 'WPM', 'WPP', 'WPRT', 'WPS', 'WRAC', 'WRAP', 'WRB', 'WRBY', 'WRK', 'WRLD', 'WRN', 'WSBC', 'WSBCP', 'WSBF', 'WSC', 'WSFS', 'WSM',
 'WSO', 'WSR', 'WST', 'WTAI', 'WTBA', 'WTER', 'WTFC', 'WTFCM', 'WTFCP', 'WTI', 'WTM', 'WTMA', 'WTMAR', 'WTMAU', 'WTMF', 'WTRE', 'WTRG', 'WTS', 'WTT', 'WTTR', 'WTV', 'WTW', 'WU', 'WUGI', 'WULF', 'WVE', 'WVVI',
 'WVVIP', 'WW', 'WWAC', 'WWACU', 'WWD', 'WWE', 'WWJD', 'WWR', 'WWW', 'WY', 'WYNN', 'WYY', 'X', 'XAIR', 'XAR', 'XB', 'XBAP', 'XBB', 'XBI', 'XBIO', 'XBIT', 'XBJA', 'XBJL', 'XBOC', 'XBTF', 'XCCC', 'XCEM', 'XCLR',
 'XCUR', 'XDAP', 'XDAT', 'XDEC', 'XDJA', 'XDJL', 'XDNA', 'XDOC', 'XDQQ', 'XDSQ', 'XEL', 'XELA', 'XELAP', 'XELB', 'XENE', 'XERS', 'XES', 'XFIN', 'XFINU', 'XFLT', 'XFOR', 'XGN', 'XHB', 'XHE', 'XHR', 'XHS', 'XHYC',
 'XHYD', 'XHYE', 'XHYF', 'XHYH', 'XHYI', 'XHYT', 'XIN', 'XITK', 'XJH', 'XJR', 'XJUN', 'XLB', 'XLC', 'XLE', 'XLF', 'XLG', 'XLI', 'XLK', 'XLO', 'XLP', 'XLRE', 'XLSR', 'XLU', 'XLV', 'XLY', 'XM', 'XME', 'XMHQ', 'XMLV',
 'XMMO', 'XMPT', 'XMTR', 'XMVM', 'XNCR', 'XNET', 'XNTK', 'XOM', 'XOMA', 'XOMAO', 'XOMAP', 'XOP', 'XOS', 'XOUT', 'XP', 'XPAX', 'XPDB', 'XPDBU', 'XPEL', 'XPER', 'XPEV', 'XPH', 'XPL', 'XPND', 'XPO', 'XPOF', 'XPON',
 'XPP', 'XPRO', 'XRAY', 'XRLV', 'XRMI', 'XRT', 'XRTX', 'XRX', 'XSD', 'XSHD', 'XSHQ', 'XSLV', 'XSMO', 'XSOE', 'XSVM', 'XSW', 'XT', 'XTAP', 'XTJA', 'XTJL', 'XTL', 'XTLB', 'XTN', 'XTNT', 'XTOC', 'XTR', 'XVOL', 'XVV',
 'XWEB', 'XXII', 'XYF', 'XYL', 'XYLD', 'XYLG', 'YALA', 'YANG', 'YCBD', 'YCL', 'YCS', 'YDEC', 'YELL', 'YELP', 'YETI', 'YEXT', 'YGMZ', 'YI', 'YINN', 'YJ', 'YJUN', 'YLD', 'YLDE', 'YMAB', 'YMAR', 'YMM', 'YOLO', 'YORW',
 'YOTA', 'YOTAR', 'YOU', 'YPF', 'YPS', 'YQ', 'YRD', 'YSEP', 'YSG', 'YTEN', 'YTPG', 'YTRA', 'YUM', 'YUMC', 'YUMY', 'YVR', 'YXI', 'YY', 'YYY', 'Z', 'ZBH', 'ZBRA', 'ZCMD', 'ZD', 'ZDGE', 'ZECP', 'ZENV', 'ZEPP', 'ZEST',
 'ZETA', 'ZEUS', 'ZEV', 'ZG', 'ZGEN', 'ZGN', 'ZH', 'ZHDG', 'ZI', 'ZIG', 'ZIM', 'ZIMV', 'ZING', 'ZION', 'ZIONL', 'ZIONO', 'ZIONP', 'ZIP', 'ZIVO', 'ZKIN', 'ZLAB', 'ZM', 'ZNTL', 'ZOM', 'ZROZ', 'ZS', 'ZSL', 'ZT',
 'ZTEK', 'ZTO', 'ZTR', 'ZTS', 'ZUMZ', 'ZUO', 'ZVIA', 'ZWS', 'ZYME', 'ZYNE', 'ZYXI']

#minute = [15,20,25,30,35,40,45,50,55,75,90,105,135,150,165,195,210,225,255,270,285,315,330,345,375,390,405,435,450,465,495,510,525,555,570,585]
for data in databaxA:
    ticker = f'{data}'
    #liste_date=['05-20', '05-21', '05-22', '05-23', '05-24', '05-25', '05-26', '05-27', '05-28', '05-29', '05-30', '05-31', '06-01', '06-02', '06-03', '06-04', '06-05', '06-06', '06-07', '06-08', '06-09', '06-10', '06-11', '06-12', '06-13', '06-14', '06-15', '06-16', '06-17', '06-18', '06-19', '06-20', '06-21', '06-22', '06-23', '06-24', '06-25', '06-26', '06-27', '06-28', '06-29', '06-30', '07-01', '07-02', '07-03', '07-04', '07-05', '07-06', '07-07', '07-08', '07-09', '07-10', '07-11', '07-12', '07-13', '07-14', '07-15', '07-16', '07-17']
    liste_date = ['01-01']
    #liste_date=['01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07', '01-08', '01-09', '01-10', '01-11', '01-12', '01-13', '01-14', '01-15', '01-16', '01-17', '01-18', '01-19', '01-20', '01-21', '01-22', '01-23', '01-24', '01-25', '01-26', '01-27', '01-28', '01-29', '01-30', '01-31', '02-01', '02-02', '02-03', '02-04', '02-05', '02-06', '02-07', '02-08', '02-09', '02-10', '02-11', '02-12', '02-13', '02-14', '02-15', '02-16', '02-17', '02-18', '02-19', '02-20', '02-21', '02-22', '02-23', '02-24', '02-25', '02-26', '02-27', '02-28', '03-01', '03-02', '03-03', '03-04', '03-05', '03-06', '03-07', '03-08', '03-09', '03-10', '03-11', '03-12', '03-13', '03-14', '03-15', '03-16', '03-17', '03-18', '03-19', '03-20', '03-21', '03-22', '03-23', '03-24', '03-25', '03-26', '03-27', '03-28', '03-29', '03-30', '03-31', '04-01', '04-02', '04-03', '04-04', '04-05', '04-06', '04-07', '04-08', '04-09', '04-10', '04-11', '04-12', '04-13', '04-14', '04-15', '04-16', '04-17', '04-18', '04-19', '04-20', '04-21', '04-22', '04-23', '04-24', '04-25', '04-26', '04-27', '04-28', '04-29', '04-30', '05-01', '05-02', '05-03', '05-04', '05-05', '05-06', '05-07', '05-08', '05-09', '05-10', '05-11', '05-12', '05-13', '05-14', '05-15', '05-16', '05-17', '05-18', '05-19', '05-20', '05-21', '05-22', '05-23', '05-24', '05-25', '05-26', '05-27', '05-28', '05-29', '05-30', '05-31', '06-01', '06-02', '06-03', '06-04', '06-05', '06-06', '06-07', '06-08', '06-09', '06-10', '06-11', '06-12', '06-13', '06-14', '06-15', '06-16', '06-17', '06-18', '06-19', '06-20', '06-21', '06-22', '06-23', '06-24', '06-25', '06-26', '06-27', '06-28', '06-29', '06-30', '07-01', '07-02', '07-03', '07-04', '07-05', '07-06', '07-07', '07-08', '07-09', '07-10', '07-11', '07-12', '07-13', '07-14', '07-15', '07-16', '07-17', '07-18', '07-19', '07-20', '07-21', '07-22', '07-23', '07-24', '07-25', '07-26', '07-27', '07-28', '07-29', '07-30', '07-31', '08-01', '08-02', '08-03', '08-04', '08-05', '08-06', '08-07', '08-08', '08-09', '08-10', '08-11', '08-12', '08-13', '08-14', '08-15', '08-16', '08-17', '08-18', '08-19', '08-20', '08-21', '08-22', '08-23', '08-24', '08-25', '08-26', '08-27', '08-28', '08-29', '08-30', '08-31', '09-01', '09-02', '09-03', '09-04', '09-05', '09-06', '09-07', '09-08', '09-09', '09-10', '09-11', '09-12', '09-13', '09-14', '09-15', '09-16', '09-17', '09-18', '09-19', '09-20', '09-21', '09-22', '09-23', '09-24', '09-25', '09-26', '09-27', '09-28', '09-29', '09-30']
    for date in liste_date :
        th1 = Process(target=Finder_IETE, args=(15,"minute",f'2023-{date}','2023-10-03',f'2023-{date}',TETE,'A'))
        th2 = Process(target=Finder_IETE,args=(20, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'B'))
        th3 = Process(target=Finder_IETE,args=(25, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'C'))
        th4 = Process(target=Finder_IETE,args=(30, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'D'))
        th5 = Process(target=Finder_IETE,args=(35, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'E'))
        th6 = Process(target=Finder_IETE,args=(40, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'F'))
        th7 = Process(target=Finder_IETE,args=(45, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'G'))
        th8 = Process(target=Finder_IETE,args=(50, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'H'))
        th9 = Process(target=Finder_IETE,args=(55, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'I'))
        th10 = Process(target=Finder_IETE,args=(75, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'J'))
        th11 = Process(target=Finder_IETE,args=(90, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'K'))
        th12 = Process(target=Finder_IETE,args=(105, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'L'))
        th13 = Process(target=Finder_IETE,args=(135, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'M'))
        th14 = Process(target=Finder_IETE,args=(150, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'N'))
        th15 = Process(target=Finder_IETE,args=(165, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'O'))
        th16 = Process(target=Finder_IETE,args=(195, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'P'))
        th17 = Process(target=Finder_IETE,args=(210, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'Q'))
        th18 = Process(target=Finder_IETE,args=(225, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'R'))
        th19 = Process(target=Finder_IETE,args=(255, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'S'))
        th20 = Process(target=Finder_IETE,args=(270, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'T'))
        th21 = Process(target=Finder_IETE,args=(285, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'U'))
        th22 = Process(target=Finder_IETE,args=(315, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'V'))
        th23 = Process(target=Finder_IETE,args=(330, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'W'))
        th24 = Process(target=Finder_IETE,args=(345, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'X'))
        th25 = Process(target=Finder_IETE,args=(375, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'Y'))
        th26 = Process(target=Finder_IETE,args=(390, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'Z'))
        th27 = Process(target=Finder_IETE,args=(405, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'AA'))
        th28 = Process(target=Finder_IETE,args=(435, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'BB'))
        th29 = Process(target=Finder_IETE,args=(450, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'CC'))
        th30 = Process(target=Finder_IETE,args=(465, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'DD'))
        th31 = Process(target=Finder_IETE,args=(495, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'EE'))
        th32 = Process(target=Finder_IETE,args=(510, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'FF'))
        th33 = Process(target=Finder_IETE,args=(525, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'GG'))
        th34 = Process(target=Finder_IETE,args=(555, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'HH'))
        th35 = Process(target=Finder_IETE,args=(570, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'II'))
        th36 = Process(target=Finder_IETE,args=(585, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'JJ'))

        th1.start()
        th2.start()
        th3.start()
        th4.start()
        th5.start()
        th6.start()
        th7.start()
        th8.start()
        th9.start()
        th10.start()
        th11.start()
        th12.start()
        th13.start()
        th14.start()
        th15.start()
        th16.start()
        th17.start()
        th18.start()
        th19.start()
        th20.start()
        th21.start()
        th22.start()
        th23.start()
        th24.start()
        th25.start()
        th26.start()
        th27.start()
        th28.start()
        th29.start()
        th30.start()
        th31.start()
        th32.start()
        th33.start()
        th34.start()
        th35.start()
        th36.start()


        th1.join()
        th2.join()
        th3.join()
        th4.join()
        th5.join()
        th6.join()
        th7.join()
        th8.join()
        th9.join()
        th10.join()
        th11.join()
        th12.join()
        th13.join()
        th14.join()
        th15.join()
        th16.join()
        th17.join()
        th18.join()
        th19.join()
        th20.join()
        th21.join()
        th22.join()
        th23.join()
        th24.join()
        th25.join()
        th26.join()
        th27.join()
        th28.join()
        th29.join()
        th30.join()
        th31.join()
        th32.join()
        th33.join()
        th34.join()
        th35.join()
        th36.join()
















