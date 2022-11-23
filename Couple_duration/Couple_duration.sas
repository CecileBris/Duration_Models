libname CONJUG '/home/cecilebrissard0/sasuser.v94/Micro/CONJUG' ; 

proc import out=CONJUG.Virage
datafile = '/home/cecilebrissard0/sasuser.v94/Micro/CONJUG/virageclean.csv'
DBMS=csv; 
run;


/*****************************/
/* FINALISATION DU NETTOYAGE */
/*****************************/
/*Renommer les variables et drop l'indice VAR1*/
/*Gérer les valeurs aberrante de Dur_relconj*/

data CONJUG.Virage (drop=VAR1);
set CONJUG.Virage;
rename Q1 = sexe Fsexcjt = sexe_conj Q4 = Habitat Q22E = Nationalite Q22 = Diff_nat Q25E = Statut_pro
		Q19e_grage = classage Q29e_5gr = Nivdip Q29 = Diff_dip CS_E_Niv1 = CSP CS = Diff_CSP REV2 = Classrev REV5 = Diff_pat REV6 = CB 
		Enf1 = Nb_enf CF8a_01 = drogalc_conj SOC = Soc_Index EA5 = SitFam14 REL1E=Religion EA16 = Press_Mariage; 
if Dur_relconj=74 or Dur_relconj=83 then delete;
run;


/*****************************/
/* STATISTIQUES DESCRIPTIVES */
/*****************************/

proc contents data=CONJUG.Virage;
run;
PROC UNIVARIATE DATA=CONJUG.Virage;
	HISTOGRAM /NORMAL ;
RUN;
proc freq data = CONJUG.Virage;
Tables sexe sexe_conj Typecpl Habitat Diffage_cjt Nationalite Diff_nat Statut_pro Etatmat classage Nivdip
 Diff_dip CSP Diff_CSP Dur_relconj Classrev Diff_pat CB Nb_enf drogalc_conj Soc_Index SitFam14 Religion DIFF_REL Press_Mariage
 C_physc12m C_psysc12m C_sexsc12m C_totsc12m C_physcve C_psyscve C_sexscve C_totscve;
run;

/* BoxPlot */
proc sgplot data=CONJUG.Virage ; 	
	vbox Dur_relconj ; 
run;
title;

proc sgplot data=CONJUG.Virage ; 	
	vbox classage ; 
run;
title;

/* Correlation */
proc corr data = CONJUG.Virage pearson plots=matrix(histogram) noprob;
run;


/*****************************/
/*        MODELISATION       */
/*****************************/

/* Quelle loi de distribution ? */
PROC SEVERITY DATA=CONJUG.Virage PRINT=ALL;
	DIST EXP WEIBULL LOGN BURR GAMMA PARETO GPD;
	LOSS Dur_relconj ; *variable expliquée;
	CLASS sexe(ref = "2") sexe_conj(ref = "1") Typecpl(ref = "4") Habitat(ref ="2") Diffage_cjt(ref ="3") Nationalite(ref ="1") Diff_nat(ref ="1") Statut_pro(ref ="1") Etatmat(ref ="2") classage(ref ="5") Nivdip(ref ="1")
 Diff_dip(ref ="2") CSP(ref ="2") Diff_CSP(ref ="0") Classrev(ref ="5") Diff_pat(ref ="2") CB(ref ="2") Nb_enf(ref ="2") drogalc_conj(ref ="0") Soc_Index(ref ="3") SitFam14(ref ="1") Religion(ref ="1") DIFF_REL(ref ="0") Press_Mariage(ref ="0")
 C_physc12m(ref ="0") C_psysc12m(ref ="0") C_sexsc12m(ref ="0") C_totsc12m(ref ="0") C_physcve(ref ="0") C_psyscve(ref ="0") C_sexscve(ref ="0") C_totscve(ref ="0") ; 
	SCALEMODEL sexe sexe_conj Typecpl Habitat Diffage_cjt Nationalite Diff_nat Statut_pro Etatmat classage Nivdip
 Diff_dip CSP Diff_CSP Classrev Diff_pat CB Nb_enf drogalc_conj Soc_Index SitFam14 Religion DIFF_REL Press_Mariage
 C_physc12m C_psysc12m C_sexsc12m C_totsc12m C_physcve C_psyscve C_sexscve C_totscve; 
RUN;
QUIT;


/*LIFETEST*/
proc lifetest data=CONJUG.Virage atrisk plots=survival(cb);
time Dur_relconj;
run;

/*On effectue maintenant des lifetest stratifies*/

/*Sexe*/
proc lifetest data=CONJUG.Virage atrisk plots=survival(cb);
time Dur_relconj;
strata sexe ;
run;

/*Age*/
proc lifetest data=CONJUG.Virage atrisk plots=survival(cb);
time Dur_relconj;
strata classage;
run;

/*Indicateur de violences conjugales*/
/* 12 dernier mois : avant la séparation (vu qu'on suppose séparation) */
proc lifetest data=CONJUG.Virage atrisk plots=survival(cb);
time Dur_relconj;
strata  C_physc12m ;
run;

proc lifetest data=CONJUG.Virage atrisk plots=survival(cb);
time Dur_relconj;
strata  C_totsc12m ;
run;

/* dans la vie du couple*/
/*totale*/
proc lifetest data=CONJUG.Virage atrisk plots=survival(cb);
time Dur_relconj;
strata  C_totscve ;
run;

/*physique*/
proc lifetest data=CONJUG.Virage atrisk plots=survival(cb);
time Dur_relconj;
strata  C_physcve ;
run;

/*psychologique*/
proc lifetest data=CONJUG.Virage atrisk plots=survival(cb);
time Dur_relconj;
strata  C_psyscve ;
run;

/*sexuelle*/
proc lifetest data=CONJUG.Virage atrisk plots=survival(cb);
time Dur_relconj;
strata  C_sexscve ;
run;


/*REGRESSION*/

/*ALL*/
proc genmod data=CONJUG.Virage;
CLASS sexe(ref = "2") sexe_conj(ref = "1") Typecpl(ref = "4") Habitat(ref ="2") Diffage_cjt(ref ="3") Nationalite(ref ="1") Diff_nat(ref ="1") Statut_pro(ref ="1") Etatmat(ref ="2") classage(ref ="5") Nivdip(ref ="1")
 Diff_dip(ref ="2") CSP(ref ="2") Diff_CSP(ref ="0") Classrev(ref ="5") Diff_pat(ref ="2") CB(ref ="2") Nb_enf(ref ="2") drogalc_conj(ref ="0") Soc_Index(ref ="3") SitFam14(ref ="1") Religion(ref ="1") DIFF_REL(ref ="0") Press_Mariage(ref ="0")
 C_physc12m(ref ="0") C_psysc12m(ref ="0") C_sexsc12m(ref ="0") C_totsc12m(ref ="0") C_physcve(ref ="0") C_psyscve(ref ="0") C_sexscve(ref ="0") C_totscve(ref ="0") ; 
model Dur_relconj = sexe sexe_conj Typecpl Habitat Diffage_cjt Nationalite Diff_nat Statut_pro Etatmat classage Nivdip
 Diff_dip CSP Diff_CSP Classrev Diff_pat CB Nb_enf drogalc_conj Soc_Index SitFam14 Religion DIFF_REL Press_Mariage
 C_physc12m C_psysc12m C_sexsc12m C_totsc12m C_physcve C_psyscve C_sexscve C_totscve /DIST=GAMMA link=log; 
run;

/*SOCIO DEMO*/
proc genmod data=CONJUG.Virage;
CLASS sexe(ref = "2") sexe_conj(ref = "1") Habitat(ref ="2") Nationalite(ref ="1") Statut_pro(ref ="1") Etatmat(ref ="2") classage(ref ="5") Nb_enf(ref ="2")  drogalc_conj(ref ="0")
Nivdip(ref ="1")
 CSP(ref ="2") Classrev(ref ="5") Diff_pat(ref ="2") CB(ref ="2")  Soc_Index(ref ="3") SitFam14(ref ="1") Religion(ref ="1") Press_Mariage(ref ="0");
model Dur_relconj = sexe sexe_conj Habitat Nationalite Statut_pro Etatmat classage Nivdip
 CSP Classrev Diff_pat CB Nb_enf drogalc_conj Soc_Index SitFam14 Religion Press_Mariage /DIST=GAMMA LINK=log; 
run;

/*SOCIO */
proc genmod data=CONJUG.Virage;
CLASS Nivdip(ref ="1")
 CSP(ref ="2") Classrev(ref ="5") Diff_pat(ref ="2") CB(ref ="2")  Soc_Index(ref ="3") SitFam14(ref ="1") Religion(ref ="1") Press_Mariage(ref ="0");
model Dur_relconj = Nivdip CSP Classrev Diff_pat CB  Soc_Index SitFam14 Religion Press_Mariage /DIST=GAMMA LINK=log; 
run;

/*DEMO*/
proc genmod data=CONJUG.Virage;
CLASS sexe(ref = "2") sexe_conj(ref = "1") Habitat(ref ="2") Nationalite(ref ="1") Statut_pro(ref ="1") Etatmat(ref ="2") classage(ref ="5") Nb_enf(ref ="2")  drogalc_conj(ref ="0");
model Dur_relconj = sexe sexe_conj Habitat Nationalite Statut_pro Etatmat classage Nb_enf drogalc_conj /DIST=GAMMA LINK=log; 
run;

/*Violences conjugales*/
proc genmod data=CONJUG.Virage;
CLASS C_physc12m(ref ="0") C_psysc12m(ref ="0") C_sexsc12m(ref ="0") C_totsc12m(ref ="0") C_physcve(ref ="0") C_psyscve(ref ="0") C_sexscve(ref ="0") C_totscve(ref ="0") ; 
model Dur_relconj = C_physc12m C_psysc12m C_sexsc12m C_totsc12m C_physcve C_psyscve C_sexscve C_totscve /DIST=GAMMA LINK=log; 
run;

/*Autres variables de couple*/
proc genmod data=CONJUG.Virage;
CLASS  Diffage_cjt(ref ="3") Diff_nat(ref ="1") Diff_dip(ref ="2")Diff_CSP(ref ="0") DIFF_REL(ref ="0") ;
model Dur_relconj = Diffage_cjt Diff_nat Diff_dip Diff_CSP DIFF_REL /DIST=GAMMA Link=log; 
run;

/*Exemple du pdf*/
proc genmod data=CONJUG.Virage;
CLASS C_totscve(ref ="0") ; 
model Dur_relconj = C_totscve /DIST=GAMMA LINK=log; 
run;


/* ! :) ! */

