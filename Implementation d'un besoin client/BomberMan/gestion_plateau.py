import random

def generer_plateau(largeur, hauteur, pourcentage_murs=20):
    """
    Génère un plateau de jeu avec :
    - Une bordure de colonnes ("C").
    - Des colonnes fixes ("C") une case sur deux, une ligne sur deux.
    - Des zones sûres ("D") autour du joueur et du spawn ethernet.
    - Des murs ("M") placés aléatoirement.
    :param largeur: Largeur du plateau (nombre de colonnes).
    :param hauteur: Hauteur du plateau (nombre de lignes).
    :param pourcentage_murs: Pourcentage de cases à transformer en murs.
    :return: Une matrice 2D représentant le plateau.
    """
    if largeur < 5 or hauteur < 5:  # Empecher un plateau trop petit
        raise ValueError("La largeur et la hauteur doivent être d'au moins 5.")

    # Initialiser le plateau avec des murs ("C") tout autour
    plateau = [["C" for _ in range(largeur)] for _ in range(hauteur)]

    # Ajouter des colonnes fixes ("C") une ligne sur deux, une case sur deux
    for y in range(1, hauteur - 1):
        for x in range(1, largeur - 1):
            if y % 2 == 0 and x % 2 == 0:
                plateau[y][x] = "C"  # Colonne fixe
            else:
                plateau[y][x] = 0  # Initialiser à vide

    # Placer le joueur et sa zone sûre
    plateau[1][1] = "J"
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = 1 + dx, 1 + dy
        if 0 <= nx < largeur and 0 <= ny < hauteur and plateau[ny][nx] != "C":
            plateau[ny][nx] = "D"  # Zone sûre pour le joueur

    # Placer le spawn ethernet et sa zone sûre
    plateau[hauteur - 2][largeur - 2] = "E"
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = largeur - 2 + dx, hauteur - 2 + dy
        if 0 <= nx < largeur and 0 <= ny < hauteur and plateau[ny][nx] != "C":
            plateau[ny][nx] = "D"  # Zone sûre pour le spawn ethernet

    # Générer des murs ("M") aléatoirement, en excluant les colonnes fixes et les zones sûres
    nb_cases = (largeur - 2) * (hauteur - 2)  # Nombre de cases à l'intérieur
    nb_murs = (pourcentage_murs * nb_cases) // 100  # Nombre de murs à placer
    murs_places = 0  # Compteur des murs

    while murs_places < nb_murs:
        x = random.randint(1, largeur - 2)
        y = random.randint(1, hauteur - 2)

        # Placer un mur si la case est vide et hors des colonnes fixes et zones sûres
        if plateau[y][x] == 0:
            plateau[y][x] = "M"
            murs_places += 1

    return plateau

def configurer_fenetre_et_cases_dynamiques(taille_plateau_x, taille_plateau_y, max_largeur=800, max_hauteur=800):
    """
    Configure la taille des cases et de la fenêtre dynamiquement pour s'adapter au plateau.
    :param taille_plateau_x: Nombre de cases en largeur
    :param taille_plateau_y: Nombre de cases en hauteur
    :param max_largeur: Largeur maximale de la fenêtre
    :param max_hauteur: Hauteur maximale de la fenêtre
    :return: Taille des cases (COTE_X, COTE_Y) et dimensions de la fenêtre (LARGEUR_FENETRE, HAUTEUR_FENETRE)
    """
    # Taille maximale possible pour une case
    case_largeur_max = max_largeur // taille_plateau_x
    case_hauteur_max = (max_hauteur - 30) // taille_plateau_y  # Réserver un espace pour la barre d'infos

    # Utiliser la taille minimale pour garder des cases carrées
    taille_case = min(case_largeur_max, case_hauteur_max)

    # Dimensions finales de la fenêtre
    LARGEUR_FENETRE = taille_plateau_x * taille_case
    HAUTEUR_FENETRE = taille_plateau_y * taille_case + taille_case  # +taille_case pour la barre d'infos

    return taille_case, taille_case, LARGEUR_FENETRE, HAUTEUR_FENETRE

# Variable globale pour indiquer si la porte a été placée
porte_placee = False

def apparition_porte(plateau):
    """
    Fait apparaître une porte au centre du plateau lorsque tous les murs ("M") sont détruits.
    Si le centre du plateau n'est pas une case valide, ajuste la position pour trouver une case valide.
    :param plateau: La matrice représentant le plateau de jeu.
    """
    global porte_placee  # Indique que cette variable est globale

    # Vérifie si la porte a déjà été placée
    if porte_placee:
        print("La porte est déjà placée.")
        return

    # Vérifier si tous les murs sont détruits
    murs_restants = any("M" in ligne for ligne in plateau)
    if murs_restants:
        print("Des murs restent encore sur le plateau. La porte ne peut pas apparaître.")
        return  # Pas de porte tant qu'il reste des murs

    print("Tous les murs sont détruits. Apparition de la porte.")

    # Calculer le centre du plateau
    centre_y = len(plateau) // 2
    centre_x = len(plateau[0]) // 2

    # Vérifier si la case au centre est valide
    def est_case_valide(x, y):
        return 0 <= x < len(plateau[0]) and 0 <= y < len(plateau) and plateau[y][x] == 0

    # Chercher une case valide à partir du centre
    for dy in range(-1, 2):  # Vérifie les cases adjacentes (1 unité autour)
        for dx in range(-1, 2):
            nx, ny = centre_x + dx, centre_y + dy
            if est_case_valide(nx, ny):
                plateau[ny][nx] = "P"  # Placer la porte
                print(f"Porte placée en position ({nx}, {ny}).")
                porte_placee = True  # Marquer la porte comme placée
                return  nx, ny

    print("Impossible de placer une porte. Aucune case valide trouvée.")

