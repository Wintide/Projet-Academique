def est_valide(Plateau,x, y):
    """
    Vérifie si une case est valide pour le déplacement.
    :param x: Coordonnée x de la case (colonne)
    :param y: Coordonnée y de la case (ligne)
    :return: True si la case est valide, False sinon
    """
    # Vérifie si (x, y) est dans les limites du plateau
    if x < 0 or x >= len(Plateau[0]) or y < 0 or y >= len(Plateau):
        return False  # Si les coordonnées sont en dehors des limites du plateau

    # Vérifie si la case n'est pas une colonne (C) ou un mur (M)
    elif Plateau[y][x] in ["C", "M", "F", "J"]:
        return False  # La case n'est pas valide (colonne ou mur)

    else:

        return True
