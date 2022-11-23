# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 19:19:46 2022

@author: ceecy
"""

import pandas as pd 
import numpy as np 


"""–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––"""
"""                             Preprocessing                               """
"""–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––"""

# Importation fichier
virage = pd.read_csv("base_virage.csv", sep=',',  encoding='latin-1')

# Il y a beaucoup trop de variables... 3860! Il va falloir choisir celles qui nous intéressent et drop toutes les autres. 
df = virage[['Q1','Fsexcjt','Typecpl','Q4','Diffage_cjt','Q22E','Q22C','Q25E','Etatmat','Q19e_grage',
             'Q29e_5gr','Q29c_5gr','CS_E_NIV1','CS_C_Niv1','Dur_relconj','REV2','REV5','REV6','Enf1','CF8a_01','SOC2a','SOC2b',
             'SOC2c','SOC2d','EA5','REL1E','REL1C','EA16','C_physc12m','C_psysc12m','C_sexsc12m','C_totsc12m',
             'C_physcve','C_psyscve','C_sexscve','C_totscve', 'C12m_cible', 'E12m_cible']]

# Puis on regarde les nan etc :
Nom_Var = df.columns
def var(nomvar,data):
    print("Nom de la var : " + nomvar)
    print(f"Nombre de modalités : {data[nomvar].nunique()}")
    print(f"Vecteurs des modalités : {data[nomvar].unique()}")
    print(f"Counts en chaque modalités : {data[nomvar].value_counts()}")
    print(data[nomvar].describe())
    print(f"La colonne a {data[nomvar].isna().sum()}  valeur(s) manquante(s)")
    print(f"La variable admet donc {(data[nomvar].isna().sum()/len(data))*100} % de valeur(s) manquante(s)")
    
for i in Nom_Var : 
    print(var(i,df))

#Il a trop de variables dans la console, on peut les regarder une par une aussi :    
print(var(Nom_Var[13],df))

""" Valeurs manquantes """ 
"""–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––"""

df.dropna(inplace=True)

""" Recodage """ 
"""–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––"""

""" Q4 """ 

def Q4(x):
    if x == 3 :
        return 3
    elif x == 2 :
        return 2
    elif x == 1 :
        return 1
df['Q4'] = df['Q4'].apply(Q4)

df.Q4.value_counts()
df.dropna(inplace=True)

""" Etatmat """ 

def Etatmat(x):
    if x == 3 :
        return 3
    elif x == 2 :
        return 2
    elif x == 4 :
        return 4
    elif x == 1 :
        return 1
df['Etatmat'] = df['Etatmat'].apply(Etatmat)
df.Etatmat.value_counts()
df.dropna(inplace=True)

""" Q22E : nationalité """ 

def Q22E(x):
    if x == 3 or x == 303 :
        return 3
    elif x == 2 or x==203  :
        return 2
    elif x == 1 or x==102 or x==103 :
        return 1
df['Q22E'] = df['Q22E'].apply(Q22E)

df.Q22E.value_counts()
df.dropna(inplace=True)


""" Q22C : nationalité conjoint """ 
   
df['Q22C'] = df['Q22C'].apply(Q22E)

df.Q22C.value_counts()
df.dropna(inplace=True)

""" Q22 : Diff_nat """ 

conditions = [
    (df['Q22E'] == 1) & (df['Q22C'] == 1),
    (df['Q22E'] == 2) & (df['Q22C'] == 2),
    (df['Q22E'] == 3) & (df['Q22C'] == 3)
    ]
choices = [1, 2, 3]

df['Q22'] = np.select(conditions, choices, default=4)

df.Q22.value_counts()
df.dropna(inplace=True)

# drop Q22C 

df.drop(columns = "Q22C", inplace = True)


""" SEXE """

df.Q1.value_counts()

df.Fsexcjt.value_counts()

df.Typecpl.value_counts()

df.dropna(inplace=True)


""" Q25E STATUT PRO """


def Q25E(x):
    if x == 1 :
        return 1
    elif x == 2 or x== 3  :
        return 2
    elif x == 4 :
        return 3
    elif x == 5 or x== 6  :
        return 4
    elif x == 7 or x== 8 or x==9 :
        return 5
    elif x == 10 or x== 11 :
        return 6
df['Q25E'] = df['Q25E'].apply(Q25E)

df.Q25E.value_counts()

""" Q25C STATUT PRO conjoint """

df.Q25C.value_counts()

df['Q25C'] = df['Q25C'].apply(Q25E)

df.Q25C.value_counts()

df.dropna(inplace=True)



""" Q29 5 GRP : NIVEAU D'ETUDE Niv_dip pour l'enquêté et le conjoint  """ 

df.Q29e_5gr.value_counts()
df.Q29c_5gr.value_counts()


def nivetude(x):
    if x == 00 :
        return 0
    elif x == 20 :
        return 1
    elif x == 30 :
        return 2
    elif x == 40 :
        return 3
    elif x == 50 :
        return 4
df['Q29e_5gr'] = df['Q29e_5gr'].apply(nivetude)
df['Q29c_5gr'] = df['Q29c_5gr'].apply(nivetude)

df.Q29e_5gr.value_counts()
df.Q29c_5gr.value_counts()

df.dropna(inplace=True)

""" Q29 : différence de NIVEAU D'ETUDE Diff_dip """ 

conditions = [
    (df['Q29e_5gr'] < df['Q29c_5gr'] ) ,
    (df['Q29e_5gr'] == df['Q29c_5gr'] ) ,
    (df['Q29e_5gr'] > df['Q29c_5gr'] ) ,
    ]
choices = [1, 2, 3]

df['Q29'] = np.select(conditions, choices, default=0)

df.Q29.value_counts()

# drop Q29c_5gr

df.drop(columns = "Q29c_5gr", inplace = True)



""" CS_E_NIV1 : CSP pour enquêté et CS_C_NIV1 pour le conjoint """

df.CS_E_NIV1.value_counts()
df.CS_C_Niv1.value_counts()

# 

def CSP(x):
    if x == 1 or x == 2 :
        return 1
    elif x == 5 or x == 6 :
        return 2
    elif x == 4 :
        return 3
    elif x ==3 :
        return 4
    elif x == 7 :
        return 5
    elif x == 8 : 
        return 6 
        
df['CS_E_NIV1'] = df['CS_E_NIV1'].apply(CSP)

# 

def CSP_C(x):
    if x == 1 or x == 2 :
        return 1
    elif x == 5 or x == 6 :
        return 2
    elif x == 4 :
        return 3
    elif x ==3 :
        return 4
    elif x == 7 or x == 8 : 
        return 0
df['CS_C_Niv1'] = df['CS_C_Niv1'].apply(CSP_C)

df.dropna(inplace=True)

df.CS_E_NIV1.value_counts()
df.CS_C_Niv1.value_counts()

""" CS : différence de CSP """


conditions = [
    (df['CS_E_NIV1'] == 1) & (df['CS_C_Niv1'] == 2 ), #1
    (df['CS_E_NIV1'] == 1) & (df['CS_C_Niv1'] == 3 ),
    (df['CS_E_NIV1'] == 1) & (df['CS_C_Niv1'] == 4 ),
    (df['CS_E_NIV1'] == 2) & (df['CS_C_Niv1'] == 3 ),
    (df['CS_E_NIV1'] == 2) & (df['CS_C_Niv1'] == 4 ),
    (df['CS_E_NIV1'] == 3) & (df['CS_C_Niv1'] == 4 ),
    (df['CS_E_NIV1'] == 1) & (df['CS_C_Niv1'] == 1 ), #2
    (df['CS_E_NIV1'] == 2) & (df['CS_C_Niv1'] == 2 ),
    (df['CS_E_NIV1'] == 3) & (df['CS_C_Niv1'] == 3 ),
    (df['CS_E_NIV1'] == 4) & (df['CS_C_Niv1'] == 4 ),
    (df['CS_E_NIV1'] == 4) & (df['CS_C_Niv1'] == 3 ), #3
    (df['CS_E_NIV1'] == 4) & (df['CS_C_Niv1'] == 2 ),
    (df['CS_E_NIV1'] == 4) & (df['CS_C_Niv1'] == 1 ),
    (df['CS_E_NIV1'] == 3) & (df['CS_C_Niv1'] == 2 ),
    (df['CS_E_NIV1'] == 3) & (df['CS_C_Niv1'] == 1 ),
    (df['CS_E_NIV1'] == 2) & (df['CS_C_Niv1'] == 1 )
    ]
choices = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3]

df['CS'] = np.select(conditions, choices, default=0)

df.CS.value_counts()

# drop CS_C_Niv1

df.drop(columns = "CS_C_Niv1", inplace = True)


""" TARGET TARGET TARGET      Dur_relconj        TARGET TARGET TARGET """

df['Dur_relconj'] = round(df['Dur_relconj']/12) 
#pour diviser par le nombre de mois dans 1 an, en arrondissant pour avoir des chiffres entiers.

df.Dur_relconj.value_counts()


""" Typecpl : type de couple """

df.Typecpl.value_counts()

def Type_cpl(x):
    if x == 'FF'  :
        return 1
    elif x == 'HH' :
        return 2
    elif x == 'HF' :
        return 3
    elif x == 'FH' :
        return 4

df['Typecpl'] = df['Typecpl'].apply(Type_cpl)

df.dropna(inplace=True)


""" Diffage_cjt: Difference age avec conjoint """

df.Diffage_cjt.value_counts()

def difage(x):
    if -28 <= x  < -1 :
        return 1
    elif x == 0 :
        return 2
    elif 1 < x <= 39 :
        return 3

df['Diffage_cjt'] = df['Diffage_cjt'].apply(difage)

df.Diffage_cjt.value_counts()

df.dropna(inplace=True)


""" Enf1 : Nombre d'enfants  """ 

def nbEnf(x):
    if x == 0 :
        return 0
    elif x == 1:
        return 1
    elif x == 2 :
        return 2
    elif x == 3 :
        return 3
    elif x >= 4 :
        return 4
    
df['Enf1'] = df['Enf1'].apply(nbEnf)

df.Enf1.value_counts()

df.dropna(inplace=True)


""" REV2 """ 

df.REV2.value_counts()

def revenu(x):
    if x == 1 :
        return 1
    elif x == 2 :
        return 2
    elif x == 3 :
        return 3
    elif x == 4 :
        return 4 
    elif x == 5 :
        return 5
    elif x == 6 :
        return 6
    elif x == 7 :
        return 7
    elif x == 8 :
        return 8
    elif x == 0 :
        return 0
    
df['REV2'] = df['REV2'].apply(revenu)

df.dropna(inplace=True)


""" REV5 """ 

df.REV5.value_counts()

def revenu(x):
    if x == 1 :
        return 1
    elif x == 2 :
        return 2
    elif x == 3 :
        return 3
    elif x == 4 :
        return 4 
    elif x == 5 :
        return 5
    
df['REV5'] = df['REV5'].apply(revenu)

df.dropna(inplace=True)


""" REV 6 """

df.REV6.value_counts()


def cb(x):
    if x == '01' or x == '0103' or x == '03' or x == '0203' or x == 1 or x == 103 or x == 3 or x == 203 :
        return 1
    elif x == '02' or x == 2 :
        return 2
    elif x == '0102' or x == '010203' or  x == 102 or  x == 10203 :
        return 3
    elif x == '04' or x==4 :
        return 4
     
df['REV6'] = df['REV6'].apply(cb)

df.REV6.value_counts()

df.dropna(inplace=True)

""" RELIGIONS pour l'enquêté et le conjoint """

def relig(x): 
    if x == 1 :
        return 1
    elif x == 2 :
        return 2
    elif x == 3 :
        return 3
    elif x == 4 :
        return 4 
    elif x == 5 :
        return 5
    elif x == 6 :
        return 6 
    elif x == 0 :
        return 0
df['REL1E'] = df['REL1E'].apply(relig)
df['REL1C'] = df['REL1C'].apply(relig)
df.REL1C.value_counts()
df.REL1E.value_counts()
df.dropna(inplace=True)

""" Diff_rel : différences de religions entre enquêté et son conjoint """

conditions = [
    (df['REL1E'] == df['REL1C']),   
    (df['REL1E'] != df['REL1C'])]  
choices = [0, 1]
df['DIFF_REL'] = np.select(conditions, choices, default=2)

df.DIFF_REL.value_counts()

# drop REL1C 

df.drop(columns = "REL1C", inplace = True)

""" SOC2 : Activité sociale """ 

# 'SOC2a','SOC2b', 'SOC2c', 'SOC2d'

df.SOC2a.value_counts()
df.SOC2b.value_counts()
df.SOC2c.value_counts()
df.SOC2d.value_counts()

conditions = [
    (df['SOC2a'] == 0) & (df['SOC2b'] == 0 ) & (df['SOC2c'] == 0 ) & (df['SOC2d'] == 0 ), #0 contact
    
    (df['SOC2a'] == 0) & (df['SOC2b'] == 0 ) & (df['SOC2c'] == 0) & (df['SOC2d'] > 0), #1 contact 
    (df['SOC2a'] == 0) & (df['SOC2b'] == 0 ) & (df['SOC2c'] > 0 ) & (df['SOC2d']== 0), 
    (df['SOC2a'] == 0) & (df['SOC2b'] > 0 ) & (df['SOC2c'] == 0 ) & (df['SOC2d'] == 0 ), 
    (df['SOC2a'] > 0) & (df['SOC2b'] == 0 ) & (df['SOC2c'] == 0 ) & (df['SOC2d'] == 0 ), 
    
    
    (df['SOC2a'] == 0) & (df['SOC2b'] == 0 ) & (df['SOC2c'] > 0 ) & (df['SOC2d'] > 0 ), #2 contact
    (df['SOC2a'] > 0) & (df['SOC2b'] > 0 ) & (df['SOC2c'] == 0 ) & (df['SOC2d'] == 0 ), #2 contact

    (df['SOC2a'] == 0) & (df['SOC2b'] > 0 ) & (df['SOC2c'] > 0 ) & (df['SOC2d'] == 0 ), #2 contact
    (df['SOC2a'] > 0) & (df['SOC2b'] == 0 ) & (df['SOC2c'] == 0 ) & (df['SOC2d'] > 0 ), #2 contact

    (df['SOC2a'] == 0) & (df['SOC2b'] > 0 ) & (df['SOC2c'] == 0 ) & (df['SOC2d'] > 0 ), #2 contact
    (df['SOC2a'] > 0) & (df['SOC2b'] == 0 ) & (df['SOC2c'] > 0 ) & (df['SOC2d'] == 0 ), #2 contact
    
    (df['SOC2a'] == 0) & (df['SOC2b'] > 0 ) & (df['SOC2c'] > 0) & (df['SOC2d'] > 0), #3 contact 
    (df['SOC2a'] > 0) & (df['SOC2b'] == 0 ) & (df['SOC2c'] > 0 ) & (df['SOC2d'] > 0), 
    (df['SOC2a'] > 0) & (df['SOC2b'] > 0 ) & (df['SOC2c'] == 0 ) & (df['SOC2d'] > 0 ), 
    (df['SOC2a'] > 0) & (df['SOC2b'] > 0 ) & (df['SOC2c'] > 0 ) & (df['SOC2d'] == 0 ), 
    
    (df['SOC2a'] > 0) & (df['SOC2b'] > 0) & (df['SOC2c'] > 0) & (df['SOC2d'] > 0)
    ]
choices = [0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4]

df['SOC'] = np.select(conditions, choices, default=5)

df.SOC.value_counts()

df.dropna(inplace=True)

#drop a b c d 

df.drop(columns = ["SOC2a","SOC2b","SOC2c","SOC2d"], inplace = True)

""" CF8a_01 : Alcool ou drogue chez le conjoint """ 

def CF8a_01(x) : 
    if x == 1 :
        return 1
    elif x == 0:
        return 0    
df['CF8a_01'] = df['CF8a_01'].apply(CF8a_01)

df.CF8a_01.value_counts()
df.dropna(inplace=True)


""" EA16 : Pression mariage """ 

def EA16(x):
    if x == 3 :
        return 1
    elif x == 2 or x == 0 or x==1 :
        return 0
df['EA16'] = df['EA16'].apply(EA16)

df.EA16.value_counts()
df.dropna(inplace=True)

""" EA5 : Situation familiale à 14 ans (enquêté) """ 

df.EA5.value_counts()

conditions = [
    (df['EA5'] == 1), #1
    (df['EA5'] == 6 ),
    (df['EA5'] == 2), #2 
    (df['EA5'] == 3 ), 
    (df['EA5'] == 4), #3
    (df['EA5'] == 5 ), 
    (df['EA5'] == 7), #4
    (df['EA5'] == 8 ),
    (df['EA5'] == 9 ),
    (df['EA5'] == 10 ),
    (df['EA5'] == 11 ),
    (df['EA5'] == 12 ),
    (df['EA5'] == 13 )
    ]
choices = [1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 4]

df['EA5'] = np.select(conditions, choices, default=0)

df.EA5.value_counts()
df.dropna(inplace=True)

def EA5(x) :
    if x == 1 :
        return 1
    elif x == 2:
        return 2
    elif x == 3:
        return 3
    elif x == 4:
        return 4  
df['EA5'] = df['EA5'].apply(EA5)
df.dropna(inplace=True)
 
""" Indicateur de violences conjugales physiques, psychologiques, sexuelles et totales
pour les 12mois précédents, et avant ces 12 mois """ 
    
def NIV(x):
    if x == 'Niv0' :
        return 0
    elif x == 'Niv1':
        return 1
    elif x == 'Niv2':
        return 2
    elif x == 'Niv3':
        return 3

df['C_physc12m'] = df['C_physc12m'].apply(NIV)
df['C_psysc12m'] = df['C_psysc12m'].apply(NIV)
df['C_sexsc12m'] = df['C_sexsc12m'].apply(NIV)
df['C_totsc12m'] = df['C_totsc12m'].apply(NIV)
df['C_physcve'] = df['C_physcve'].apply(NIV)
df['C_psyscve'] = df['C_psyscve'].apply(NIV)
df['C_sexscve'] = df['C_sexscve'].apply(NIV)
df['C_totscve'] = df['C_totscve'].apply(NIV)

df.C_physc12m.value_counts()
# ""0.0    15388
# 1.0       45
# 2.0       29
# 3.0       22
# Name: C_physc12m, dtype: int64""
df.C_psysc12m.value_counts()
# 0    14824
# 2      276
# 1      218
# 3      167
# Name: C_psysc12m, dtype: int64
df.C_sexsc12m.value_counts()
# "0.0    15445
# 2.0       11
# 1.0       10
# Name: C_sexsc12m, dtype: int64"
df.C_totsc12m.value_counts()
# 0.0    14796
# 1.0      459
# 2.0      150
# 3.0       62
# Name: C_totsc12m, dtype: int64
df.C_physcve.value_counts()
# "0.0    15255
# 1.0      123
# 3.0       80
# 2.0       26
# Name: C_physcve, dtype: int64"
df.C_psyscve.value_counts()
# 0.0    15000
# 1.0      217
# 2.0      177
# 3.0       90
# Name: C_psyscve, dtype: int64
df.C_sexscve.value_counts()
# Out[22]: 
# 0    15436
# 2       32
# 1       17
# Name: C_sexscve, dtype: int64
df.C_totscve.value_counts()
# 0.0    14900
# 1.0      287
# 2.0      162
# 3.0      134
# Name: C_totscve, dtype: int64

"""–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––"""

#Assurons nous qu'il ne reste aucune valeur manquante:
    
df.dropna(inplace=True)

#On regarde la répartition de la variable de filtrage :
    
df.C12m_cible.value_counts()

# drop des variables de filtrage - nous n'avons que les gens en couple dans notre base.

df.drop(columns = ["C12m_cible","E12m_cible"], inplace = True)


""" Extraction pour travailler sous SAS """ 
"""–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––"""
   
df.to_csv("virageclean.csv", sep=',')
