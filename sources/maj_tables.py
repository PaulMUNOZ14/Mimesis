#Projet : Mimesis
#Auteur : Noah LARZILLIERE

'------------------------------------------------------------------------------------------------------------'

                    #   Importations 

import sqlite3 
import os

'------------------------------------------------------------------------------------------------------------'

                    # Définition des fonctions et variables

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datas')    # chemin vers le répertoire data

def maj_parties(id_Partie, position_x, position_y, interactions) :
    """
    Entrées : id_Partie     (int)   : Numéro d'identification de la partie
              position_x    (int)   : Position horizontale du joueur
              position_y    (int)   : Position verticale du joueur
              interactions  (list)  : Liste des différentes interactions

    Met à jour la table Parties avec les valeurs données par le jeu
    """
    
    connexion = sqlite3.connect(os.path.join(DATA_DIR, 'sauvegarde.db'))    # connexion à la base de données
    curseur = connexion.cursor()
    curseur.execute("""UPDATE Parties SET position_x = ?, position_y = ?, interaction1 = ?, interaction2 = ?, interaction3 = ?, interaction4 = ?, interaction5 = ? WHERE id_Partie = ? """, (position_x, position_y, interactions[0], interactions[1], interactions[2], interactions[3], interactions[4], id_Partie))   # met à jour la table, selon le numéro d'identification
    connexion.commit()  # valide les modifications
    connexion.close()   # déconnexion de la base de données