# Projet : Mimesis
# Auteur : Joan GUILBERT

'------------------------------------------------------------------------------------------------------------'

                    #   Importations

import pygame as py
from menu_principal import texte

'------------------------------------------------------------------------------------------------------------'

                    #   Définition de la fonction principale

def intro(Fen, clock, touches):
    """
    Entrées : Fen      (pygame.Surface)    : Fenêtre sur laquelle se déroule le jeu
              clock    (pygame.Clock)      : Gère la temporalité de la fenêtre
              touches  (Touches)           : Informations concernant les touches utilisées dans le jeu

    Affiche l'introduction lors d'une nouvelle partie jusqu'à ce que le joueur appuie sur une touche
    """
    
    text = [
                "Vous incarnez un testeur de sécurité",
                "employé par le directeur du musée Mimesis",
                "afin de vérifier la sécurité du bâtiment.",
                "Votre objectif est de dérober l'œuvre maîtresse",
                "des lieux puis sortir sans vous faire attraper.",
                "",
                "Touches actuelles :",
                f"Avancer : {touches.bindings['avancer']} | Reculer : {touches.bindings['reculer']} | Gauche : {touches.bindings['gauche']} | Droite : {touches.bindings['droite']} | Intéragir : {touches.bindings['interagir']}"
            ]
    intro = True
    py.mouse.set_visible(False) # rend la souris invisible

    while intro:    # boucle d'introduction au jeu
        
        for event in py.event.get():    # gestion des événements
            if event.type == py.QUIT:   # met fin à la boucle
                intro = False
                py.quit()
                return None     # met fin au jeu
            elif event.type == py.VIDEORESIZE:                          # |
                new_w = max(event.w, 1024)                              # |
                new_h = max(event.h, 768)                               # | gestion de la taille de fenêtre minimale
                if new_w != event.w or new_h != event.h:                # |
                    py.display.set_mode((new_w, new_h), py.RESIZABLE)   # |
            if event.type == py.KEYUP:  # le joueur décide de fermer l'introduction
                intro = False
                
            Fen.fill("black")

            for i, ligne in enumerate(text):                                                                                        # |
                intro_surf, intro_rect = texte(ligne, 30, None, "white")                                                            # |
                zone_max = (intro_rect.height + 15) * len(text) - 15                                                                # |
                intro_rect.center = (Fen.get_width() // 2, Fen.get_height() // 2 - zone_max // 2 + i * (intro_rect.height + 15))    # | affichage des
                Fen.blit(intro_surf, intro_rect)                                                                                    # | textes de
                                                                                                                                    # | l'introduction
            press_surf, press_rect = texte("APPUYEZ SUR UNE TOUCHE", 50, None, "white")                                             # |
            press_rect.center = (Fen.get_width() // 2, Fen.get_height() - 40)                                                       # |
            Fen.blit(press_surf, press_rect)                                                                                        # |

            py.display.flip()   # | mise à jour
            clock.tick(60)      # | de la fenêtre

'------------------------------------------------------------------------------------------------------------'

                    # Exécution manuelle du fichier

if __name__ == '__main__':
    from controles import Touches
    py.init()
    Fen = py.display.set_mode((0, 0), py.FULLSCREEN)
    clock = py.time.Clock()
    intro(Fen, clock, touches = Touches())
    py.quit()