# Projet : Mimesis
# Auteur : Joan GUILBERT

'------------------------------------------------------------------------------------------------------------'

                    #   Importation 

import pygame as py

'------------------------------------------------------------------------------------------------------------'

                    # Définition des fonctions et variables

py.init()                                           # |
ecran = py.display.set_mode((0, 0), py.FULLSCREEN)  # | initialisation de la fenêtre générale des menus
horloge = py.time.Clock()                           # |

def is_fullscreen():
    """
    Sorties : bool(flags & py.FULLSCREEN)   (bool)  : Si la fenêtre est en autre chose que fenêtré

    Renvoie si la fenêtre donnée est en plein écran ou en fenêtré
    """
    
    flags = py.display.get_surface().get_flags()    # récupère les paramètres de format de la fenêtre
    return bool(flags & py.FULLSCREEN)

def toggle_fullscreen():
    global ecran
    """
    Sorties : ecran (pygame.Surface)    : Fenêtre générale pour tout les menus

    Modifie la fenêtre pour la faire basculer entre plein écran et fenêtré
    """
    
    size = py.display.get_surface().get_size()
    if is_fullscreen(): # mode fenêtré
        ecran = py.display.set_mode((size[0] - 16, size[1] - 9), py.RESIZABLE)
    else:               # mode plein écran
        ecran = py.display.set_mode((0, 0), py.FULLSCREEN)