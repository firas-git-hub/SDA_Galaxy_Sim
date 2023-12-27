import math
import numpy as np
import scipy.constants as cstnt
import random
import tkinter as tk

G = 6.67430e-11
theta = 0.5 

class Node:
   def __init__(self, data):
      self.left = None
      self.middle = None
      self.right = None
      self.data = data
   def PrintTree(self):
      print(self.data)

class etoile:
   def __init__(self,ex,ey,rx,ry,em):
      self.p_x = ex
      self.p_y = ey
      self.r_x = rx
      self.r_y = ry
      self.m = em




etoile_tab = []
def etoile_generator():
   
   for i in range(50):
      x = round(random.uniform(10, 120), 2)
      y = round(random.uniform(10, 120), 2)
      rx = round(random.uniform(10, 120), 2)
      ry = round(random.uniform(10, 120), 2)
      m = round(random.uniform(2000000, 10000000), 4)
      etoile_objet= etoile(x,y,rx,ry,m)
      etoile_tab.append(etoile_objet)


def etoile_tab_print():
   for patate in etoile_tab:
      print("X : ",patate.p_x," Y : ",patate.p_y," vitesse X: ",patate.r_x," vitesse y: ",patate.r_y," Masse : ",patate.m)



etoile_generator()
etoile_tab_print()


def draw_etoiles(canvas):
    for etoile_objet in etoile_tab:
        x = etoile_objet.p_x
        y = etoile_objet.p_y
        canvas.create_oval(x, y, x+2, y+2, fill='yellow')  # Dessiner un point jaune pour représenter l'étoile

root = tk.Tk()
root.title("Étoiles")

canvas = tk.Canvas(root, width=150, height=150, bg='black')
canvas.pack()

draw_etoiles(canvas)

root.mainloop()


def delta_r (tab):
   delta_t = 0.1
   etoile_delta =[]
   etoile1 = etoile_tab[0]
   delta_r_x = etoile1.r_x * delta_t
   delta_r_y = etoile1.r_y * delta_t
   etoile_delta.append(delta_r_x)  
   etoile_delta.append(delta_r_y)  
   print(etoile_delta[0], " et ", etoile_delta[1])
   return etoile_delta

delta_r(etoile_tab)



"""



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