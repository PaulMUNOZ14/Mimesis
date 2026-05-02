# Projet : Mimesis
# Auteur : Paul MUNOZ, Joan GUILBERT

'------------------------------------------------------------------------------------------------------------'

                    #   Importations 

import pygame
from menu_principal import afficher_texte_menu, bouton, texte, fond_texte, bg
from gestion_ecran import is_fullscreen, toggle_fullscreen, ecran, horloge

'------------------------------------------------------------------------------------------------------------'

                    #   Définition des fonctions et variables 

def menu_réglages(touches):
    global ecran
    """
    Entrées : touches   Touches)            : Informations concernant les touches utilisées dans le jeu
              ecran     (pygame.Surface)    : Fenêtre générale pour tout les menus
            
    Sorties : ecran     (pygame.Surface)    : Fenêtre générale pour tout les menus
        
    Affiche le menu des réglages
    """

    def close_menu():
        nonlocal menu
        """
        Entrées : menu  (bool)  : Si la boucle des crédits continue ou s'arrête

        Sorties : menu  (bool)  : Si la boucle des crédits continue ou s'arrête

        Met fin au menu des réglages
        """
        
        menu = False

    menu = True
    while menu: # boucle principale
        for event in pygame.event.get():    # gestion des événements
            touches.handle_event(event) # vérifie si une touche est en train d'être changée
            if event.type == pygame.QUIT:   # met fin à la boucle
                menu = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    # met fin à la boucle
                    menu = False
            if event.type == pygame.VIDEORESIZE:                                # |
                new_w = max(event.w, 1024)                                      # |
                new_h = max(event.h, 768)                                       # | gestion de la taille de fenêtre minimale
                if new_w != event.w or new_h != event.h:                        # |
                    pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)   # |

        ecran.fill('black')                                                                                             # |
        ecran.blit(bg, (ecran.get_width() // 2 - bg.get_width() // 2, ecran.get_height() // 2 - bg.get_height() // 2))  # | affichage des fonds
        fond_texte(ecran.get_width() // 2 - 375, 0, 750, ecran.get_height(), 'black', 150)                              # | et du titre du menu
        afficher_texte_menu("Réglages")                                                                                 # |

        if is_fullscreen(): # l'image du bouton de mode de fenêtre est en plein écran
            fs_image = ("fullscreen.png", "fullscreen_pressed.png")
        else:               # l'image du bouton de mode de fenêtre est en fenêtré
            fs_image = ("windowed.png", "windowed_pressed.png")
        
        texte_touches_changer = [
            "Avancer",
            "Reculer",
            "Droite",
            "Gauche",
            "Interagir"
        ]
        actions = ['avancer', 'reculer', 'droite', 'gauche', 'interagir']

        ecran_largeur, ecran_hauteur = ecran.get_size()   
        bouton(fs_image[0], fs_image[1], ecran.get_width() // 2 - 350, ecran.get_height() // 2 - 50, 100, 100, toggle_fullscreen)   # affichage du bouton de mode de fenêtre

        for i, action in enumerate(actions):                                                                                                                    # |
            line = texte_touches_changer[i]                                                                                                                     # |
            TextSurf, TextRect = texte(line, 50)                                                                                                                # |
            TextRect.left = ecran_largeur // 2 - 90                                                                                                             # |
            TextRect.centery = ecran_hauteur // 2 - 200 + i * 100                                                                                               # |
            ecran.blit(TextSurf, TextRect)                                                                                                                      # | affichage des actions et leur touche associée
                                                                                                                                                                # | et des boutons pour changer les touches
            bouton("binding.png", "binding_pressed.png", ecran_largeur // 2 - 200 , TextRect.centery - 43, 90, 87, lambda a = action : touches.start_edit(a))   # |
                                                                                                                                                                # |
            touche_surf, touche_rect = texte(touches.bindings[action], 50)                                                                                      # |
            touche_rect.center = (ecran_largeur // 2 - 155, TextRect.centery)                                                                                   # |
            ecran.blit(touche_surf, touche_rect)                                                                                                                # |

        bouton("retour.png", "retour_pressed.png", ecran_largeur // 2 - 150, ecran_hauteur - 130, 300, 111, close_menu) # affichage du bouton de fin du menu

        texte_surface = texte("Appuyez sur ECHAP pour retourner en arrière")[0] # | rappel de retour au menu
        pygame.display.get_surface().blit(texte_surface, (10, 10))              # | principal en appuyant sur ECHAP

        pygame.display.flip()   # | mise à jour
        horloge.tick(60)        # | de la fenêtre

'------------------------------------------------------------------------------------------------------------'

                    # Exécution manuelle du fichier

if __name__ == '__main__':
    from controles import Touches
    menu_réglages(touches = Touches())
    pygame.quit()