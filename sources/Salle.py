# Projet : Mimesis
# Auteur : Joan GUILBERT

'------------------------------------------------------------------------------------------------------------'

                    #   Importation

import pygame as py

'------------------------------------------------------------------------------------------------------------'

                    #   Définition de la classe

class Salle:
    """
    Attributs : nom             (str)           : Nom de la salle, de l'objet ou de l'interaction
                zone_hitbox     (pygame.Rect)   : Zone interne de l'élément
                zone_réelle     (pygame.Rect)   : Zone externe de l'élément

    Gère les salles, les objets non traversables et les zones d'interactions
    """

    def __init__(self, nom, pos_x, pos_y, largeur, hauteur):
        """
        Entrées : nom       (str)   : Nom de la salle, de l'objet ou de l'interaction
                  pos_x     (int)   : Position horizontale du centre de l'élément
                  pos_y     (int)   : Position verticale du centre de l'élément
                  largeur   (int)   : Largeur de l'élément
                  hauteur   (int)   : Hauteur de l'élément

        Initialise les zones de la salle, l'objet ou l'interaction ainsi que le nom qui y est associé
        """
        
        self.nom = nom
        self.zone_hitbox = py.rect.Rect(pos_x - largeur // 2, pos_y - hauteur // 2, largeur, hauteur)   # zone interne
        if nom[1] == 'H':   # couloir horitontal                                                                                # |
            self.zone_réelle = py.rect.Rect(pos_x - 5 - largeur // 2, pos_y - 64 - hauteur // 2, largeur, hauteur + 128)        # |
        elif nom[1] == 'V': # couloir vertical                                                                                  # | zone
            self.zone_réelle = py.rect.Rect(pos_x - 5 - largeur // 2, pos_y - 64 - hauteur // 2, largeur + 128, hauteur)        # | externe
        else:                                                                                                                   # |
            self.zone_réelle = py.rect.Rect(pos_x - 5 - largeur // 2, pos_y - 64 - hauteur // 2, largeur + 128, hauteur + 128)  # |

    def getPos(self):
        """
        Sorties : zone_réelle.center    ((int, int))    : Positions du centre de l'élément

        Renvoie la position centrale de l'élément donnée
        """
        
        return self.zone_réelle.center

    def setPos(self, centerx, centery):
        """
        Entrées : centerx   (int)   : Nouvelle position horizontale du centre de l'élément
                  centery   (int)   : Nouvelle position verticale du centre de l'élément

        Modifie le centre de l'élément donnée selon les coordonées passées en paramètre
        """
        
        self.zone_réelle.center = (centerx, centery)
        self.zone_hitbox.center = (centerx, centery)
    
    def getHitbox(self):
        """
        Sorties : zone_hitbox   (pygame.Rect)   : Zone interne de l'élément

        Renvoie la zone intérieure de l'élément donné
        """
        
        return self.zone_hitbox
    
    def getReal(self):
        """
        Sorties : zone_réelle   (pyagame.Rect)  : Zone externe de l'élément

        Renvoie la zone extérieure de l'élément donné
        """
        
        return self.zone_réelle
    
'------------------------------------------------------------------------------------------------------------'

                    #   Tests manuels

if __name__ == "__main__":
    S = Salle("Salle", 0, 0, 10, 10)
    S.setPos(5, 5)
    assert S.getPos() == (5, 5)
    print("Zone interne : ", S.getHitbox(), ", Zone externe : ", S.getReal())