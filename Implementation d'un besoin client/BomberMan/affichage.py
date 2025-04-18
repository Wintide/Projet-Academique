

pos_colonnes = {}
pos_murs = {}


def affichage_plateau(Plateau,COTE_X, COTE_Y, jeu):
    global ethernet, pos_murs, pos_colonnes
    """"
    Affiche le plateau de jeu à l'écran.
    :param plateau: La matrice représentant le plateau de jeu.
    :param COTE_X: La largeur d'une case en pixels.
    :param COTE_Y: La hauteur d'une case en pixels.
    :param jeu: L'objet représentant l'interface graphique.
    """

    ligne_i = 1
    case_i = 0
    for Ligne in Plateau:
        for Case in Ligne:

            if Case == 0 or Case == "D" or Case == "F" or Case == "J":
                case_i += 1
            elif Case == "M":
                mur = jeu.afficherImage(case_i*COTE_X, ligne_i*COTE_Y, "images/mur.png")
                pos_murs[(case_i,ligne_i-1)] = mur
                case_i += 1
            elif Case == "C":
                colonne = jeu.afficherImage(case_i*COTE_X, ligne_i*COTE_Y,"images/colonne.png")
                pos_colonnes[(case_i,ligne_i-1)] = colonne
                case_i += 1
            elif Case == "E":
                ethernet = jeu.afficherImage(case_i*COTE_X, ligne_i*COTE_Y,"images/ethernet.png")
                case_i += 1
        ligne_i += 1
        case_i = 0


def mettre_a_jour_plateau(jeu, plateau, changements, dimensions, pos_fantomes):
    """
    Met à jour le plateau après un changement (explosion, déplacement, etc.), et réactualise le dictionnaire pos_fantomes.
    :param jeu: L'objet représentant l'interface graphique.
    :param plateau: La matrice représentant le plateau de jeu.
    :param changements: Liste de tuples contenant les coordonnées (x, y) des cases modifiées.
    :param dimensions: Dictionnaire contenant les dimensions du jeu.
    :param pos_fantomes: Dictionnaire des positions des fantômes (clé: (x, y), valeur: image).
    :return: Le dictionnaire des fantomes actualiser
    """
    COTE_X = dimensions["COTE_X"]
    COTE_Y = dimensions["COTE_Y"]
    for x, y in changements:
        # Effacer la case (on suppose que le fond est vert)
        jeu.dessinerRectangle(x * COTE_X, y * COTE_Y + COTE_Y, COTE_X, COTE_Y, "green")

        # Afficher l'état actuel de la case
        Case = plateau[y][x]  # Récupérer la valeur de la case dans le plateau

        if Case == 0:
            # Case vide ou porte (on laisse le fond vert pour une case vide)
            for fantome in pos_fantomes:
                if (x, y) == (fantome["x"], fantome["y"]):
                    # Si la case est vide mais reste dans pos_fantomes, on supprime l'entrée
                    jeu.supprimer(fantome["image"])
                    pos_fantomes.remove(fantome)

        elif Case == "M":
            # Afficher un mur
            jeu.afficherImage(x * COTE_X, y * COTE_Y + COTE_Y, "images/mur.png")
            print("mur affiché")
        elif Case == "C":
            # Afficher une colonne
            jeu.afficherImage(x * COTE_X, y * COTE_Y + COTE_Y, "images/colonne.png")
        elif Case == "P":
            # Afficher une porte
            jeu.afficherImage(x * COTE_X, y * COTE_Y + COTE_Y, "images/porte.png")
        elif Case == "F":
            # Si un fantôme est présent sur cette case
            for fantome in pos_fantomes:
                if (x, y) == (fantome["x"], fantome["y"]):
                    # Si un fantôme est déjà enregistré à cette position, ne rien faire
                    pass
                else:
                    fantome = {
                        "x": x,
                        "y": y,
                        "image": jeu.afficherImage(x * COTE_X, y * COTE_Y + COTE_Y, "images/fantome.png"),
                        "ax": x,
                        "ay": y
                    }
                    pos_fantomes.append(fantome)

    return pos_fantomes

def ajouter_score(points, joueur):
    """
    Ajoute des points au score et met à jour l'affichage.
    :param points: Nombre de points à ajouter.
    :param joueur: Dictionnaire contenant les informations du joueur (score, vies, etc.).
    :return: Le nouveau score.
    """

    joueur["score"] += points


    return joueur








