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
import functions, os, conf

#####Initialisation#####

#repertoire
Rep = conf.repertory

#vérivication si rep/backup existe, sinon le créé
if not os.path.isdir(Rep+ "backup"):
    os.mkdir(Rep+"backup")
#vérivication si rep/tmp existe, sinon le créé
if not os.path.isdir(Rep+ "tmp"):
    os.mkdir(Rep+"tmp")

#####fonction#####
def backupAll(cur):
    listDB = functions.listDB(cur)

    for table in listDB:
        functions.backingUp(Rep + "backup/" + table + ".sql", table)

    functions.archive(Rep + "backup")

def launchRestore():
    # Liste les archives existante
    list = functions.listArchive(Rep + "backup")
    i = 0
    for arch in list:
        print(str(i) + " : " + arch)
        i += 1
    index = int(input("choisissez le numéro de la sauvegarde à récupérer "))

    # extraction et restauration de l'archive souaité
    functions.restoreBackUp(Rep, index)



#####Code#####

##sauvegarde  et archivage de toute les DB
cur = functions.connector("clement")
#backupAll(cur)

launchRestore()





