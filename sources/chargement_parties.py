#Projet : Mimesis
#Auteur : Noah LARZILLIERE 

'------------------------------------------------------------------------------------------------------------'

                    #   Importations 

import sqlite3
import os

'------------------------------------------------------------------------------------------------------------'

                    # Définition des fonctions et variables

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datas')    # chemin vers le répertoire data

def search_partie(pseudo = str):
    """
    Entrées : pseudo        (str)   : Pseudo entré par le joueur

    Sorties : res_partie    (list)  : Liste contenant toutes les sauvegardes affiliées au pseudo du joueur

    Renvoie une liste des sauvegardes liées au pseudo du joueur
    """
    
    connexion = sqlite3.connect(os.path.join(DATA_DIR, 'sauvegarde.db'))    # connexion à la base de données
    curseur = connexion.cursor()
    res_partie = curseur.execute("SELECT P.id_Partie, P.position_x, P.position_y, P.interaction1, P.interaction2, P.interaction3, P.interaction4, P.interaction5 FROM Parties P JOIN Liaison L ON P.id_Partie = L.id_Partie JOIN Joueurs J ON J.pseudo = L.pseudo WHERE J.pseudo = ?",(pseudo,))    # exécution de la commande
    res_partie = res_partie.fetchall()  # conversion en liste
    connexion.close()   # déconnexion de la base de données
    return res_partie

def search_joueur(pseudo = str):
    """
    Entrées : pseudo        (str)   : Pseudo entré par le joueur

    Sorties : res_infos_jr  (list)  : Liste contenant les informations affilées au pseudo du joueur

    Renvoie une liste des informations liées au pseudo du joueur
    """
    
    connexion = sqlite3.connect(os.path.join(DATA_DIR, 'sauvegarde.db'))    # connexion à la base de données
    curseur = connexion.cursor()
    res_infos_jr = curseur.execute("SELECT * FROM Joueurs WHERE Joueurs.pseudo = ?",(pseudo,))  # exécution de la commande
    res_infos_jr = res_infos_jr.fetchall()  # conversion en liste
    connexion.close()   # déconnexion de la base de données
    return res_infos_jr