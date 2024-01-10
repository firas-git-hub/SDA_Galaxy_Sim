import numpy as np
import math
import random
import scipy.constants as cstnt
from Particule import Particule
from Point import Point


class BHTreeNode:

    # Ce parametre est utilise pour allegire le calculs des forces lorsque
    # les particules sont tros proche l'un de l'autre
    s_soft = 0.1 * 0.1

    # Constante gravitationelle ui vas etre definit en dehors de cette classe
    s_gamma = 30.0
    # le facteur distance entre quadrant et particule / diametre du quadrant
    theta = 0.9

    # les particules qui ne sont pas assignees a un noeud de l'arbre
    objetsNonAssignees = []

    # statistique pour voire combien de caluls on etaient fait pour estimer la force.
    # Dans le code cpp c'est l'attribut s_stat._nNumCalc
    nbCalculsPourEstimerForce = 0

    def __init__(self, parent, min: Point, max: Point):

        self.quadrant = ''
        self.particule: Particule = None
        # le nb de particules dans ce noeud. Dans le code cpp c'est l'attribut _num
        self.nbParticules = 0
        self.parent = parent
        self.min = min
        self.max = max
        self.centre = Point(min.x + (max.x - min.x) / 2.0,
                            min.y + (max.y - min.y) / 2.0)  # Centre du neoud
        self.masse = 0
        self.enfants: list[BHTreeNode] = [None, None, None, None]
        self.centreDeMasse = Point()
        # Si le calculs approximative des forces est possible. dans cpp c'est l'attribut _bSubdivided
        self.calcForceApproxPossible = False

    def isRacine(self) -> bool:
        return self.parent == None

    def isFeuille(self) -> bool:
        # pas d'enfants => noeud est une feuille
        return (self.enfants[0] == None and
                self.enfants[1] == None and
                self.enfants[2] == None and
                self.enfants[3] == None)

    def tresProche(self) -> bool:
        return self.calcForceApproxPossible

    def nbObjetsNonAssignees() -> int | None:
        return len(BHTreeNode.objetsNonAssignees)

    def __reiniDrapeau(self):
        self.calcForceApproxPossible = False
        for i in range(4):
            if (self.enfants[i]):
                self.enfants[i].__reiniDrapeau()
        return

    def reiniStat(self):
        if (not self.isRacine()):
            return
        BHTreeNode.nbCalculsPourEstimerForce = 0
        self.__reiniDrapeau()

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
        BHTreeNode.objetsNonAssignees = []

    def obtenirQuadrant(self, x: float, y: float) -> str | None:
        if (x <= self.centre.x and y <= self.centre.y):
            return 'SW'
        elif (x <= self.centre.x and y >= self.centre.y):
            return 'NW'
        elif (x >= self.centre.x and y >= self.centre.y):
            return 'NE'
        elif (x >= self.centre.x and y <= self.centre.y):
            return 'SE'
        elif (x > self.max.x or y > self.max.y or x < self.min.x or y < self.min.y):
            raise RuntimeError(
                "Pas possible de determinee quadrant\n fonc: obtenirQuadrant")
        else:
            raise RuntimeError(
                "Pas possible de determiner quadrant\n fonc: obtenirQuadrant")

    def creeNoeudQuad(self, quadrant: str):
        match  quadrant:
            case 'SW':
                return BHTreeNode(self, self.min, self.centre)
            case 'NW':
                return BHTreeNode(self,
                                  Point(self.min.x, self.centre.y),
                                  Point(self.centre.x, self.max.y))
            case 'NE':
                return BHTreeNode(self, self.centre, self.max)
            case 'SE':
                return BHTreeNode(self,
                                  Point(self.centre.x, self.min.y),
                                  Point(self.max.x, self.centre.y))
            case _:
                raise RuntimeError(
                    "Pas possible de deeterminer quadrant\n fonc: creeNoeudQuad")

    def calcDistributionMasse(self):
        # dans le cas s'il y a un particule dans le quadrant,
        # la masse du noeud = mase du particule et centre de mass
        # du noeud = position de ce particule
        if self.nbParticules == 1:
            assert (self.particule.position)
            assert (self.particule.vitesse)
            assert (self.particule.acceleration)
            self.masse = self.particule.masse
            self.centreDeMasse = self.particule.position

        # S'il y a plusieurs particules dans le noeud alors on
        # calcule le centre de masse et la msse du noeud differement
        else:
            self.masse = 0
            self.centreDeMasse = Point(0, 0)

            # La maniere que cette methode recursive est arrangee fait d'une
            # facon que la masse vas etre additionne en debutant avec
            # les feuills jusqu'a le haut de l'arbre.
            for i in range(4):
                if (self.enfants[i]):
                    self.enfants[i].calcDistributionMasse()
                    self.masse += self.enfants[i].masse
                    self.centreDeMasse.x += self.enfants[i].centreDeMasse.x * \
                        self.enfants[i].masse
                    self.centreDeMasse.y += self.enfants[i].centreDeMasse.y * \
                        self.enfants[i].masse
            self.centreDeMasse.x /= self.masse
            self.centreDeMasse.y /= self.masse

    def calcAcc(particule1: Particule, particule2: Particule) -> Point | None:
        acc = Point(0, 0)
        if particule1 == particule2:
            return acc

        x1, y1 = particule1.position.x, particule1.position.y
        x2, y2, m2 = particule2.position.x, particule2.position.y, particule2.masse

        r = np.sqrt((x1 - x2) * (x1 - x2) +
                    (y1 - y2) * (y1 - y2) + BHTreeNode.s_soft)
        if r > 0:
            k = BHTreeNode.s_gamma * m2 / (r * r * r)
            acc.x += k * (x2 - x1)
            acc.y += k * (y2 - y1)
        else:
            acc.x = 0
            acc.y = 0
        return acc

    def calcForceArbre(self, particule1: Particule) -> Point:
        acc = Point(0, 0)
        r = 0
        k = 0
        d = 0

        if self.nbParticules == 1:
            acc = BHTreeNode.calcAcc(particule1, self.particule)
            BHTreeNode.nbCalculsPourEstimerForce += 1

        else:
            r = np.sqrt((particule1.position.x - self.centreDeMasse.x) * (particule1.position.x - self.centreDeMasse.x) +
                        (particule1.position.y - self.centreDeMasse.y) * (particule1.position.y - self.centreDeMasse.y))
            d = self.max.x - self.min.x
            if ((d / r) <= BHTreeNode.theta):
                self.calcForceApproxPossible = False
                k = BHTreeNode.s_gamma * self.masse / (r * r * r)
                acc.x = k * (self.centreDeMasse.x - particule1.position.x)
                acc.y = k * (self.centreDeMasse.y - particule1.position.y)
                BHTreeNode.nbCalculsPourEstimerForce += 1
            else:
                self.calcForceApproxPossible = True
                buf: Point = Point(0, 0)
                for q in range(4):
                    if self.enfants[q]:
                        buf = self.enfants[q].calcForceArbre(particule1)
                        acc.x += buf.x
                        acc.y += buf.y
        return acc

    def calcForce(self, particule: Particule) -> Point:
        acc: Point = self.calcForceArbre(particule)
        if len(BHTreeNode.objetsNonAssignees):
            for i in range(len(BHTreeNode.objetsNonAssignees)):
                buf = BHTreeNode.calcAcc(
                    particule, BHTreeNode.objetsNonAssignees[i])
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
        print(espace + "Centre de masse x = " +
              str(self.centreDeMasse.x) + ";")
        print(espace + "Centre de masse y = " +
              str(self.centreDeMasse.y) + ")\n")

        for i in range(4):
            if self.enfants[i]:
                self.enfants[i].imprimerNoeud(i, niveau+1)

    # Cette fonction existe pour faire le lien entre l'enfant et le quadrant.
    # Dans le code c++, cette fonctionalite est traduite par les nombre qu'un enum
    # assigne a chaque element. Par ex, dans l'enum de cPP NE prendra la valeur0
    # NW prendra la valeur 1, etc. comme il sont l'element 1 et 2 du enum respectivement
    def traduireQuadrantAIndexEnfant(quadrant):
        match  quadrant:
            case 'NE':
                return 0
            case 'NW':
                return 1
            case 'SW':
                return 2
            case 'SE':
                return 3
            case _:
                return None

    def insert(self, nouveauParticule: Particule, level):
        p1: Particule = nouveauParticule

        if ((p1.position.x < self.min.x or p1.position.x > self.max.x) or (p1.position.y < self.min.y or p1.position.y > self.max.y)):
            error_message = (
                f"Particle position ({p1.position.x}, {p1.position.y}) "
                f"is outside tree node (min.x={self.min.x}, max.x={self.max.x}, "
                f"min.y={self.min.y}, max.y={self.max.y})"
            )
            raise RuntimeError(error_message)

        # s'il y a plusieurs particules dans un noeud, donc il faut
        # que ce noeud ait des enfants afin que le nb de partocules est egal a 1.
        # s'il a plusieurs enfants, on vas le decoupe.
        if self.nbParticules > 1:
            eQuad = self.obtenirQuadrant(p1.position.x, p1.position.y)
            eQuadIndex = BHTreeNode.traduireQuadrantAIndexEnfant(eQuad)
            if not self.enfants[eQuadIndex]:
                self.enfants[eQuadIndex] = self.creeNoeudQuad(eQuad)
            self.enfants[eQuadIndex].insert(nouveauParticule, level + 1)

        # si le nb de particules est 1, c'est sur que le neoud est une feuille,
        # je cree des enfants pour ce noeud et je donne le particule premier
        # a un des enfants.
        elif self.nbParticules == 1:
            assert (self.isFeuille() or self.isRacine())
            p2 = self.particule

            if (p1.position.x == p2.position.x) and (p1.position.y == p2.position.y):
                BHTreeNode.objetsNonAssignees.append(nouveauParticule)
            else:
                eQuad = self.obtenirQuadrant(p2.position.x, p2.position.y)
                eQuadIndex = BHTreeNode.traduireQuadrantAIndexEnfant(eQuad)
                if not self.enfants[eQuadIndex]:
                    self.enfants[eQuadIndex] = self.creeNoeudQuad(eQuad)
                self.enfants[eQuadIndex].insert(self.particule, level + 1)
                self.particule = None

                eQuad = self.obtenirQuadrant(p1.position.x, p1.position.y)
                eQuadIndex = BHTreeNode.traduireQuadrantAIndexEnfant(eQuad)
                if not self.enfants[eQuadIndex]:
                    self.enfants[eQuadIndex] = self.creeNoeudQuad(eQuad)
                self.enfants[eQuadIndex].insert(nouveauParticule, level + 1)
        elif self.nbParticules == 0:
            self.particule = nouveauParticule

        self.nbParticules += 1

# THIS IS FOR TESTING


# testParent = BHTreeNode(None,None,None,Point(0,0), Point(10,10))
# testChild1 = BHTreeNode(None,None,testParent,Point(0,0), Point(5,5))
# testChild2 = BHTreeNode(None,None,testParent,Point(0,0), Point(4,7))
# testParent.nbCalculsPourEstimerForce = 10
# testChild1.nbCalculsPourEstimerForce = 15
# testChild2.nbCalculsPourEstimerForce = 17
# testChild1.calcForceApproxPossible = True
# testChild2.calcForceApproxPossible = True
# testParent.enfants[0] = testChild1
# testParent.enfants[3] = testChild2
# print(testParent.enfants[0].calcForceApproxPossible)
# print(testParent.enfants[3].calcForceApproxPossible)
# testParent.reiniStat()
# print(testChild1.calcForceApproxPossible)
# print(testChild2.calcForceApproxPossible)

rootNode = BHTreeNode(None, Point(0, 0), Point(20, 20))
# p1 = etoile(3.0, 9.0, 9.0, 2.0, 3.0632, -4.2885, 20.0)
# p2 = etoile(8.0, 2.0, 2.0, 7.0, -10.0632, 15.2885, 13.0)
# etoile_tab = [p1, p2]
p1 = Particule(Point(3.0, 9.0), Point(9.0, 2.0), Point(3.0632, -4.2885), 20.0)
p2 = Particule(Point(8.0, 2.0), Point(2.0, 7.0),
               Point(-10.0632, 15.2885), 13.0)
# p3 = Particule(Point(11,9), Point(5,1), Point(3,7), 250)
# p4 = Particule(Point(12,11), Point(4,2), Point(2,1), 250)
# p5 = Particule(Point(6,8), Point(1,1), Point(1,1), 250)
# p6 = Particule(Point(21,8), Point(1,1), Point(1,1), 250)
rootNode.insert(p1, 0)
rootNode.insert(p2, 0)
# rootNode.insert(p3,0)
# rootNode.insert(p4,0)
# rootNode.insert(p5,0)
# rootNode.insert(p5,0)

print(rootNode.enfants[2].enfants[3].calcForce(
    rootNode.enfants[2].enfants[1].particule))
# print(rootNode.enfants[0].centreDeMasse)
# print(rootNode.enfants[0].nbParticules)
# print(rootNode.enfants[0].calcDistributionMasse())
# print(rootNode.enfants[0].centreDeMasse)

# print(rootNode.isRacine())


s_gamma = 30.0
class et:
    def __init__(self, px, py, vx, vy, em):
        self.p = [px, py]
        self.v = [vx, vy]
        self.m = em

class etoile:
    def __init__(self, px, py, vx, vy, ax, ay, em):
        self.p = [px, py]
        self.v = [vx, vy]
        self.a = [ax, ay]
        self.m = em

etoile_tab = []

def norm_vector1(etoile1, etoile2):
    x = etoile2.p[0] - etoile1.p[0]
    y = etoile2.p[1] - etoile1.p[1]
    norme = math.sqrt((x**2)+(y**2))
    return norme

def formule_acceleration1(tab, i):
    etoile_first = tab[i]
    total_x = 0
    total_y = 0
    for e in tab:
        if e == etoile_first:
            continue
        else:
            total_x = total_x + (((e.m * etoile_first.m) / (norm_vector1(etoile_first, e)) ** 3)
                                 * (e.p[0] - etoile_first.p[0]))

            total_y = total_y + (((e.m * etoile_first.m) / (norm_vector1(etoile_first, e)) ** 3)
                                 * (e.p[1] - etoile_first.p[1]))

    end_x = s_gamma * total_x
    end_y = s_gamma * total_y
    end_x1 = end_x / etoile_first.m
    end_y1 = end_y / etoile_first.m

    tableau = [end_x1, end_y1]
    return tableau

def etoile_generator():
    et_tab = []
    for i in range(2):
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
        etoile_objet = etoile(et_tab[i].p[0], et_tab[i].p[1], et_tab[i].v[0], et_tab[i].v[1], ax, ay, et_tab[i].m)
        etoile_tab.append(etoile_objet)
        i += 1

# Appel de la fonction pour générer les étoiles
etoile_generator()

# Affichage des étoiles générées
for etoile_objet in etoile_tab:
    print(f"Position: ({etoile_objet.p[0]}, {etoile_objet.p[1]}), "
          f"Vitesse: ({etoile_objet.v[0]}, {etoile_objet.v[1]}), "
          f"Accélération: ({etoile_objet.a[0]}, {etoile_objet.a[1]}), "
          f"Masse: {etoile_objet.m}")

