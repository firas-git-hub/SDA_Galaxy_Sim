import numpy as np
import math
import scipy.constants as cstnt
import Particule

class BHTreeNode:

    enfants = [None, None, None, None]
    masse = 0

    def __init__(self, quadrant, particules, parent, min, max, center):
        self.quadrant = quadrant,
        self.particules = particules,
        self.parent = parent,
        self.min = min,
        self.max = max,
        center = min.x + (max.x - min.x) / 2.0, min.y + (max.y - min.y) / 2.0