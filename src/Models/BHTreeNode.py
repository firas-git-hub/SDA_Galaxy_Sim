import numpy as np
import math
import scipy.constants as cstnt
from Particule import Particule
from Point import Point

class BHTreeNode:
    
    # Ce parametre est utilise pour allegire le calculs des forces lorsque
    # les particules sont tros proche l'un de l'autre
    s_soft = 0.1 * 0.1 
    
    # Constante gravitationelle ui vas etre definit en dehors de cette classe
    s_gamma = 0
    
    # le facteur distance entre quadrant et particule / diametre du quadrant
    theta = None
    
    def __init__(self, parent, min: Point, max: Point):
        
        self.quadrant = ''
        self.particule: Particule = None
        self.nbParticules = 0 # le nb de particules dans ce noeud. Dans le code cpp c'est l'attribut _num
        self.parent = parent
        self.min = min
        self.max = max
        self.centre = Point(min.x + (max.x - min.x) / 2.0, min.y + (max.y - min.y) / 2.0)
        self.masse = 0
        self.enfants: list[BHTreeNode] = [None, None, None, None]
        self.centreDeMasse = Point()
        self.nbCalculsPourEstimerForce = 0 # statistique pour voire combien de caluls on etaient fait pour estimer la force
        self.calcApproximeePossible = False # Si le calculs approximative des forces est possible
        self.objetsNonAssignees = [] # les particules qui ne sont pas assignees a un noeud de l'arbre

    def isRacine(self):
        return self.parent == None
    
    def isFeuille(self):
        # pas d'enfants => noeud est une feuille
        return (self.enfants[0] == None and
               self.enfants[1] == None and
               self.enfants[2] == None and
               self.enfants[3] == None)

    # def tresProche() <---- do i need this ?

    def nbObjetsNonAssignees(self):
        return len(self.objetsNonAssignees)

    def reiniStat(self):
        if (not self.isRacine()):
            return
        self.nbCalculsPourEstimerForce = 0
        self.__reiniDrapeau()

    def __reiniDrapeau(self):
        self.calcApproximeePossible = False
        for i in range(4):
            if(self.enfants[i]):
                self.enfants[i].__reiniDrapeau()
        return
    
    def reiniArbre(self, min: Point, max: Point):
        if (not self.isRacine()):
            return
        for i in range(4):
            self.enfants[i] = None
        self.min = min
        self.max = max
        self.centre = Point(
            min.x + (max.x - min.x) / 2.0,
            min.y + (max.y - min.y) / 2.0
        )
        self.masse = 0
        self.centreDeMasse = Point()
        self.nbParticules = 0
        self.objetsNonAssignees = []

    def rammeneQuadrant(self, x: float, y: float):
        if(x <= self.center.x and y <= self.center.y):
            return 'SW'
        elif (x<= self.center.x and y >= self.center.y):
            return 'NW'
        elif (x >= self.center.x and y >= self.center.y):
            return 'NE'
        elif (x > self.max.x or y > self.max.y or x < self.min.x or y < self.min.y):
            return 'SE'
        else:
            return None
        
    def creeNoeudQuad(self, quadrant: str):
        match  quadrant:
            case 'SW':
                return BHTreeNode(self, self.min, self.centre)
            case 'NW':
                return BHTreeNode(self,
                                  Point(self.min.x, self.center.y),
                                  Point(self.center.x, self.max.y))
            case 'NE':
                return BHTreeNode(self, self.centre, self.max)
            case 'SE':
                return BHTreeNode(self,
                                  Point(self.center.x, self.min.y),
                                  Point(self.max.x, self.center.y))
            case _:
                return None


    def calcDistributionMasse(self):
        # dans le cas s'il y a un particule dans le quadrant,
        # la masse du noeud = mase du particule et centre de mass 
        # du noeud = position de ce particule
        if self.nbParticules == 1 :
            self.masse = self.particule.masse
            self.centreDeMasse = self.particule.position
            
        # S'il y a plusieurs particules dans le noeud alors on
        # calcule le centre de masse et la msse du noeud differement
        else :
            self.masse = 0
            self.centreDeMasse = Point(0, 0)
            
            for i in range(4):
                if(self.enfants[i]):
                    self.enfants[i].calcDistributionMasse()
                    self.masse += self.enfants[i].masse
                    self.centreDeMasse.x += self.enfants[i].centreDeMasse.x * self.enfants[i].masse
                    self.centreDeMasse.y += self.enfants[i].centreDeMasse.y * self.enfants[i].masse
        self.centreDeMasse.x /= self.masse
        self.centreDeMasse.y /= self.masse

    def calcAcc(particule1: Particule, particule2: Particule) -> Point|None :
        acc = Point(0, 0)
        if particule1 == particule2 :
            return None
        x1, y1 = particule1.position.x, particule1.position.y
        x2, y2, m2 = particule2.position.x, particule2.position.y, particule2.masse
        
        r = np.sqrt((x1 - x2) * (x1 - x2) + 
                    (y1 - y2) * (y1 - y2) + BHTreeNode.s_soft)
        
        if r > 0 :
            k = BHTreeNode.s_gamma * m2 / (r * r * r)
            acc.x += k * (x2 - x1)
            acc.y += k * (y2 - y1)
        else :
            acc.x = 0
            acc.y = 0
        return acc
    
    def calcForceArbre(self, particule1: Particule)-> Point :
        acc = Point(0, 0)
        r = 0
        k = 0
        d = 0
        
        if self.nbParticules == 1:
            acc = BHTreeNode.calcAcc(particule1, self.particule)
            self.nbCalculsPourEstimerForce += 1
        
        else:
            r = np.sqrt((particule1.position.x - self.centreDeMasse.x) * (particule1.position.x - self.centreDeMasse.x) +
                 (particule1.position.y - self.centreDeMasse.y) * (particule1.position.y - self.centreDeMasse.y))
            d = self.max.x - self.min.x
            if((d / r) <= self.theta):
                self.calcApproximeePossible = False
                k = self.s_gamma * self.masse / (r * r * r)
                acc.x = k * (self.centreDeMasse.x - particule1.position.x)
                acc.y = k * (self.centreDeMasse.y - particule1.position.y)
                self.nbCalculsPourEstimerForce += 1
            else:
                self.calcApproximeePossible = True
                buf: Point = Point(0, 0)
                for q in range(4):
                    if self.enfants[q]:
                        buf = self.enfants[q].calcForceArbre()
                        acc.x += buf.x
                        acc.y += buf.y
        return acc
        
    def calcForce(self, particule: Particule)-> Point :
        acc: Point = self.calcForceArbre(particule)
        if len(self.objetsNonAssignees):
            for i in range(len(self.objetsNonAssignees)):
                buf = BHTreeNode.calcAcc(particule, self.objetsNonAssignees[i])
                acc.x += buf.x
                acc.y += buf.y
        return acc
    
    def imprimerNoeud(self, quadrant: int, niveau: int):
        espace = ""
        for i in range(niveau):
            espace += " "
        print(espace + "Quadrant" + str(quadrant) + ": ")
        print(espace + "(nb de particules = " + str(self.nbParticules) + "; ")
        print(espace + "mass = " + str(self.masse) + ";")
        print(espace + "Centre de masse x = " + str(self.centreDeMasse.x) + ";")
        print(espace + "Centre de masse y = " + str(self.centreDeMasse.y) + ")\n")
        
        for i in range(4):
            if self.enfants[i]:
                self.enfants[i].imprimerNoeud(i, niveau+1)
        
# THIS IS FOR TESTING


# testParent = BHTreeNode(None,None,None,Point(0,0), Point(10,10))
# testChild1 = BHTreeNode(None,None,testParent,Point(0,0), Point(5,5))
# testChild2 = BHTreeNode(None,None,testParent,Point(0,0), Point(4,7))
# testParent.nbCalculsPourEstimerForce = 10
# testChild1.nbCalculsPourEstimerForce = 15
# testChild2.nbCalculsPourEstimerForce = 17
# testChild1.calcApproximeePossible = True
# testChild2.calcApproximeePossible = True
# testParent.enfants[0] = testChild1
# testParent.enfants[3] = testChild2
# print(testParent.enfants[0].calcApproximeePossible)
# print(testParent.enfants[3].calcApproximeePossible)
# testParent.reiniStat()
# print(testChild1.calcApproximeePossible)
# print(testChild2.calcApproximeePossible)