# Projet : Mimesis
# Auteur : Paul MUNOZ, Joan GUILBERT

'------------------------------------------------------------------------------------------------------------'

                    #   Importations 

import pygame
from menu_principal import afficher_texte_menu, bouton, texte, fond_texte, bg
from gestion_ecran import ecran, horloge

'------------------------------------------------------------------------------------------------------------'

                    # Définition des fonctions et variables

def menu_crédits():
    global ecran
    """
    Entrées : ecran (pygame.Surface)    : Fenêtre générale pour tout les menus

    Sorties : ecran (pygame.Surface)    : Fenêtre générale pour tout les menus

    Affiche le menu des crédits
    """

    def close_menu():
        nonlocal menu
        """
        Entrées : menu  (bool)  : Si la boucle des crédits continue ou s'arrête

        Sorties : menu  (bool)  : Si la boucle des crédits continue ou s'arrête

        Met fin au menu des crédits
        """
        
        menu = False
    
    texte_credit = [
        "»»-———— Développeurs ————-««",
        "",
        "Paul MUNOZ",
        "Joan GUILBERT",
        "Noah LARZILLIÈRE",
        "",
        "»»-———— Graphiste ————-««",
        "",
        "Eloïse GUILBERT",
        "",
        "»»-————  Crée  Pour  ————-««",
        "",
        "Trophées NSI",
        "2025",
        "",
        "»»-————    Classe    ————-««",
        "",
        "Terminale Générale (NSI)",
        "Institut Lemonnier",
        "Caen"
    ]

    menu = True
    while menu: # boucle principale
        for event in pygame.event.get():    # gestion des événements
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
        afficher_texte_menu("-- MIMESIS --")                                                                            # |

        ecran_largeur, ecran_hauteur = ecran.get_size()     # |
        zone_haut = 300                                     # | calcul de la zone
        zone_bas = 250                                      # | d'affichage des crédits
        espace_dispo = ecran_hauteur - zone_haut - zone_bas # |
        
        nb_lignes = len(texte_credit)                                   # |
        taille_max = int(min(50, espace_dispo // (nb_lignes * 0.8)))    # | calcul de la taille du texte
        taille_police = max(24, taille_max)                             # |
        
        def get_line_height(i):
            """
            Entrées : i                             (str)   : Ligne du texte

            Sorties : return int(taille_police * x) (int)   : Taille des espacements
            """

            if texte_credit[i].strip() == "":   # Si on saute une ligne
                return int(taille_police * 0.5)  # 50% de l'espacement normal
            return int(taille_police * 1.0)  # espacement normal
        
        total_hauteur = sum(get_line_height(i) for i in range(nb_lignes))   # |
        y_start = zone_haut + (espace_dispo - total_hauteur) // 2           # | calcul des placements des lignes du texte
        y_offset = 0                                                        # |

        for i, line in enumerate(texte_credit):                         # |
            TextSurf, TextRect = texte(line, taille_police)             # |
            TextRect.center = (ecran_largeur // 2, y_start + y_offset)  # | affiche chaque ligne du texte
            ecran.blit(TextSurf, TextRect)                              # |
            y_offset += get_line_height(i)                              # | 

        bouton("retour.png", "retour_pressed.png", ecran_largeur // 2 - 150, ecran_hauteur - 130, 300, 111, close_menu) # affichage du bouton de fin du menu

        texte_surface= texte("Appuyez sur ECHAP pour retourner au menu principal")[0]   # | rappel de retour au menu
        pygame.display.get_surface().blit(texte_surface, (10, 10))                      # | principal en appuyant sur ECHAP

        pygame.display.update() # | mise à jour
        horloge.tick(60)        # | de la fenêtre

'------------------------------------------------------------------------------------------------------------'

                    # Exécution manuelle du fichier

if __name__ == '__main__':
    menu_crédits()
    pygame.quit()