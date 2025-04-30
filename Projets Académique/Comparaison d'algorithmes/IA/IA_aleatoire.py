def voisinis_possibles(niveau, sommet_courant):
    """
        Donne les voisins du sommet courant qui sont valides (ne sortent pas de la matrice).

        Args :
            niveau (list) : Liste représentant le niveau sous forme de matrice, où chaque élément représente
                               une case du niveau
            sommet_courant (tuple) : Position actuelle du sommet sous forme de tuple (y, x)

        Returns :
            v_possibles (list) : liste des voisins possibles du sommet courant, qui ne sont pas hors
                    des limites du niveau.
    """
    v_possibles = []
    for v in [
        (sommet_courant[0] + 1, sommet_courant[1]),
        (sommet_courant[0] - 1, sommet_courant[1]),
        (sommet_courant[0], sommet_courant[1] + 1),
        (sommet_courant[0], sommet_courant[1] - 1)
    ]:
        # print(f"Vérification de la case : {v}")
        if 0 <= v[1] < len(niveau) and 0 <= v[0] < len(niveau[0]):
            # print(f"Ajoutée comme voisine possible : {v}")
            v_possibles.append(v)
    # print(f"Voisins possibles pour {sommet_courant} : {v_possibles}")
    return v_possibles

def direction(avant, apres):
    """
           Calcule la direction du déplacement entre deux points.

           Args :
               avant (tuple) : La position initiale sous forme de tuple (y, x)
               apres (tuple) : La position finale sous forme de tuple (y, x)

        Returns :
            str : la direction du déplacement sous la forme d'un caractère ('B', 'H', 'D', 'G')
    """
    dx = apres[0] - avant[0]
    dy = apres[1] - avant[1]
    dictionnaire_directions = {'(0, 1)' : 'B', '(0, -1)' : 'H', '(1, 0)' : 'D', '(-1, 0)' : 'G'}
    # Traduire les déplacements en actions
    for cle in dictionnaire_directions:
        if cle == str((dx, dy)):
            return dictionnaire_directions[cle]  # Direction correspondante

class IA_Bomber:
    def __init__(self, num_joueur, game_dict, timer_global, timer_fantome):
        self._num_joueur = num_joueur # Le numéro de l'IA
        self._chemin = []  # Stocke le chemin actuel
        self._minerais_position = None # Position du minerai atteint
        self._upgrade_position = None # Position de l'upgrade
        self._explosions_positions = {} # Les zones incluent dans la portée d'une bombe quelconque
        self._fantomes_positions = {} # Les zones incluent à une distance de 3 d'un fantôme
        self._memoire_minerais = [] # Les minerais déjà cassés

    def enregistrer_chemin(self, voisin, sommet_depart, predecesseurs):
        """
            Enregistre le chemin parcouru depuis un sommet voisin jusqu'au sommet de départ en utilisant les prédécesseurs.

            Args :
                voisin (tuple) : Le sommet actuel, à partir duquel on remonte vers le sommet de départ
                sommet_depart (tuple) : Le sommet de départ à partir duquel le chemin est reconstruit
                predecesseurs (dict) : Dictionnaire des prédécesseurs pour chaque sommet, utilisé pour reconstruire le chemin

            Returns :
                None
        """
        while voisin != sommet_depart:
            self._chemin.insert(0, voisin)
            voisin = predecesseurs[voisin]
        self._chemin.insert(0, voisin)

    def parcours_largeur(self, niveau, sommet_depart, zone_danger):
        """
            Algorithme de recherche du plus court chemin à partir d'un point de départ donné.

            Args :
                sommet_depart (tuple) : coordonnées à partir duquel on commence le parcours en largeur
                zone_danger (bool) : indique si l'IA est dans une zone dangereuse à fuir
                niveau (list) : liste de chaînes de caractères représentant les lignes de la map

            Returns :
                None ou des variables pour stopper le processus si besoin
        """
        distance = {sommet_depart: 0}
        predecesseurs = {}
        attente = [sommet_depart] # file d'attente
        while len(attente) > 0:
            sommet_courant = attente.pop(0)  # sommet dont on va chercher les voisins
            v_possibles = voisinis_possibles(niveau, sommet_courant)
            for v in v_possibles:
                if niveau[v[1]][v[0]] == ' ' and v not in distance:  # Case vide et inconnue
                    distance[v] = distance[sommet_courant] + 1
                    predecesseurs[v] = sommet_courant
                    attente.append(v)
                    if zone_danger and not self.est_zone_danger(v):
                        return self.enregistrer_chemin(v, sommet_depart, predecesseurs)
                elif niveau[v[1]][v[0]] not in [' ', 'C', 'E'] and v not in distance and not zone_danger:
                    predecesseurs[v] = sommet_courant
                    self.enregistrer_chemin(v, sommet_depart, predecesseurs)
                    if niveau[v[1]][v[0]] == 'U': # Si un upgrade est trouvé
                        self._upgrade_position = self._chemin[-1]
                        return self._upgrade_position
                    elif niveau[v[1]][v[0]] == 'M' and self._chemin[-2] not in self._memoire_minerais:  # Si un minerai est trouvé
                        self._memoire_minerais.append(self._chemin[-2])
                        self._minerais_position = self._chemin[-2]
                        return self._minerais_position
        self._chemin = []

    def definir_zones_danger(self, liste_bombes, liste_fantomes, niveau):
        """
            Définit les zones d'explosion pour chaque bombe en fonction de leur portée.

            Args :
                liste_bombes (list) : liste des bombes, chaque bombe étant un dictionnaire, où 'position' est la position de la bombe
                                          et 'portée' est la portée de l'explosion
                liste_fantomes (list) : liste des fantomes, chaque fantome étant un dictionnaire, où 'position' est la position du fantome
                niveau (list) : liste de chaînes de caractères représentant les lignes de la map

            Returns :
                None
        """
        self._fantomes_positions = {}
        self._explosions_positions = {}
        dangers = {'bombes' : [liste_bombes, self._explosions_positions], 'fantomes' : [liste_fantomes, self._fantomes_positions]}
        for danger in dangers:
            for element in dangers[danger][0]:
                portee = 3
                if danger == 'bombes':
                    portee = element['portée']
                dangers[danger][1][f'{element['position']}'] = [element['position']]
                if danger == 'fantomes':
                    for diagonale in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                        position_portee = (element['position'][0] + diagonale[0], element['position'][1] + diagonale[1])
                        dangers[danger][1][f'{element['position']}'] += [position_portee]
                for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    for p in range(1, portee + 1):
                        position_portee = (element['position'][0] + d[0] * p, element['position'][1] + d[1] * p)
                        if niveau[position_portee[1]][position_portee[0]] in ['C', 'E']:
                            break
                        if danger == 'fantomes' and niveau[position_portee[1]][position_portee[0]] == 'M':
                            break
                        dangers[danger][1][f'{element['position']}'] += [position_portee]

    def est_zone_danger(self, position):
        """
            Vérifie si une position donnée fait partie des zones dangereuses.

            Args :
                position (tuple) : la position à vérifier

            Returns :
                bool : True si la position est dans une zone dangereuse, sinon False
        """
        for dangers in [self._explosions_positions, self._fantomes_positions]:
            for danger in dangers:
                for d in dangers[danger]:
                    if d == position:
                        return True
        return False

    def action(self, game_dict):
        """
            Appelé à chaque décision du joueur IA.

            Args :
                game_dict (dict) : décrit l'état actuel de la partie au moment
                où le joueur doit décider son action

            Returns :
                str : une action
        """
        position_actuelle = game_dict['bombers'][self._num_joueur]['position']
        self.definir_zones_danger(game_dict['bombes'], game_dict['fantômes'], game_dict['map'])
        zone_danger = self.est_zone_danger(position_actuelle)

        # Si l'IA a atteint une zone entourée d'au moins un minerai
        if position_actuelle == self._minerais_position and not zone_danger:
            self._minerais_position = None
            self._chemin = []
            return 'X'

        # Si l'IA a atteint un upgrade
        if position_actuelle == self._upgrade_position:
            self._upgrade_position = None
            self._chemin = []

        # Si l'IA est dans la portée d'une bombe et/ou qu'elle n'a pas de chemin (doit se réfugier ou trouver des minerais)
        if not self._chemin:
            self.parcours_largeur(game_dict['map'], position_actuelle, zone_danger)

        # Si l'IA a un chemin, elle doit continuer à se déplacer
        if self._chemin:
            # Si le prochain pas de l'IA n'est pas dans une zone à risque et qu'elle n'est pas déjà en zone risquée, elle continue sinon elle reste sur place
            if not zone_danger and not self.est_zone_danger(self._chemin[1]):
                prochain_pas = self._chemin.pop(1)  # Prendre la première case du chemin
                if len(self._chemin) == 1:
                    self._chemin = []
                return direction((position_actuelle[0], position_actuelle[1]), (prochain_pas[0], prochain_pas[1]))
            elif not zone_danger and self.est_zone_danger(self._chemin[1]):
                return 'N'
            # Si l'IA est dans une zone à risque, elle continue son chemin vers une zone non risquée
            else:
                prochain_pas = self._chemin.pop(1) # Prendre la deuxième case du chemin et pas la première (la position du joueur)
                if len(self._chemin) == 1:
                    self._chemin = []
                return direction((position_actuelle[0], position_actuelle[1]), (prochain_pas[0], prochain_pas[1]))

        # Si aucun chemin n'est trouvé, l'IA reste sur place
        return 'N'
