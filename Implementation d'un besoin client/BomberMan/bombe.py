from affectation import perdre_vie, spawn_item
from affichage import mettre_a_jour_plateau, ajouter_score
import random
from parametres import *

# Liste des bombes avec leurs données
bombes = []

def actualiser_bombe():
    global bombes
    bombes = []



def ajout_bombe(jeu, x, y, tours_restants, dimensions):
    """
    Ajoute une bombe à la liste des bombes avec ses coordonnées et le nombre de tours avant l'explosion.
    :param jeu: Objet Jeu pour afficher des images.
    :param x: Coordonnée x de la bombe.
    :param y: Coordonnée y de la bombe.
    :param tours_restants: Nombre de tours avant l'explosion.
    :param dimensions: Dictionnaire contenant les dimensions des cases et des images.
    """
    COTE_X = dimensions["COTE_X"]
    COTE_Y = dimensions["COTE_Y"]
    # Créer l'image de la bombe
    bomb = jeu.afficherImage(x * COTE_X, y * COTE_Y + COTE_Y, "images/bomb.png")
    if bomb is None:
        print(f"Erreur : l'image de la bombe n'a pas pu être créée à ({x}, {y})")
        return

    # Ajouter la bombe à la liste des bombes
    bombes.append({"x": x, "y": y, "tours_restants": tours_restants, "image": bomb})

# Liste des images d'explosion
images_explosion = []

def explosion_bombe(jeu, Plateau, x, y, running, affichages, dimensions,joueur):
    """
    Affiche l'effet d'explosion et stoppe la propagation si elle croise une colonne.
    :param jeu: Objet Jeu pour afficher des images.
    :param Plateau: La matrice représentant le plateau de jeu.
    :param x: Coordonnée x de la bombe.
    :param y: Coordonnée y de la bombe.
    :param running: Booléen indiquant si le jeu est en cours.
    :param affichages: Dictionnaire des éléments graphiques affichés.
    :param dimensions: Dictionnaire contenant les dimensions des cases et des images.
    :param joueur: Dictionnaire contenant les informations du joueur (portée, score).
    :return: Les dictionnaires actualiséss
    """
    COTE_X = dimensions["COTE_X"]
    COTE_Y = dimensions["COTE_Y"]

    global images_explosion

    # Directions pour l'explosion (centre, droite, gauche, haut, bas)
    directions = [
        [(i, 0) for i in range(1, joueur["portee"]+1)],  # Droite
        [(-i, 0) for i in range(1, joueur["portee"]+1)], # Gauche
        [(0, -i) for i in range(1, joueur["portee"]+1)], # Haut
        [(0, i) for i in range(1, joueur["portee"]+1)],  # Bas
        [(0, 0)]                              # Centre
    ]

    # Affiche l'effet d'explosion pour chaque direction
    for direction in directions:
        for dx, dy in direction:
            nx, ny = x + dx, y + dy

            # Vérifier que la case est dans les limites du plateau
            if 0 <= nx < len(Plateau[0]) and 0 <= ny < len(Plateau):
                # Stopper la propagation si une colonne est rencontrée
                if Plateau[ny][nx] == "C":
                    break  # Arrête la propagation dans cette direction

                # Déclencher les explosions en chaîne pour les bombes voisines
                for bombe in bombes:
                    if bombe["x"] == nx and bombe["y"] == ny and bombe["tours_restants"] >= 1:
                        bombe["tours_restants"] = 1

                # Afficher l'effet visuel d'explosion
                explosion = jeu.afficherImage(nx * COTE_X, ny * COTE_Y + COTE_Y, "images/explosion.png")
                images_explosion.append(explosion)

                # Vérifier si le joueur est touché
                if Plateau[ny][nx] == "J":
                    joueur, running, affichages = perdre_vie(
                        jeu, dimensions, running, joueur, affichages
                    )

    return images_explosion, running, joueur, affichages





def gerer_bombes(jeu, Plateau, dimensions, pos_fantomes, joueur, running, affichages):
    """
    Gère toutes les bombes sur le plateau.
    :param jeu: Objet Jeu pour afficher des images.
    :param Plateau: La matrice représentant le plateau de jeu.
    :param dimensions: Dictionnaire contenant les dimensions des cases et des images.
    :param pos_fantomes: Liste des positions des fantômes.
    :param joueur: Dictionnaire contenant les informations du joueur (portée, score).
    :param running: Booléen indiquant si le jeu est en cours.
    :param affichages: Dictionnaire des éléments graphiques affichés.
    :return: Nouveau score, nouveau nombre de vies, nouvel état du jeu et nouvelles affichages.
    """

    global bombes

    bombes_a_retirer = []

    for bombe in bombes:
        joueur, running, affichages, bombe_a_supprimer, pos_fantomes = gerer_bombe(
            jeu, Plateau, bombe, dimensions, pos_fantomes, joueur, running, affichages
        )

        if bombe_a_supprimer:
            bombes_a_retirer.append(bombe)

    # Supprimer les bombes marquées pour suppression
    for bombe in bombes_a_retirer:


        jeu.supprimer(bombe["image"])

        bombes.remove(bombe)

    return joueur, running, affichages, pos_fantomes


def gerer_bombe(jeu, Plateau, bombe, dimensions, pos_fantomes, joueur, running, affichages):
    """
    Gère l'état d'une seule bombe : réduction du compteur, explosion et mise à jour visuelle.
    Les changements sur le plateau sont appliqués avant l'affichage des effets visuels d'explosion.
    :param jeu: Objet Jeu pour afficher des images.
    :param Plateau: La matrice représentant le plateau de jeu.
    :param bombe: Dictionnaire représentant une seule bombe.
    :param dimensions: Dictionnaire contenant les dimensions du plateau et des cases.
    :param pos_fantomes: Liste contenant les positions des fantômes.
    :param joueur: Dictionnaire contenant les informations du joueur (score, vies, etc.).
    :param running: État du jeu (True ou False).
    :param affichages: Dictionnaire des éléments graphiques affichés.
    :return: joueur, running, affichages, bombe_a_supprimer, pos_fantomes
    """

    x, y = bombe["x"], bombe["y"]
    bombe_a_supprimer = False
    liste_tempo_item = []
    changements = []

    # Réduire le compteur de la bombe
    bombe["tours_restants"] -= 1

    if bombe["tours_restants"] == 0:
        # Gérer les changements sur le plateau
        directions = [
            [(i, 0) for i in range(1, joueur["portee"] + 1)],  # Droite
            [(-i, 0) for i in range(1, joueur["portee"] + 1)],  # Gauche
            [(0, -i) for i in range(1, joueur["portee"] + 1)],  # Haut
            [(0, i) for i in range(1, joueur["portee"] + 1)],  # Bas
            [(0, 0)]  # Centre
        ]

        for direction in directions:
            for dx, dy in direction:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(Plateau[0]) and 0 <= ny < len(Plateau):
                    if Plateau[ny][nx] == "C":
                        break  # Arrête la propagation dans cette direction

                    if Plateau[ny][nx] == "F":  # Fantôme
                        for fantome in pos_fantomes:
                            if (nx, ny) == (fantome["x"], fantome["y"]):
                                jeu.supprimer(fantome["image"])
                                pos_fantomes.remove(fantome)
                                joueur = ajouter_score(100, joueur)  # Ajouter 100 points
                                Plateau[ny][nx] = 0
                                changements.append((nx, ny))

                    elif Plateau[ny][nx] == "M":  # Mur
                        joueur = ajouter_score(10, joueur)  # Ajouter 10 points
                        Plateau[ny][nx] = 0
                        changements.append((nx, ny))
                        liste_tempo_item.append((nx, ny))  # Ajouter pour potentielle génération d'item


        # Mettre à jour le plateau visuellement
        pos_fantomes = mettre_a_jour_plateau(jeu, Plateau, changements, dimensions, pos_fantomes)

        # Gestion des items sur les cases affectées
        for item_x, item_y in liste_tempo_item:
            if random.random() < probabilité_items:  # Probabilité de 20% de générer un item
                spawn_item(jeu, Plateau, item_x, item_y, dimensions)

        # Activer l'effet visuel d'explosion après les changements
        bombe["images_explosion"], running, joueur, affichages = explosion_bombe(
            jeu, Plateau, x, y, running, affichages, dimensions, joueur
        )

    elif bombe["tours_restants"] == -1:
        # Retirer les effets d'explosion
        for img in bombe.get("images_explosion", []):
            jeu.supprimer(img)

        # Supprimer les images d'explosion et marquer la bombe pour suppression
        bombe_a_supprimer = True

    return joueur, running, affichages, bombe_a_supprimer, pos_fantomes






