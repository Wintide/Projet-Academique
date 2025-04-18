#
# Fonctions liées au joueur / "J"
#
from validation import est_valide
from bombe import ajout_bombe
from datetime import datetime
from affectation import items_au_sol,augmenter_niveau
from parametres import *


def trouve_joueur_position(plateau):
    """
    Recherche la position du joueur ("J) dans la matrice du plateau.
    :param plateau: La matrice représentant le plateau de jeu
    :return: Les coordonnées (x, y) du joueur, ou None si le joueur n'est pas trouvé
    """
    for y in range(0,len(plateau)):  # Parcourir chaque ligne
        for x in range(0,len(plateau[y])):  # Parcourir chaque colonne
            if plateau[y][x] == "J":  # Si la case contient un joueur

                return x, y  # Retourne les coordonnées (x, y)

    return None  # Si le joueur n'est pas trouvé


def deplace_joueur(plateau, jeu, joueur,running,dimensions,affichages):
    """
    Déplace le joueur sur le plateau en fonction des entrées clavier.
    Supprime l'image précédente avant d'afficher la nouvelle position.
    Crée une bombe si la touche espace est pressée.
    :param plateau: La matrice représentant le plateau de jeu
    :param jeu: L'objet qui gère l'affichage et les événements
    :param joueur: Dictionnaire contenant les infos du joueur
    :param running: Booléen indiquant si le jeu est en cours
    :param dimensions: Dictionnaire contenant les dimensions du plateau et des cases
    :param affichages: Dictionnaire contenant les objets Affichage pour afficher les textes
    """
    COTE_X = dimensions["COTE_X"]
    COTE_Y = dimensions["COTE_Y"]
    LARGEUR_FENETRE = dimensions["LARGEUR_FENETRE"]
    HAUTEUR_FENETRE = dimensions["HAUTEUR_FENETRE"]
    x_joueur, y_joueur = joueur["joueur_x"],joueur["joueur_y"]  # position du joueur
    moves = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0), "z": (0, -1), "s": (0, 1), "q": (-1, 0), "d": (1, 0)}

    while True:  # Boucle jusqu'à ce qu'une action valide soit effectuée
        direction = jeu.attendreTouche()  # Attend une entrée utilisateur

        if direction in moves:  # Déplacement
            dx, dy = moves[direction]
            x_nouvelle, y_nouvelle = x_joueur + dx, y_joueur + dy

            if est_valide(plateau, x_nouvelle, y_nouvelle):  # Vérifie si la case est valide
                # Supprimer l'image précédente
                if joueur is not None:
                    jeu.supprimer(joueur["img_joueur"])
                else:
                    print("Erreur : 'joueur' est None lors de la suppression.")


                if plateau[y_nouvelle][x_nouvelle] == "I":  # Si le joueur est sur une case avec un item

                    for item in items_au_sol:
                        if item["x"] == x_nouvelle and item["y"] == y_nouvelle:
                            jeu.supprimer(item["image"])
                            items_au_sol.remove(item)
                            plateau[y_nouvelle][x_nouvelle] = 0  # Libérer la case
                            joueur, affichages, = augmenter_niveau(jeu,joueur,affichages,dimensions)





                # Afficher la nouvelle position
                joueur["img_joueur"] = jeu.afficherImage(x_nouvelle * COTE_X, y_nouvelle * COTE_Y + COTE_Y, "images/joueur.png")
                if joueur is None:
                    print("Erreur : échec de l'affichage de l'image du joueur.")


                # Vérification de la victoire
                if plateau[y_nouvelle][x_nouvelle] == "P":
                    print("Victoire ! Vous avez atteint la porte !")
                    jeu.afficherImage(LARGEUR_FENETRE/2 - COTE_X*2.5, HAUTEUR_FENETRE/2 - COTE_Y*2.5,"images/victoire.png")  # Affiche un message
                    running = False  # Arrêter le jeu
                    with open('liste_scores.txt', 'a') as f:
                        f.write("Score:  ")
                        f.write(str(joueur["score"]))
                        f.write(" Manche gagnée")
                        date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                        f.write(" Date: ")
                        f.write(date)
                        f.write("\n")
                    return joueur, running, affichages  # Arrêter le jeu
                # Mettre à jour le plateau
                plateau[y_joueur][x_joueur] = 0
                plateau[y_nouvelle][x_nouvelle] = "J"
                joueur["joueur_x"], joueur["joueur_y"] = x_nouvelle,y_nouvelle

                break  # Sortir de la boucle après un déplacement valide

            else:
                print(f"Case ({x_nouvelle}, {y_nouvelle}) invalide pour le déplacement.")

        elif direction == "space":  # Poser une bombe
            ajout_bombe(jeu, x_joueur, y_joueur, tours_restants_bombes, dimensions)
            break  # Sortir de la boucle après avoir posé une bombe
        elif direction=="Delete":
            running = False
            print("Jeu intérrompu")
            jeu.afficherImage(LARGEUR_FENETRE/2 - COTE_X*2.5, HAUTEUR_FENETRE/2 - COTE_Y*2.5, "images/erreur.png")  # Affiche un message
            return joueur, running, affichages
        elif direction=="Return":

            for ligne in plateau:
                print(' '.join(str(case).center(3) for case in ligne))








        else:
            print("Action invalide. Veuillez essayer à nouveau.")

    return joueur, running, affichages


def deplace_joueur_souris(plateau, jeu, dimensions, joueur, running, affichages):
    """
    Déplace le joueur selon la position de la souris. Empêche le jeu de continuer
    tant qu'un déplacement valide n'est pas effectué.
    Crée une bombe si la case selectionner est la case actuelle.
    :param plateau: La matrice représentant le plateau de jeu
    :param jeu: L'objet qui gère l'affichage et les événements
    :param joueur: Dictionnaire contenant les infos du joueur
    :param running: Booléen indiquant si le jeu est en cours
    :param dimensions: Dictionnaire contenant les dimensions du plateau et des cases
    :param affichages: Dictionnaire contenant les objets Affichage pour afficher les textes
    """
    COTE_X = dimensions["COTE_X"]
    COTE_Y = dimensions["COTE_Y"]
    LARGEUR_FENETRE = dimensions["LARGEUR_FENETRE"]
    HAUTEUR_FENETRE = dimensions["HAUTEUR_FENETRE"]
    x_joueur, y_joueur = joueur["joueur_x"], joueur["joueur_y"]  # position du joueur

    while True:  # Boucle infinie jusqu'à un déplacement valide
        clic = jeu.attendreClic()

        # Calculer les déplacements relatifs
        dx, dy = clic.x // COTE_X - x_joueur, clic.y // COTE_Y - y_joueur - 1

        # Vérifie si le clic est un déplacement valide (1 case adjacente)
        if abs(dx) + abs(dy) == 1:  # Déplacement valide
            x_nouvelle = x_joueur + dx
            y_nouvelle = y_joueur + dy

            if est_valide(plateau, x_nouvelle, y_nouvelle):  # Vérifie si la case est valide
                # Supprimer l'image précédente
                if joueur is not None:
                    jeu.supprimer(joueur["img_joueur"])
                else:
                    print("Erreur : 'joueur' est None lors de la suppression.")

                if plateau[y_nouvelle][x_nouvelle] == "I":  # Si le joueur est sur une case avec un item

                    for item in items_au_sol:
                        if item["x"] == x_nouvelle and item["y"] == y_nouvelle:
                            jeu.supprimer(item["image"])
                            items_au_sol.remove(item)
                            plateau[y_nouvelle][x_nouvelle] = 0  # Libérer la case
                            joueur, affichages, = augmenter_niveau(jeu, joueur, affichages, dimensions)

                # Afficher la nouvelle position
                joueur["img_joueur"] = jeu.afficherImage(x_nouvelle * COTE_X, y_nouvelle * COTE_Y + COTE_Y,
                                                         "images/joueur.png")
                if joueur is None:
                    print("Erreur : échec de l'affichage de l'image du joueur.")

                # Vérification de la victoire
                if plateau[y_nouvelle][x_nouvelle] == "P":
                    print("Victoire ! Vous avez atteint la porte !")
                    jeu.afficherImage(LARGEUR_FENETRE / 2 - COTE_X * 2.5, HAUTEUR_FENETRE / 2 - COTE_Y * 2.5,
                                      "images/victoire.png")  # Affiche un message
                    running = False  # Arrêter le jeu
                    with open('liste_scores.txt', 'a') as f:
                        f.write("Score:  ")
                        f.write(str(joueur["score"]))
                        f.write(" Manche gagnée")
                        date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                        f.write(" Date: ")
                        f.write(date)
                        f.write("\n")
                    return joueur, running, affichages  # Arrêter le jeu
                # Mettre à jour le plateau
                plateau[y_joueur][x_joueur] = 0
                plateau[y_nouvelle][x_nouvelle] = "J"
                joueur["joueur_x"], joueur["joueur_y"] = x_nouvelle, y_nouvelle

                # Mettre à jour le plateau
                plateau[y_joueur][x_joueur] = 0  # Libérer l'ancienne position
                plateau[y_nouvelle][x_nouvelle] = "J"  # Occuper la nouvelle position
                break  # Sortir de la boucle une fois le déplacement effectué
            else:
                print(f"Case ({x_nouvelle}, {y_nouvelle}) invalide pour le déplacement.")
        elif dx == 0 and dy == 0:  # Si le clic est sur la case actuelle
            ajout_bombe(jeu, x_joueur, y_joueur, tours_restants_bombes, dimensions)  # Place une bombe
            break  # Permet de sortir de la boucle pour poser une bombe
        else:
            print("Le clic ne correspond pas à un déplacement valide (1 case).")

    return joueur, running, affichages












