from BHTreeHelper import BHTreeHelper
from BHTreeNode import BHTreeNode
from Particule import *
from Point import Point

rootNode:BHTreeNode = BHTreeNode(None, Point(0, 0), Point(200, 200))
parti = [
    Particule(Point(3.0, 9.0), Point(9.0, 2.0), Point(3.0632, -4.2885), 20.0),
    Particule(Point(8.0, 2.0), Point(2.0, 7.0), Point(-10.0632, 15.2885), 13.0),
    Particule(Point(11,9), Point(5,1), Point(3,7), 250),
    Particule(Point(12,11), Point(4,2), Point(2,1), 250),
    Particule(Point(6,8), Point(1,1), Point(1,1), 250),
    Particule(Point(21,8), Point(1,1), Point(1,1), 250)
]

# rootNode = BHTreeHelper.construireArbre(rootNode, parti)
parti, rootNode = BHTreeHelper.eval(rootNode, parti)