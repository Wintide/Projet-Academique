from parametres import *
from datetime import datetime
Liste_de_competence = []


def perdre_vie(jeu, dimensions, running, joueur, affichages):
    """
    Réduit le nombre de vies du joueur et met à jour l'affichage.
    :param jeu: L'objet gérant l'affichage.
    :param running: Booléen indiquant si le jeu est en cours.
    :param joueur: Dictionnaire contenant les informations du joueur.
    :param affichages: Dictionnaire contenant les objets Affichage pour afficher les textes.
    :return: Nombre de vies mises à jour, booléen indiquant si le jeu est en cours, score actuel, identifi
    """
    COTE_X = dimensions["COTE_X"]
    COTE_Y = dimensions["COTE_Y"]
    LARGEUR_FENETRE = dimensions["LARGEUR_FENETRE"]
    HAUTEUR_FENETRE = dimensions["HAUTEUR_FENETRE"]
    joueur["vies"] -= 1
    print(f"Vies restantes : {joueur["vies"]}")

    # Mettre à jour l'affichage des vies
    jeu.supprimer(affichages["affichage_vies"])
    affichages["affichage_vies"] = jeu.afficherTexte(f"{joueur["vies"]}", COTE_X * 16.5, COTE_Y // 2, "red", 18)

    if joueur["vies"] <= 0:
        print("Game Over!")
        jeu.afficherImage(LARGEUR_FENETRE/2 - COTE_X*2.5, HAUTEUR_FENETRE/2 - COTE_Y*2.5, "images/gameover.png")
        running = False  # Fin du jeu
        with open('liste_scores.txt', 'a') as f:
            f.write("Score:  ")
            f.write(str(joueur["score"]))
            f.write(" Manche perdu")
            date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            f.write(" Date: ")
            f.write(date)
            f.write("\n")
    return joueur, running, affichages

# Liste des items au sol
items_au_sol = []


def spawn_item(jeu, Plateau, x, y, dimensions, tours_restants=tours_restants_items):
    """
    Fait apparaître un item au sol à la position spécifiée.
    :param jeu: Objet Jeu pour gérer l'affichage.
    :param Plateau: La matrice représentant le plateau.
    :param x: Coordonnée x de la case.
    :param y: Coordonnée y de la case.
    :param dimensions: Dictionnaire contenant les dimensions des cases et des images.
    :param tours_restants: Nombre de tours avant disparition de l'item.
    """
    COTE_X = dimensions["COTE_X"]
    COTE_Y = dimensions["COTE_Y"]
    # Vérifier que la case est valide (vide)
    if Plateau[y][x] == 0:

        # Créer l'image de l'item
        item_image = jeu.afficherImage(x * COTE_X, y * COTE_Y + COTE_Y, "images/upgrade.png")
        if item_image is None:
            print("Erreur : l'image de l'item n'a pas pu être créée à ({}, {})".format(x, y))
            return

        # Ajouter l'item à la liste des items au sol
        items_au_sol.append({"x": x, "y": y, "image": item_image, "tours_restants": tours_restants})



        # Mettre à jour le plateau
        Plateau[y][x] = "I"  # "I" pour Item

def gerer_items(jeu, Plateau):
    """
    Gère la disparition des items au sol après un certain nombre de tours.
    :param jeu: Objet Jeu pour gérer l'affichage.
    :param Plateau: La matrice représentant le plateau.
    """
    items_a_retirer = []

    for item in items_au_sol:
        # Réduire le compteur de tours
        item["tours_restants"] -= 1


        # Vérifier si l'item doit être retiré
        if item["tours_restants"] <= 0:
            x, y = item["x"], item["y"]
            # Supprimer l'image de l'item
            jeu.supprimer(item["image"])
            # Marquer l'item pour suppression
            items_a_retirer.append(item)
            # Libérer la case sur le plateau
            Plateau[y][x] = 0

    # Supprimer les items marqués
    for item in items_a_retirer:
        items_au_sol.remove(item)

def augmenter_niveau(jeu,joueur,affichages,dimensions):
    """
    Augmente le niveau du joueur.
    :param jeu: Objet Jeu pour gérer l'affichage.
    :param joueur: Dictionnaire contenant les informations du joueur.
    :param affichages: Dictionnaire contenant les objets Affichage pour afficher les textes.
    :param dimensions: Dictionnaire contenant les dimensions des cases et des images.
    :return: Niveau actuel, nombre de vies, portée actuelle, et dictionnaire des objets Affichage.
    """
    COTE_X = dimensions["COTE_X"]
    COTE_Y = dimensions["COTE_Y"]


    joueur["niveau"] += 1
    if joueur["niveau"]%2 == 0:
        joueur["portee"] += 1
        print(f"Portée de: {joueur["portee"]}")

    elif joueur["niveau"]%2 == 1:
        joueur["vies"] += 1
        jeu.supprimer(affichages["affichage_vies"])
        affichages["affichage_vies"] = jeu.afficherTexte(f"{joueur["vies"]}", COTE_X * 16.5, COTE_Y // 2, "red", 18)
        print(f"{joueur["vies"]} coeur")

    jeu.supprimer(affichages["affichage_niveau"])
    affichages["affichage_niveau"] = jeu.afficherTexte(f"{joueur["niveau"]}", COTE_X * 18.5, COTE_Y // 2, "yellow", 18)
    print(f"Niveau augmenté : {joueur["niveau"]}")

    return joueur, affichages

