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


def restoreAllAction(rep_path):
    #TODO efacer la totalité de chaque tableau avant de lancer la restauration

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







#    sql = open(list_path['tmp_path'] + "/" + dbase + ".sql", 'w')
#
#    # se connecter à la BDD
#    dbcur = functions.connector(p.HOST, p.USER, p.PASSWORD, dbase)
#
#    # Récuperer la liste des tables
#    dbcur.execute("""SELECT table_name FROM information_schema.tables
#                   WHERE table_schema = 'public'""")
#
#    # pour chaque table
#    for table in dbcur.fetchall():
#
#        # récupéerer chaque ligne
#        dbcur.execute("""SELECT * FROM %s""" % (table))
#
#        # pour chaque ligne
#        for ligne in dbcur.fetchall():
#            None
#    dbcur.close()
#    print(dbase)