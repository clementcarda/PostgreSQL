#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#Auteur Clément Cardarelli
#Date Création 12/02
#
#
#corp principale de l'appli


#####Importation#####
import functions
import actions as act
import os
import parameter as p
from sys import argv

#####Initialisation#####

#repertoires
rep_path = os.path.dirname(os.path.abspath(__file__))

backup_path = p.BACKUP_PATH
if backup_path is None:
    backup_path = rep_path+'/backup'

tmp_path = p.TMP_PATH
if tmp_path is None:
    tmp_path = rep_path+'/tmp'

#créer un tableau associatif avec tous les chemins utiliser par l'appli
list_path = {'rep_path': rep_path,
             'backup_path': backup_path,
             'tmp_path': tmp_path}




#vérivication si rep /backup et /tmp existe, sinon les créer
if not os.path.isdir(backup_path):
   os.mkdir(backup_path)
if not os.path.isdir(tmp_path):
    os.mkdir(tmp_path)




#####Code#####

#tente une connexion à postgres ou renvoie une exceprtion en cas d'echec
try:
    cur = functions.connector(p.HOST, p.USER, p.PASSWORD)
except:
    raise Exception("Something went wrong with the conection")



# tableau associant une fonction de actions.py pour chaque argument
actions = {
    '-h': "print('this is help')",
    '-l': "act.listDBAction(cur)",
    '-s': "act.backupAllAction(cur, list_path, p.NB_BACKUP)",
    '-r': "act.restoreAllAction(rep_path)"
}

#lors du lancement de l'appli vérifie si un argumant est placé
if len(argv) == 2:
    exec(actions[argv[1]])
else:
    exec(actions['-h'])
