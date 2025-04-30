from joueur import trouve_joueur_position
from affichage import ajouter_score
from validation import est_valide
from gestion_plateau import apparition_porte

# Modele
plateau = [
    ["C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C"],
    ["C","J","D","D",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"C"],
    ["C","D","C","D","C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C"],
    ["C","D","D","D",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"C"],
    ["C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C"],
    ["C",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"C"],
    ["C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C"],
    ["C",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"C"],
    ["C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C"],
    ["C",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"D","D","D","C"],
    ["C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C",0,"C","D","C","D","C"],
    ["C",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"D","D","E","C"],
    ["C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C","C"]

]

plateau2 = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
]

x_joueur, y_joueur = trouve_joueur_position(plateau)
assert x_joueur == 1 and y_joueur == 1


joueur = {
        "joueur_x": 1,
        "joueur_y": 1,
        "img_joueur": 0,
        "score": 0,
        "vies": 3,
        "niveau": 0,
        "portee": 1
    }

ajouter_score(10, joueur)
assert joueur["score"] == 10

assert not est_valide(plateau, 6, 2)
assert est_valide(plateau, 6, 1)

px,py = apparition_porte(plateau2)
assert px == 1 and py == 1
print(plateau2)



