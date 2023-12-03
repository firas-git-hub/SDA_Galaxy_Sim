import numpy as np
import math
import scipy.constants as cstnt

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