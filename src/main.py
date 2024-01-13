import random
import math
import tkinter as tk
import pickle

from Point import Point
from Particule import Parti
from Particule import Particule
from BHTreeNode import BHTreeNode

def printEnfants(node: BHTreeNode):
    # cnt = 0
    # for el in enfants:
    #     if hasattr(el, "enfants"):
    #         cnt = cnt + printEnfants(el.enfants)
    #     if el and el.nbParticules == 1:
    #         cnt += 1
    # return cnt
    if hasattr(node, "enfants"):
        for el in node.enfants:
            if hasattr(el, "nbParticules"):
                print(el.nbParticules, end=' ')
        print()
        for el in node.enfants:
            printEnfants(el)

def generate_Parti():
    position = Point(round(random.uniform(10, 700), 2),
                     round(random.uniform(10, 700), 2))
    vitesse = Point(round(random.uniform(-5, 5), 2),
                    round(random.uniform(-5, 5), 2))
    masse = round(random.uniform(400000, 1200000), 4)
    parti = Parti(position, vitesse, masse)
    return parti

def generate_Particule(tab_par, tab_particule, G):
    i = 0
    while i < len(tab_par):
        acceleration_point = formule_acceleration(tab_par, i, G)
        """
        ax = acceleration_point.x
        ay = acceleration_point.y
        p_a = Point(ax, ay)
        """
        p = Particule(tab_par[i].position,
                      tab_par[i].vitesse, acceleration_point, tab_par[i].masse)
        tab_particule.append(p)
        i += 1
    return tab_particule

def norm_vector(p1, p2):
    x = p2.position.x - p1.position.x
    y = p2.position.y - p1.position.y
    norme = math.sqrt((x**2) + (y**2))
    return norme

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
                 * (e.position.x - etoile_first.position.x))

            total_y = total_y + \
                (((e.masse * etoile_first.masse) / (norm_vector(etoile_first, e)) ** 3)
                 * (e.position.y - etoile_first.position.y))

    end_x = G * total_x
    end_y = G * total_y
    end_x1 = end_x / etoile_first.masse
    end_y1 = end_y / etoile_first.masse
    p_acc = Point(end_x1, end_y1)
    return p_acc
    

def update_particles(canvas, particule_list):
    for particule in particule_list:
        particule.position.x += particule.vitesse.x
        particule.position.y += particule.vitesse.y

def draw_particles(canvas, particule_list):
    canvas.delete("all")
    for particule in particule_list:
        x, y = particule.position.x, particule.position.y
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue")

def animate(canvas, particule_list):
    update_particles(canvas, particule_list)
    draw_particles(canvas, particule_list)
    canvas.after(50, animate, canvas, particule_list)


# On met à jour les vitesses d'une étoile
def vitesse_update(tab_etoile, position_etoile_tab, acceleration, delta_temps):
    e = tab_etoile[position_etoile_tab]
    acceleration_x = acceleration.x
    acceleration_y = acceleration.y
    #acceleration_x = tab_acceleration[0]
    #acceleration_y = tab_acceleration[1]
    #vitesse_new = []
    vitesse_x = e.vitesse.x + acceleration_x * delta_temps
    vitesse_y = e.vitesse.y + acceleration_y * delta_temps
    vitesse_new = Point(vitesse_x,vitesse_y)
    return vitesse_new



# On met à jour les positions d'une étoile
def position_update(tab_etoile, position_etoile_tab, vitesse, delta_temps):
    e = tab_etoile[position_etoile_tab]
    vitesse_x = vitesse.x
    vitesse_y = vitesse.y
    #position = []
    position_x = e.position.x + vitesse_x * delta_temps
    position_y = e.position.y + vitesse_y * delta_temps
    position_new = Point(position_x, position_y)
    return position_new

def update_etoile(tab_etoile, position_etoile_tab, position_point, acceleration_point, vitesse_point):
    e = tab_etoile[position_etoile_tab]
    e.position.x = position_point.x
    e.position.y = position_point.y
    e.vitesse.x = vitesse_point.x
    e.vitesse.y = vitesse_point.y
    e.acceleration.x = acceleration_point.x
    e.acceleration.y = acceleration_point.y
    tab_etoile[position_etoile_tab] = e


def main():
    G = 6.67430 * (10**(-11))
    nombre_de_particule = 100
    particule_list = []
    delta_temps = 0.5

    parti_list = [generate_Parti() for _ in range(nombre_de_particule)]
    particule_list = generate_Particule(parti_list, particule_list, G)

    def tracer_rectangles(coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        canvas.create_rectangle(x1, y1, x2, y2, outline="red")

    def draw_etoiles(canvas):
        canvas.delete("all")
        for etoile_objet in particule_list:
            x = etoile_objet.position.x
            y = etoile_objet.position.y
            # Dessiner un point jaune pour représenter l'étoile
            canvas.create_oval(x+10, y+10, x+5, y+5, fill='yellow')
            #print("x = ", x, "y =", y)


    rootNode = BHTreeNode(None, Point(0, 0), Point(2000, 2000))

    #draw_etoiles(canvas)
    for i in range(len(particule_list)):
        try:
            rootNode.insert(particule_list[i], 0)
        except:
            pass

    
    min_values, max_values = rootNode.get_min_max_values_of_children()


    coordonnees_rectangles = [
    [(min_values[i].x, min_values[i].y), (max_values[i].x, max_values[i].y)] 
    for i in range(len(min_values))
    ]

    # print(coordonnees_rectangles)

    # Trouver les coordonnées minimales et maximales pour déterminer la taille du canevas
    min_x = min(coord[0][0] for coord in coordonnees_rectangles)
    min_y = min(coord[0][1] for coord in coordonnees_rectangles)
    max_x = max(coord[1][0] for coord in coordonnees_rectangles)
    max_y = max(coord[1][1] for coord in coordonnees_rectangles)

    # Création de la fenêtre Tkinter
    fenetre = tk.Tk()
    fenetre.title("Tracer des rectangles rouges")

    # Ajouter une marge pour s'assurer que tout le rectangle est visible
    marge = 10
    canvas = tk.Canvas(fenetre, width=max_x - min_x + 2*marge, height=max_y - min_y + 2*marge)
    canvas.pack()

    #draw_etoiles(canvas)
    

    # Tracer les rectangles à partir des coordonnées ajustées
    for coords in coordonnees_rectangles:
        adjusted_coords = (
            (coords[0][0] - min_x) + marge,
            (coords[0][1] - min_y) + marge,
            (coords[1][0] - min_x) + marge,
            (coords[1][1] - min_y) + marge
        )
        tracer_rectangles(adjusted_coords[:2], adjusted_coords[2:])
    
    def update_and_draw(canvas, particule_list, rootNode, min_x, min_y, marge):
        i = 0
        
        

        while i < len(particule_list):
            acc = formule_acceleration(particule_list, i, G)
            pos = position_update(particule_list, i, particule_list[i].vitesse, delta_temps)
            vit = vitesse_update(particule_list, i, acc, delta_temps)
            update_etoile(particule_list, i, pos, acc, vit)
            i += 1

        
        
        rootNode.reiniArbre(Point(0, 0), Point(2000, 2000))

        for i in range(len(particule_list)):
            try:
                rootNode.insert(particule_list[i], 0)
            except:
                pass

        min_values, max_values = rootNode.get_min_max_values_of_children()


        draw_etoiles(canvas)
        coordonnees_rectangles = [
            [(min_values[i].x, min_values[i].y), (max_values[i].x, max_values[i].y)]
            for i in range(len(min_values))
        ]

        # Tracer les rectangles à partir des coordonnées ajustées
        for coords in coordonnees_rectangles:
            adjusted_coords = (
                (coords[0][0] - min_x) + marge,
                (coords[0][1] - min_y) + marge,
                (coords[1][0] - min_x) + marge,
                (coords[1][1] - min_y) + marge
            )
            tracer_rectangles(adjusted_coords[:2], adjusted_coords[2:])

        # Planifier l'appel à update_and_draw après 50 millisecondes
        canvas.after(50, update_and_draw, canvas, particule_list, rootNode, min_x, min_y, marge)



    

    # Planifier la première mise à jour après 50 millisecondes
    fenetre.after(1000, update_and_draw, canvas, particule_list, rootNode, min_x, min_y, marge)

    # Lancer la boucle principale Tkinter
    fenetre.mainloop()

    """
    def update_and_draw(canvas, particule_list, rootNode):
        i = 0
        while i < len(particule_list):
            acc = formule_acceleration(particule_list, i, G)
            pos = position_update(particule_list, i, particule_list[i].vitesse, delta_temps)
            vit = vitesse_update(particule_list, i, acc, delta_temps)
            update_etoile(particule_list, i, pos, acc, vit)
            i += 1

        draw_etoiles(canvas)

        rootNode.reiniArbre(Point(0, 0), Point(750, 750))

        for i in range(len(particule_list)):
            rootNode.insert(particule_list[i], 0)

        min_values, max_values = rootNode.get_min_max_values_of_children()

        coordonnees_rectangles = [
            [(min_values[i].x, min_values[i].y), (max_values[i].x, max_values[i].y)]
            for i in range(len(min_values))
        ]

        # Tracer les rectangles à partir des coordonnées ajustées
        for coords in coordonnees_rectangles:
            adjusted_coords = (
                (coords[0][0] - min_x) + marge,
                (coords[0][1] - min_y) + marge,
                (coords[1][0] - min_x) + marge,
                (coords[1][1] - min_y) + marge
            )
            tracer_rectangles(adjusted_coords[:2], adjusted_coords[2:])

        # Planifier l'appel à update_and_draw après 50 millisecondes
        fenetre.after(50, update_and_draw, canvas, particule_list, rootNode)
    """


if __name__ == "__main__":
    main()