from typing import List
from BHTreeNode import BHTreeNode
from Point import Point
from Particule import Particule, Etat, EtatDeriv

class initBHTree:
    def __init__(self) -> None:
        self.etatInitial: List[Etat] = []
        self.mass: List[int] = []
        self.root: BHTreeNode = BHTreeNode(None, Point(), Point())
        self.min: Point = Point()
        self.max: Point = Point()
        self.centre: Point = Point()
        self.regionOfInterest = 1
        self.timeStep = 1
        self.nbParticules = 0
        
        self.initArbre()
        

    def resetDim():
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