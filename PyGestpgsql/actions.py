#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#Auteur Clément Cardarelli
#Date Création 20/03
#
#
#Contient les action de notre application


import functions
import parameter as p

def listDBAction(cursor):
    for el in functions.listDB(cursor):
        print(el)

def backupAllAction(cursor, list_path, nb_backup):
    #vérifier nombre d'archive, en suprimer si nécessaire
    functions.limitNBArchive(list_path['backup_path'], nb_backup)
    #créer un .sql par db
    listdb = functions.listDB(cursor)

    #pour chaque BDD
    for dbase in listdb:

        #créer un sql correspodant
        functions.pgDump(dbase, list_path['tmp_path'])

    #archiver lles sql dans un tar.gz nommé en fonction de la date
    functions.archive(list_path['tmp_path'], list_path['backup_path'])


def restoreAllAction(list_path):
    #TODO efacer la totalité de chaque tableau avant de lancer la restauration

    #liste les archives existante et demande au user quel sauvegarde restaurer
    listArchive = functions.listArchive(list_path['backup_path'])

    choosedArchive = functions.chooseArchive(listArchive)

    functions.restoreBackUp(list_path, choosedArchive)


def restoreOneAction():
    #TODO demander au user quel BDD il souhaite restaurer,
        # faire comme restoreAll mais uniquement pour la BDD selectionné
    None