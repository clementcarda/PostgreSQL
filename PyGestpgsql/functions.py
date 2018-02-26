#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#Auteur Clément Cardarelli
#Date Création 12/02
#
#Derniere Modification 26/02
#
#bases des fonctions de notre appli

#####Importations#####
import tarfile
import psycopg2
import os
import re
from datetime import datetime

#####Fonctions#####
def connector(user):
    #Definition de la chaine de texte de connexion
    conn_string = "host='localhost' user='"+user+"'"

    # tente une connexion, si elle echoue cela levera une erreure
    conn = psycopg2.connect(conn_string)

    # conn.cursor retourne un objet curseur qui peut servir à
    # exécuter des commandes postgres
    cursor = conn.cursor()

    return cursor

def listDB(cur):
    #execute une commande pour récupérer toutes les bases de données
    cur.execute("""SELECT datname FROM pg_database WHERE datistemplate = false""")
    #créé et retourne la liste de ces bases de données
    list = []
    for table in cur.fetchall():
        list.append(table[0])
    return list

def backingUp(bpath, dbname):
   os.system("pg_dump "+dbname+" > "+bpath)

def nameArchive():
    now = datetime.now()
    name = str(now.year)+"-"+str(now.month)+"-"+str(now.day)+" "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)
    return name

def archive(backupFolder):
    name = nameArchive()
    tf = tarfile.open(backupFolder+"/"+name+".tar.gz", "x:gz")

    list = os.listdir(backupFolder)
    regx = re.compile("^.+sql$")
    for file in list:
        if regx.match(file):
            tf.add(backupFolder+"/"+file, arcname=file, recursive=False)
            os.system("rm "+backupFolder+"/"+file)
    tf.close()

def listArchive(backupFolder):
    list = os.listdir(backupFolder)
    listArch = []
    for archive in list:
        i = 0
        for el in archive:
            if el == '.':
                listArch.append(archive[0:i])
                break
            i += 1
    return listArch

