from typing import List
from BHTreeNode import BHTreeNode
from Point import Point
from Particule import Particule, Etat, EtatDeriv

class BHTreeHelper:

    @staticmethod
    def construireArbre(rootNode: BHTreeNode, particules: List[Particule])-> BHTreeNode:
        # rootNode.reiniArbre(
        #     Point(rootNode.centre.x, rootNode.centre.y),
        #     Point(rootNode.centre.x, rootNode.centre.y)
        #     )
        count = 0
        for i in range(len(particules)):
            try:
                rootNode.insert(particules[i], 0)
                count += 1
            except:
                pass
        rootNode.calcDistributionMasse()
        rootNode.centre = rootNode.centreDeMasse
        return rootNode
        
    # Passe de t(i) a t(i+1) et fait une MAJ des accelerations et des vitesses des particules
    @staticmethod
    def eval(rootNode: BHTreeNode, particules: List[Particule]):
        rootNode = BHTreeHelper.construireArbre(rootNode, particules)
        for i in range(1, len(particules)):
            acc = rootNode.calcForce(particules[i])
            particules[i].etatDeriv.acceleration.x = acc.x
            particules[i].etatDeriv.acceleration.y = acc.y
            particules[i].etatDeriv.vitesse.y = particules[i].etat.vitesse.y
            particules[i].etatDeriv.vitesse.y = particules[i].etat.vitesse.y
        
        # Le particule 0 est calculer en dernier a cause des statistiques
        # qui sont en relation aveec le particule 0 et pas les autres.
        rootNode.reiniStat()
        acc = rootNode.calcForce(particules[0])
        particules[0].etatDeriv.acceleration.x = acc.x
        particules[0].etatDeriv.acceleration.y = acc.y
        particules[0].etatDeriv.vitesse.y = particules[0].etat.vitesse.y
        particules[0].etatDeriv.vitesse.y = particules[0].etat.vitesse.y
        return particules, rootNode