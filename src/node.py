import math
import numpy as np
import scipy.constants as cstnt
import random
import tkinter as tk

# choisir le bon G
G = 30
theta = 0.5


class Node:
    def __init__(self, data):
        self.left = None
        self.middle = None
        self.right = None
        self.data = data

    def PrintTree(self):
        print(self.data)


# la classe etoile, sans acceleration car pour calculer acceleration initiale nous avons besoin d'une classe avant de la classe etoile
class et:
    def __init__(self, px, py, vx, vy, em):
        self.p = []
        self.p.append(px)
        self.p.append(py)
        self.v = []
        self.v.append(vx)
        self.v.append(vy)
        self.m = em


class etoile:
    def __init__(self, px, py, vx, vy, ax, ay, em):
        self.p = []
        self.p.append(px)
        self.p.append(py)
        self.v = []
        self.v.append(vx)
        self.v.append(vy)
        self.a = []
        self.a.append(ax)
        self.a.append(ay)
        self.m = em


etoile_tab = []



def norm_vector1(etoile1, etoile2):
    x = etoile2.p[0] - etoile1.p[0]
    y = etoile2.p[1] - etoile1.p[1]
    norme = math.sqrt((x**2)+(y**2))
    return norme

def formule_acceleration1(tab, i):
    etoile_first = tab[i]
   # taille = len(etoile_tab)
    total_x = 0
    total_y = 0
    for e in tab:
        if e == etoile_first:
            continue
        else:
            total_x = total_x + \
                (((e.m * etoile_first.m) / (norm_vector1(etoile_first, e)) ** 3)
                 * (e.p[0] - etoile_first.p[0]))

            total_y = total_y + \
                (((e.m * etoile_first.m) / (norm_vector1(etoile_first, e)) ** 3)
                 * (e.p[1] - etoile_first.p[1]))

    end_x = G * total_x
    # print("end_x = ", end_x)
    end_y = G * total_y
    # print("end_y = ", end_y)
    end_x1 = end_x / etoile_first.m
    # print("end_x1 = ", end_x1)
    end_y1 = end_y / etoile_first.m
    # print("end_y1 = ", end_y1)

    tableau = [end_x1, end_y1]
    return tableau


def etoile_generator():
    et_tab = []
    for i in range(5):
        px = round(random.uniform(10, 120), 2)
        py = round(random.uniform(10, 120), 2)
        vx = round(random.uniform(10, 120), 2)
        vy = round(random.uniform(10, 120), 2)
        m = round(random.uniform(40000, 120000), 4)
        et_objet = et(px, py, vx, vy, m)
        et_tab.append(et_objet)
    i = 0
    while i < len(et_tab):
        acceleration_tab = formule_acceleration1(et_tab, i)
        ax = acceleration_tab[0]
        ay = acceleration_tab[1]
        etoile_objet = etoile(px, py, vx, vy, ax, ay, m)
        etoile_tab.append(etoile_objet)
        i += 1


def etoile_tab_print():
    for patate in etoile_tab:
        print("X : ", patate.p[0], " Y : ", patate.p[1], " Vitesse X: ",
              patate.v[0], " Vitesse y: ", patate.v[1], " Acceleration X: ", patate.a[0], " Acceleration Y: ", patate.a[1], " Masse : ", patate.m)


etoile_generator()
etoile_tab_print()
# rendre dynamique

def draw_etoiles(canvas):
    for etoile_objet in etoile_tab:
        x = etoile_objet.p[0]
        y = etoile_objet.p[1]
        # Dessiner un point jaune pour représenter l'étoile
        canvas.create_oval(x, y, x+2, y+2, fill='yellow')


root = tk.Tk()
root.title("Étoiles")

canvas = tk.Canvas(root, width=150, height=150, bg='black')
canvas.pack()

draw_etoiles(canvas)

root.mainloop()



# en plus, peut etre ca va nous aider


def delta_p(tab):
    delta_t = 0.1
    etoile_delta = []
    etoile1 = etoile_tab[0]
    delta_p_x = etoile1.p[0] * delta_t
    delta_p_y = etoile1.p[1] * delta_t
    etoile_delta.append(delta_p[0])
    etoile_delta.append(delta_p[1])
    print(etoile_delta[0], " et ", etoile_delta[1])
    return etoile_delta


# delta_p(etoile_tab)


def norm_vector(etoile1, etoile2):
    x = etoile2.p[0] - etoile1.p[0]
    y = etoile2.p[1] - etoile1.p[1]
    norme = math.sqrt((x**2)+(y**2))
    return norme

"""
# test
p1 = etoile(3.0, 9.0, 9.0, 2.0, 3.0632, -4.2885, 20.0)
p2 = etoile(8.0, 2.0, 2.0, 7.0, -10.0632, 15.2885, 13.0)
etoile_tab = [p1, p2]
"""

# calcule de l'acceleration d'une etoile
def formule_acceleration(tab, i):
    etoile_first = tab[i]
   # taille = len(etoile_tab)
    total_x = 0
    total_y = 0
    for e in tab:
        if e == etoile_first:
            continue
        else:
            total_x = total_x + \
                (((e.m * etoile_first.m) / (norm_vector(etoile_first, e)) ** 3)
                 * (e.p[0] - etoile_first.p[0]))

            total_y = total_y + \
                (((e.m * etoile_first.m) / (norm_vector(etoile_first, e)) ** 3)
                 * (e.p[1] - etoile_first.p[1]))

    end_x = G * total_x
    # print("end_x = ", end_x)
    end_y = G * total_y
    # print("end_y = ", end_y)
    end_x1 = end_x / etoile_first.m
    # print("end_x1 = ", end_x1)
    end_y1 = end_y / etoile_first.m
    # print("end_y1 = ", end_y1)

    tableau = [end_x1, end_y1]
    return tableau


# print(a)

# On met à jour les vitesses d'une étoile
def vitesse_update(tab_etoile, position_etoile_tab, tab_acceleration, delta_temps):
    e = tab_etoile[position_etoile_tab]
    acceleration_x = tab_acceleration[0]
    acceleration_y = tab_acceleration[1]
    vitesse_new = []
    vitesse_x = e.v[0] + acceleration_x * delta_temps
    vitesse_y = e.v[1] + acceleration_y * delta_temps
    vitesse_new.append(vitesse_x)
    vitesse_new.append(vitesse_y)
    return vitesse_new


def position_update(tab_etoile, position_etoile_tab, tab_vitesse, delta_temps):
    e = tab_etoile[position_etoile_tab]
    vitesse_x = tab_vitesse[0]
    vitesse_y = tab_vitesse[1]
    position = []
    position_x = e.p[0] + vitesse_x * delta_temps
    position_y = e.p[1] + vitesse_y * delta_temps
    position.append(position_x)
    position.append(position_y)
    return position


def update_etoile(tab_etoile, position_etoile_tab, tab_position, tab_acceleration, tab_vitesse):
    e = tab_etoile[position_etoile_tab]
    e.p[0] = tab_position[0]
    e.p[1] = tab_position[1]
    e.v[0] = tab_vitesse[0]
    e.v[1] = tab_vitesse[1]
    e.a[0] = tab_acceleration[0]
    e.a[1] = tab_acceleration[1]
    tab_etoile[position_etoile_tab] = e


"""
pa = [10,150]
pb = [801,512]
update_etoile(etoile_tab,1,pa,pb)
print(etoile_tab[1].r_y)
"""


"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!! TRES IMPORTANT ASPECT PHYSIQUE (SOROUSH) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
acceleration -> position update -> vitesse_update
acceleration : position (ancien)
position update: vitesse (ancien)
"""


new_acceleration = formule_acceleration(etoile_tab, 0)
print("New Acceleration  : ", new_acceleration)
new_position = position_update(etoile_tab, 0, etoile_tab[0].v, 2)
print("New Position      : ", new_position)
new_vitesse = vitesse_update(etoile_tab, 0, new_acceleration, 2)
print("New Vitesse       : ", new_vitesse)


"""
crated by : @ Hubble


# This is for testing remove later

def calcForceBetweenParticles2d(p1, p2):
    #Creation du vecteur resultant de la formule avec les coordonnees x, y
    resVect = np.array([0, 0])
    # J'ai pas utilise la method math.pow puisque l'operateur 
    # de multiplication * est plus rapide que la methode math.pow()
    # Le resultat est un vecteur
    distBetweenPtcls = math.sqrt((p2.x - p1.x) * (p2.x - p1.x) +
                                 (p2.y - p1.y) * (p2.y - p1.y))
    print(distBetweenPtcls)
    ptclsVectDiff = p2.vect - p1.vect
    print(ptclsVectDiff)
    res = cstnt.G * ( p1.mass*p2.mass ) * ptclsVectDiff / distBetweenPtcls
    return res


def calcForceBetweenParticles3d(p1, p2):
    res = np.array
    distBetweenPtcls = math.sqrt((p2.x - p1.x) * (p2.x - p1.x) +
                                 (p2.y - p1.y) * (p2.y - p1.y) + 
                                 (p2.z - p1.z) * (p2.z - p1.z))
    ptclsVectDiff = p2.vect - p1.vect
    res = cstnt.G * ( p1.mass*p2.mass ) * ptclsVectDiff / distBetweenPtcls
    return res

# This is for testing remove later
class Particle2D:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.vect = np.array([x, y])
        self.mass = mass

ptcl2D1 = Particle2D(2, 10, 150)
ptcl2D2 = Particle2D(4, 6, 200)

print(calcForceBetweenParticles2d(ptcl2D1, ptcl2D2))

"""
