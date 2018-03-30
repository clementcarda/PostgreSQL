# PostgreSQL
projet postgreSQL

##Mise en place
Renseigez dans parameter.py
- dans HOST le host de votre base PostgresSQL
- dans USER le nom de l'utilisateur (attention l'utilisateur doit au 
    moins avoir les droit de SELECT, INSERT et DELETE)
- dans PASSWORD le mot de passe de l'utilisateur en question
- dans NB_BACKUP le nombre d'archive maximal que vous souhaitez conserver

Eventuellement si vous le souhaitez vous pouvez renseigner dans BACKUP_PATH 
    le chemin vers votre dossier de sauvegarde où seront stocké toutes vos archives 

##Utilisation
Pour utiliser l'application il suffit de le lancer main.py avec python en ajoutant 
    à la fin l'argument associer à la commande souhaité
    

`python3 main.py -h` : afficher l'aide  
`python3 main.py -l` : liste les bases de données existante  
`python3 main.py -s` : créer un archive de l'état actuel de toute les bases de données  
`python3 main.py -r` : demande à l'utilisateur de choisir une des archive et la restaure

##L'Archivage
Les archives sont stockées dans le dossier de backup renseigné ou par défaut et sont 
nomée en fonction de la date de création selon le format suivant :  
année-mois-jour_heure-minute-seconde.tar.gz
   
