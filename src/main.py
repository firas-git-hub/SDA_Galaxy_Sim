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
    vitesse = Point(round(random.uniform(10, 700), 2),
                    round(random.uniform(10, 700), 2))
    masse = round(random.uniform(40000, 120000), 4)
    parti = Parti(position, vitesse, masse)
    return parti

def generate_Particule(tab_par, tab_particule, G):
    i = 0
    while i < len(tab_par):
        acceleration_tab = formule_acceleration(tab_par, i, G)
        ax = acceleration_tab[0]
        ay = acceleration_tab[1]
        p_a = Point(ax, ay)
        p = Particule(tab_par[i].position,
                      tab_par[i].vitesse, p_a, tab_par[i].masse)
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
   # taille = len(etoile_tab)
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
    # print("end_x = ", end_x)
    end_y = G * total_y
    # print("end_y = ", end_y)
    end_x1 = end_x / etoile_first.masse
    # print("end_x1 = ", end_x1)
    end_y1 = end_y / etoile_first.masse
    # print("end_y1 = ", end_y1)
    """
    tableau = [end_x1, end_y1]
    return tableau
    """ 
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
    G = 30
    nombre_de_particule = 40
    particule_list = []

    # parti_list = [generate_Parti() for _ in range(nombre_de_particule)]
    # particule_list = generate_Particule(parti_list, particule_list, G)
    # with open('data.pkl', 'wb') as f:
    #     pickle.dump(particule_list, f, pickle.HIGHEST_PROTOCOL)
    particule_list
    with open('data.pkl', 'rb') as f:
        particule_list = pickle.load(f)


    rootNode = BHTreeNode(None, Point(0, 0), Point(750, 750))

    for i in range(len(particule_list)):
        rootNode.insert(particule_list[i], 0)

    print(printEnfants(rootNode))
    
    min_values, max_values = rootNode.get_min_max_values_of_children()

    """
    coordonnees_rectangles = [
        [(min_values[0].x, min_values[0].y), (max_values[0].x, max_values[0].y)],
        # Ajoutez d'autres coordonnées au besoin
    ]
    """
    #print("Min values of children:", min_values[2])
    #print("Max values of children:", max_values[2])


    def tracer_rectangles(coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        canvas.create_rectangle(x1, y1, x2, y2, outline="red")

    def draw_etoiles(canvas):
        for etoile_objet in particule_list:
            x = etoile_objet.position.x
            y = etoile_objet.position.y
            # Dessiner un point jaune pour représenter l'étoile
            canvas.create_oval(x+10, y+10, x+5, y+5, fill='yellow')
            #print("x = ", x, "y =", y)
    """
    # Coordonnées des rectangles dans un tableau
    coordonnees_rectangles = [
        [(min_values[0].x, min_values[0].y), (max_values[0].x, max_values[0].y)],
        [(min_values[1].x, min_values[1].y), (max_values[1].x, max_values[1].y)],
        [(min_values[2].x, min_values[2].y), (max_values[2].x, max_values[2].y)],
        [(min_values[3].x, min_values[3].y), (max_values[3].x, max_values[3].y)],
        [(min_values[4].x, min_values[4].y), (max_values[4].x, max_values[4].y)],
    ]
    """
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

    draw_etoiles(canvas)

    # Tracer les rectangles à partir des coordonnées ajustées
    for coords in coordonnees_rectangles:
        adjusted_coords = (
            (coords[0][0] - min_x) + marge,
            (coords[0][1] - min_y) + marge,
            (coords[1][0] - min_x) + marge,
            (coords[1][1] - min_y) + marge
        )
        tracer_rectangles(adjusted_coords[:2], adjusted_coords[2:])

    # Lancer la boucle principale Tkinter
    fenetre.mainloop()
    
    """
    for index, parti in enumerate(parti_list, start=1):
        print(f"Parti {index}:\n{parti}\n")
  
    for index, particule in enumerate(particule_list, start=1):
        print(f"Parti {index}:\n{particule}\n")
    """



    


"""
    root = tk.Tk()
    root.title("Particle Simulation")

    canvas = tk.Canvas(root, width=1500, height=1500, bg="white")
    canvas.pack()

    animate(canvas, particule_list)

    root.mainloop()
"""
if __name__ == "__main__":
    main()