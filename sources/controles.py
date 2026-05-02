# Projet : Mimesis
# Auteur : Paul MUNOZ

'------------------------------------------------------------------------------------------------------------'

                    #   Importation

import pygame

'------------------------------------------------------------------------------------------------------------'

                    #   Définition de la classe

class Touches:
    """
    Attributs : bindings        (dict)  : Dictionnaire des associations action-touche
                current_edit    (str)   : Action en cours de modification, None si aucune

    Gère la configuration des touches du jeu
    """
    def __init__(self):
        """
        Initialise les touches avec leur valeur par défaut
        """
        
        self.bindings = {
            'avancer': 'UP',    # |
            'reculer': 'DOWN',  # |
            'droite': 'RIGHT',  # | peut être modifié ici pour ne pas avoir à changer à chaque fois
            'gauche': 'LEFT',   # |
            'interagir': 'F'    # |
        }
        self.current_edit = None    # par défaut, aucune touche en cours de modification

    def get_key_name(self, key):
        """
        Entrées : key                           (int)   : Code de la touche selon pygame

        Sorties : pygame.key.name(key).upper()  (str)   : Nom en majuscule de la touche

        Convertit un code de touche pygame en son nom de touche
        """

        return pygame.key.name(key).upper()

    def start_edit(self, action):
        """
        Entrées : action    (str)   : Nom de l'action à modifier

        Démarre le processus de modification de touche en explicitant l'action associée
        """

        self.current_edit = action

    def handle_event(self, event):
        """
        Entrées : event (pygame.Event)  : Événement quelconque renvoyé par le menu des réglages

        Modifie la touche selon l'action associée et selon la touche appuyée par le joueur
        """

        if self.current_edit and event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE: # si une touche est à modifier et si le joueur appuie sur une touche
            self.bindings[self.current_edit] = self.get_key_name(event.key) # modifie la touche selon l'action
            self.current_edit = None    # remet la modification de touche par défaut
