# Projet : Mimesis
# Auteur : Paul MUNOZ, Joan GUILBERT

'------------------------------------------------------------------------------------------------------------'

                    #   Importations 

import pygame
from arbre import Arbre
from menu_principal import afficher_texte_menu, bouton, texte, bg
from gestion_ecran import ecran, horloge

'------------------------------------------------------------------------------------------------------------'

                    #   Définition des fonctions et variables 

def menu_progression(interactions):
    global ecran, nb_noeuds
    """
    Entrées : interaction   ([bool, bool, bool, bool, bool])    : Liste contenant les états d'interactions d'une partie
              ecran         (pygame.Surface)                    : Fenêtre générale pour tout les menus

    Sorties : ecran         (pygame.Surface)                    : Fenêtre générale pour tout les menus
              nb_noeuds     (dict)                              : Dictionnaire du nombre de noeuds de l'arbre par étage
    
    Affiche le menu de progression avec l'arbre de progression propre à la partie
    """
    
    menu = True

    def close_menu():
        nonlocal menu
        """
        Entrées : menu  (bool)  : Si la boucle de progression continue ou s'arrête

        Sorties : menu  (bool)  : Si la boucle de progression continue ou s'arrête

        Met fin au menu de progression
        """
        
        menu = False

    arbre = Arbre()                                                     # |
    racine = arbre.racine                                               # |
    choix1_yes = arbre.ajouter_gauche(racine, "Sécurité désactivée")    # |
    choix1_no = arbre.ajouter_droit(racine, "Sécurité activée")         # |
    choix2_1_yes = arbre.ajouter_gauche(choix1_yes, "Oeuvre volée")     # |
    choix2_1_no = arbre.ajouter_droit(choix1_yes, "Oeuvre non volée")   # |
    choix2_2_yes = arbre.ajouter_gauche(choix1_no, "Oeuvre volée")      # |
    choix2_2_no = arbre.ajouter_droit(choix1_no, "Oeuvre non volée")    # | création de l'arbre
    choix3_2_1_yes1 = arbre.ajouter_gauche(choix2_1_yes, "Fin 1")       # | de progression
    choix3_2_1_no1 = arbre.ajouter_droit(choix2_1_yes, "Fin 2")         # |
    choix3_2_1_yes2 = arbre.ajouter_gauche(choix2_1_no, "Fin 3")        # |
    choix3_2_1_no2 = arbre.ajouter_droit(choix2_1_no, "Fin 4")          # |
    choix3_2_2_yes1 = arbre.ajouter_gauche(choix2_2_yes, "Fin 5")       # |
    choix3_2_2_no1 = arbre.ajouter_droit(choix2_2_yes, "Fin 6")         # |
    choix3_2_2_yes2 = arbre.ajouter_gauche(choix2_2_no, "Fin 7")        # |
    choix3_2_2_no2 = arbre.ajouter_droit(choix2_2_no, "Fin 8")          # |

    racine.visite = True                                # |
    choix1_yes.visite = interactions[0]                 # |
    choix1_no.visite = not interactions[0]              # |
    if choix1_yes.visite:   # Sécurité désactivée       # |
        choix2_1_yes.visite= interactions[1]            # |
        choix2_1_no.visite= not interactions[1]         # |
        if choix2_1_yes.visite:     # Oeuvre volée      # |
            choix3_2_1_yes1.visite = interactions[2]    # |
            choix3_2_1_no1.visite = interactions[4]     # |
        elif choix2_1_no.visite:    # Oeuvre non volée  # | modifie les valeurs
            choix3_2_1_yes2.visite = interactions[2]    # | de l'arbre selon les
            choix3_2_1_no2.visite = interactions[4]     # | interactions effectuées
    elif choix1_no.visite:  # Sécurité activée          # |
        choix2_2_yes.visite= interactions[1]            # |
        choix2_2_no.visite= not interactions[1]         # |
        if choix2_2_yes.visite:     # Oeuvre volée      # |
            choix3_2_2_yes1.visite = interactions[2]    # |
            choix3_2_2_no1.visite = interactions[4]     # |
        elif choix2_2_no.visite:    # Oeuvre non volée  # |
            choix3_2_2_yes2.visite = interactions[2]    # |
            choix3_2_2_no2.visite = interactions[4]     # |

    while menu: # boucle principale
        for event in pygame.event.get():    # gestion des événements
            if event.type == pygame.QUIT:   # met fin à la boucle
                menu = False
                exit()
            if event.type == pygame.VIDEORESIZE:                                # |
                new_w = max(event.w, 1024)                                      # |
                new_h = max(event.h, 768)                                       # | gestion de la taille de fenêtre minimale
                if new_w != event.w or new_h != event.h:                        # |
                    pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)   # |

        ecran.fill('black')                                                                                             # |
        ecran.blit(bg, (ecran.get_width() // 2 - bg.get_width() // 2, ecran.get_height() // 2 - bg.get_height() // 2))  # | affichage des fonds et du titre du menu
        afficher_texte_menu("Arbre de progression")                                                                     # |

        zone = [ecran.get_width() - 50, ecran.get_height() - 200]   # zone maximal d'affichage de l'arbre
        nb_noeuds = {0 : 0, 1 : 0, 2 : 0, 3 : 0}    # dictionnaire des noeuds par profondeur
        
        ecran_largeur, ecran_hauteur = ecran.get_size()
        bouton("retour.png", "retour_pressed.png", ecran_largeur // 2 - 150, ecran_hauteur - 130, 300, 111, close_menu) # affichage du bouton de fin du menu

        afficher_arbre(arbre.racine, zone, profondeur = 0)  # appel de la fonction qui affiche l'arbre

        pygame.display.update() # | mise à jour
        horloge.tick(60)        # | de la fenêtre

def afficher_arbre(arbre, zone, profondeur):
    global nb_noeuds
    """
    Entrées : arbre         (Noeud)         : Arbre créé par récurrence à partir d'un certain noeud de l'arbre originel
              zone          ([int, int])    : Zone maximale sur laquelle peut s'étendre l'arbre de progression
              profondeur    (int)           : Profondeur de l'arbre actuel par rapport à l'arbre originel
              nb_noeuds     (dict)          : Dictionnaire du nombre de noeuds de l'arbre par étage
    
    Construit graphiquement un arbre binaire en utilisant la récurrence
    """
    
    if arbre is None:   # Si l'arbre est vide, ne fait rien
        return
    
    if arbre.visite:            # |
        couleur = "lightgreen"  # |
        text = arbre.texte      # | modife la couleur du fond et du
    else:                       # | texte selon les interactions faites
        couleur = "lightblue"   # |
        text = "???"            # |

    découpage_y = zone[1] // 4                                              # |
    center_y = 100 + découpage_y // 2 + profondeur * découpage_y            # |
    découpage_x = zone[0] // 2 ** profondeur                                # |
    center_x = 50 + découpage_x // 2 + nb_noeuds[profondeur] * découpage_x  # | calcul et positionnement des zones de textes
    text_surf, text_rect = texte(text, 30, couleur = 'black')               # |
    text_rect.center = (center_x, center_y)                                 # |
    arbre.position = (center_x, center_y + text_rect.height // 2 + 5)       # |

    if profondeur != 0: # Pas de lien de parenté pour la racine
        pygame.draw.aaline(ecran, 'black', (center_x, center_y - text_rect.height // 2 - 5), arbre.parent.position)                                 # | affiche chaque noeud
    pygame.draw.rect(ecran, couleur, pygame.rect.Rect(text_rect.left - 5, text_rect.top - 5 , text_rect.width + 10, text_rect.height + 10), 0, 3)   # | de l'arbre et le relie
    ecran.blit(text_surf, text_rect)                                                                                                                # | à son noeud parent

    nb_noeuds[profondeur] += 1  # modifie le nombre de noeuds positionnés par profondeur

    if arbre.gauche:    # si elle existe, recommence le processus pour la branche de gauche
        afficher_arbre(arbre.gauche, zone, profondeur = profondeur + 1) # appel de récurrence
    
    if arbre.droite:    # si elle existe, recommence le processus pour la branche de droite
        afficher_arbre(arbre.droite, zone, profondeur = profondeur + 1) # appel de récurrence

'------------------------------------------------------------------------------------------------------------'

                    # Exécution manuelle du fichier

if __name__ == '__main__':
    menu_progression([0, 0, 0, 0, 0])
    pygame.quit()