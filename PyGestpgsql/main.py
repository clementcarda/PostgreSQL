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
import functions, os

#####Initialisation#####
#repertoire de sauvegarde
backupRep = "/home/clement/Cours/B2/Base_de_Données/PostgreSQL/Projet/PostgreSQL/PyGestpgsql/backup"
#vérivication si rep existe, sinon le créé
if not os.path.isdir(backupRep):
    os.mkdir(backupRep)

#####Code#####

##sauvegarde  et archivage de toute les DB
cur = functions.connector("clement")
listDB = functions.listDB(cur)

for table in listDB:
    functions.backingUp(backupRep+"/"+table+".sql", table)

functions.archive(backupRep)

#Liste les archives existante
print(functions.listArchive(backupRep))