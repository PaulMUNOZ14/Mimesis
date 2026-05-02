# Projet : Mimesis
# Auteur : Paul MUNOZ, Joan GUILBERT

'------------------------------------------------------------------------------------------------------------'

                    #   Importations 

import pygame
import os
from gestion_ecran import ecran, horloge

'------------------------------------------------------------------------------------------------------------'

                    # Définition des fonctions et variables

os.environ['SDL_VIDEO_MINIMUM_WIDTH'] = '1024'  # | configuration de la taille
os.environ['SDL_VIDEO_MINIMUM_HEIGHT'] = '768'  # | minimale de la fenêtre
pygame.font.init()  # initialisation de la police de texte

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datas')    # chemin vers le répertoire data

IMAGES = {                                                                                                                      # |
    # Boutons principaux                                                                                                        # |
    "jouer.png": pygame.image.load(os.path.join(DATA_DIR, "jouer.png")).convert_alpha(),                                        # |
    "jouer_pressed.png": pygame.image.load(os.path.join(DATA_DIR, "jouer_pressed.png")).convert_alpha(),                        # |
    "réglages1.png": pygame.image.load(os.path.join(DATA_DIR, "réglages1.png")).convert_alpha(),                                # |
    "réglages1_pressed.png": pygame.image.load(os.path.join(DATA_DIR, "réglages1_pressed.png")).convert_alpha(),                # |
    "credits.png": pygame.image.load(os.path.join(DATA_DIR, "credits.png")).convert_alpha(),                                    # |
    "credits_pressed.png": pygame.image.load(os.path.join(DATA_DIR, "credits_pressed.png")).convert_alpha(),                    # |
    "quitter.png": pygame.image.load(os.path.join(DATA_DIR, "quitter.png")).convert_alpha(),                                    # |
    "quitter_pressed.png": pygame.image.load(os.path.join(DATA_DIR, "quitter_pressed.png")).convert_alpha(),                    # |
                                                                                                                                # |
    # Options                                                                                                                   # |
    "fullscreen.png": pygame.image.load(os.path.join(DATA_DIR, "fullscreen.png")).convert_alpha(),                              # |
    "fullscreen_pressed.png": pygame.image.load(os.path.join(DATA_DIR, "fullscreen_pressed.png")).convert_alpha(),              # |
    "windowed.png": pygame.image.load(os.path.join(DATA_DIR, "windowed.png")).convert_alpha(),                                  # |
    "windowed_pressed.png": pygame.image.load(os.path.join(DATA_DIR, "windowed_pressed.png")).convert_alpha(),                  # |
    "binding.png": pygame.image.load(os.path.join(DATA_DIR, "binding.png")).convert_alpha(),                                    # |
    "binding_pressed.png": pygame.image.load(os.path.join(DATA_DIR, "binding_pressed.png")).convert_alpha(),                    # |
    "retour.png": pygame.image.load(os.path.join(DATA_DIR, "retour.png")).convert_alpha(),                                      # | préchargement de toutes
    "retour_pressed.png": pygame.image.load(os.path.join(DATA_DIR, "retour_pressed.png")).convert_alpha(),                      # | les images des boutons
                                                                                                                                # | (permet de réduire la latence)
    # fonction_load_save.py                                                                                                     # |
    "save_file.png": pygame.image.load(os.path.join(DATA_DIR, "save_file.png")).convert_alpha(),                                # |
    "save_file_pressed.png": pygame.image.load(os.path.join(DATA_DIR, "save_file_pressed.png")).convert_alpha(),                # |
    "nouvelle_partie.png": pygame.image.load(os.path.join(DATA_DIR, "nouvelle_partie.png")).convert_alpha(),                    # |
    "nouvelle_partie_pressed.png": pygame.image.load(os.path.join(DATA_DIR, "nouvelle_partie_pressed.png")).convert_alpha(),    # |
                                                                                                                                # |
    # Game.py                                                                                                                   # |
    "reprendre.png": pygame.image.load(os.path.join(DATA_DIR, "reprendre.png")).convert_alpha(),                                # |
    "reprendre_pressed.png": pygame.image.load(os.path.join(DATA_DIR, "reprendre_pressed.png")).convert_alpha(),                # |
    "réglages2.png": pygame.image.load(os.path.join(DATA_DIR, "réglages2.png")).convert_alpha(),                                # |
    "réglages2_pressed.png": pygame.image.load(os.path.join(DATA_DIR, "réglages2_pressed.png")).convert_alpha(),                # |
    "sauvegarder.png": pygame.image.load(os.path.join(DATA_DIR, "sauvegarder.png")).convert_alpha(),                            # |
    "sauvegarder_pressed.png": pygame.image.load(os.path.join(DATA_DIR, "sauvegarder_pressed.png")).convert_alpha(),            # |
    "menu_principal.png": pygame.image.load(os.path.join(DATA_DIR, "menu_principal.png")).convert_alpha(),                      # |
    "menu_principal_pressed.png": pygame.image.load(os.path.join(DATA_DIR, "menu_principal_pressed.png")).convert_alpha(),      # |
    "progression.png": pygame.image.load(os.path.join(DATA_DIR, "progression.png")).convert_alpha(),                            # |
    "progression_pressed.png": pygame.image.load(os.path.join(DATA_DIR, "progression_pressed.png")).convert_alpha()             # |
}                                                                                                                               # |                                                                                                     

bg = pygame.image.load(os.path.join(DATA_DIR, "wall.png")).convert_alpha()  # | importation de
bg = pygame.transform.smoothscale(bg, (bg.get_width(), bg.get_height()))    # | l'image de fond

active_button = None    # bouton en cours d'appui

def texte(text, taille_police = 20, police = None, couleur = 'WHITE'):
    """
    Entrées : text                      (str)                   : Texte à afficher
              taille_police             (int)                   : Taille du texte
              police                    (str)                   : Police du texte
              couleur                   ((int, int, int) / str) : Couleur du texte en RGB

    Sorties : texte_surface             (pygame.Surface)        : Surface contenant le texte rendu
              texte_surface.get_rect()  (pygame.Rect)           : Dimensions de la surface de texte
    
    Renvoie la surface et les dimensions d'un texte donné pour pouvoir l'afficher
    """

    if police is None:  # s'il n'y a pas de police
        chemin_police = os.path.join(DATA_DIR, 'LinLibertine_R.ttf')    # police par défaut
    else:
        chemin_police = os.path.join(DATA_DIR, police)

    font = pygame.font.Font(chemin_police, taille_police)   # crée le système d'écriture
    texte_surface = font.render(text, True, couleur)    # crée la surface du texte
    return texte_surface, texte_surface.get_rect()

def bouton(image_inactive, image_active, x_position, y_position, largeur, hauteur, action = None):
    global active_button
    """
    Entrées : image_inactive    (str)                   : Nom du fichier image pour l'état normal du bouton
              image_active      (str)                   : Nom du fichier image pour l'état survolé du bouton
              x_position        (int)                   : Position horizontale du coin supérieur gauche du bouton
              y_position        (int)                   : Position verticale du coin supérieur gauche du bouton
              largeur           (int)                   : Largeur du bouton
              hauteur           (int)                   : Hauteur du bouton
              action            (function)              : Fonction à exécuter lorsqu'on clique sur le bouton, None si aucune fonction n'est à appeler
              active_button     ((int, int, int, int))  : Zone du bouton en cours d'appui, None si aucun bouton n'est appuyé

    Sorties : active_button     ((int, int, int, int))  : Zone du bouton en cours d'appui, None si aucun bouton n'est appuyé

    Crée et affiche un bouton interatif avec une image pour chaque état (normal et actif) et qui effectue une action donnée
    """
    
    mouse_pos = pygame.mouse.get_pos()  # position de la souris
    mouse_pressed = pygame.mouse.get_pressed()  # pressions des clics et boutons de la souris
    survol = x_position < mouse_pos[0] < x_position + largeur and y_position < mouse_pos[1] < y_position + hauteur  # si la souris se trouve sur la zone du bouton ou non

    image_inactive_surface = IMAGES[image_inactive] # | charge les images
    image_active_surface = IMAGES[image_active]     # | associées au bouton

    image_inactive_surface = pygame.transform.scale(image_inactive_surface, (largeur, hauteur)) # | redimensionne les
    image_active_surface = pygame.transform.scale(image_active_surface, (largeur, hauteur))     # | images comme voulu

    if not image_active_surface.get_locked() or not image_inactive_surface.get_locked():
        if survol:  # affiche le bouton comme actif
            ecran.blit(image_active_surface, (x_position, y_position))
        else:       # affiche le bouton comme normal
            ecran.blit(image_inactive_surface, (x_position, y_position))

    if survol and mouse_pressed[0]: # si le joueur clic sur la zone du bouton
        if active_button is None:   # si aucun autre bouton n'est appuyé
            active_button = (x_position, y_position, largeur, hauteur)
    
    if active_button == (x_position, y_position, largeur, hauteur): # si le bouton appuyé est le bouton actuel
        if not survol:  # si la souris n'est plus sur le bouton
            active_button = None    # annule l'appui
            return
        if not mouse_pressed[0]:    # si le bouton est relâché
            if survol and action is not None:   # si une action est donnée et si la souris est encore sur la zone du bouton
                active_button = None
                action()  # Appel la fonction donnée

def fond_texte(left, top, w, h, color, opac):
    """
    Entrées : left  (int)                   : Position horizontale du coin supérieur gauche de la zone de fond
              top   (int)                   : Position verticale du coin supérieur gauche de la zone de fond
              w     (int)                   : Largeur de la zone de fond
              h     (int)                   : Hauteur de la zone de fond
              color ((int, int, int) / str) : Couleur de la zone de fond
              opac  (int)                   : Opacité de la surface, entre 0 et 255

    Sorties : Ø     (pygame.Surface)        : Applique la zone de fond

    Applique un fond d'une couleur et d'une opacité définie, permet de mieux visuliser les textes
    """
    
    fond = pygame.surface.Surface((w, h))   # défini une surface
    fond.fill(color)    # applique une couleur définie
    fond.set_alpha(opac)    # change l'opacité de la surface
    ecran.blit(fond, pygame.rect.Rect(left, top, w, h)) # applique la surface sur la fenêtre

def afficher_texte_menu(text, police = None, couleur = "WHITE"):
    """
    Entrées : text      (str)                   : Titre du menu
              police    (str)                   : Police voulue pour le titre
              couleur   ((int, int, int) / str) : Couleur du titre
        
    Sorties : Ø         (pygame.Surface)        : Applique la surface de texte
    
    Affiche le titre du menu actuel en haut de l'écran (plus spécifique que la fonction texte())
    """

    ecran_largeur = ecran.get_size()[0]
    texte_surface, texte_rect = texte(text, 70, police, couleur)    # définit la surface et la dimension de la zone de texte
    texte_rect.center = (ecran_largeur // 2, 100)   # positionne le texte centré en haut du menu
    ecran.blit(texte_surface, texte_rect)   # applique la surface sur la fenêtre

def menu_principal(fonc_jeu, touches):
    global ecran, active_button
    """
    Entrées : fonc_jeu          (fonction)              : Contient la fonction load_save() pour continuer vers le jeu
              touches           (Touches)               : Informations concernant les touches utilisées dans le jeu
              ecran             (pygame.Surface)        : Fenêtre générale pour tout les menus
              active_button     ((int, int, int, int))  : Zone du bouton en cours d'appui, None si aucun bouton n'est appuyé

    Sorties : ecran             (pygame.Surface)        : Fenêtre générale pour tout les menus
              active_button     ((int, int, int, int))  : Zone du bouton en cours d'appui, None si aucun bouton n'est appuyé
    
    Affiche le menu principal
    """

    pygame.mouse.set_visible(True)                                              # | remet la souris visible et
    pygame.mouse.set_pos((ecran.get_width() / 2), ecran.get_height() / 2 - 2)   # | au centre de la fenêtre

    def close_menu():
        nonlocal menu
        """
        Entrées : menu  (bool)  : Si la boucle du menu principal continue ou s'arrête

        Sorties : menu  (bool)  : Si la boucle du menu principal continue ou s'arrête

        Met fin au menu principal et renvoie au menu de chargement de sauvegarde
        """
        
        menu = False
        from menu_réglages import is_fullscreen # empêche les problèmes d'appel en boucle
        fonc_jeu(touches, is_fullscreen(), ecran.get_size())    # appel du menu de chargement de sauvegarde

    menu = True
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
        ecran.blit(bg, (ecran.get_width() // 2 - bg.get_width() // 2, ecran.get_height() // 2 - bg.get_height() // 2))  # | affichage des fonds
        fond_texte(ecran.get_width() // 2 - 275, 0, 550, ecran.get_height(), 'black', 150)                              # | et du titre du menu
        afficher_texte_menu("-- MIMESIS --")                                                                            # |
        
        bouton("jouer.png", "jouer_pressed.png", ecran.get_width() // 2 - 138, ecran.get_height() // 2 - 219, 276, 102, close_menu)                                 # |
        from menu_réglages import menu_réglages # empêche les problèmes d'appel en boucle                                                                           # |
        bouton("réglages1.png", "réglages1_pressed.png", ecran.get_width() // 2 - 138, ecran.get_height() // 2 - 107, 276, 102, lambda : menu_réglages(touches))    # | affichage des boutons
        from menu_crédits import menu_crédits   # empêche les problèmes d'appel en boucle                                                                           # | du menu principal
        bouton("credits.png", "credits_pressed.png", ecran.get_width() // 2 - 138, ecran.get_height() // 2 + 5, 276, 102, menu_crédits)                             # |
        bouton("quitter.png", "quitter_pressed.png", ecran.get_width() // 2 - 138, ecran.get_height() // 2 + 117, 276, 102, exit)                                   # |

        pygame.display.update() # | mise à jour
        horloge.tick(60)        # | de la fenêtre

'------------------------------------------------------------------------------------------------------------'

                    # Exécution manuelle du fichier

if __name__ == '__main__':
    from fonction_load_save import load_save
    from controles import Touches
    menu_principal(load_save, touches = Touches())
    pygame.quit()