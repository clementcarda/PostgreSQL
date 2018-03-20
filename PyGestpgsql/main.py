#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#Auteur Clément Cardarelli
#Date Création 12/02
#
#Derniere Modification 26/02
#
#corp principale de l'appli


#####Importation#####
import functions
import os
import yaml

#####Initialisation#####

#repertoire
rep = os.getcwd()


rep = open("/home/clement/Cours/B2/Base_de_Données/PostgreSQL/Projet/PostgreSQL/PyGestpgsql/parameter.yml", "r+")
try:
    param = yaml.load(rep)
except yaml.YAMLError as exc:
    print(exc)
print(param)


Rep = "home/clement/Cours/B2/Base_de_Données/PostgreSQL/Projet/PostgreSQL/PyGestpgsql/"

#vérivication si rep/backup existe, sinon le créé
#if not os.path.isdir(Rep+ "backup"):
#    os.mkdir(Rep+"backup")
#vérivication si rep/tmp existe, sinon le créé
#if not os.path.isdir(Rep+ "tmp"):
#    os.mkdir(Rep+"tmp")




#####Code#####

##sauvegarde  et archivage de toute les DB
cur = functions.connector("clement")
