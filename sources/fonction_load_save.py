# Projet : Mimesis
# Auteur : Joan GUILBERT

'------------------------------------------------------------------------------------------------------------'

                    #   Importations 

import pygame as py
import os
from menu_principal import menu_principal, texte, bouton, fond_texte
from gestion_ecran import is_fullscreen
from chargement_parties import *
from insertion import *


'------------------------------------------------------------------------------------------------------------'

                    # Définition des fonctions et variables

def init(format, size):
    global Fen, clock 
    global barre, scroll_bar, input_rect, dir, bg
    global liste_saves, scroll, scroll_level, add_coef, coef, coef_scroll, cooldown, text, on_click, actif, scrollable, différence
    """
    Entrées : format        (bool)              : Si la fenêtre précédente était en plein écran ou en fenêtré
              size          ((int, int))        : Dimensions de l'ancienne fenêtre si fenêtré, sinon None

    Sorties : Fen           (pygame.Surface)    : Fenêtre sur laquelle se déroule le chargement de sauvegarde
              clock         (pygame.Clock)      : Gère la temporalité de la fenêtre
              barre         (pygame.Rect)       : Contour de la barre de défilement
              scroll_bar    (pygame.Rect)       : Barre permettant de faire monter ou descendre la liste des sauvegardes
              input_rect,   (pygame.Rect)       : Entrée par laquelle le joueur rentre son pseudo
              liste_saves   (list)              : Liste contenant toutes les sauvegardes affiliées au pseudo du joueur
              scroll        (int)               : Niveau de défilement par molette
              scroll_level  (int)               : Niveau de défilement manuel
              add_coef      (int / float)       : Coefficient ajouté à la barre de défilement pour suivre le niveau de défilement
              coef          (int / float)       : Coefficient entre la barre de défilement et l'ensemble des sauvegardes
              coef_scroll   (int / float)       : Coefficient entre le défilement par molette et la barre de défilement
              cooldown      (int)               : Sécurité empêchant la création de plusieurs sauvegardes en un clic
              text          (str)               : Contient le pseudo du joueur
              on_click      (bool)              : Si le joueur appuie, permet le défilement manuel
              actif         (bool)              : Si la zone de texte est saisie, active la saisie du texte
              scrollable    (bool)              : Si un défilement est possible
              différence    (bool)              : Si l'on passe de défilement manuel à molette ou inversement

    Initialise et renvoie la fenêtre, les éléments graphiques et les variables du programme
    """

    py.init()                                                       # |
    if format:                                                      # |
        Fen = py.display.set_mode((0, 0), py.FULLSCREEN)            # | initialisation
    else:                                                           # | de la fenêtre
        Fen = py.display.set_mode((size[0], size[1]), py.RESIZABLE) # |
    clock = py.time.Clock()                                         # |

    barre = py.rect.Rect(Fen.get_width() // 2 + 220, 100, 20, Fen.get_height() - 200)           # |
    scroll_bar = py.rect.Rect(Fen.get_width() // 2 + 220, 100, 20, Fen.get_height() - 200)      # | initalisation des éléments graphiques
    input_rect = py.rect.Rect(Fen.get_width() // 2 - 450, Fen.get_height() // 2 - 35, 200, 70)  # |

    dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datas') # chemin vers le répertoire data

    bg = py.image.load(os.path.join(dir, "wall.png")).convert_alpha()       # | importation
    bg = py.transform.smoothscale(bg, (bg.get_width(), bg.get_height()))    # | des images
    
    liste_saves = []    # |
    scroll = 0          # |
    scroll_level = 0    # |
    add_coef = 0        # |
    coef = 0            # |
    coef_scroll = 0     # | initialisation
    cooldown = 0        # | des variables
    text = ''           # |
    on_click = False    # |
    actif = False       # |
    scrollable = False  # |
    différence = False  # |

def extract(text):
    global scroll_bar, liste_saves, add_coef, coef, coef_scroll, scrollable
    """
    Entrées : text          (str)               : Contient le pseudo du joueur
              barre         (pygame.Rect)       : Contour de la barre de défilement
              scroll_bar    (pygame.Rect)       : Barre permettant de faire monter ou descendre la liste des sauvegardes              

    Sorties : scroll_bar    (pygame.Rect)       : Barre permettant de faire monter ou descendre la liste des sauvegardes
              liste_saves   (list)              : Liste contenant toutes les sauvegardes affiliées au pseudo du joueur
              add_coef      (int / float)       : Coefficient ajouté à la barre de défilement pour suivre le niveau de défilement
              coef          (int / float)       : Coefficient entre la barre de défilement et l'ensemble des sauvegardes
              coef_scroll   (int / float)       : Coefficient entre le défilement par molette et la barre de défilement
              scrollable    (bool)              : Si un défilement est possible

    Recherche si le pseudo existe dans la BDD et le crée si ce n'est pas le cas, puis recherche les parties associées et modifie l'affichage selon le nombre de parties
    """

    if text != '':  # vérifie que l'entrée de texte n'est pas vide
        if search_joueur(text) == []:   # si le pseudo n'existe pas
            insert_joueur(text)
            liste_saves = []
        else:
            liste_saves = search_partie(text)
    
    if len(liste_saves) * 160 - 10 > barre.height:  # si l'ensemble des sauvegardes à afficher dépasse la barre (représentant la fenêtre)
        coef = (len(liste_saves) * 160 - 10) / barre.height                                                                         # |
        scroll_bar.height = round(barre.height / coef)                                                                              # | modifie la barre
        coef_scroll = ((len(liste_saves) * 160 + 200) - len(liste_saves) - Fen.get_height()) / (barre.height - scroll_bar.height)   # | de défilement selon 
        add_coef = scroll_bar.centery                                                                                               # | le nombre de sauvegardes
        scrollable = True                                                                                                           # |
    else:
        coef = 0                                                                                # |
        scroll_bar = py.rect.Rect(Fen.get_width() // 2 + 220, 100, 20, Fen.get_height() - 200)  # | remet la barre
        coef_scroll = 0                                                                         # | de défilement
        add_coef = 0                                                                            # | par défaut
        scrollable = False                                                                      # |
        
def new_save(text, touches):
    global cooldown, liste_saves
    """
    Entrées : text          (str)           : Contient le pseudo du joueur
              touches       (Touches)       : Informations concernant les touches utilisées dans le jeu
              cooldown      (int)           : Sécurité empêchant la création de plusieurs sauvegardes en un clic
              liste_saves   (list)          : Liste contenant toutes les sauvegardes affiliées au pseudo du joueur

    Sorties : cooldown      (int)           : Sécurité empêchant la création de plusieurs sauvegardes en un clic

    Crée une nouvelle sauvegarde et réinitialise le cooldown du bouton associé
    """

    if cooldown <= 0:   # empêche la création de plusieurs sauvegardes en un clic
        cooldown = 10
        if text != "":  # vérifie que l'entrée de texte n'est pas vide
            if search_joueur(text) == []:   # si le pseudo n'existe pas
                insert_joueur(text)
            id = insert_partie()
            insert_liaison(id, text)
            liste_saves = search_partie(text)
            select(-1, touches, "new")

def select(i, touches, avancée = None):
    global run
    """
    Entrées : i         (int)           : Numéro de sauvegarde
              touches   (Touches)       : Informations concernant les touches utilisées dans le jeu
              avancée   (str / None)    : Si il s'agit d'une nouvelle partie, sinon None
              run       (bool)          : Si la boucle de chargement de sauvegarde continue ou s'arrête

    Sorties : run       (bool)          : Si la boucle de chargement de sauvegarde continue ou s'arrête

    Exécute la partie jeu selon le fichier de sauvegarde sélectionné et met fin à la boucle de chargement de sauvegarde
    """

    from Game import jeu    # empêche les fonctions de boucler entre elles
    run = False
    partie = liste_saves[i]
    jeu(partie, touches, is_fullscreen(), Fen.get_size(), avancée) # appel de la partie jeu

'------------------------------------------------------------------------------------------------------------'

                    # Fonction principale

def load_save(touches, format, size):
    global Fen, barre, scroll_bar, input_rect, scroll, scroll_level, add_coef, coef, coef_scroll, cooldown, text, on_click, actif, scrollable, différence
    """
    Entrées : touches       (Touches)           : Informations concernant les touches utilisées dans le jeu
              format        (bool)              : Si la fenêtre précédente était en plein écran ou en fenêtré
              size          ((int, int))        : Dimensions de l'ancienne fenêtre si fenêtré, sinon None
              Fen           (pygame.Surface)    : Fenêtre sur laquelle se déroule le chargement de sauvegarde
              barre         (pygame.Rect)       : Contour de la barre de défilement
              scroll_bar    (pygame.Rect)       : Barre permettant de faire monter ou descendre la liste des sauvegardes
              input_rect,   (pygame.Rect)       : Entrée par laquelle le joueur rentre son pseudo
              scroll        (int)               : Niveau de défilement par molette
              scroll_level  (int)               : Niveau de défilement manuel
              add_coef      (int / float)       : Coefficient ajouté à la barre de défilement pour suivre le niveau de défilement
              coef          (int / float)       : Coefficient entre la barre de défilement et l'ensemble des sauvegardes
              coef_scroll   (int / float)       : Coefficient entre le défilement par molette et la barre de défilement
              cooldown      (int)               : Sécurité empêchant la création de plusieurs sauvegardes en un clic
              text          (str)               : Contient le pseudo du joueur
              on_click      (bool)              : Si le joueur appuie, permet le défilement manuel
              actif         (bool)              : Si la zone de texte est saisie, active la saisie du texte
              scrollable    (bool)              : Si un défilement est possible
              différence    (bool)              : Si l'on passe de défilement manuel à molette ou inversement

    Sorties : Fen           (pygame.Surface)    : Fenêtre sur laquelle se déroule le chargement de sauvegarde
              add_coef      (int / float)       : Coefficient ajouté à la barre de défilement pour suivre le niveau de défilement
              cooldown      (int)               : Sécurité empêchant la création de plusieurs sauvegardes en un clic
              différence    (bool)              : Si l'on passe de défilement manuel à molette ou inversement

    Boucle principale du chargement de sauvegardes, s'occupe d'afficher la fenêtre et l'ensemble des éléments graphiques et gère les différentes fonctionnalitées liées au chargement de sauvegardes
    """

    init(format, size)  # initialise les variables nécessaires à l'ensemble du fichier

    resizing = False
    run = True
    while run:  # boucle principale
        for event in py.event.get():    # gestion des événements
            if event.type == py.QUIT:   # met fin à la boucle
                run = False
                py.quit()
            if event.type == py.VIDEORESIZE:                                # |
                new_w = max(event.w, 1024)                                  # |
                new_h = max(event.h, 768)                                   # |
                if new_w != event.w or new_h != event.h:                    # | gestion de la taille
                    Fen = py.display.set_mode((new_w, new_h), py.RESIZABLE) # | de fenêtre minimale
                scroll = 0                                                  # |
                scroll_level = 0                                            # |
                resizing = True                                             # |
            if event.type == py.MOUSEBUTTONDOWN:
                if barre.left < py.mouse.get_pos()[0] < barre.right and barre.top < py.mouse.get_pos()[1] < barre.bottom:   # |
                    actif = False                                                                                           # | active le défilement avec la barre
                    on_click = True                                                                                         # |
                if input_rect.collidepoint(py.mouse.get_pos()): # |
                    actif = True                                # |
                    text = ''                                   # | rend la zone de texte interactive
                else:                                           # |
                    actif = False                               # |
            if event.type == py.MOUSEBUTTONUP:  # désactive le défilement avec la barre
                on_click = False
            if event.type == py.MOUSEWHEEL and scrollable: # défilement avec la molette de la souris
                if différence:                                                                              # |
                    scroll = - scroll_level // 10 * 10                                                      # | réinitialise le défilement
                    add_coef = barre.top + scroll_bar.height // 2 + (10 / coef_scroll) * (- scroll / 10)    # | manuel et l'adapte à 
                    scroll_level = 0                                                                        # | celui de la molette
                    différence = False                                                                      # |

                if event.y > 0 and scroll - scroll_level < 0:   # |
                    scroll += 10                                # | fait descendre
                    add_coef -= 10 / coef_scroll                # | les sauvegardes
                    scroll_bar.centery = round(add_coef)        # |
                    
                if event.y < 0 and scroll - scroll_level + (len(liste_saves) * 160 - 10) > Fen.get_height() - 200:  # |
                    scroll -= 10                                                                                    # |
                    add_coef += 10 / coef_scroll                                                                    # |
                    if add_coef > barre.bottom - scroll_bar.height // 2:                                            # | fait monter les sauvegardes
                        scroll_bar.centery = barre.bottom - scroll_bar.height // 2                                  # |
                    else:                                                                                           # |
                        scroll_bar.centery = round(add_coef)                                                        # |
                        
            if event.type == py.KEYDOWN:
                if actif:   # entrée du texte dans la zone de texte
                    if event.key == py.K_BACKSPACE: # enlève le dernier caractère
                        text = text[:-1]
                    elif event.key == py.K_ESCAPE:  # sort de la zone de texte
                        actif = False
                    elif event.key == py.K_RETURN and text != "":   # exécute la fontion de recherche lorsque la zone de texte n'est pas vide
                        actif = False
                        extract(text)
                    elif not(event.key in (py.K_TAB, py.K_CAPSLOCK, py.K_LSHIFT, py.K_RSHIFT, py.K_LCTRL, py.K_RCTRL, py.K_LSUPER, py.K_RSUPER, py.K_LALT, py.K_RALT, py.K_KP_ENTER, py.K_NUMLOCK, py.K_NUMLOCKCLEAR, py.K_PAGEUP, py.K_PAGEDOWN, py.K_HOME, py.K_END, py.K_DELETE, py.K_INSERT, py.K_LMETA, py.K_RMETA, py.K_PAUSE, py.K_SCROLLLOCK, py.K_PRINTSCREEN, py.K_F1, py.K_F2, py.K_F3, py.K_F4, py.K_F5, py.K_F6, py.K_F7, py.K_F8, py.K_F9, py.K_F10, py.K_F11, py.K_F12)):    # ajoute le caractère entré par l'utilisateur
                        text += event.unicode
                else:
                    if event.key == py.K_ESCAPE:    # retour au menu principal
                        run = False
                        menu_principal(load_save, touches)  # appel du menu principal

        if on_click:                                                                                                    # |
            scroll = 0                                                                                                  # |
            if barre.top + scroll_bar.height // 2 <= py.mouse.get_pos()[1] <= barre.bottom - scroll_bar.height // 2:    # |
                mouse_y = py.mouse.get_pos()[1]                                                                         # |
                scroll_bar.centery = mouse_y                                                                            # |
                scroll_level = round(coef * (scroll_bar.centery - 100 - scroll_bar.height // 2))                        # | gère le défilement avec la barre et bouge la
            elif py.mouse.get_pos()[1] < barre.top + scroll_bar.height // 2:                                            # | barre de défilement selon la position de la souris
                scroll_bar.centery = barre.top + scroll_bar.height // 2                                                 # |
                scroll_level = 0                                                                                        # |
            elif py.mouse.get_pos()[1] > barre.bottom - scroll_bar.height // 2:                                         # |
                scroll_bar.centery = barre.bottom - scroll_bar.height // 2 - 1                                          # |
                scroll_level = round(coef * (barre.bottom - scroll_bar.height - 100))                                   # |
            différence = True

        Fen.fill('black')                                                                                                                                                       # |
        Fen.blit(bg, (Fen.get_width() // 2 - bg.get_width() // 2, Fen.get_height() // 2 - bg.get_height() // 2))                                                                # |
                                                                                                                                                                                # |
        for i in range(len(liste_saves)):                                                                                                                                       # |
            décalage = scroll - scroll_level + i * 160                                                                                                                          # |
            bouton("save_file.png", "save_file_pressed.png", Fen.get_width() // 2 - 190, 100 + décalage, 400, 150, lambda : select(i, touches))                                 # |
            save_num_surf, save_num_rect = texte(str(i + 1), 50)                                                                                                                # |
            save_num_rect.center = (Fen.get_width() // 2 + 10, 100 + décalage + 75)                                                                                             # |
            Fen.blit(save_num_surf, save_num_rect)                                                                                                                              # |
                                                                                                                                                                                # |
        py.draw.rect(Fen, 'white', scroll_bar, 0, 3)                                                                                                                            # |
        py.draw.rect(Fen, 'lightgrey', barre, 3, 3)                                                                                                                             # |
                                                                                                                                                                                # |
        if not is_fullscreen() and resizing:    # s'il y a un redimensionnement de la fenêtre                                                                                   # |
            barre = py.rect.Rect(Fen.get_width() // 2 + 220, 100, 20, Fen.get_height() - 200)           # |                                                                     # | affichage des
            scroll_bar = py.rect.Rect(Fen.get_width() // 2 + 220, 100, 20, scroll_bar.height)           # |                                                                     # | éléments graphiques
            input_rect = py.rect.Rect(Fen.get_width() // 2 - 450, Fen.get_height() // 2 - 35, 200, 70)  # | redéfinition des éléments graphiques                                # |
            extract(text)                                                                               # |                                                                     # |
            resizing = False                                                                            # |                                                                     # |
                                                                                                                                                                                # |
        fond_texte(Fen.get_width() // 2 - 500, 0, 300, Fen.get_height(), 'black', 150)                                                                                          # |
        py.draw.rect(Fen, 'white', input_rect, 3, 10)                                                                                                                           # |
        input_surf, input_rect_ = texte(text, 40)                                                                                                                               # |
        input_rect_.center = input_rect.center                                                                                                                                  # |
        text_surf, text_rect = texte("Entrez votre pseudo", 35)                                                                                                                 # |
        text_rect.center = (input_rect.centerx, input_rect.centery - 70)                                                                                                        # |
        Fen.blit(text_surf, text_rect)                                                                                                                                          # |
        Fen.blit(input_surf, input_rect_)                                                                                                                                       # |
                                                                                                                                                                                # |
        bouton("nouvelle_partie.png", "nouvelle_partie_pressed.png", input_rect.centerx - 147, input_rect.bottom + 20, 1764 // 6, 1044 // 6, lambda : new_save(text, touches))  # |
        if cooldown > 0:    # gère le compte à rebour du bouton
            cooldown -= 1

        py.display.flip()   # | mise à jour
        clock.tick(60)      # | de la fenêtre

'------------------------------------------------------------------------------------------------------------'

                    # Exécution manuelle du fichier

if __name__ == '__main__':
    from controles import Touches
    load_save(touches = Touches(), format = True, size = None)
    py.quit()