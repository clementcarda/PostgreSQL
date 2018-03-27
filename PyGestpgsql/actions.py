#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#Auteur Clément Cardarelli
#Date Création 20/03
#
#
#Contient les action de notre application


import functions

def listDBAction(cursor):
    for el in functions.listDB(cursor):
        print(el)

def backupAllAction(cursor, rep_path):
    functions.backupAll(cursor, rep_path)

def restoreOneAction(rep_path):
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