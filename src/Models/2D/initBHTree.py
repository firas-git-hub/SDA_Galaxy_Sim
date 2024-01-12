from typing import List
from BHTreeNode import BHTreeNode
from Point import Point
from Particule import Particule, Etat, EtatDeriv

class initBHTree:
    def __init__(self) -> None:
        self.etatInitial: List[Etat] = []
        self.masses: List[float] = []
        self.root: BHTreeNode = BHTreeNode(None, Point(), Point())
        self.min: Point = Point()
        self.max: Point = Point()
        self.centre: Point = Point()
        self.regionOfInterest = 1
        self.timeStep = 1
        self.nbParticules = 0
        
        self.init()
        
    def obtenirCentreDeMasse(self)-> Point:
        return self.root.centreDeMasse 
    
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

    def construitArbre(self, particules: List[Particule]):
        self.root.reiniArbre(
            Point(self.centre.x - self.regionOfInterest, self.centre.y - self.regionOfInterest),
            Point(self.centre.x + self.regionOfInterest, self.centre.y + self.regionOfInterest)
            )
        count = 0

        for i in range(self.nbParticules):
            try:
                self.root.insert(particules[i], 0)
                count += 1
            except:
                pass