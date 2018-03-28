#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#Auteur Clément Cardarelli
#Date Création 12/02

#
#bases des fonctions de notre appli

#####Importations#####
import getpass
import tarfile
import psycopg2
import os
import re
from datetime import datetime

import sys
from crontab import CronTab
import yaml
import pureyaml

#####Fonctions#####

#créer un connecteur avec la base de donnée PostGres
def connector(host, user, psswd, dbase = None):
    #Definition de la chaine de texte de connexion
    conn_string = "host='"+host+"' user='"+user+"' password='"+psswd+"'"
    if dbase is not None:
        conn_string += "database='"+dbase+"'"

    # tente une connexion, si elle echoue cela levera une erreure
    conn = psycopg2.connect(conn_string)

    # conn.cursor retourne un objet curseur qui peut servir à
    # exécuter des commandes postgres
    cursor = conn.cursor()

    return cursor

#renvoie une liste des bases de données de la BDD
def listDB(cursor):
    #execute une commande pour récupérer toutes les bases de données
    cursor.execute("""SELECT datname FROM pg_database WHERE datistemplate = false""")
    #créé et retourne la liste de ces bases de données
    list = []
    for table in cursor.fetchall():
        list.append(table[0])
    return list

#génère un nom pour l'archive en prenant la date
def nameArchive():
    now = datetime.now()
    year = str(now.year)
    month = str(now.month)
    if now.month < 10:
        month = "0"+month
    day = str(now.day)
    if now.day < 10:
        day = "0"+month
    hour = str(now.hour)
    if now.hour < 10:
        hour = "0"+hour
    minute = str(now.minute)
    if now.minute < 10:
        minute = "0" + minute
    second = str(now.second)
    if now.second < 10:
        second = "0" + second
    name = year+"-"+month+"-"+day+"_"+hour+":"+minute+":"+second
    return name

#créer une archive avec les fichier .sql de la sauvegarde
def archive(originFolder, targetFolder):
    name = nameArchive()
    tf = tarfile.open(targetFolder+"/"+name+".tar.gz", "x:gz")

    list = os.listdir(originFolder)
    regx = re.compile("^.+sql$")
    for file in list:
        if regx.match(file):
            tf.add(originFolder+"/"+file, arcname=file, recursive=False)
            os.system("rm "+originFolder+"/"+file)
    tf.close()

#liste le nombre d'archive et si elle dépasse la limite autorisé en supprime 1
def limitNBArchive(targetFolder, nbMax):
    listArch = os.listdir(targetFolder)
    if len(listArch) >= nbMax:
        os.system("rm "+targetFolder+"/"+listArch[0])

#renvoie une liste des archives du répertoire de sauvegar
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






#restore une sauvegarde
def restoreBackUp(bpath,archive):
    arch = tarfile.open(bpath+"/backup/"+archive+".tar.gz")
    arch.extractall(bpath+"/tmp")
    arch.close()
    listSQL = os.listdir(bpath+"/tmp/")
    for sql in listSQL:
        dbname = ""
        i = 0
        for el in sql:
            if el == ".":
                dbname = sql[0:i]
            i += 1
        print("\nrestoring "+dbname)
        os.system("psql "+dbname+" < "+bpath+"/tmp/"+sql)
        os.system("rm "+bpath+"/tmp/"+sql)