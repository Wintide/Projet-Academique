#
# Fonctions liées au fantomes / "F"
#
from PIL import Image
from validation import est_valide
import random







def ajout_fantome(jeu, x, y, dimensions, Plateau, pos_fantomes):
    """
    Ajoute un fantôme à la liste des fantômes avec ses coordonnées.
    Le fantôme doit apparaître sur une case adjacente valide (pas une case 'E').
    :param jeu: Objet Jeu pour afficher des images.
    :param x: Coordonnée x de la case "E" où le fantôme doit apparaître.
    :param y: Coordonnée y de la case "E" où le fantôme doit apparaître.
    :param dimensions: Dictionnaire contenant les dimensions du plateau et des cases.
    :param Plateau: La matrice représentant le plateau de jeu.
    :param pos_fantomes: Liste des fantômes
    """
    COTE_X = dimensions["COTE_X"]
    COTE_Y = dimensions["COTE_Y"]

    # Chercher une case adjacente valide pour le spawn
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Haut, Bas, Gauche, Droite
    random.shuffle(directions)  # Mélanger pour un peu de hasard dans l'apparition

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(Plateau[0]) and 0 <= ny < len(Plateau):
            # Vérifier que la case n'est pas une colonne (C) et qu'elle est vide
            if Plateau[ny][nx] == "D" or Plateau[ny][nx] == 0:  # Case vide
                # Créer l'image du fantôme

                fantome_image = jeu.afficherImage(nx * COTE_X, ny * COTE_Y + COTE_Y, "images/fantome.png")
                if fantome_image is None:
                    print(f"Erreur : l'image du fantôme n'a pas pu être créée à ({nx}, {ny})")
                    return

                # Ajouter le fantôme au dictionnaire pos_fantomes avec les coordonnées comme clé

                fantome = {
                    "x": nx,
                    "y": ny,
                    "image": fantome_image,
                    "ax": None,
                    "ay": None
                }
                pos_fantomes.append(fantome)
                Plateau[ny][nx] = "F"  # Marquer la case comme occupée par un fantôme

                return pos_fantomes # Une fois que le fantôme est placé, on arrête


    print(f"Impossible de placer un fantôme autour de la case ({x}, {y}).")
    return pos_fantomes





def deplace_fantome(plateau, jeu, dimensions, pos_fantomes):
    """
    Déplace tous les fantômes présents sur le plateau, en évitant les collisions avec d'autres fantômes,
    les cases "E", et leur case précédente (ax, ay).
    :param plateau: La matrice représentant le plateau de jeu
    :param jeu: L'objet moteur graphique
    :param dimensions: Dictionnaire contenant les dimensions du jeu
    :param pos_fantomes: Liste des fantômes avec leurs coordonnées et images
    :return: Mise à jour de la liste des fantômes
    """
    COTE_X = dimensions["COTE_X"]
    COTE_Y = dimensions["COTE_Y"]
    pos_fantomes_actualise = []  # Liste des fantômes actualisés

    for fantome in pos_fantomes:
        x_fantome = fantome["x"]
        y_fantome = fantome["y"]
        ax, ay = fantome.get("ax"), fantome.get("ay")  # Case précédente

        # Les directions possibles
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Haut, Bas, Gauche, Droite
        random.shuffle(directions)  # Mélanger pour rendre les déplacements aléatoires

        # Essayer chaque direction jusqu'à en trouver une valide
        for dx, dy in directions:
            x_nouvelle = x_fantome + dx
            y_nouvelle = y_fantome + dy

            # Vérifier si la nouvelle position est valide et respecte les contraintes
            if (
                est_valide(plateau, x_nouvelle, y_nouvelle) and
                not any(f["x"] == x_nouvelle and f["y"] == y_nouvelle for f in pos_fantomes) and
                plateau[y_nouvelle][x_nouvelle] != "E" and
                plateau[y_nouvelle][x_nouvelle] != "J" and
                (x_nouvelle, y_nouvelle) != (ax, ay)  # Ne pas revenir sur la case précédente
            ):
                # Supprimer l'image actuelle du fantôme
                jeu.supprimer(fantome["image"])

                # Créer une nouvelle image pour le fantôme à la nouvelle position
                new_image = jeu.afficherImage(x_nouvelle * COTE_X, y_nouvelle * COTE_Y + COTE_Y, "images/fantome.png")

                # Mettre à jour le plateau
                plateau[y_fantome][x_fantome] = 0  # Libérer l'ancienne case
                plateau[y_nouvelle][x_nouvelle] = "F"  # Occuper la nouvelle case

                # Ajouter le fantôme mis à jour dans la nouvelle liste
                fantome["x"], fantome["y"], fantome["image"], fantome["ax"], fantome["ay"] = x_nouvelle, y_nouvelle, new_image, x_fantome, y_fantome
                pos_fantomes_actualise.append(fantome)

                break  # Le fantôme a bougé, passer au suivant

            elif (
                plateau[y_nouvelle][x_nouvelle] == "J" and
                (x_nouvelle, y_nouvelle) != (ax, ay)  # Ne pas revenir sur la case précédente
            ):

                # Modifier les cases anciennes pour que le fantomes repartent dans le sens inverse
                fantome["ax"], fantome["ay"] = x_nouvelle, y_nouvelle
                pos_fantomes_actualise.append(fantome)

                break  # Le fantôme a fait son action

        else:
            # Si aucune direction valide n'a été trouvée, ramener le fantome à la position précédente
            if (fantome["ax"], fantome["ay"]) != (None, None):
                jeu.supprimer(fantome["image"])
                fantome["image"] = jeu.afficherImage(ax * COTE_X, ay * COTE_Y + COTE_Y, "images/fantome.png")
                fantome["x"], fantome["y"], fantome["ax"], fantome["ay"] = fantome["ax"], fantome["ay"], fantome["x"], fantome["y"]
                pos_fantomes_actualise.append(fantome)  # Le fantôme a été ramassé, passer au suivant
                plateau[fantome["y"]][fantome["x"]] = "F"
                plateau[fantome["ay"]][fantome["ax"]] = 0


    return pos_fantomes_actualise




def gerer_fantomes(jeu, Plateau, dimensions, pos_fantomes):
    """
    Gère le spawn des fantômes et leur déplacement.
    :param jeu: L'objet moteur graphique
    :param Plateau: La matrice représentant le plateau de jeu
    :param dimensions: Dictionnaire contenant les dimensions du jeu
    :param pos_fantomes: Liste des fantômes
    :return: Liste mise à jour des fantômes
    """
    for y in range(len(Plateau)):
        for x in range(len(Plateau[y])):
            if Plateau[y][x] == "E":
                pos_fantomes = ajout_fantome(jeu, x, y, dimensions, Plateau, pos_fantomes)



    return pos_fantomes






