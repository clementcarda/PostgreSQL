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
import parameter
from getpass import getuser
from sys import argv

#####Initialisation#####

#repertoires
rep_path = os.path.dirname(os.path.abspath(__file__))

backup_path = parameter.BACKUP_PATH
if backup_path is None:
    backup_path = rep_path+'/backup'

tmp_path = parameter.TMP_PATH
if tmp_path is None:
    tmp_path = rep_path+'/tmp'




#vérivication si rep /backup et /tmp existe et /tmp, sinon les créer
if not os.path.isdir(backup_path):
   os.mkdir(backup_path)
if not os.path.isdir(tmp_path):
    os.mkdir(tmp_path)




#####Code#####
user = getuser()
try:
    cur = functions.connector(user)
except:
    raise Exception("Something went wrong with the conection")

actions = {
    '-h': "print('this is help')",
    '-l': "act.listDBAction(cur)",
    '-s': "act.backupAllAction(cur, rep_path)",
    '-r': "act.restoreOneAction(rep_path)"
}

if len(argv) == 2:
    exec(actions[argv[1]])
else:
    exec(actions['-h'])
