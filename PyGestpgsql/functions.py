#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#Auteur Clément Cardarelli
#Date Création 12/02

#
#bases des fonctions de notre appli

#####Importations#####
import tarfile
import psycopg2
import os
import re
from datetime import datetime
import parameter as p

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
        conn_string += "dbname='"+dbase+"'"

    # tente une connexion, si elle echoue cela levera une erreure
    conn = psycopg2.connect(conn_string)

    # conn.cursor retourne un objet curseur qui peut servir à
    # exécuter des commandes postgres
    #cursor = conn.cursor()

    return conn

#renvoie une liste des bases de données de la BDD
def listDB(cursor):
    #execute une commande pour récupérer toutes les bases de données
    cursor.execute("""SELECT datname FROM pg_database WHERE datistemplate = false""")
    #créé et retourne la liste de ces bases de données
    list = []
    for table in cursor.fetchall():
        list.append(table[0])
    return list

#dump la BDD dans un .sql
def pgDump(dbase, path):
    os.system("pg_dump {0} > {1}/{0}.sql".format(dbase, path))

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
    name = year+"-"+month+"-"+day+"_"+hour+"-"+minute+"-"+second
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
    listArch.sort()
    if len(listArch) >= nbMax:
        i = 0
        while i <= len(listArch)-nbMax:
            os.system("rm {0}/{1}".format(targetFolder, listArch[i]))
            i += 1

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

#propose à l'utilisateur de choisir l'archive à restorer
def chooseArchive(listArchive):
    i = 0
    print("liste des archives")
    for archive in listArchive:
        i += 1
        print(i, ': ' + archive)
    nbArch = input('quel achive souhaitez vous restorer? ')
    nbArch = int(nbArch) - 1

    print("nous restorons : {0}".format(listArchive[nbArch]))
    return listArchive[nbArch]

#restore une sauvegarde
def restoreBackUp(bpath,choosed_archive):
    arch = tarfile.open("{0}/{1}.tar.gz".format(bpath['backup_path'],
                                                                 choosed_archive))
    arch.extractall(bpath['tmp_path'])
    arch.close()
    listSQL = os.listdir(bpath['tmp_path'])
    for sql in listSQL:
        dbname = ""
        i = 0
        for el in sql:
            if el == ".":
                dbname = sql[0:i]
            i += 1

        eraseTable(dbname)
        os.system("psql {0} < {1}/{2}".format(dbname, bpath['tmp_path'], sql))
        os.system("rm {0}/{1}".format(bpath['tmp_path'], sql))

#efface les tables de la base de donnée
def eraseTable(dbname):
    #se connecter à la BDD
    dbconn = connector(p.HOST, p.USER, p.PASSWORD, dbname)
    dbcur = dbconn.cursor()

    dbcur.execute("""SELECT table_name FROM information_schema.tables
                   WHERE table_schema = 'public'""")

    for table in dbcur.fetchall():

        dbcur.execute("""DELETE FROM {0}""".format(table[0]))

    dbconn.commit()
    dbcur.close()