import random
from image import *
from affichage import mettre_a_jour_plateau
from tkiteasy import ouvrirFenetre
from joueur import deplace_joueur,deplace_joueur_souris,trouve_joueur_position
from bombe import gerer_bombes,actualiser_bombe
from affichage import affichage_plateau
from fantome import gerer_fantomes,deplace_fantome
from affectation import perdre_vie, gerer_items
from datetime import datetime
from gestion_plateau import *




jouer = True #Ici la variable jouer nous sert a relancer le jeu a la fin de la partie grace a une boucle  si le joueur le souhaite
while jouer:
    from parametres import * # La position de l'imporation est primordial ici si l'on veut réinitialisé les valeurs
    #
    # Création du plateau de jeu
    #



    # Generation du plateau grace a la fonction
    Plateau = generer_plateau(largeur, hauteur, pourcentage_murs) #Vous pouvez mettre un plateau deja créer a la place de la fonction de génération
    # "0" case vide
    # "D" case vide (zone depart/safe)
    # "C" colonne
    # "M" mur
    # "J" joueur
    # "E" prise ethernet
    # "F" fantome
    # "P" Porte


    # Definitions de la largeur et la hauteur de la fenêtre
    COTE_X, COTE_Y, LARGEUR_FENETRE, HAUTEUR_FENETRE = configurer_fenetre_et_cases_dynamiques(len(Plateau[0]), len(Plateau), 600, 600)

    dimensions = {
        "COTE_X": COTE_X,
        "COTE_Y": COTE_Y,
        "LARGEUR_FENETRE": LARGEUR_FENETRE,
        "HAUTEUR_FENETRE": HAUTEUR_FENETRE
    }

    # Chargement des images
    charger_images(dimensions["COTE_X"], dimensions["COTE_Y"])


    #
    #Initialisation
    #
    jeu = ouvrirFenetre(dimensions["LARGEUR_FENETRE"], dimensions["HAUTEUR_FENETRE"])


    #
    # Mode de jeu
    #
    souris = jeu.afficherImage(dimensions["LARGEUR_FENETRE"]/2, (dimensions["HAUTEUR_FENETRE"]*1)/3 - dimensions["COTE_Y"], "images/souris.png")
    clavier = jeu.afficherImage(dimensions["LARGEUR_FENETRE"]/2 - (dimensions["COTE_X"]*5), (dimensions["HAUTEUR_FENETRE"]*1)/3 - dimensions["COTE_Y"], "images/clavier.png")
    liste_scores = jeu.afficherImage(dimensions["LARGEUR_FENETRE"]/2 - (dimensions["COTE_X"]*3), (dimensions["HAUTEUR_FENETRE"]*2)/3, "images/score.png")
    top3 = jeu.afficherImage(dimensions["LARGEUR_FENETRE"]/2, (dimensions["HAUTEUR_FENETRE"]*2)/3, "images/trophee.png")

    definie = False # Boucle tant que  le mode de jeu n'a pas ete definie
    while not definie:
        clic = jeu.attendreClic()
        # Mode de jeu: clavier
        if clavier.x < clic.x < clavier.x + dimensions["COTE_X"]*5 and clavier.y < clic.y < clavier.y + dimensions["COTE_Y"]*5:
            ModeDeJeux = 0
            definie = True
        # Mode de jeu: souris
        elif souris.x < clic.x < souris.x +dimensions["COTE_X"]*5 and souris.y < clic.y < souris.y +dimensions["COTE_Y"]*5:
            ModeDeJeux = 1
            definie = True
        # Appel du tableau des scores
        elif liste_scores.x < clic.x < liste_scores.x +dimensions["COTE_X"]*3 and liste_scores.y < clic.y < liste_scores.y + dimensions["COTE_Y"]*3:
            jeu.supprimer(souris)
            jeu.supprimer(clavier)
            jeu.supprimer(liste_scores)
            jeu.supprimer(top3)
            with open('liste_scores.txt', 'r') as fichier:  # Ouvre le fichier contenant les scores
                liste_des_lignes = [ligne.strip() for ligne in fichier]  # Charger tous les scores dans une liste

            total_scores = len(liste_des_lignes)
            page_actuelle = 0  # Page de départ
            scores_par_page = 10  # Nombre de scores affichés par page


            def afficher_scores(page):
                """
                Affiche les scores pour la page donnée.
                :param page: Index de la page (0 pour la première page).
                """
                # Supprimer les scores précédemment affichés
                for score_affiche in liste_des_scores:
                    jeu.supprimer(score_affiche)
                liste_des_scores.clear()

                # Calculer les indices de début et de fin pour la page
                debut = page * scores_par_page
                fin = min(debut + scores_par_page, total_scores)

                # Afficher les scores pour la page
                for i, ligne in enumerate(liste_des_lignes[debut:fin]):
                    y_offset = dimensions["COTE_Y"] * (i + 1) + 20
                    element_score = jeu.afficherTexte(ligne, dimensions["LARGEUR_FENETRE"]/2 , y_offset, "white", 14)
                    liste_des_scores.append(element_score)


            # Initialisation de l'affichage
            liste_des_scores = []
            afficher_scores(page_actuelle)

            retour_menu = False
            retour = jeu.afficherImage(0, 0, "images/retour.png")
            suivant = jeu.afficherImage(dimensions["LARGEUR_FENETRE"] - (dimensions["COTE_X"]*4), (dimensions["HAUTEUR_FENETRE"]*2)/3, "images/suivant.png")
            precedent = jeu.afficherImage((dimensions["COTE_X"]*2)/2, (dimensions["HAUTEUR_FENETRE"]*2)/3, "images/precedent.png")


            while not retour_menu:
                clic_2 = jeu.attendreClic()

                # Bouton Retour
                if retour.x < clic_2.x < retour.x +dimensions["COTE_X"]*3 and retour.y < clic_2.y < retour.y + dimensions["COTE_Y"]*3:
                    retour_menu = True
                    jeu.supprimer(retour)
                    jeu.supprimer(suivant)
                    jeu.supprimer(precedent)
                    for e in liste_des_scores:
                        jeu.supprimer(e)

                    souris = jeu.afficherImage(dimensions["LARGEUR_FENETRE"] / 2, (dimensions["HAUTEUR_FENETRE"] * 1) / 3 - dimensions["COTE_Y"], "images/souris.png")
                    clavier = jeu.afficherImage(dimensions["LARGEUR_FENETRE"] / 2 - (dimensions["COTE_X"] * 5), (dimensions["HAUTEUR_FENETRE"] * 1) / 3 - dimensions["COTE_Y"],
                                                "images/clavier.png")
                    liste_scores = jeu.afficherImage(dimensions["LARGEUR_FENETRE"] / 2 - (dimensions["COTE_X"] * 3), (dimensions["HAUTEUR_FENETRE"] * 2) / 3,
                                                     "images/score.png")
                    top3 = jeu.afficherImage(dimensions["LARGEUR_FENETRE"] / 2, (dimensions["HAUTEUR_FENETRE"] * 2) / 3,
                                             "images/trophee.png")

                # Bouton Suivant
                elif suivant.x < clic_2.x < suivant.x + dimensions["COTE_X"]*3 and suivant.y < clic_2.y < suivant.y + dimensions["COTE_Y"]*3:
                    if (page_actuelle + 1) * scores_par_page < total_scores:  # Vérifier si une page suivante existe
                        page_actuelle += 1
                        afficher_scores(page_actuelle)

                # Bouton Précédent
                elif precedent.x < clic_2.x < precedent.x + dimensions["COTE_X"]*3 and precedent.y < clic_2.y < precedent.y + dimensions["COTE_Y"]*3:
                    if page_actuelle > 0:  # Vérifier si une page précédente existe
                        page_actuelle -= 1
                        afficher_scores(page_actuelle)

        #Bouton top 3 des scores
        elif top3.x < clic.x < top3.x + dimensions["COTE_X"]*3 and top3.y < clic.y < top3.y + dimensions["COTE_Y"]*3:
            jeu.supprimer(top3)
            jeu.supprimer(souris)
            jeu.supprimer(clavier)
            jeu.supprimer(liste_scores)
            # Affichage du Top 3
            top_score = []
            titre = jeu.afficherTexte("Top 3 des scores:", dimensions["LARGEUR_FENETRE"] / 2, dimensions["COTE_Y"] * 2,
                                      "white", 18)
            with open('liste_scores.txt', 'r') as fichier:
                liste_des_lignes = [ligne.strip() for ligne in fichier]
                liste_des_scores = sorted(liste_des_lignes, key=lambda x: int(x.split()[1]), reverse=True)
                for i, t_score in enumerate(liste_des_scores[:3]):
                    y_offset = dimensions["COTE_Y"] * (i * 2 + 1) + 20
                    element_score = jeu.afficherTexte(t_score, dimensions["LARGEUR_FENETRE"] / 2,y_offset*2 + 2*dimensions["COTE_Y"], "white", 14)
                    top_score.append(element_score)

            gold = jeu.afficherImage(dimensions["LARGEUR_FENETRE"]/2 - dimensions["COTE_X"]/2, y_offset-dimensions["COTE_Y"]*2,"images/gold.png")
            argent = jeu.afficherImage(dimensions["LARGEUR_FENETRE"]/2 - dimensions["COTE_X"]/2, y_offset*1.5-dimensions["COTE_Y"],"images/argent.png")
            bronze = jeu.afficherImage(dimensions["LARGEUR_FENETRE"] / 2 - dimensions["COTE_X"] / 2, y_offset*2,
                                       "images/bronze.png")
            # Retour au menu depuis le Top 3
            retour_top3 = jeu.afficherImage(0, 0, "images/retour.png")
            retour_menu = False
            while not retour_menu:
                clic = jeu.attendreClic()
                if retour_top3.x < clic.x < retour_top3.x + dimensions["COTE_X"] * 3 and retour_top3.y < clic.y < retour_top3.y + dimensions["COTE_Y"] * 3:
                    retour_menu = True
                    # Suppression des éléments du Top 3
                    jeu.supprimer(retour_top3)
                    for e in top_score:
                        jeu.supprimer(e)

                    liste_des_scores.clear()
                    liste_des_lignes.clear()
                    top_score.clear()
                    jeu.supprimer(titre)
                    jeu.supprimer(gold)
                    jeu.supprimer(argent)
                    jeu.supprimer(bronze)
                    souris = jeu.afficherImage(dimensions["LARGEUR_FENETRE"] / 2,
                                               (dimensions["HAUTEUR_FENETRE"] * 1) / 3 - dimensions["COTE_Y"],
                                               "images/souris.png")
                    clavier = jeu.afficherImage(dimensions["LARGEUR_FENETRE"] / 2 - (dimensions["COTE_X"] * 5),
                                                (dimensions["HAUTEUR_FENETRE"] * 1) / 3 - dimensions["COTE_Y"],
                                                "images/clavier.png")
                    liste_scores = jeu.afficherImage(dimensions["LARGEUR_FENETRE"] / 2 - (dimensions["COTE_X"] * 3),
                                                     (dimensions["HAUTEUR_FENETRE"] * 2) / 3, "images/score.png")
                    top3 = jeu.afficherImage(dimensions["LARGEUR_FENETRE"] / 2, (dimensions["HAUTEUR_FENETRE"] * 2) / 3,
                                             "images/trophee.png")
    jeu.supprimer(souris)
    jeu.supprimer(clavier)
    jeu.supprimer(liste_scores)
    jeu.supprimer(top3)


    #
    #Generation du plateau
    #


    for l in range(0,dimensions["LARGEUR_FENETRE"]+1,dimensions["COTE_X"]):
        for h in range(0,dimensions["HAUTEUR_FENETRE"]+1,dimensions["COTE_Y"]):
            case_verte = jeu.dessinerRectangle(l,h,dimensions["COTE_X"],dimensions["COTE_Y"],"green")


    #Barre grise en haut de l'ecrant
    BARRE_INFO = jeu.dessinerRectangle(0,0,dimensions["LARGEUR_FENETRE"]+1,dimensions["COTE_Y"],"grey70")

    #Ajout des textes
    affichage_tour = jeu.afficherTexte(f"Tour: {tour}", dimensions["COTE_X"] * 5, dimensions["COTE_Y"] // 2, "white", 18)
    affichage_score = jeu.afficherTexte(f"Score: {score}",dimensions["COTE_X"]*12,dimensions["COTE_Y"]//2,"white",18)
    coeur = jeu.afficherImage(dimensions["COTE_X"] * 17, 0,"images/vie.png")
    etoile = jeu.afficherImage(dimensions["COTE_X"] * 19, 0,"images/niveau.png")
    affichage_vies = jeu.afficherTexte(f"{vies}", dimensions["COTE_X"] * 16.5, dimensions["COTE_Y"] // 2, "red", 18)
    affichage_niveau = jeu.afficherTexte(f"{niveau}", dimensions["COTE_X"] * 18.5, dimensions["COTE_Y"] // 2, "yellow", 18)
    joueur_x, joueur_y = trouve_joueur_position(Plateau)
    img_joueur = jeu.afficherImage(joueur_x * dimensions["COTE_X"], joueur_y*dimensions["COTE_Y"] + dimensions["COTE_Y"], "images/joueur.png")
    affichage_plateau(Plateau,dimensions["COTE_X"], dimensions["COTE_Y"],jeu) # Appel de la fonction pour afficher le plateau de jeu
    actualiser_bombe()

    affichages = {
        "affichage_tour": affichage_tour,
        "affichage_score": affichage_score,
        "coeur": coeur,
        "etoile": etoile,
        "affichage_vies": affichage_vies,
        "affichage_niveau": affichage_niveau
    }

    joueur = {
        "joueur_x": joueur_x,
        "joueur_y": joueur_y,
        "img_joueur": img_joueur,
        "score": score,
        "vies": vies,
        "niveau": niveau,
        "portee": portee
    }

    pos_fantomes = []  # Dictionnaire de positions des fantômes

    #
    # Boucle principale du jeu (avec système de tour par tour)
    #
    running = True # Variable de jeu
    porte_apparue = False  # Drapeau pour indiquer si la porte a déjà été ajoutée

    while running:
        tour -= 1

        # Vérifier si tous les murs sont détruits et ajouter une porte si nécessaire
        if not porte_apparue and not any("M" in ligne for ligne in Plateau):
            x,y = apparition_porte(Plateau)
            changements = [(x,y)]# Ajouter la porte
            pos_fantomes = mettre_a_jour_plateau(jeu, Plateau, changements, dimensions, pos_fantomes)
            porte_apparue = True  # Marquer que la porte a été ajoutée

        # Gérer les bombes (réduire les tours restants)
        joueur, running, affichages, pos_fantomes = gerer_bombes(jeu, Plateau, dimensions, pos_fantomes, joueur,
                                                            running, affichages)
        jeu.supprimer(affichages["affichage_score"])
        affichages["affichage_score"] = jeu.afficherTexte(f"Score: {joueur["score"]}", dimensions["COTE_X"] * 12, dimensions["COTE_Y"] // 2, "white", 18)




        # Mode jeux : clavier
        if ModeDeJeux == 0 and running:
            joueur, running, affichages = deplace_joueur(Plateau, jeu, joueur, running, dimensions,affichages)

        # Mode jeux : souris
        elif ModeDeJeux == 1 and running:
            joueur, running, affichages = deplace_joueur_souris(Plateau, jeu, dimensions, joueur, running, affichages)

        gerer_items(jeu, Plateau)




        # Déplacer les fantômes si présents
        if len(pos_fantomes) and running:

            pos_fantomes = deplace_fantome(Plateau, jeu, dimensions,pos_fantomes)

        # Vérifier si un fantôme est adjacent au joueur
        x_joueur, y_joueur = joueur["joueur_x"], joueur["joueur_y"]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x_joueur + dx, y_joueur + dy
            if 0 <= nx < len(Plateau[0]) and 0 <= ny < len(Plateau):
                if Plateau[ny][nx] == "F":  # Fantôme adjacent
                    joueur, running, affichages = perdre_vie(jeu, dimensions, running, joueur,
                                                             affichages)  # Lui retirer 1 de vie
                    for fantome in pos_fantomes:
                        if fantome["x"] == nx and fantome["y"] == ny:
                            fantome["ax"],fantome["ay"] = x_joueur,y_joueur


        # Ajouter un fantômes
        if tour != 200 and tour != 0 and tour % 20 == 0 and running:  # Spawn des fantômes tous 20 tours
            pos_fantomes = gerer_fantomes(jeu, Plateau, dimensions, pos_fantomes)  # Gérer les fantômes


        # Affiche le tour actuel dans la fenêtre
        if running:
            jeu.supprimer(affichages["affichage_tour"])
            affichages["affichage_tour"] = jeu.afficherTexte(f"Tour: {tour}", dimensions["COTE_X"] * 5, dimensions["COTE_Y"] // 2, "white", 18)
        if tour == 0 and running:
            running = False  # Fin du jeu
            jeu.afficherImage(dimensions["LARGEUR_FENETRE"]/2 - dimensions["COTE_X"]*2.5, dimensions["HAUTEUR_FENETRE"]/2 - dimensions["COTE_Y"]*2.5, "images/gameover.png")
            with open('liste_scores.txt', 'a') as f:
                f.write("Score:  ")
                f.write(str(score))
                f.write(" Manche perdu")
                date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                f.write(" Date: ")
                f.write(date)
                f.write("\n")


        # Fin de la boucle, le `recupererClic()` permet de relancer la boucle et l'interface
        jeu.recupererClic()


    rejouer = jeu.afficherImage(dimensions["LARGEUR_FENETRE"]/2 - dimensions["COTE_X"]*4, dimensions["HAUTEUR_FENETRE"]/2 + dimensions["COTE_Y"]*2.5, "images/rejouer.png")
    quitter = jeu.afficherImage(dimensions["LARGEUR_FENETRE"]/2 + dimensions["COTE_X"], dimensions["HAUTEUR_FENETRE"]/2 + dimensions["COTE_Y"]*2.5, "images/quitter.png")


    fin = False
    while not fin:
        clic = jeu.attendreClic()
        # Option : rejouer
        if rejouer.x < clic.x < rejouer.x + dimensions["COTE_X"]*3 and rejouer.y < clic.y < rejouer.y + dimensions["COTE_Y"]*3:
            jeu.fermerFenetre()
            pos_fantomes.clear()  # Supprimer les fantômes
            fin = True  # Fin de la boucle de jeu
        # Option : quitter
        elif quitter.x < clic.x < quitter.x + dimensions["COTE_X"]*3 and quitter.y < clic.y < quitter.y + dimensions["COTE_Y"]*3:
            # Fermeture fenêtre
            jeu.fermerFenetre()
            exit()  # Termine le programme


# Boucle à vide qui attend un clic
while jeu.recupererClic() is None:
    continue

# Fermeture fenêtre
jeu.fermerFenetre()