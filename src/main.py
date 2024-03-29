import random
from Point import Point
from Particule import Parti
from Particule import Particule
import math
import numpy as np
import scipy.constants as cstnt
import tkinter as tk


def generate_Parti():
    position = Point(round(random.uniform(10, 120), 2),
                     round(random.uniform(10, 120), 2))
    vitesse = Point(round(random.uniform(10, 120), 2),
                    round(random.uniform(10, 120), 2))
    masse = round(random.uniform(40000, 120000), 4)
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


# calcule de l'acceleration d'une etoile
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
    nombre_de_particule = 5
    particule_list = []


    parti_list = [generate_Parti() for _ in range(nombre_de_particule)]
    particule_list = generate_Particule(parti_list, particule_list, G)


    # Afficher les Parti et Particule
    """for index, parti in enumerate(parti_list, start=1):
        print(f"Parti {index}:\n{parti}\n")
  
    for index, particule in enumerate(particule_list, start=1):
        print(f"Parti {index}:\n{particule}\n")"""


if __name__ == "__main__":
    main()




# generer la particule_list sans la fonction generate_Particule
"""
    i = 0
    while i < len(parti_list):
        acceleration_tab = formule_acceleration(parti_list, i, G)
        ax = acceleration_tab[0]
        ay = acceleration_tab[1]
        p_a = Point(ax, ay)
        p = Particule(parti_list[i].position,
                      parti_list[i].vitesse, p_a, parti_list[i].masse)
        particule_list.append(p)
        i += 1
"""