from math import sqrt
from os import stat
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics as stats
from scipy.stats import mannwhitneyu

def read_cs(file_name):
    return pd.read_csv(file_name,index_col = None)

def description(nr):
    if nr == 0:
        print("""
        id -> identyfikator
        date -> data sprzedazy dzialki
        price -> cena podana w dolarach
        bedrooms -> ilosc sypialni w domu
        bathrooms -> ilosc lazienek w domu
        sqft_living -> powierzchnia domu w stopach kwadratowych
        sqft_lot -> powierzchnia calkowita
        floors -> ilość pięter w domu
        waterfront -> czy dom ma widok na wode
        view -> ilość osob ktore oglądały dom przed kupnem, z powodu niejasności skąd pochodzą dane te kolumnę pominę dla bezpieczeństwa
        condition -> nadawana na podstawie stponia 'grade' i roku zbudowania oznacza jak 'długo' dom wytrzyma bez remontu
        grade -> stopien nadawany na podsatwie uzytych mateirałów , im wyższy tym lepsze materiały zostały użyte
        sqft_above -> powierzchnia górnych kondygnacji
        sqft_basement -> powierzchnia piwnicy
        yr_built -> rok zbudowania
        yr_renovated -> rok remontu
        zipcode -> kod pocztowy
        lat -> szerokogsc geograficzna
        long -> dlogosc geograficzna
        sqft_living15 -> srednia powierzchnia w obrębie 15 domow
        sqft_lot15 -> srednia powierzchnia calkkowita 15 najbliższych działek 
                """)
def oblicz_bin(df):
    range = df.max() - df.min()
    n = len(df)
    std = df.std()
    return round(range * np.cbrt(n)/(3.49*std),0)

def test_z(df,year):
    cena = df[df["yr_built"] == year]["price"]
    cena_srednia = round(cena.mean(),2)
    H0 = cena_srednia - 5000
    print("\nZaobserwowano że srednia cena domów do roku: {} wynosiła: {}.".format(year,cena_srednia))
    print("czy w takim takkim razie można twierdzić że średnia wynosi {}".format(H0))
    print("poziom istotności w tym teście wynosi 0.01\n")
    alfa = 0.01
    crit_value = round(2.326347874,3)
    licznosc = len(cena)
    odchylenie_std = cena.std()
    wartosc_statystyki = round((cena_srednia - H0)/odchylenie_std*sqrt(licznosc),3)
    print("wartosc statystyki, otrzymana przy wykorzystaniu testu Z wynosi: {}".format(wartosc_statystyki))
    if(wartosc_statystyki > crit_value):
        print("odrzucamy hipoteze zerowa, poniewaz znajduje sie ona w obszarze krytycznym ktry wynosi: {}".format(crit_value))
    else:
        print("przyjmujemy hipoteze zerowa, poniewaz nie znajduje sie ona w obszarze krytycznym ktory wynosi: {}".format(crit_value))

def korelacja(b_1975,a_1975,mediana):
    korelacja_przed = np.corrcoef(b_1975["price"],b_1975["sqft_living"])
    korelacja_po = np.corrcoef(a_1975["price"],a_1975["sqft_living"])
    print("Korelacja ceny do 'sqft_living', przed rokiem 1975:\n",korelacja_przed[0][1],"\nKorelacja ceny do 'sqft_living', po roku 1975:\n",korelacja_po[0][1])
    print("mozna zauwazyc ze korelacja ceny domow do ich wielkosci wzrosla po roku {}".format(mediana))

def test_MannWhitney(df,year1 = 1975,year2 = 2000):
    print("\nNie wiadomo czy nasze dane posiadaj rozklad normalny.")
    print("Chcemy sprawdzic czy rozklad cen domow zbudowanych w roku {} jest rowny rozkladowi domow zbudowanych w {}.".format(year1,year2))
    print("Aby to sprawdzic nalezy zastosowac test nieparametryczny, w tym przypadku zastosowalem test U Manna-Whittneya.")
    print("Sprawdzimy czy rozklady sa sobie rowne.")
    alpha = 0.05
    sample1 = df[df["yr_built"] == year1]["price"]
    sample2 = df[df["yr_built"] == year2]["price"]

    stat,p = mannwhitneyu(sample1,sample2)
    if p > alpha:
        print("Takie same dystrybuant, nie mozna odrzucic hipotezy zerowej\n")
    else:
        print("rozne dystrybuanty, nalezy odrzucic hipoteze zerowa\n")

    fig3,axa3 = plt.subplots(1,2,sharey=True)
    axa3[0].hist(sample1,bins=int(oblicz_bin(sample1)))
    axa3[1].hist(sample2,bins=int(oblicz_bin(sample2)))
    axa3[0].set_xlabel("Price")
    axa3[1].set_xlabel("Price")
    axa3[0].set_ylabel("Count")
    axa3[0].set_title("{}".format(year1))
    axa3[1].set_title("{}".format(year2))
    plt.show()
#Source od Data:
#https://www.kaggle.com/swathiachath/kc-housesales-data/data
print("EKSPLORACJA DANYCH:")
print("Będę analizował dane dotyczące domów w king County w USA\n"
      "Opis kolumn wraz z kilkoma pierwszymi wierszami znajduje sie ponizej.\n")

dataframe = read_cs('kc_house_data.csv')
pd.set_option('display.max_columns',None)
columns = list(dataframe)
print(columns,"\n")
print(dataframe.head(3))
description(0)
print("\nNie będę analizwoal kolumn 'DATE','ZIPCODE','LAT','LONG',ponieważ nie stanowią one mojego zainteresowania.")
dataframe.drop(['date','zipcode','lat','long'],axis="columns",inplace=True)

print("obliczamy statystyki opisowe")
print(dataframe.describe().loc[["min","max","mean","std","25%","50%","75%"]],"\n")


fig,axa = plt.subplots(1,1)
axa.boxplot(dataframe["price"])
axa.set_title("Box plot of prices")
axa.set_ylabel("Value")

fig1,axa1 = plt.subplots(1,1)
axa1.hist(dataframe["price"],bins=int(oblicz_bin(dataframe["price"])),color="red")
axa1.set_ylabel("Count")
axa1.set_xlabel("Value")
axa1.set_title("Distribution of prices")
plt.show()

mediana_lat = dataframe["yr_built"].median()
print("mediana wynosi roku budowy wynosi {}. Z tego powodu bedziemy analizowac ceny domów sprzed oraz po roku {}\n".format(mediana_lat,mediana_lat))
before_1975 = dataframe[dataframe["yr_built"] < mediana_lat]
after_1975 = dataframe[dataframe["yr_built"] >= mediana_lat]
before_1975 = before_1975.sample(n=5000)
after_1975 = after_1975.sample(n=5000)
fig2,axa2 = plt.subplots(1,2,sharey=True)
axa2[0].hist(before_1975["price"],bins=int(oblicz_bin(before_1975["price"])))
axa2[1].hist(after_1975["price"],bins=int(oblicz_bin(after_1975["price"])))
plt.show()

korelacja(before_1975,after_1975,mediana_lat)
test_z(dataframe,mediana_lat)
test_MannWhitney(dataframe,1918,2014)