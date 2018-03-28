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

    for dbase in listdb:
        open(list_path['tmp_path']+dbase+".sql", 'w')
        #dans chaque .sql récupérer toute les tables
            #pour chaque ligne de chaque table écrire un INSERT dans le .sql
        dbcur = functions.connector(p.HOST, p.USER, p.PASSWORD, dbase)
        dbcur.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public'""")
        for table in dbcur.fetchall():
            print(table)


    #functions.archive(list_path['tmp_path'], list_path['backup_path'])


def restoreAllAction(rep_path):
    #liste les archives existante et demande au user quel sauvegarde restaurer
    listArchive = functions.listArchive(rep_path+'/backup')
    i = 0
    print("liste des archives")
    for archive in listArchive:
        i+=1
        print(i, ': '+archive)
    nbArch = input('quel achive souhaitez vous restorer? ')
    nbArch = int(nbArch)-1

    print("nous restorons :", listArchive[nbArch])

    functions.restoreBackUp(rep_path, listArchive[nbArch])