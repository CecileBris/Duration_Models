# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 13:04:13 2021

@author: ceecy
"""

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
import re
import seaborn as sns
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
#; sns.set_theme()

dfS = pd.read_csv(r'C:\Users\ceecy\PythonScripts\Micro\SIP06.csv', sep=',', engine='python')
dfSdisco=dfS.head()
dfS.describe()
print(dfSdisco)

Nom_Var = dfS.columns

def var(nomvar,data):
    print(f"Nom de la variable : {nomvar}")
    print(f"Nombre de modalités : {data[nomvar].nunique()}")
    print(f"Vecteurs des modalités : {data[nomvar].unique()}")
    print(f"Counts en chaque modalités : {data[nomvar].value_counts()}")
    print(data[nomvar].describe())
    print(f"La colonne a {data[nomvar].isna().sum()}  valeur(s) manquante(s)")
    print(f"La variable admet donc {(data[nomvar].isna().sum()/len(data))*100} % de valeur(s) manquante(s)")

var(Nom_Var[1],dfS) #0% ; sexenq ; float

var(Nom_Var[2],dfS) #0% ; fpermer ; float

var(Nom_Var[3],dfS) #0% ; flnais ; float

var(Nom_Var[4],dfS) #8.16% ; 1114 ; fnaip ; float
#0 ? 2 moda : 1;2 et nan
dfS["fnaip"].fillna(0, inplace=True) #comme on a ouvert la table avec SAS il a replace les 0 par NAN donc normal

var(Nom_Var[5],dfS) #1.4% ; 192 ; fnaim ; float
#Médiane ou 0 ? 2 moda : 1;2 et nan
dfS["fnaim"].fillna(0, inplace=True) #idem

var(Nom_Var[6],dfS) #4.6% ; 632 ; fnivdip ; float
#Médiane ou 0 ? 2 moda : 1;2... à 8 et nan
dfS["fnivdip"].fillna(0, inplace=True) #idem

var(Nom_Var[7],dfS) #0% ; fhand ; float ; 2 moda 1;2

var(Nom_Var[8],dfS) #0% ; fmaldu ; float ; 2 moda 1;2

var(Nom_Var[9],dfS) #0% ; fsafa ; float ; 3 moda 1;2;3

var(Nom_Var[10],dfS) #0% ; fdec ; float ; 2 moda 1;2
 
var(Nom_Var[11],dfS) #0% ; fsep ; float ; 2 moda 1;2

var(Nom_Var[12],dfS) #0% ; fcofam ; float ; 2 moda 1;2

var(Nom_Var[13],dfS) #0% ; fdrog ; float ; 3 moda 2;3;1
#pourquoi 2 en prems ? à recoder ? Non c good comme ça 

var(Nom_Var[14],dfS) #0% ; fepr ; float ; 2 moda 1;2

var(Nom_Var[15],dfS) #0% ; fviopr ; float ; 2 moda 2;1

var(Nom_Var[16],dfS) #0% ; fgue ; float ; 2 moda 2;1

var(Nom_Var[17],dfS) #0% ; fsitua ; float ; 7 moda 1;2; ... 7

var(Nom_Var[18],dfS) #0% ; fnelev ; float ; 14 moda 1;2n...14

var(Nom_Var[19],dfS) #35.44% ; 4837 ; zremen ; float ; 2 moda 1;2
#qu'apporte t elle ?- SUPP ou Médiane / Moyenne ? 
dfS["zremen"].fillna(0, inplace=True)
#faire des tranches de revenu
#remplacer les -1 par la Médiane
#mettre des nan dans -1
def zremen(x):
    if x == -1 :
        return
    else : 
        return x
dfS['zremen'] = dfS['zremen'].apply(zremen)
#remplacer nan par la médiane
dfS['zremen'].fillna(dfS['zremen'].median(), inplace=True)

"""def zremen_(x):
    if x <= 565.34 and x != 0 : #entre 0 et le rsa/personne
        return 1
    elif x <= 1554.58 and x >= 565.34 and x != 0 : #entre le rsa et le smic/personne
        return 2
    elif x <= 1789 and x >= 1554.58 and x != 0 : #entre le smic et le salaire médian/personne
        return 3
    else : 
        if x != 0 : #tout ce qu'il y a au dessus
            return 4
        if x == 0 : #salaire = 0
            return 0
dfS['zremen'] = dfS['zremen'].apply(zremen_)"""

var(Nom_Var[20],dfS) #0% ; zben_1 ; float ; 2 moda 0;1

var(Nom_Var[21],dfS) #0% ; zsyn_1 ; float ; 2 moda 0;1

var(Nom_Var[22],dfS) #0% ; zpol_1 ; float ; 2 moda 0;1

var(Nom_Var[23],dfS) #0% ; zreli_1 ; float ; 2 moda 0;1

var(Nom_Var[24],dfS) #0% ; zspo_1 ; float ; 2 moda 0;1

var(Nom_Var[25],dfS) #0% ; zart_1 ; float ; 2 moda 0;1

var(Nom_Var[26],dfS) #0% ; sq1g ; float ; 5 moda 1;...5

var(Nom_Var[27],dfS) #0% ; sq2g ; float ; 2 moda 2;1

var(Nom_Var[28],dfS) #0% ; sq3g ; float ; 2 moda 2;1

var(Nom_Var[29],dfS) #96.62% ; 13187 ; eacap ; float ; 2 moda 
#trop de manquantes - SUPP - arrêt maladie 

#ordinal de 1 à 4 avec 4 le mieux (jamais)
var(Nom_Var[30],dfS) #39.02% ; 5326 ; eahsem ; float ; 5 moda 0; ...4 et nan 
#trop de manquantes - SUPP ?? - Médiane ? Recode ?
dfS[dfS['eahsem'].isna()] 
dfS["eahsem"].fillna(0, inplace=True)


var(Nom_Var[31],dfS) #39.02% ; 5326 ; eahsem ; float ; 5 moda 0; ...4 et nan 
#trop de manquantes - SUPP ?? - Médiane ? Recode ? - 0 sns rep - ordinal de 1 à 4 avec 4 le mieux (jamais)
dfS[dfS['eadepl'].isna()]
dfS["eadepl"].fillna(0, inplace=True)

var(Nom_Var[32],dfS) #39.02% ; 5326 ; eairre ; float ; 5 moda 0; ...4 et nan 
#trop de manquantes - SUPP ?? - Médiane ? Recode ?
dfS[dfS['eairre'].isna()]
dfS['eairre'].fillna(0, inplace=True)

var(Nom_Var[33],dfS) #39.02% ; 5326 ; eaexi ; float ; 5 moda 0; ...4 et nan 
#trop de manquantes - SUPP ?? - Médiane ? Recode ? - suppromer que les obsv
dfS[dfS['eaexi'].isna()]
dfS["eaexi"].fillna(0, inplace=True)

var(Nom_Var[34],dfS) #39.02% ; 5326 ; ealour ; float ; 5 moda 0; ...4 et nan 
#trop de manquantes - SUPP ?? - Médiane ? Recode ?
dfS[dfS['ealour'].isna()]
dfS["ealour"].fillna(0, inplace=True)

var(Nom_Var[35],dfS) #39.02% ; 5326 ; eabrui ; float ; 5 moda 0; ...4 et nan 
#trop de manquantes - SUPP ?? - Médiane ? Recode ?
dfS[dfS['eabrui'].isna()]
dfS["eabrui"].fillna(0, inplace=True)

var(Nom_Var[36],dfS) #39.02% ; 5326 ; eaenv ; float ; 5 moda 0; ...4 et nan 
#trop de manquantes - SUPP ?? - Médiane ? Recode ?
dfS[dfS['eaenv'].isna()]
dfS["eaenv"].fillna(0, inplace=True)

var(Nom_Var[37],dfS) #39.02% ; 5326 ; eacom ; float ; 5 moda 0; ...4 et nan 
#trop de manquantes - SUPP ?? - Médiane ? Recode ?
dfS[dfS['eacom'].isna()]
dfS["eacom"].fillna(0, inplace=True)

var(Nom_Var[38],dfS) #39.02% ; 5326 ; ealati ; float ; 5 moda 0; ...4 et nan 
#trop de manquantes - SUPP ?? - Médiane ? Recode ?
dfS[dfS['ealati'].isna()]
dfS["ealati"].fillna(0, inplace=True)

var(Nom_Var[39],dfS) #39.02% ; 5326 ; eahum ; float ; 5 moda 0; ...4 et nan 
#trop de manquantes - SUPP ?? - Médiane ? Recode ?
dfS[dfS['eahum'].isna()]
dfS["eahum"].fillna(0, inplace=True)

var(Nom_Var[40],dfS) #39.02% ; 5326 ; eapeur ; float ; 5 moda 0; ...4 et nan 
#trop de manquantes - SUPP ?? - Médiane ? Recode ?
dfS[dfS['eapeur'].isna()]
dfS["eapeur"].fillna(0, inplace=True)

var(Nom_Var[41],dfS) #39.02% ; 5326 ; eaethi ; float ; 5 moda 0; ...4 et nan 
#trop de manquantes - SUPP ?? - Médiane ? Recode ?
dfS[dfS['eaethi'].isna()]
dfS["eaethi"].fillna(0, inplace=True)

#pas d'emploi ; 5 pas de rep ; 1 à 4 souvent à jamais
var(Nom_Var[42],dfS) #39.02% ; 5326 ; eafam ; float ; 6 moda 0; ...5 et nan 
#trop de manquantes - SUPP ?? - Médiane ? Recode ? par 0 à différer de 5
dfS[dfS['eafam'].isna()]
dfS["eafam"].fillna(0, inplace=True)

var(Nom_Var[43],dfS) #39.02% ; 5326 ; eacol ; float ; 6 moda 0; ...5 et nan 
#trop de manquantes - SUPP ?? - Médiane ? Recode ? par 
dfS[dfS['eacol'].isna()]
dfS["eacol"].fillna(0, inplace=True)

#Pourcentage des périodes d’emplois longs dans l’itinéraire professionnel (nombre  d’années en emplois longs / durée de l’itinéraire professionnel) 
#si ya pas de valeur c qu'il manque les dates d'emploi - 0 ?
var(Nom_Var[44],dfS) #1.86% ; 254 ; elip ; float ; 94 moda 
#0? Médiane ? Recode ?
dfS["elip"].fillna(0, inplace=True)

var(Nom_Var[45],dfS) #0% ; agenq ; float ; 56 moda

var(Nom_Var[46],dfS) #0% ; EDM ; object ; 2 moda oui non à reco en 1;0
def EDM(x):
    if x == 'non' :
        return 0
    else :
        return 1
  
dfS['EDM'] = dfS['EDM'].apply(EDM)
 
var(Nom_Var[47],dfS) #0% ; TAG ; object ; 2 moda oui non à reco en 1;0
def TAG(x):
    if x == 'non' :
        return 0
    else :
        return 1
  
dfS['TAG'] = dfS['TAG'].apply(TAG)

#voir avec troncature pour les 9999 - question de censure
var(Nom_Var[48],dfS) #81.74% ; duree_chomage ; float ; attention 9999 + nan > 0 ? ; 24 moda
#0 si jamais au chomage et on met quoi pour les 9999 = actuellement au chomage ? remplacer 9999 par 9 et voir quel est le max d'année ?? 
dfS["duree_chomage"].fillna(0, inplace=True)

var(Nom_Var[49],dfS) #86.57% ; duree_handi ; float ; attention 9999 + nan > 0 ? ; 35 moda
dfS["duree_handi"].fillna(0, inplace=True)

var(Nom_Var[50],dfS) #53.63% ; 7319 ;  maladie_chronique ; object ; 15 moda + nan à reco en 0;1 ... 15
#nan 'Cardio-vasculaire' 'Endocrinienne ou métabolique' 'Os et articulations' 'Pulmonaire' 'Nerveux ou psychique' 'Autre' 'Peau'
#'Neurologique' 'Digestif' 'ORL' 'Cancer' 'Oculaire' 'Dépendance' 'Bouche et dents' 'Urinaire et génital'

df_dum=pd.get_dummies(dfS['maladie_chronique'])
df_dum.head()

df = dfS.merge(df_dum, how='left', left_index=True, right_index=True)

print(df)
"""
def maladie_chronique(x):
    if x == 'nan' :
        return 0
    elif x == 'Bouche et dents' :
        return 1
    elif x == 'Cancer' :
        return 2
    elif x == 'Cardio-vasculaire' :
        return 3
    elif x == 'Dépendance' :
        return 4
    elif x == 'Digestif' :
        return 5
    elif x == 'Endocrinienne ou métabolique' :
        return 6
    elif x == 'Nerveux ou psychique' :
        return 7
    elif x == 'Neurologique' :
        return 8
    elif x == 'Oculaire' :
        return 9
    elif x == 'Os et articulations' :
        return 10
    elif x == 'ORL' :
        return 11
    elif x == 'Peau' :
        return 12
    elif x == 'Pulmonaire' :
        return 13
    elif x == 'Urinaire et génital' :
        return 14
    else:
        return 15
    
dfS['maladie_chronique'] = dfS['maladie_chronique'].apply(maladie_chronique)
 """
#SUPPRIMER LES COL AVEC TROP DE V.Manq
column_with_nan = df.columns[df.isnull().any()]
print(column_with_nan)
for column in column_with_nan:
    if df[column].isnull().sum()*100.0/df.shape[0] > 50:      #30 - 50% ??     
        df.drop(column,1, inplace=True)
        
df.to_csv(r'C:\Users\ceecy\PythonScripts\Micro\SIP06_Cleanst.csv')
dfS = pd.read_csv(r'C:\Users\ceecy\PythonScripts\Micro\SIP06_Cleanst.csv', sep=',', engine='python')
"""
def zremen_(x):
    if x <= 1554.58 and x != 0 : #entre le rsa et le smic/personne
        return 1
    elif x <= (1554.58*3) and x >= 1554.58 and x != 0 : #entre le smic et le salaire médian/personne
        return 2
    else : 
        if x != 0 : #tout ce qu'il y a au dessus
            return 3
        if x == 0 : #salaire = 0
            return 0
dfS['zremen'] = dfS['zremen'].apply(zremen_)
var(Nom_Var[19],dfS) #35.44% ; 4837 ; zremen ; float ; 2 moda 1;2
"""
dfS.to_csv(r'C:\Users\ceecy\PythonScripts\Micro\SIP06Cleanst.csv')
