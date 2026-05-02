#Projet : Mimesis
#Auteur : Noah LARZILLIERE

'------------------------------------------------------------------------------------------------------------'

                    #   Importations 

import sqlite3
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datas')    # chemin vers le répertoire data

'------------------------------------------------------------------------------------------------------------'

                    # Création des différentes tables


connexion = sqlite3.connect(os.path.join(DATA_DIR, 'sauvegarde.db'))    # connexion à la base de données
curseur = connexion.cursor()
curseur.execute("DROP TABLE IF EXISTS Joueurs") # supprime la table si elle existe déjà
curseur.execute("""CREATE TABLE Joueurs (pseudo TEXT PRIMARY KEY, oeuvre1 BOOLEAN, oeuvre2 BOOLEAN, oeuvre3 BOOLEAN)""")    # création de la table Joueurs
connexion.commit()  # valide les modifications
connexion.close()   # déconnexion de la base de données

connexion = sqlite3.connect(os.path.join(DATA_DIR, 'sauvegarde.db'))# connexion à la base de données
curseur = connexion.cursor()
curseur.execute("DROP TABLE IF EXISTS Parties") # supprime la table si elle existe déjà
curseur.execute("""CREATE TABLE Parties (id_Partie INTEGER PRIMARY KEY AUTOINCREMENT, position_x INTEGER, position_y INTEGER, interaction1 BOOLEAN, interaction2 BOOLEAN, interaction3 BOOLEAN, interaction4 BOOLEAN, interaction5 BOOLEAN)""") # création de la table Parties
connexion.commit()  # valide les modifications
connexion.close()   # déconnexion de la base de données

#Création de la table Liaison
connexion = sqlite3.connect(os.path.join(DATA_DIR, 'sauvegarde.db'))    # connexion à la base de données
curseur = connexion.cursor()
curseur.execute("DROP TABLE IF EXISTS Liaison") # supprime la table si elle existe déjà
curseur.execute("""CREATE TABLE Liaison (id_Partie INTEGER, pseudo TEXT, FOREIGN KEY(id_Partie) REFERENCES Parties(id_Partie), FOREIGN KEY(pseudo) REFERENCES Joueurs(pseudo))""")   # création de la table Liaison
connexion.commit()  # valide les modifications
connexion.close()   # déconnexion de la base de données