#Projet : Mimesis
#Auteur : Noah LARZILLIERE 

'------------------------------------------------------------------------------------------------------------'

                    #   Importations 

import sqlite3
import os

'------------------------------------------------------------------------------------------------------------'

                    # Définition des fonctions et variables

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datas')    # chemin vers le répertoire data

def insert_joueur(a, b = False, c = False, d = False):
    """
    Entrées : a (str)   : Pseudo du joueur
              b (bool)  : Si oeuvre 1 volée |
              c (bool)  : Si oeuvre 2 volée | à développer dans une future version
              d (bool)  : Si oeuvre 3 volée |

    Ajoute un nouveau pseudo dans la table Joueurs (et les oeuvres volées associées)
    """
    
    connexion = sqlite3.connect(os.path.join(DATA_DIR, 'sauvegarde.db'))    # connexion à la base de données
    curseur = connexion.cursor()
    curseur.execute("""INSERT INTO Joueurs VALUES (?, ?, ?, ?)""", (a, b, c, d))    # crée un nouvel enregistrement
    connexion.commit()  # valide les modifications
    connexion.close()   # déconnexion de la base de données

def insert_partie(a = 0, b = 0, c = False, d = False, e = False, f = False, g = False):
    """
    Entrées : a     (int)   : Position horizontale du joueur
              b     (int)   : Position verticale du joueur
              c     (bool)  : Si interaction avec la sécurité
              d     (bool)  : Si interaction avec l'oeuvre
              e     (bool)  : Si interaction avec la porte de secours
              f     (bool)  : Si interaction avec la clé
              g     (bool)  : Si interaction avec la porte principale

    Sorties : id[0] (int)   : Numéro d'identification de la partie

    Crée une nouvelle partie dans la table Parties, puis renvoie son numéro d'identification
    """
    
    connexion = sqlite3.connect(os.path.join(DATA_DIR, 'sauvegarde.db'))    # connexion à la base de données
    curseur = connexion.cursor()
    curseur.execute("""INSERT INTO Parties (position_x, position_y, interaction1, interaction2, interaction3, interaction4, interaction5) VALUES (?, ?, ?, ?, ?, ?, ?)""", (a, b, c, d, e, f, g))   # crée un nouvel enregistrement
    connexion.commit()  # valider les modifications
    id = curseur.execute("SELECT max(Parties.id_Partie) FROM Parties")  # recherche la dernière partie de la table
    id = id.fetchone()  # conversion en liste
    connexion.close()   # déconnexion de la base de données
    return id[0]

def insert_liaison(a = int, b = str):
    """
    Entrées : a (int)   : Numéro d'identification de la partie
              b (str)   : Pseudo du joueur

    Ajoute une nouvelle liaison entre le pseudo du joueur et la nouvelle partie
    """
    
    connexion = sqlite3.connect(os.path.join(DATA_DIR, 'sauvegarde.db'))    # connexion à la base de données
    curseur = connexion.cursor()
    curseur.execute("""INSERT INTO Liaison VALUES (?,?)""",(a,b))   # crée un nouvel enregistrement
    connexion.commit()  # valide les modifications
    connexion.close()   # déconnexion de la base de données