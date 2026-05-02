# Projet : Mimesis
# Auteur : Joan GUILBERT

'------------------------------------------------------------------------------------------------------------'

                    #   Importations 

import pygame as py
import os
from Salle import Salle
from Interact import Interact
from maj_tables import maj_parties
from menu_principal import menu_principal, bouton, texte, fond_texte
from menu_réglages import menu_réglages
from menu_progression import menu_progression
from gestion_ecran import is_fullscreen

'------------------------------------------------------------------------------------------------------------'

                    #   Définition des fonctions et variables 

def initialisation():
    global Fen, Fen_size, clock, resizable, plan, plan_no_cam, plan_no_vase, plan_no_all, player, player_g, player_d, key, inter_but
    """
    Sorties : Fen           (pygame.Surface)    : Fenêtre sur laquelle se déroule le jeu
              Fen_size      ((int, int))        : Dimensions de l'écran
              clock         (pygame.Clock)      : Gère la temporalité de la fenêtre
              resizable     (bool)              : Si l'écran est en fenêtré ou en plein écran
              plan          (pygame.Surface)    : Carte du jeu 
              plan_no_cam   (pygame.Surface)    : Carte du jeu avec le système de sécurité éteint
              plan_no_vase  (pygame.Surface)    : Carte du jeu sans l'oeuvre à voler
              plan_no_all   (pygame.Surface)    : Carte du jeu sans aucun des deux
              player        (pygame.Surface)    : Joueur à l'état fixe
              player_g      (pygame.Surface)    : Joueur marchant du côté gauche
              player_d      (pygame.Surface)    : Joueur marchant du côté droit
              key           (pygame.Surface)    : Clé de la porte principale
              inter_but     (pygame.Surface)    : Bouton d'intéraction

    Initialise et renvoie la fenêtre et les éléments graphiques
    """
    
    py.init()
    Fen_size = py.display.get_desktop_sizes()[0]        # |
    Fen = py.display.set_mode((0, 0), py.FULLSCREEN)    # | initialisation
    clock = py.time.Clock()                             # | de la fenêtre
    resizable = False                                   # |

    text_surf, text_rect = texte("CHARGEMENT", 40)          # |
    text_rect.center = (Fen_size[0] // 2, Fen_size[1] // 2) # | affiche CHARGEMENT lors de
    Fen.blit(text_surf, text_rect)                          # | l'initialisation de la partie
    py.display.update()                                     # |

    dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datas') # chemin vers le répertoire data

    plan = py.image.load(os.path.join(dir, "plan.png")).convert_alpha()                             # |
    plan = py.transform.smoothscale(plan, (plan.get_width() // 4, plan.get_height() // 4))          # |
    plan_no_cam = py.image.load(os.path.join(dir, "plan_no_cam.png")).convert_alpha()               # |
    plan_no_cam = py.transform.smoothscale(plan_no_cam, (plan.get_width(), plan.get_height()))      # | importation des
    plan_no_vase = py.image.load(os.path.join(dir, "plan_no_vase.png")).convert_alpha()             # | images de fond
    plan_no_vase = py.transform.smoothscale(plan_no_vase, (plan.get_width(), plan.get_height()))    # |
    plan_no_all = py.image.load(os.path.join(dir, "plan_no_all.png")).convert_alpha()               # |
    plan_no_all = py.transform.smoothscale(plan_no_all, (plan.get_width(), plan.get_height()))      # |

    player = py.image.load(os.path.join(dir, "player.png")).convert_alpha()                                     # |
    player = py.transform.smoothscale(player, (player.get_width() // 14, player.get_height() // 14))            # |
    player_g = py.image.load(os.path.join(dir, "player_g.png")).convert_alpha()                                 # | importation des
    player_g = py.transform.smoothscale(player_g, (player_g.get_width() // 14, player_g.get_height() // 14))    # | images du joueur
    player_d = py.image.load(os.path.join(dir, "player_d.png")).convert_alpha()                                 # |
    player_d = py.transform.smoothscale(player_d, (player_d.get_width() // 14, player_d.get_height() // 14))    # |

    key = py.image.load(os.path.join(dir, "clé.png")).convert_alpha()           # | importation de
    key = py.transform.smoothscale(key, (key.get_width(), key.get_height()))    # | l'image de la clé

    inter_but = py.image.load(os.path.join(dir, "binding.png")).convert_alpha()                                     # | importation de l'image
    inter_but = py.transform.smoothscale(inter_but, (inter_but.get_width() // 16, inter_but.get_height() // 16))    # | du bouton d'interaction

def observe_display(Fen):
    global etat
    """
    Entrées : Fen   (pygame.Surface)    : Fenêtre sur laquelle se déroule le jeu
              etat  (bool)              : Si la fenêtre est enregistrée en tant que plein écran ou en fenêtré

    Sorties : etat  (bool)              : Si la fenêtre est enregistrée en tant que plein écran ou en fenêtré

    Vérifie que la fenêtre n'a pas changé lorsqu'on sort du menu d'options
    """

    if etat != is_fullscreen(): # si il y a changement
        set_display_resizable(Fen.get_size())   # modifie les placements des éléments
        etat = is_fullscreen()

def set_display_resizable(size):
    global resizable, Fen, Fen_size
    """
    Entrées : size      ((int, int))                                                    : Nouvelle dimension à appliquer
              resizable (bool)                                                          : Si l'écran est en fenêtré ou en plein écran
              Fen_size  ((int, int))                                                    : Dimensions de l'écran

    Sorties : resizable (bool)                                                          : Si l'écran est en fenêtré ou en plein écran
              Fen       (pygame.Surface)                                                : Fenêtre sur laquelle se déroule le jeu
              Fen_size  ((int, int))                                                    : Dimensions de l'écran

    Modifie l'emplacement des éléments selon si la fenêtre est en plein écran ou en fenêtré et selon la taille de la fenêtre afin de toujours centrer les éléments sur le joueur
    """

    if resizable:   # pour passer en plein écran
        actual_size = py.display.get_desktop_sizes()[0]
        for room in rooms:                                                              # |
            centerx, centery = room.getPos()                                            # |
            centerx -= Fen_size[0] // 2                                                 # |
            centery -= Fen_size[1] // 2                                                 # | modifie la position
            room.setPos(centerx + actual_size[0] // 2, centery + actual_size[1] // 2)   # | des éléments pour les
        plan[0].centerx += actual_size[0] // 2 - Fen_size[0] // 2                       # | adapter au plein écran
        plan[0].centery += actual_size[1] // 2 - Fen_size[1] // 2                       # |
        key[0].centerx += actual_size[0] // 2 - Fen_size[0] // 2                        # |
        key[0].centery += actual_size[1] // 2 - Fen_size[1] // 2                        # |
        Fen_size = actual_size
        py.display.set_mode((Fen_size[0], Fen_size[1]), py.FULLSCREEN)  # change la fenêtre en plein écran selon la résolution de l'écran
        resizable = False
    else:
        py.display.set_mode((size[0], size[1]), py.RESIZABLE)  # change la fenêtre en fenêtré selon une résolution donnée
        resizable = True

def reprendre():
    global pause
    """
    Entrées : pause (bool)  : Si le jeu est en pause ou non

    Sorties : pause (bool)  : Si le jeu est en pause ou non

    Permet au bouton "Reprendre" de changer la variable de pause
    """

    pause = False

def quitter(touches):
    global run
    """
    Entrées : touches   (Touches)   : Informations concernant les touches utilisées dans le jeu
              run       (bool)      : Si la boucle de jeu continue ou s'arrête

    Sorties : run       (bool)      : Si la boucle de jeu continue ou s'arrête

    Met fin à la boucle de jeu et renvoie au menu principal
    """

    from fonction_load_save import load_save    # empêche les fonctions de boucler entre elles
    run = False
    menu_principal(load_save, touches)  # appel du menu principal

'------------------------------------------------------------------------------------------------------------'

                    # Fonction principale

def jeu(partie, touches, format, size, avancée):
    global Fen, Fen_size, rooms, plan, player, player_g, player_d, key, inter_but, pause, etat
    """
    Entrées : partie    (list)                                                          : Contient les informations relatives à la sauvegarde chargée
              touches   (Touches)                                                       : Informations concernant les touches utilisées dans le jeu
              format    (bool)                                                          : Si la fenêtre précédente était en plein écran ou en fenêtré
              size      ((int, int))                                                    : Dimensions de l'ancienne fenêtre si fenêtré, sinon None
              avancée   (str)                                                           : Si il s'agit d'une nouvelle partie, sinon None
              Fen       (pygame.Surface)                                                : Fenêtre sur laquelle se déroule le jeu
              Fen_size  ((int, int))                                                    : Dimensions de l'écran
              rooms     (list)                                                          : Liste des éléments graphiques à déplacer
              plan      (pygame.Rect, (pygame.Surface, pygame.Surface, pygame.Surface)) : Ensemble zone de la carte et images associées
              player    (pygame.Surface)                                                : Joueur à l'état fixe
              player_g  (pygame.Surface)                                                : Joueur marchant du côté gauche
              player_d  (pygame.Surface)                                                : Joueur marchant du côté droit
              key       (pygame.Rect, (pygame.Surface, pygame.Surface, pygame.Surface)) : Ensemble zone de la clé et image associée
              inter_but (pygame.Surface)                                                : Bouton d'intéraction
              pause     (bool)                                                          : Si le jeu est en pause ou non
              etat      (bool)                                                          : Si la fenêtre est enregistrée en tant que plein écran ou en fenêtré

    Returns : Fen       (pygame.Surface)                                                : Fenêtre sur laquelle se déroule le jeu
              Fen_size  ((int, int))                                                    : Dimensions de l'écran
              rooms     (list)                                                          : Liste des éléments graphiques à déplacer
              plan      (pygame.Rect, (pygame.Surface, pygame.Surface, pygame.Surface)) : Ensemble zone de la carte et images associées
              player    (pygame.Surface)                                                : Joueur à l'état fixe
              player_g  (pygame.Surface)                                                : Joueur marchant du côté gauche
              player_d  (pygame.Surface)                                                : Joueur marchant du côté droit
              key       (pygame.Rect, (pygame.Surface, pygame.Surface, pygame.Surface)) : Ensemble zone de la clé et image associée
              etat      (bool)                                                          : Si la fenêtre est enregistrée en tant que plein écran ou en fenêtré

    Boucle principale du jeu, s'occupe d'afficher la fenêtre et l'ensemble des éléments graphiques et gère les différentes fonctionnalitées liées au jeu
    """

    initialisation()    # initialise les variables nécessaires à l'ensemble du fichier

    # salles :                                                                      # |
    S1 = Salle('S1', Fen_size[0] // 2 - 60, Fen_size[1] // 2 - 5, 670, 670)         # |
    S2 = Salle('S2', Fen_size[0] // 2 - 1165, Fen_size[1] // 2 - 5, 670, 670)       # |
    S3 = Salle('S3', Fen_size[0] // 2 + 1049, Fen_size[1] // 2 - 5, 670, 670)       # |
    S4 = Salle('S4', Fen_size[0] // 2 - 60, Fen_size[1] // 2 + 1103, 670, 670)      # |
                                                                                    # |
    # intersections :                                                               # |
    INT1 = Salle('INT1', Fen_size[0] //2 - 1170, Fen_size[1] // 2 + 1107, 50, 50)   # |
    INT2 = Salle('INT2', Fen_size[0] //2 + 1043, Fen_size[1] // 2 + 1107, 50, 50)   # |
                                                                                    # |
    # couloirs :                                                                    # |
    CV1 = Salle('CV1', Fen_size[0] // 2 - 66, Fen_size[1] // 2 + 613, 50, 440)      # |
    CV2 = Salle('CV2', Fen_size[0] // 2 - 1170, Fen_size[1] // 2 + 771, 50, 757)    # |
    CV3 = Salle('CV3', Fen_size[0] // 2 + 1043, Fen_size[1] // 2 + 771, 50, 757)    # |
    CH1 = Salle('CH1', Fen_size[0] // 2 + 558, Fen_size[1] // 2, 441,50)            # |
    CH2 = Salle('CH2', Fen_size[0] // 2 - 549, Fen_size[1] // 2, 437,50)            # |
    CH3 = Salle('CH3', Fen_size[0] // 2 + 711, Fen_size[1] // 2 + 1107, 747, 50)    # |
    CH4 = Salle('CH4', Fen_size[0] // 2 - 706, Fen_size[1] // 2 + 1107, 752, 50)    # |
                                                                                    # | création des
    # zones non traversables :                                                      # | éléments interactifs
    O1_1 = Salle('O1', Fen_size[0] // 2 - 1300, Fen_size[1] // 2 - 335, 500, 150)   # |
    O1_2 = Salle('O1', Fen_size[0] // 2 - 1500, Fen_size[1] // 2 - 190, 150, 150)   # |
    O2 = Salle('O2', Fen_size[0] // 2 - 60, Fen_size[1] // 2 - 300, 200, 200)       # |
    O3 = Salle('O3', Fen_size[0] // 2 + 1060, Fen_size[1] // 2 - 260, 150, 220)     # |
    O4 = Salle('O4', Fen_size[0] // 2 + 1330, Fen_size[1] // 2 - 145, 200, 200)     # |
    O5 = Salle('O5', Fen_size[0] // 2 + 1310, Fen_size[1] // 2 + 240, 150, 150)     # |
    O6 = Salle('O6', Fen_size[0] // 2 + 765, Fen_size[1] // 2 - 290, 150, 150)      # |
    O7_1 = Salle('O7', Fen_size[0] // 2 - 295, Fen_size[1] // 2 + 930, 350, 100)    # |
    O7_2 = Salle('O7', Fen_size[0] // 2 - 168, Fen_size[1] // 2 + 840, 95, 110)     # |
    O8 = Salle('O8', Fen_size[0] // 2 - 65, Fen_size[1] // 2 + 1490, 420, 30)       # |
    O9 = Salle('O9', Fen_size[0] // 2 - 1580, Fen_size[1] // 2 + 180, 100, 220)     # |
                                                                                    # |
    # zones d'intéraction :                                                         # |
    I1 = Salle('I1', Fen_size[0] // 2 - 1305, Fen_size[1] // 2 - 265, 520, 300)     # |
    I2 = Salle('I2', Fen_size[0] // 2 - 59, Fen_size[1] // 2 - 290, 350, 350)       # |
    I3 = Salle('I3', Fen_size[0] // 2 - 1500, Fen_size[1] // 2 + 180, 80, 300)      # |
    I4 = Salle('I4', Fen_size[0] // 2 + 770, Fen_size[1] // 2 - 290, 300, 300)      # |
    I5 = Salle('I5', Fen_size[0] // 2 - 60, Fen_size[1] // 2 + 1440, 480, 100)      # |

    rooms = [S1, S2, S3, S4, INT1, INT2, CV1, CV2, CV3, CH1, CH2, CH3, CH4, O1_1, O1_2, O2, O3, O4, O5, O6, O7_1, O7_2, O8, O9, I1, I2, I3, I4, I5]

    center_hitbox = py.rect.Rect(Fen_size[0] // 2 - 5, Fen_size[1] // 2 - 5, 10, 10)   # zone centrale simulant le joueur

    plan = (py.rect.Rect(0, 0, plan.get_width(), plan.get_height()), (plan, plan_no_cam, plan_no_vase, plan_no_all))    # |
    plan[0].centerx = center_hitbox.centerx                                                                             # | initialisation du
    plan[0].top = 0                                                                                                     # | placement des fonds
    plan[0].centery += S1.getHitbox().centery - S1.getReal().height // 2 - 46                                           # |

    key = (py.rect.Rect(0, 0, key.get_width(), key.get_height()), key)  # |
    key[0].center = O6.getHitbox().center                               # | initialisation du placement de la clé
    key[0].centerx += 50                                                # |

    inter_but = (py.rect.Rect(0, 0, inter_but.get_width(), inter_but.get_height()), inter_but)  # | initialisation du placement
    inter_but[0].center = (center_hitbox.centerx, center_hitbox.centery + 100)                  # | du bouton d'interaction

    if not format:  # si la fenêtre précédente était en fenêtré, adapte la fenêtre actuelle selon l'ancienne
        set_display_resizable(size)
        etat = False
    else:   # sinon met directement la fenêtre en plein écran (également lors des tests du fichier)
        py.display.set_mode((0, 0), py.FULLSCREEN)
        etat = True

    touche = ""             # |
    angle = 0               # |
    last_angle = 0          # | initialisation de
    cooldown = 20           # | variables internes
    mouv = False            # | à la boucle
    pause = False           # |
    can_interact = False    # |

    if partie == None:  # charge une partie sans sauvegarde (pour les tests du fichier)
        Intéractions = Interact()
        pos_x_save, pos_y_save = 0, 0
        fin = False

    else:   # charge les différents éléments de la sauvegarde choisie
        id_partie, pos_x_save, pos_y_save, inter1, inter2, inter3, inter4, inter5 = [partie[i] for i in range(len(partie))]
        Intéractions = Interact(inter1, inter2, inter3, inter4, inter5) # |
        inter = [inter1, inter2, inter3, inter4, inter5]                # | charge les intéractions
        for i in range(4):                                              # | selon le fichier de
            if inter[i]:                                                # | sauvegarde sélectionné
                del rooms[13 + i]                                       # |

        if inter3 or inter5:    # |
            fin = True          # | vérifie si la partie n'a
        else:                   # | pas déjà été terminée
            fin = False         # |
    
    décalage = (S2.getReal().centerx - center_hitbox.centerx, S2.getReal().centery - center_hitbox.centery) # décalage par rapport au centre de la carte

    for room in rooms:                                                          # |
        x, y = room.getPos()                                                    # |
        room.setPos(x - pos_x_save + décalage[0], y - pos_y_save + décalage[1]) # | modifie le placement
    plan[0].centerx -= pos_x_save - décalage[0]                                 # | des éléments selon
    plan[0].centery -= pos_y_save - décalage[1]                                 # | le fichier de sauvegarde
    key[0].centerx -= pos_x_save - décalage[0]                                  # |
    key[0].centery -= pos_y_save - décalage[1]                                  # |

    if avancée == "new":    # si nouvelle partie
        from Intro import intro     # | importe et exécute le
        intro(Fen, clock, touches)  # | programme d'introduction

    run = True
    while run:  # boucle principale
        for event in py.event.get():    # gestion des événements
            if event.type == py.QUIT:   # met fin à la boucle
                run = False
                exit()
            elif event.type == py.VIDEORESIZE:                          # |
                new_w = max(event.w, 1024)                              # |
                new_h = max(event.h, 768)                               # | gestion de la taille de fenêtre minimale
                if new_w != event.w or new_h != event.h:                # |
                    py.display.set_mode((new_w, new_h), py.RESIZABLE)   # |
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:    # |
                    if pause:                   # | gère la mise en
                        pause = False           # | pause lorsqu'on appuie
                    else:                       # | sur la touche Echap
                        pause = True            # |
                if event.key == py.key.key_code(touches.bindings['interagir']):                                                                                                                                 # |
                    if not pause:                                                                                                                                                                               # |
                        for room in rooms:                                                                                                                                                                      # |
                            if (room.nom[0] == 'I' and room.nom[1] in ('1', '2', '3', '4', '5')) and center_hitbox.colliderect(room.getHitbox()):                                                               # |
                                if room.nom == 'I3' or (room.nom == 'I5' and Intéractions.getInteract()[3]):                                                                                                    # |
                                    Intéractions.interaction(int(room.nom[1]))                                                                                                                                  # | gère l'interaction avec
                                    rooms.remove(room)                                                                                                                                                          # | un élément interactif
                                    fin = True                                                                                                                                                                  # |
                                    maj_parties(id_partie, center_hitbox.centerx - rooms[0].getPos()[0] + décalage[0], center_hitbox.centery - rooms[0].getPos()[1] + décalage[1], Intéractions.getInteract())  # |
                                elif room.nom[1] in ('1', '2', '4'):                                                                                                                                            # |
                                    Intéractions.interaction(int(room.nom[1]))                                                                                                                                  # |
                                    rooms.remove(room)                                                                                                                                                          # |
            if fin and event.type == py.KEYUP:  # pour retourner au menu principal lors d'une fin
                if cooldown == 0:
                    quitter(touches)

        observe_display(Fen)    # observe si la fenêtre a changé d'état

        if resizable:                                                                               # |
            actual_size = Fen.get_size()                                                            # |
            if Fen_size != actual_size:                                                             # |
                for room in rooms:                                                                  # |
                    centerx, centery = room.getPos()                                                # |
                    centerx -= Fen_size[0]//2                                                       # |
                    centery -= Fen_size[1]//2                                                       # | modifie la position des éléments pour
                    room.setPos(centerx + actual_size[0] // 2, centery + actual_size[1] // 2)       # | les adapter à la fenêtre en fenêtré
                plan[0].centerx += actual_size[0] // 2 - Fen_size[0] // 2                           # |
                plan[0].centery += actual_size[1] // 2 - Fen_size[1] // 2                           # |
                key[0].centerx += actual_size[0] // 2 - Fen_size[0] // 2                            # |
                key[0].centery += actual_size[1] // 2 - Fen_size[1] // 2                            # |
                center_hitbox = py.rect.Rect(Fen_size[0] // 2 - 5, Fen_size[1] // 2 - 5, 10, 10)    # |
                Fen_size = actual_size                                                              # |

        if fin:     # met fin à la partie et annonce le résultat
            if cooldown > 0:
                cooldown -= 1

            py.mouse.set_visible(True)

            # textes :
            F1 = [
                "Vous avez réussi à vous échapper avec l’œuvre.",
                "Le système de sécurité ne vous a pas repéré.",
                "Vous sortez par la porte de secours en toute sécurité."
            ]
            F2 = [
                "Vous avez réussi à vous échapper avec l’œuvre.",
                "Le système de sécurité ne vous a pas repéré.",
                "Vous sortez par la porte principale en toute sécurité.",
            ]
            F3 = [
                "Vous avez réussi à vous échapper sans emporter l’œuvre.",
                "Le système de sécurité ne vous a pas repéré.",
                "Vous sortez par la porte de secours en toute sécurité."
            ]
            F4 = [
                "Vous avez réussi à vous échapper sans emporter l’œuvre.",
                "Le système de sécurité ne vous a pas repéré.",
                "Vous sortez par la porte principale.",
                "Mais un garde à l'extérieur vous apperçoit et vous arrête."
            ]
            F5 = [
                "Vous avez réussi à vous échapper avec l’œuvre.",
                "Malheureusement, le système de sécurité vous a repéré.",
                "En sortant par la porte de secours, vous ne vous faites pas arrêté."
            ]
            F6 = [
                "Vous avez réussi à vous échapper avec l’œuvre.",
                "Malheureusement, le système de sécurité vous a repéré.",
                "En sortant par la porte d'entrée, vous vous faites arrêté."
            ]
            F7 = [
                "Vous avez réussi à vous échapper sans emporter l’œuvre.",
                "Malheureusement, le système de sécurité vous a repéré.",
                "En sortant par la porte de secours, vous ne vous faites pas arrêté."
            ]
            F8 = [
                "Vous avez réussi à vous échapper sans emporter l’œuvre.",
                "Malheureusement, le système de sécurité vous a repéré.",
                "En sortant par la porte principale, vous vous faites arrêté."
            ]

            inter1, inter2, inter3, inter4, inter5 = Intéractions.getInteract()
            if inter1:  # sécurité désactivée
                if inter2:  # vase volé
                    if inter3:  # porte de secours
                        text = F1
                    else:           # porte principale
                        text = F2
                else:       # vase non volé
                    if inter3:  # porte de secours
                        text = F3
                    else:           # porte principale
                        text = F4
            else:       # sécurité activée
                if inter2:  # vase volé
                    if inter3:  # porte de secours
                        text = F5
                    else:           # porte principale
                        text = F6
                else:       # vase non volé
                    if inter3:  # porte de secours
                        text = F7
                    else:           # porte principale
                        text = F8

            Fen.fill("black")

            bouton("progression.png", "progression_pressed.png", Fen_size[0] // 2 - 216, Fen_size[1] - 200, 432, 102, lambda : menu_progression(Intéractions.getInteract())) # menu de l'arbre de progression

            for i, ligne in enumerate(text):                                                                                    # |
                fin_surf, fin_rect = texte(ligne, 30, None, "white")                                                            # |
                zone_max = (fin_rect.height + 15) * len(text) - 15                                                              # |
                fin_rect.center = (Fen.get_width() // 2, Fen.get_height() // 2 - zone_max // 2 + i * (fin_rect.height + 15))    # | affichage
                Fen.blit(fin_surf, fin_rect)                                                                                    # | des textes
                                                                                                                                # | de fin
            press_surf, press_rect = texte("APPUYEZ SUR UNE TOUCHE", 50, None, "white")                                         # |
            press_rect.center = (Fen.get_width() // 2, Fen.get_height() - 40)                                                   # |
            Fen.blit(press_surf, press_rect)                                                                                    # |

        else:
            if not pause:   # lorsqu'on joue
                py.mouse.set_visible(False) # cache la souris
                if py.mouse.get_pos() != center_hitbox.center:  # replace la souris au centre pour le menu de pause
                    py.mouse.set_pos(center_hitbox.center)
                center_hitbox = py.rect.Rect(Fen_size[0] // 2 - 5, Fen_size[1] // 2 - 5, 10, 10)   # replace la zone centrale du joueur
                inter_but[0].center = (center_hitbox.centerx, center_hitbox.centery + 100)  # replace le bouton d'interaction

                for room in rooms:
                    if center_hitbox.colliderect(room.getHitbox()) and not(room.nom[0] == 'I' and room.nom[1] in ('1', '2', '3', '4', '5')) and not(room.nom[0] == 'O'):    # | modifie la zone sur laquel s'appliquent
                        actual_room = room                                                                                                                                  # | les restrictions de déplacements
                    if center_hitbox.colliderect(room.getHitbox()) and room.nom[0] == 'I' and room.nom[1] in ('1', '2', '3', '4', '5'):
                        can_interact = True
                        if room.nom == 'I5' and not Intéractions.getInteract()[3]:
                            can_interact = False
                    if room.nom[0] == 'O' and center_hitbox.colliderect(room.getReal()):                                                                # |
                        hitbox = room.getHitbox()                                                                                                       # |
                        if touche == '':                                                                                                                # |
                            if hitbox.right - 64 > center_hitbox.left <= hitbox.right and hitbox.bottom > center_hitbox.centery > hitbox.top:           # |
                                touche = "right"                                                                                                        # |
                            if hitbox.left + 64 < center_hitbox.right >= hitbox.left and hitbox.bottom > center_hitbox.centery > hitbox.top:            # |
                                touche = "left"                                                                                                         # |
                            if hitbox.bottom - 64 < center_hitbox.centery - 64 <= hitbox.bottom and hitbox.left < center_hitbox.centerx < hitbox.right: # |
                                touche = "top"                                                                                                          # |
                            if hitbox.top + 64 > center_hitbox.bottom + 64 >= hitbox.top and hitbox.left < center_hitbox.centerx < hitbox.right:        # | gère les collisions avec les
                                touche = "bottom"                                                                                                       # | objets non traversables
                        else:                                                                                                                           # |
                            if hitbox.right - 64 > center_hitbox.left <= hitbox.right and hitbox.bottom > center_hitbox.centery > hitbox.top:           # |
                                touche += "-right"                                                                                                      # |
                            if hitbox.left + 64 < center_hitbox.right >= hitbox.left and hitbox.bottom > center_hitbox.centery > hitbox.top:            # |
                                touche += "-left"                                                                                                       # |
                            if hitbox.bottom - 64 < center_hitbox.top - 64 <= hitbox.bottom and hitbox.left < center_hitbox.centerx < hitbox.right:     # |
                                touche += "-top"                                                                                                        # |
                            if hitbox.top + 64 > center_hitbox.bottom + 64 >= hitbox.top and hitbox.left < center_hitbox.centerx < hitbox.right:        # |
                                touche += "-bottom"                                                                                                     # |

                keys = py.key.get_pressed()
                if keys[py.key.key_code(touches.bindings['avancer'])] and (center_hitbox.top > actual_room.getHitbox().top or actual_room.nom[1] == 'V' or (actual_room.nom in ("INT1", "INT2") and actual_room.getHitbox().top < center_hitbox.centery)) and touche != "top" and touche != "top-left" and touche != 'top-right' and touche != "right-top" and touche != "left-top":
                    # modifie la position des éléments pour déplacer le joueur vers le nord, prend en compte les collisions
                    for room in rooms:
                        center = room.getPos()
                        room.setPos(center[0], center[1] + 10)
                    plan[0].centery += 10
                    key[0].centery += 10
                    angle = 0
                    mouv = True
                if keys[py.key.key_code(touches.bindings['reculer'])] and (center_hitbox.bottom < actual_room.getHitbox().bottom or actual_room.nom[1] == 'V') and touche != "bottom" and touche != "bottom-left" and touche != 'bottom-right' and touche != "right-bottom" and touche != "left-bottom":
                    # modifie la position des éléments pour déplacer le joueur vers le sud, prend en compte les collisions
                    for room in rooms:
                        center = room.getPos()
                        room.setPos(center[0], center[1] - 10)
                    plan[0].centery -= 10
                    key[0].centery -= 10
                    angle = 180
                    mouv = True
                if keys[py.key.key_code(touches.bindings['gauche'])] and (center_hitbox.left > actual_room.getHitbox().left or actual_room.nom[1] == 'H' or actual_room.nom == 'INT2') and touche != "left" and touche != "top-left" and touche != 'bottom-left' and touche != "left-top" and touche != 'left-bottom':
                    # modifie la position des éléments pour déplacer le joueur vers l'ouest, prend en compte les collisions
                    for room in rooms:
                        center = room.getPos()
                        room.setPos(center[0] + 10, center[1])
                    plan[0].centerx += 10
                    key[0].centerx += 10
                    angle = 90
                    mouv = True
                if keys[py.key.key_code(touches.bindings['droite'])] and (center_hitbox.right < actual_room.getHitbox().right or actual_room.nom[1] == 'H' or actual_room.nom == 'INT1')  and touche != "right" and touche != "bottom-right" and touche != 'top-right' and touche != "right-top" and touche != "right-bottom":
                    # modifie la position des éléments pour déplacer le joueur vers l'est, prend en compte les collisions
                    for room in rooms:
                        center = room.getPos()
                        room.setPos(center[0] - 10, center[1])
                    plan[0].centerx -= 10
                    key[0].centerx -= 10
                    angle = 270
                    mouv = True
                if not(keys[py.key.key_code(touches.bindings['avancer'])] or keys[py.key.key_code(touches.bindings['reculer'])] or keys[py.key.key_code(touches.bindings['gauche'])] or keys[py.key.key_code(touches.bindings['droite'])]) and mouv:    # | réinitialise l'effet de
                    mouv = False                                                                                                                                                                                                                        # | déplacement du joueur

                touche = "" # réinitialise les collisions avec les objets non traversables

                if last_angle != angle:                                             # |
                    player = py.transform.rotate(player, - last_angle + angle)      # | modifie l'angle du joueur
                    player_g = py.transform.rotate(player_g, - last_angle + angle)  # | pour le faire pointer dans
                    player_d = py.transform.rotate(player_d, - last_angle + angle)  # | la direction de son mouvement
                    last_angle = angle                                              # |
            else:   # lorsque le jeu est en pause
                py.mouse.set_visible(True)  # rend la souris visible
            
            Fen.fill('black')

            inter = Intéractions.getInteract()          # |
            if inter[0] and inter[1]:                   # |
                Fen.blit(plan[1][3], plan[0].topleft)   # |
            elif inter[0]:                              # | affiche le fond
                Fen.blit(plan[1][1], plan[0].topleft)   # | du jeu selon les
            elif inter[1]:                              # | interactions faites
                Fen.blit(plan[1][2], plan[0].topleft)   # |
            else:                                       # |
                Fen.blit(plan[1][0], plan[0].topleft)   # |

            if not inter[3]:                        # | affiche la clé si elle
                Fen.blit(key[1], key[0].topleft)    # | n'a pas été ramassée

            if can_interact or (can_interact and Intéractions.getInteract()):                   # |
                Fen.blit(inter_but[1], inter_but[0].topleft)                                    # |
                text_surf, text_rect = texte(touches.bindings['interagir'], 30, None, "white")  # | affiche le bouton d'interaction lorsque le
                text_rect.center = inter_but[0].center                                          # | joueur rentre dans une zone d'interaction
                Fen.blit(text_surf, text_rect)                                                  # |
                can_interact = False                                                            # |

            if mouv:
                if compteur >= 10:                                                                                                              # |
                    Fen.blit(player_g, (center_hitbox.centerx - player_g.get_width() // 2, center_hitbox.centery - player_g.get_height() // 2)) # |
                elif 10 > compteur >= 0:                                                                                                        # |
                    Fen.blit(player_d, (center_hitbox.centerx - player_d.get_width() // 2, center_hitbox.centery - player_d.get_height() // 2)) # | affiche un effet de
                else:                                                                                                                           # | déplacement du joueur
                    Fen.blit(player, (center_hitbox.centerx - player.get_width() // 2, center_hitbox.centery - player.get_height() // 2))       # |
                    compteur = 20                                                                                                               # |
                compteur -= 1                                                                                                                   # |
            else:
                Fen.blit(player, (center_hitbox.centerx - player.get_width() // 2, center_hitbox.centery - player.get_height() // 2))   # | affiche le joueur
                compteur = 20                                                                                                           # | lorsqu'il ne bouge pas

            if pause:   # lorsque le jeu est en pause
                fond_texte(0, 0, Fen_size[0], Fen_size[1], 'black', 200) # applique un filtre semi-transparent
                bouton("reprendre.png", "reprendre_pressed.png", Fen_size[0] // 2 - 200, Fen_size[1] // 2 - 204 - 15, 432, 102, reprendre)                                                                                                                                                                          # |
                bouton("réglages2.png", "réglages2_pressed.png", Fen_size[0] // 2 - 200, Fen_size[1] // 2 - 102 - 5, 432, 102, lambda : menu_réglages(touches))                                                                                                                                                     # | affiche les boutons
                bouton("sauvegarder.png", "sauvegarder_pressed.png", Fen_size[0] // 2 - 200, Fen_size[1] // 2 + 5, 432, 102, lambda : maj_parties(id_partie, center_hitbox.centerx - rooms[0].getPos()[0] + décalage[0], center_hitbox.centery - rooms[0].getPos()[1] + décalage[1], Intéractions.getInteract()))   # | du menu de pause
                bouton("menu_principal.png", "menu_principal_pressed.png", Fen_size[0] // 2 - 200, Fen_size[1] // 2 + 102 + 15, 432, 102, lambda : quitter(touches))                                                                                                                                                # |

        py.display.flip()   # | mise à jour
        clock.tick(60)      # | de la fenêtre

'------------------------------------------------------------------------------------------------------------'

                    # Exécution manuelle du fichier

if __name__ == '__main__':
    from controles import Touches
    jeu(None, touches = Touches(), format = True, size = None, avancée = "new")
    py.quit()