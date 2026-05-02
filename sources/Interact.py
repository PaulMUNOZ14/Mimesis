# Projet : Mimesis
# Auteur : Joan GUILBERT

'------------------------------------------------------------------------------------------------------------'

                    #   Définition de la classe 

class Interact:
    """
    Attributs : interact_1  (bool)  : Si interaction avec la sécurité
                interact_2  (bool)  : Si interaction avec l'oeuvre
                interact_3  (bool)  : Si interaction avec la porte de secours
                interact_4  (bool)  : Si interaction avec la clé
                interact_5  (bool)  : Si interaction avec la porte principale

    Gère les différentes interactions du jeu
    """

    def __init__(self, i1 = False, i2 = False, i3 = False, i4 = False, i5 = False):
        """
        Args : i1   (bool)  : Si interaction avec la sécurité, False par défaut
               i2   (bool)  : Si interaction avec l'oeuvre, False par défaut
               i3   (bool)  : Si interaction avec la porte de secours, False par défaut
               i4   (bool)  : Si interaction avec la clé, False par défaut
               i5   (bool)  : Si interaction avec la porte principale, False par défaut
        
        Initialise les intéractions selon les données du fichier de sauvegarde
        """
        
        self.interact_1 = i1    # |
        self.interact_2 = i2    # |
        self.interact_3 = i3    # | états d'interaction
        self.interact_4 = i4    # |
        self.interact_5 = i5    # |

    def getInteract(self):
        """
        Sorties : interact_1  (bool)  : Si interaction avec la sécurité
                  interact_2  (bool)  : Si interaction avec l'oeuvre
                  interact_3  (bool)  : Si interaction avec la porte de secours
                  interact_4  (bool)  : Si interaction avec la clé
                  interact_5  (bool)  : Si interaction avec la porte principale

        Renvoie les états de toutes les interactions
        """
        
        return self.interact_1, self.interact_2, self.interact_3, self.interact_4, self.interact_5

    def interaction(self, interact):
        """
        Entrées : interact  (int)   : Numéro correspondant à l'interaction

        Préconditions : interact est censé être compris entre 1 et 5

        Modifie l'état de l'interaction donnée par le numéro entré en paramètre
        """
        if interact == 1:   # Si interaction avec la sécurité
            self.interact_1 = True
        elif interact == 2: # Si interaction avec l'oeuvre
            self.interact_2 = True
        elif interact == 3: # Si interaction avec la porte de secours
            self.interact_3 = True
        elif interact == 4: # Si interaction avec la clé
            self.interact_4 = True
        else:               # Si interaction avec la porte principale
            self.interact_5 = True

'------------------------------------------------------------------------------------------------------------'

                    #   Tests manuels

if __name__ == "__main__":       
    interaction = Interact()
    for inter in interaction.getInteract():
        assert inter == False
    interaction.interaction(3)
    assert interaction.interact_3 == True