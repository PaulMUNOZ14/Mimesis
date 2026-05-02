# Projet : Mimesis
# Auteur : Paul MUNOZ, Joan GUILBERT

'------------------------------------------------------------------------------------------------------------'

                    #   Importations 

import pygame as py
import os
from controles import Touches
from menu_principal import menu_principal, texte
from fonction_load_save import load_save
from gestion_ecran import ecran

'------------------------------------------------------------------------------------------------------------'

                    #   Appel du menu principal 

py.init()                                           # |
py.display.set_caption("Mimesis Museum")            # |
size = py.display.get_desktop_sizes()[0]            # | initialisation de la fenêtre
center = (size[0] // 2, size[1] // 2)               # |
clock = py.time.Clock()                             # |

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datas')    # chemin vers le répertoire data

bg = py.image.load(os.path.join(DATA_DIR, "wall.png")).convert_alpha()                      # |
bg = py.transform.smoothscale(bg, (bg.get_width(), bg.get_height()))                        # | importation des
title = py.image.load(os.path.join(DATA_DIR, "titre.png")).convert_alpha()                  # | images d'introduction
title = py.transform.smoothscale(title ,(title.get_width() // 4, title.get_height() // 4))  # |

icon = py.image.load(os.path.join(DATA_DIR, "icone.ico"))   # | modifie l'icone
py.display.set_icon(icon)                                   # | de la fenêtre

py.mouse.set_visible(False) # rend la souris invisible

run = True
while run:  # boucle principale
    for event in py.event.get():    # gestion des événements
        if event.type == py.QUIT:   # met fin à la boucle
            run = False
            exit()
        if event.type == py.KEYDOWN and event.key != py.K_PRINTSCREEN:    # lorsque n'importe quelle touche est appuyée
            run = False
            config_touches = Touches()  # initialisation des touches d'interactions
            menu_principal(load_save, config_touches)   # appel du menu principal

    ecran.fill('black')                                                                                                     # |
    ecran.blit(bg, (ecran.get_width() // 2 - bg.get_width() // 2, ecran.get_height() // 2 - bg.get_height() // 2))          # |
    ecran.blit(title, (ecran.get_width() // 2 - title.get_width() // 2, ecran.get_height() // 2 - title.get_height() // 2)) # | affichage du menu
    text_surf, text_rect = texte("APPUYEZ SUR UNE TOUCHE", 50)                                                              # | d'introduction
    text_rect.center = (ecran.get_width() // 2, ecran.get_height() - 40)                                                    # |
    ecran.blit(text_surf, text_rect)                                                                                        # |

    py.display.flip()   # | mise à jour
    clock.tick(60)      # | de la fenêtre