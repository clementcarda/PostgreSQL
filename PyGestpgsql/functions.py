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
def connector(user):
    #Definition de la chaine de texte de connexion
    conn_string = "host='localhost' user='"+user+"'"

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

#Créer une sauvegarde d'une base de données dbname dans le répertoire bpath
def backingUp(bpath, dbname):
   os.system("pg_dump "+dbname+" > "+bpath)

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
    name = year+"-"+month+"-"+day+" "+hour+":"+minute+":"+second
    return name

#créer une archive avec les fichier .sql de la sauvegarde
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
    clearDB()
    listSQL = os.listdir(bpath+"/tmp/")
    for sql in listSQL:
        dbname = ""
        i = 0
        for el in sql:
            if el == ".":
                dbname = sql[0:i]
            i += 1

        os.system("psql "+dbname+" < "+bpath+"/tmp/"+sql)
        os.system("rm "+bpath+"/tmp/"+sql)

def paramCron(rep, conf):
    user = getpass.getuser
    my_cron = CronTab(user)
    job = my_cron.new(command='python3 '+rep+'main.py')
    job.setall(conf)
    my_cron.write

def backupAll(cursor, Rep):
    DB = listDB(cursor)

    for table in DB:
        backingUp(Rep + "/backup/" + table + ".sql", table)

    archive(Rep + "/backup")

def launchRestore(Rep):
    # Liste les archives existante
    list = listArchive(Rep + "backup")
    i = 0
    for arch in list:
        print(str(i) + " : " + arch)
        i += 1
    index = int(input("choisissez le numéro de la sauvegarde à récupérer "))

    # extraction et restauration de l'archive souaité
    restoreBackUp(Rep, index)

def pushParameters(rep_path, param):
    with open(rep_path + "/parameter.yml", 'w') as yaml_file:
        yaml_file.write(yaml.dump(param, default_flow_style=False))

def clearDB():
    cur = connector('clement')
    try:
        cur.execute(
            "SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name")
        rows = cur.fetchall()
        for row in rows:
            print
            "dropping table: ", row[1]
            cur.execute("drop table " + row[1] + " cascade")
        cur.close()
    except:
        print
        "Error: ", sys.exc_info()[1]