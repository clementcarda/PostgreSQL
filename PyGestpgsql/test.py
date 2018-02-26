#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#Auteur Clément Cardarelli
#Date Création 12/02
#

import fileinput, conf

for line in fileinput.input(conf.repertory+"conf.py", inplace=True):
    text = line
    print(text)
    #print(line.replace( 'test = ', 'test = "0 0 0 0 0"'))


