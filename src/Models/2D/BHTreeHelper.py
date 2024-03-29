import sys
sys.path.append(r"/src/Models/2D")

from typing import List
from BHTreeNode import BHTreeNode
from Point import Point
from Particule import Particule, Etat, EtatDeriv

class BHTreeHelper:
    def __init__(self) -> None:
        self.etatInitial: List[Etat] = []
        self.masses: List[float] = []
        self.racine: BHTreeNode = BHTreeNode(None, Point(), Point())
        self.min: Point = Point()
        self.max: Point = Point()
        self.centre: Point = Point()
        self.regionOfInterest = 1
        self.timeStep = 1
        self.nbParticules = 0
        
        self.init()
        
    def obtenirCentreDeMasse(self)-> Point:
        return self.racine.centreDeMasse 
    
    def resetDim(self, num: int, stepsize: float):
        self.num = num
        self.etatInitial = []
        self.masses = []
        self.timeStep = stepsize
        self.max.x = float("-inf")
        self.max.y = float("-inf")
        self.min.x = float("inf")
        self.min.y = float("inf")
        self.centre = Point(0, 0)
        
    def init3Paricules():
        pass
        

    def initArbre():
        pass

    def construireArbre(self, particules: List[Particule]):
        self.racine.reiniArbre(
            Point(self.centre.x - self.regionOfInterest, self.centre.y - self.regionOfInterest),
            Point(self.centre.x + self.regionOfInterest, self.centre.y + self.regionOfInterest)
            )
        count = 0

        for i in range(self.nbParticules):
            try:
                self.racine.insert(particules[i], 0)
                count += 1
            except:
                pass
        self.racine.calcDistributionMasse()
        self.centre = self.racine.centreDeMasse
    
    def eval(self, particules: List[Particule]):
        self.construireArbre(particules)
        for i in range(1,self.num):
            acc = self.racine.calcForce(particules[i])
            particules[i].etatDeriv.acceleration.x = acc.x
            particules[i].etatDeriv.acceleration.y = acc.y
            particules[i].etatDeriv.vitesse.y = particules[i].etat.vitesse.y
            particules[i].etatDeriv.vitesse.y = particules[i].etat.vitesse.y
        
        # Le particule 0 est calculer en dernier a cause des statistiques
        # qui sont en relation aveec le particule 0 et pas les autres.
        self.racine.reiniStat()
        acc = self.racine.calcForce(particules[0])
        particules[0].etatDeriv.acceleration.x = acc.x
        particules[0].etatDeriv.acceleration.y = acc.y
        particules[0].etatDeriv.vitesse.y = particules[0].etat.vitesse.y
        particules[0].etatDeriv.vitesse.y = particules[0].etat.vitesse.y
            
