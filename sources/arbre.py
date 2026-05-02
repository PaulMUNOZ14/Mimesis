# Projet : Mimesis
# Auteur : Paul MUNOZ

'------------------------------------------------------------------------------------------------------------'

                    # Définition des classes

class Noeud:
    """
    Attributs : texte       (str)           : Nom du nouveau noeud
                visite      (bool)          : Si l'interaction associée au noeud a été effectuée
                parent      (Noeud)         : Noeud parent du nouveau noeud
                gauche      (Noeud)         : Branche gauche du nouveau noeud, None si aucun
                droite      (Noeud)         : Branche droite du nouveau noeud, None si aucun
                position    ((int, int))    : Position graphique du nouveau noeud

    Crée chaque noeud d'un arbre binaire et leur liaison
    """
    
    def __init__(self, texte = "", parent = None):
        """
        Entrées : texte     (str)   : Nom du nouveau noeud
                  parent    (Noeud) : Noeud parent du nouveau noeud, None si aucun

        Initialise un noeud tel une feuille de l'arbre
        """
        
        self.texte = texte
        self.visite = False
        self.parent = parent
        self.gauche = None
        self.droite = None
        self.position = (0, 0)

class Arbre:
    """
    Attributs : racine              (Noeud) : Racine de l'ensemble de l'arbre
                largeur_noeud       (int)   : Largeur graphique des noeuds
                hauteur_noeud       (int)   : Hauteur graphique des noeuds
                espacement_vertical (int)   : Espacement vertical entre chaque étage

    Crée l'arbre binaire demandé selon les liaisons de chaque noeud
    """
    
    def __init__(self):
        """
        Initialise l'arbre par sa racine et les proportions graphiques dont il a besoin
        """
        
        self.racine = Noeud("Début")
        self.largeur_noeud = 200
        self.hauteur_noeud = 60
        self.espacement_vertical = 120

    def ajouter_gauche(self, parent, texte):
        """
        Entrées : parent    (Noeud) : Noeud parent du noeud à rajouter
                  texte     (str)   : Nom du noeud à rajouter

        Crée et renvoie un nouveau noeud à gauche du noeud actuel
        """
        
        nouveau = Noeud(texte, parent)  # crée le nouveau noeud
        parent.gauche = nouveau # ajoute le noeud à l'arbre
        return nouveau

    def ajouter_droit(self, parent, texte):
        """
        Entrées : parent    (Noeud) : Noeud parent du noeud à rajouter
                  texte     (str)   : Nom du noeud à rajouter

        Crée et renvoie un nouveau noeud à droite du noeud actuel
        """

        nouveau = Noeud(texte, parent)  # crée le nouveau noeud
        parent.droite = nouveau # ajoute le noeud à l'arbre
        return nouveau
    
    def profondeur_max(self):
        """
        Sorties : self.calcul_profondeur(self.racine)   (int)   : Profondeur calculée depuis la racine

        Renvoie la profondeur maximale de l'arbre
        """
        
        return self.calcul_profondeur(self.racine)

    def calcul_profondeur(self, noeud):
        """
        Entrées : noeud                                                                                         (Noeud) : Noeud actuel depuis lequel est calculé la profondeur

        Sorties : return 1 + max(self.calcul_profondeur(noeud.gauche), self.calcul_profondeur(noeud.droite))    (int)   : Profondeur depuis le noeud actuel, 0 s'il s'agit d'une feuille
        """
        
        if noeud is None:   # si le noeud actuel est une feuille
            return 0
        return 1 + max(     # calcule la profondeur par récurrence
            self.calcul_profondeur(noeud.gauche), 
            self.calcul_profondeur(noeud.droite)
        )

    def calculer_positions(self, ecran_largeur, y_start, espace_vertical):
        """
        Entrées : ecran_largeur     (int)   : Largeur de la fenêtre
                  y_start           (int)   : Position verticale de départ
                  espace_vertical   (int)   : Espacement vertical entre chaque étage
        
        Redéfinit l'espacement entre les noeuds puis calcule les positions des noeuds
        """
        
        self.espacement_vertical = espace_vertical
        self._calculer_position_recursif(   # calcule des positions des noeuds
            self.racine, 
            x=ecran_largeur // 2,
            y=y_start,
            decalage_horizontal=ecran_largeur // 4
        )

    def _calculer_position_recursif(self, noeud, x, y, decalage_horizontal):
        """
        Entrées : noeud                 (Noeud) : Noeud actuel dont il faut calculer la position
                  x                     (int)   : Position horizontale du nouveau centre du noeud
                  y                     (int)   : Position verticale du début du noeud
                  decalage_horizontal   (int)   : Espacement horizontal entre chaque noeud
        """
        
        if noeud is None:   # si le noeud actuel est une feuille
            return 
        
        noeud.position = (x - self.largeur_noeud//2, y) # redéfinit la position du noeud
        
        if noeud.gauche:    # s'il existe, redéfinit la branche de gauche
            self._calculer_position_recursif(noeud.gauche,      # appel de récurrence
                                           x - decalage_horizontal, 
                                           y + self.espacement_vertical, 
                                           decalage_horizontal//1.5)
        
        if noeud.droite:    # s'il existe, redéfinit la branche de droite
            self._calculer_position_recursif(noeud.droite,      # appel de récurrence
                                           x + decalage_horizontal, 
                                           y + self.espacement_vertical, 
                                           decalage_horizontal//1.5)