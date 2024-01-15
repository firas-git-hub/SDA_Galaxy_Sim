import random
import math
import tkinter as tk
from BHTreeHelper import *

from Point import Point
from Particule import Particule
from BHTreeNode import BHTreeNode

# Generation des particules sans l'acceleration initiale
def generate_Parti():
    position = Point(round(random.uniform(200, 600), 2),
                     round(random.uniform(200, 600), 2))
    vitesse = Point(round(random.uniform(-15, 15), 2),
                    round(random.uniform(-15, 15), 2))
    masse = round(random.uniform(4000, 1200000), 4)
    parti = Particule(position, vitesse, Point(), masse)
    return parti

# Generation des particules avec l'acceleration initiale
def generate_Particule(tab_par, tab_particule, G):
    i = 0
    while i < len(tab_par):
        acceleration_point = formule_acceleration(tab_par, i, G)
        p = Particule(tab_par[i].etat.position,
                      tab_par[i].etat.vitesse, acceleration_point, tab_par[i].masse)
        tab_particule.append(p)
        i += 1
    tab_particule.append(Particule(Point(450,450), Point(0, 0), Point(0, 0), 9999999999999))
    return tab_particule

def norm_vector(p1: Particule, p2: Particule):
    x = p2.etat.position.x - p1.etat.position.x
    y = p2.etat.position.y - p1.etat.position.y
    norme = math.sqrt((x**2) + (y**2))
    return norme

# Calcule de l'interaction entre les particules sans la formule de Barnes Hut
def formule_acceleration(tab, i, G):
    etoile_first = tab[i]
    total_x = 0
    total_y = 0
    for e in tab:
        if e == etoile_first:
            continue
        else:
            total_x = total_x + \
                (((e.masse * etoile_first.masse) / (norm_vector(etoile_first, e)) ** 3)
                 * (e.etat.position.x - etoile_first.etat.position.x))

            total_y = total_y + \
                (((e.masse * etoile_first.masse) / (norm_vector(etoile_first, e)) ** 3)
                 * (e.etat.position.y - etoile_first.etat.position.y))

    end_x = G * total_x
    end_y = G * total_y
    end_x1 = end_x / etoile_first.masse
    end_y1 = end_y / etoile_first.masse
    p_acc = Point(end_x1, end_y1)
    return p_acc

# On met à jour les vitesses d'une étoile
def vitesse_update(tab_etoile, position_etoile_tab, acceleration, delta_temps):
    e = tab_etoile[position_etoile_tab]
    acceleration_x = acceleration.x
    acceleration_y = acceleration.y
    vitesse_x = e.etat.vitesse.x + acceleration_x * delta_temps
    vitesse_y = e.etat.vitesse.y + acceleration_y * delta_temps
    vitesse_new = Point(vitesse_x,vitesse_y)
    return vitesse_new



# On met à jour les positions d'une étoile
def position_update(tab_etoile, position_etoile_tab, vitesse, delta_temps):
    e = tab_etoile[position_etoile_tab]
    vitesse_x = vitesse.x
    vitesse_y = vitesse.y
    position_x = e.etat.position.x + vitesse_x * delta_temps
    position_y = e.etat.position.y + vitesse_y * delta_temps
    position_new = Point(position_x, position_y)
    return position_new

# On met a jour la particule dans le tableau
def update_etoile(tab_etoile, position_etoile_tab, position_point, acceleration_point, vitesse_point):
    e = tab_etoile[position_etoile_tab]
    e.etat.position.x = position_point.x
    e.etat.position.y = position_point.y
    e.etat.vitesse.x = vitesse_point.x
    e.etat.vitesse.y = vitesse_point.y
    e.etatDeriv.acceleration.x = acceleration_point.x
    e.etatDeriv.acceleration.y = acceleration_point.y
    tab_etoile[position_etoile_tab] = e


def main():
    G = 6.67430 * (10**(-11))
    nombre_de_particule = 250
    particule_list = []
    delta_temps = 0.5

    parti_list = [generate_Parti() for _ in range(nombre_de_particule)]
    particule_list = generate_Particule(parti_list, particule_list, G)

    # Creation de la racine du quad tree
    rootNode = BHTreeNode(None, Point(0, 0), Point(800, 800))
    
    # Utilisation de la methode Construire arbre dans BHTreeHelper.py pour gerer l'insertion et le calcul du centre de masse
    rootNode = BHTreeHelper.construireArbre(rootNode, particule_list)
    
    # Pour tracer les quadrants du quad tree dans l'affichage
    min_values, max_values = rootNode.get_min_max_values_of_children()

    def tracer_rectangles(coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        canvas.create_rectangle(x1, y1, x2, y2, outline="red")

    def draw_etoiles(canvas):
        canvas.delete("all")
        for etoile_objet in particule_list:
            x = etoile_objet.etat.position.x
            y = etoile_objet.etat.position.y
            canvas.create_oval(x+10, y+10, x+5, y+5, fill='yellow')
    
    min_values, max_values = rootNode.get_min_max_values_of_children()

    coordonnees_rectangles = [
    [(min_values[i].x, min_values[i].y), (max_values[i].x, max_values[i].y)] 
    for i in range(len(min_values))
    ]


    min_x = min(coord[0][0] for coord in coordonnees_rectangles)
    min_y = min(coord[0][1] for coord in coordonnees_rectangles)
    max_x = max(coord[1][0] for coord in coordonnees_rectangles)
    max_y = max(coord[1][1] for coord in coordonnees_rectangles)

    # fenêtre Tkinter
    fenetre = tk.Tk()
    fenetre.title("Tracer des rectangles rouges")

    marge = 10
    canvas = tk.Canvas(fenetre, width=max_x - min_x + 2*marge, height=max_y - min_y + 2*marge, background="black")
    canvas.pack()

    draw_etoiles(canvas)
    
    # Tracer tout les quadrants du quad tree dans une boucle
    for coords in coordonnees_rectangles:
        adjusted_coords = (
            (coords[0][0] - min_x) + marge,
            (coords[0][1] - min_y) + marge,
            (coords[1][0] - min_x) + marge,
            (coords[1][1] - min_y) + marge
        )
        tracer_rectangles(adjusted_coords[:2], adjusted_coords[2:])
    
    # Methode de l'affichage dynamique
    def update_and_draw(canvas, particule_list, rootNode, min_x, min_y, marge):
        
        # Reconstruction de l'arbre pour chaque moment du temps (dans ce cas c'est delta_temps)
        i = 0
        rootNode = BHTreeNode(None, Point(0, 0), Point(2000, 2000))
        
        # MAJ des particules
        while i < len(particule_list):
            acc = formule_acceleration(particule_list, i, G)
            pos = position_update(particule_list, i, particule_list[i].etat.vitesse, delta_temps)
            vit = vitesse_update(particule_list, i, acc, delta_temps)
            update_etoile(particule_list, i, pos, acc, vit)
            i += 1
        
        particule_list, rootNode = BHTreeHelper.eval(rootNode, particule_list)

        min_values, max_values = rootNode.get_min_max_values_of_children()

        draw_etoiles(canvas)

        coordonnees_rectangles = [
            [(min_values[i].x, min_values[i].y), (max_values[i].x, max_values[i].y)]
            for i in range(len(min_values))
        ]

        for coords in coordonnees_rectangles:
            adjusted_coords = (
                (coords[0][0] - min_x) + marge,
                (coords[0][1] - min_y) + marge,
                (coords[1][0] - min_x) + marge,
                (coords[1][1] - min_y) + marge
            )
            tracer_rectangles(adjusted_coords[:2], adjusted_coords[2:])

        canvas.after(50, update_and_draw, canvas, particule_list, rootNode, min_x, min_y, marge)

    fenetre.after(5, update_and_draw, canvas, particule_list, rootNode, min_x, min_y, marge)

    fenetre.mainloop()


if __name__ == "__main__":
    main()
    