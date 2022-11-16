libname Micro 'C:\Users\ceecy\OneDrive - Universit� Paris-Dauphine\Economie\M1\Micro\Projet' ; 

proc import out=Micro.SIP06cle
datafile = 'C:\Users\ceecy\PythonScripts\Micro\SIP06_Cleanst.csv'
DBMS=csv; 
run;

/*La gestion des valeurs manquantes et l'encodage des variables le n�cessitant ont �t� effectu�es sur le logiciel de code Python*/
/*Il reste n�anmoins quelques variables � mettre en forme :*/
	
	/**************************/
	/* TRAITEMENTS DE DONNEES */
	/**************************/


/*cr�ation d'une variable indiquant si on est au ch�mage ou non : si la personne n'a jamais �t� au ch�mage elle prend la valeur 0 ; si il y a une dur�e elle prend la valeur 1 */
data Micro.SIP06cl; 
set Micro.SIP06cle; 
if fsitua=4 then chomeur_actu=1; /*oui*/
else chomeur_actu=0; /*non*/
run ;
/*on compare avec nos dur�es de ch�mage pour voir si on a les m�me oui/non*/
data Micro.SIP06c; 
set Micro.SIP06cl; 
if duree_chomage=9999 then duree_chomage=.; /*on remplace les 9999 par des na '.' 
car sinon �a tire la distribution vers le haut dans tous les mod�les*/
if duree_chomage=0 then chomeur=0; /*non*/
else chomeur=1; /*oui*/
run ;
/*Les deux ne collent pas mais on va centrer notre �tude sur ceux qui ont une dur�e de ch�mage disponible ; m�me s'il en sont sortie */

/*on a une var polytomique ordonn�e donc on va donc cr�er une nouvelle variable pour regrouper par modalit�
Avant �a on s'est assur� qu'il y avait un effectif suffisant sur chaque modalit�*/
/*on ne peut pas utiliser dur�e handi a priori ; voir la repr�sentativit� des 9999 dans la table de chomeurs*/
data Micro.SIP06c;
set Micro.SIP06c;
if duree_handi in (1:10) then duree_handi=1; /*dur�e de handicap de moins de 10 ans */
if duree_handi in (10:57) then duree_handi=2; /*dur�e de handicap comprise entre 10 et 57ans*/
if duree_handi = 9999 then duree_handi=3; /*encore handicap�*/ /*on ne sait pas si �a fait 2 ans 5 ans ou 40 ans donc on va sup la varianle je pense*/
run;

/*on regroupe les famille de 4 enfants et plus dans la modalit� 4*/
data Micro.SIP06c;
set Micro.SIP06c;
if fnelev = 0 then fnelev_2=0;
if fnelev = 1 then fnelev_2=1;
if fnelev = 2 then fnelev_2=2;
if fnelev = 3 then fnelev_2=3;
if fnelev in (4:13) then fnelev_2=4;
run;
data Micro.SIP06c;
set Micro.SIP06c;
if sexenq = 1 then sexenq=0;
if sexenq = 2 then sexenq=1;
run;
data Micro.SIP06c;
set Micro.SIP06c;
if sq2g = 1 then sq2g=1; /*OUI*/
if sq2g = 2 then sq2g=0; /*NON*/
run;

/*on cr�er une table comportant uniquement les ch�meurs, ou personne ayant d�j� �t� au ch�mage, pour lesquels on a une dur�e*/
data Micro.SIP06;
set Micro.SIP06c;
if chomeur=0 and chomeur_actu=0 then delete; 
run;

/*on cr�er des classes pour les variables de pourcent d'emploi, revenus et d'�ge - on veut des tranches �quilibr�es :*/

proc rank data=Micro.SIP06 groups=3 out=Micro.SIPrank;
	var zremen; ranks classrev;
run;
proc rank data=Micro.SIPrank groups=5 out=Micro.SIPra;
	var agenq; ranks classage;
run;
proc rank data=Micro.SIPra groups=5 out=Micro.SIPr;
	var elip; ranks classelip;
run;

/*on cr�er la variable de censure*/
data Micro.SIPr;
set Micro.SIPr;
if duree_chomage>27 then censure=0;
else censure=1;
run;

/*On ne garde que les variables que l'on souhaite utiliser & qui paraissent coh�rente dans l'explication de duree_chomage*/

data Micro.SIP;
set Micro.SIPr;
keep sexenq fsitua fnelev_2 fnivdip flnais fnaim fpermer 
classelip elip
classrev zremen
classage agenq
duree_chomage chomeur chomeur_actu censure
duree_handi sq2g TAG EDM
zben_1 zsyn_1 zpol_1 zreli_1 zart_1 zspo_1 ;
run;

/*****************************/
/* STATISTIQUES DESCRIPTIVES */
/*****************************/

proc contents data=Micro.SIP06cle;
run;
PROC UNIVARIATE DATA=Micro.SIP06cle;
	HISTOGRAM /NORMAL ;
RUN;
proc freq data = Micro.SIP06cle;
Tables duree_chomage EDM TAG agenq censure chomeur chomeur_actu duree_chomage 
duree_handi elip flnais fnaim fnelev_2 fnivdip fpermer fsitua sexenq sq2g zart_1 zben_1 zpol_1 zreli_1 
zremen zspo_1 zsyn_1 ;
run;
/********************************************************/
proc contents data=Micro.SIP;
run;
PROC UNIVARIATE DATA=Micro.SIP;
	HISTOGRAM /NORMAL ;
RUN;
proc freq data = Micro.SIP;
Tables duree_chomage EDM TAG agenq censure chomeur chomeur_actu classage classelip classrev duree_chomage 
duree_handi elip flnais fnaim fnelev_2 fnivdip fpermer fsitua sexenq sq2g zart_1 zben_1 zpol_1 zreli_1 
zremen zspo_1 zsyn_1 ;
run;

/****************/
/* MODELISATION */
/****************/

/*TEST*/ /*On veut savoir quelle est la meilleure loi pour estimer le mod�le*/
PROC SEVERITY DATA=Micro.SIP PRINT=ALL EMPIRICALCDF=KAPLANMEIER;
	DIST EXP WEIBULL LOGN BURR ;
	LOSS duree_chomage / RIGHTCENSORED=censure; *variable expliqu�e;
	CLASS sexenq(ref = "1") flnais(ref="1") 
fnelev_2(ref="2") fnivdip(ref="4") 
fnaim(ref="1") fpermer(ref="4") 
classrev(ref="0") classage(ref="2") classelip(ref="0")
zben_1(ref="0") zsyn_1(ref="0") zpol_1(ref="0") zreli_1(ref="0") zart_1(ref="0") zspo_1(ref="0")
duree_handi(ref="1") sq2g(ref="1") EDM(ref="0") TAG(ref="0") ; 
	SCALEMODEL fnelev_2 fnivdip flnais fnaim fpermer sq2g classrev sexenq classage zben_1 zsyn_1 
zpol_1 zreli_1 zart_1 zspo_1 duree_handi EDM TAG ; 
RUN;
QUIT;


/*LIFETEST*/
proc lifetest data=Micro.SIP atrisk plots=survival(cb);
time duree_chomage*censure(0);
run;

/*On effectue maintenant des lifetest stratifi�s*/

/*Sexe*/
proc lifetest data=Micro.SIP atrisk plots=survival(cb);
time duree_chomage*censure(0);
strata sexenq;
run;
/*plus long en 1 donc si msexe f�minin donc logique*/

/*Maladie chronique*/
proc lifetest data=Micro.SIP atrisk plots=survival(cb);
time duree_chomage*censure(0);
strata sq2g;
run;
/*plus long en 0 donc si maladie chronique donc logique*/

/*Nationalit�*/
proc lifetest data=Micro.SIP atrisk plots=survival(cb);
time duree_chomage*censure(0);
strata flnais;
run;
/*plus long en 2 que en 3 donc si devenu fran�ais donc logique mais plus long en 1*/
/*on ne rejette pas H0 : les 3 strates ont la m�me fonction de survie*/

/*b�n�volat*/
proc lifetest data=Micro.SIP atrisk plots=survival(cb);
time duree_chomage*censure(0);
strata zben_1;
run;
/*on ne rejette pas H0 : les deux strates ont la m�me fonction de survie*/

/*Sport*/
proc lifetest data=Micro.SIP atrisk plots=survival(cb);
time duree_chomage*censure(0);
strata zspo_1;
run;
/*plus long en 0 donc si pas de sport donc logique*/

/*Handicap*/
proc lifetest data=Micro.SIP atrisk plots=survival(cb);
time duree_chomage*censure(0);
strata duree_handi;
run;
/*pas significatif*/

/*pas significatif*/ /*pourtant en 1 (handi>10ans) on sort moins vite du ch�mage qu'en 0(<10ans)*/
/*La dur�e de handicap n'apporte pas d'information et les 9999 portent � confusion donc on la remplace par .*/

/*On lance une r�gression globale*/
proc phreg data=Micro.SIP;
CLASS sexenq(ref = "1") flnais(ref="1") 
fnelev_2(ref="2") fnivdip(ref="4") 
fnaim(ref="1") fpermer(ref="4") 
classrev(ref="0") classage(ref="2") classelip(ref="0")
zben_1(ref="0") zsyn_1(ref="0") zpol_1(ref="0") zreli_1(ref="0") zart_1(ref="0") zspo_1(ref="0")
duree_handi(ref="1") sq2g(ref="1") EDM(ref="0") TAG(ref="0") ; 
model duree_chomage*censure(0) = fnelev_2 fnivdip flnais fnaim fpermer sq2g classrev sexenq classage 
zben_1 zsyn_1 zpol_1 zreli_1 zart_1 zspo_1 duree_handi EDM TAG; 
run;

/*param�tre pour g�rer la discontinuit� de duree_ch�mage : ties - pb des �v�nements simultan�s car on n'observe pas la date exacte*/
/*m�thode d'Efron*/
/*M�me chose avec EFRON pour comparer la diff�rence entre le traitement de la discontinuit� ou pas*/
proc phreg data=Micro.SIP;
CLASS sexenq(ref = "1") flnais(ref="1") 
fnelev_2(ref="2") fnivdip(ref="4") 
fnaim(ref="1") fpermer(ref="4") 
classrev(ref="0") classage(ref="2") 
zben_1(ref="0") zsyn_1(ref="0") zpol_1(ref="0") zreli_1(ref="0") zart_1(ref="0") zspo_1(ref="0")
duree_handi(ref="1") sq2g(ref="1") EDM(ref="0") TAG(ref="0") ; 
model duree_chomage = fnelev_2 fnivdip flnais fnaim fpermer sq2g classrev sexenq classage 
zben_1 zsyn_1 zpol_1 zreli_1 zart_1 zspo_1 duree_handi EDM TAG /TIES=EFRON; 
run;

/*On estime param�tre par param�tre ou grp par grp*/
/*Tout d'abord les plurimodales*/
/*Situation*/ /*nope paske autocorr�lation 
*Il y a endog�n�it� entre duree_chomage et la situation actuelle (fsitua) de la personne car si fsitua=4 alors duree_chomage=3;
proc phreg data=Micro.SIP;
CLASS  fsitua(ref="1");
model duree_chomage*censure(0) = fsitua /TIES=EFRON;
run;*/

/*Nb d'enfants*/
proc phreg data=Micro.SIP;
CLASS fnelev_2(ref="2"); 
model duree_chomage*censure(0) = fnelev_2 /TIES=EFRON;
run;

/*niveau de dipl�me*/
proc phreg data=Micro.SIP;
CLASS fnivdip(ref="4"); 
model duree_chomage*censure(0) = fnivdip /TIES=EFRON;
run;

/*Qui nous a �lev� ?*/
proc phreg data=Micro.SIP;
CLASS fpermer(ref="1") ; 
model duree_chomage = fpermer /TIES=EFRON;
run;

/*Nationalit�*/
proc phreg data=Micro.SIP;
CLASS flnais(ref="1"); 
model duree_chomage*censure(0) = flnais /TIES=EFRON; 
run;
/*PAS SIGNIFICATIF*/

/*Puis on regroupe*/
/*Revenu age et sexe*/
proc phreg data=Micro.SIP;
CLASS sexenq(ref = "1")
classrev(ref="0") classage(ref="2") ;
model duree_chomage = classrev sexenq classage /TIES=EFRON; 
run;

/*Etat de sant�=maladie chronique ou handicap; selon age et sport*/
proc phreg data=Micro.SIP;
CLASS sexenq(ref = "1") zspo_1(ref="0")
duree_handi(ref="1") sq2g(ref="1") ; 
model duree_chomage*censure(0) = sq2g sexenq zspo_1 duree_handi/TIES=EFRON; 
run;
/*EDM et TAG*/
proc phreg data=Micro.SIP;
CLASS EDM(ref = "0") TAG(ref="0") ; 
model duree_chomage*censure(0) = TAG EDM /TIES=EFRON; 
run;
/*variables t�moignant d'autres activit�s*/
proc phreg data=Micro.SIP;
CLASS zben_1(ref="0") zsyn_1(ref="0") zpol_1(ref="0") zreli_1(ref="0") zart_1(ref="0") zspo_1(ref="0") ; 
model duree_chomage*censure(0) = zben_1 zsyn_1 zpol_1 zreli_1 zart_1 zspo_1 /TIES=EFRON; 
run;
/*seul le sport et art sont significatifs, on le retire pour voir le comportement des autres*/
proc phreg data=Micro.SIP;
CLASS zben_1(ref="0") zsyn_1(ref="0") zpol_1(ref="0") zreli_1(ref="0") ; 
model duree_chomage*censure(0) = zben_1 zsyn_1 zpol_1 zreli_1 / TIES=EFRON;
run;
/*toujours pas significatif*/

/*Nationalit� + Nationalit� m�re + �lev� par qui ?*/
proc phreg data=Micro.SIP;
CLASS flnais(ref="1") fnaim(ref="1") fpermer(ref="1") ;
model duree_chomage*censure(0) = flnais fnaim fpermer /TIES=EFRON;
run;
/*pas significatif pour flnais*/


