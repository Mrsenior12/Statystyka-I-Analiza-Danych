import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics as stats
from scipy import stats

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
    elif nr == 1:
        print("""
        Mediana wynosi 1975, z tego powodu zamierzam analizować cenę domów sprzed oraz po roku 1975
        """)
    elif nr == 2:
        print("""
        Można zauważyć że korelacja ceny do powierzchni domu wzrosła 
        """)
# funkcja ma za zadanie zrobienie szeregów rozdzielczych dla wsz
#Source od Data:
#https://www.kaggle.com/swathiachath/kc-housesales-data/d
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
#axa[0,0].hist(dataframe["price"],bins=20)
#axa[0,1].boxplot(dataframe["bedrooms"])
#axa[1,0].hist(dataframe["bathrooms"])
#axa[1,1].hist(dataframe["sqft_living"])
axa.boxplot(dataframe["price"])
axa.set_title("Box plot of prices")
axa.set_ylabel("Value")

fig1,axa1 = plt.subplots(1,1)
axa1.hist(dataframe["price"],bins=20,color="red")
axa1.set_ylabel("Count")
axa1.set_xlabel("Value")
axa1.set_title("Distribution of prices")
plt.show()

mediana = dataframe["yr_built"].median()
print(mediana)
description(1)
before_1975 = dataframe[dataframe["yr_built"] < 1975]
after_1975 = dataframe[dataframe["yr_built"] >= 1975]
before_1975 = before_1975.sample(n=5000)
after_1975 = after_1975.sample(n=5000)
fig2,axa2 = plt.subplots(1,2,sharey=True)
axa2[0].hist(before_1975["price"],bins=25)
axa2[1].hist(after_1975["price"],bins=25)
plt.show()

korelacja_przed = np.corrcoef(before_1975["price"],before_1975["sqft_living"])
korelacja_po = np.corrcoef(after_1975["price"],after_1975["sqft_living"])
print("Korelacja ceny do 'sqft_living', przed rokiem 1975:\n",korelacja_przed[0][1],"\nKorelacja ceny do 'sqft_living', po roku 1975:\n",korelacja_po[0][1])

#before_1975 = dataframe[(dataframe["yr_built"] < 1975 ) & (dataframe["yr_built"] >= 1965)]
#print(dataframe.iloc[:,1].head(3))
#print("Kolejnym krokiem, jest obliczenie statystyk opisowych.")
#print(dataframe.describe())
#intent = count_intent(dataframe)
#how_many_cases = len(dataframe["intent"])
#means = count_mean(intent,how_many_cases)

#suicides_firs_half = dataframe[(dataframe["intent"] == "Suicide") & (dataframe["month"] < 6)]
#suicides_second_half = dataframe[(dataframe["intent"] == "Suicide") & (dataframe["month"] >= 6)]

#nation = dataframe.groupby(["race"]).size()
#print(nation)
#fig,axa = plt.subplots(1,2)
#axa[0].hist(suicides_firs_half["month"],bins=6)
#axa[1].hist(suicides_second_half["month"],bins=6)

#axa[0].set_xlabel("miesiac")
#axa[0].set_ylabel("ilosc samobojstw")
#axa[1].set_xlabel("miesiac")

