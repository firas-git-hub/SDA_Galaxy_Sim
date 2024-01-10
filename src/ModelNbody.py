import math
import random
from Constants import Constants  # Importez votre fichier Constants.py
from IModel import IModel  # Importez votre fichier IModel.py
from Point import Point  # Importez votre fichier Vector.py
from BHTree import BHTreeNode  # Importez votre fichier BHTree.py
# Importez votre fichier Types.py
from Types import ParticleData, PODState, PODAuxState


class ModelNBody(IModel):
    def __init__(self):
        super().__init__("N-Body simulation (2D)")
        self._pInitial = None
        self._pAux = None
        self._root = BHTreeNode(Point(), Point())
        self._min = Point()
        self._max = Point()
        self._center = Point()
        self._camDir = Point()
        self._camPos = Point()
        self._roi = 1
        self._timeStep = 1
        self._num = 0
        self._bVerbose = False

        BHTreeNode.s_gamma = Constants.Gamma / \
            (Constants.ParsecInMeter ** 3) * Constants.MassOfSun * \
            (365.25 * 86400) * (365.25 * 86400)

        # self.Init()
        self.InitCollision()
        # self.Init3Body()

    def __del__(self):
        del self._pInitial
        del self._pAux

    def SetROI(self, roi):
        self._roi = roi

    def GetSuggestedTimeStep(self):
        return self._timeStep

    def GetROI(self):
        return self._roi

    def GetCenterOfMass(self):
        cm2d = self._root.GetCenterOfMass()
        return Vec3D(cm2d.x, cm2d.y, 0)

    def GetCamDir(self):
        return self._camDir

    def GetCamPos(self):
        return self._camPos

    def GetInitialState(self):
        return self._pInitial

    def GetOrbitalVelocity(self, p1, p2):
        x1, y1, m1 = p1._pState.x, p1._pState.y, p1._pAuxState.mass
        x2, y2 = p2._pState.x, p2._pState.y

        r = [x1 - x2, y1 - y2]
        dist = math.sqrt(r[0] ** 2 + r[1] ** 2)

        v = math.sqrt(self.gamma_1 * m1 / dist)

        p2._pState.vx = (r[1] / dist) * v
        p2._pState.vy = (-r[0] / dist) * v

    def ResetDim(self, num, stepsize):
        self._num = num
        self.SetDim(self._num * 4)

        del self._pInitial
        self._pInitial = [PODState() for _ in range(num)]

        del self._pAux
        self._pAux = [PODAuxState() for _ in range(num)]

        self._timeStep = stepsize

        self._max.x = self._max.y = float('-inf')
        self._min.x = self._min.y = float('inf')
        self._center = Vec2D(0, 0)


def Init(self):
    # Reset model size
    self.ResetDim(5000, 100000)

    mass = 0  # for storing the total mass

    # initialize particles
    ct = 0
    blackHole, macho = ParticleData(), [ParticleData() for _ in range(10)]

    for k in range(40):
        for l in range(100):
            if ct >= self._num:
                break

            st = self._pInitial[ct]
            st_aux = self._pAux[ct]

            if ct == 0:
                blackHole._pState = st
                blackHole._pAuxState = st_aux

                # particle zero is special; it's the trace particle that is not part
                # of the simulation and can be positioned with the mouse
                st.x = st.y = 0
                st.vx = st.vy = 0
                st_aux.mass = 1000000  # 431000;   # 4.31 Millionen Sonnenmassen
            elif ct == 1 or ct == 2:
                idx = ct - 1
                macho[idx]._pState = st
                macho[idx]._pAuxState = st_aux

                # particle zero is special; it's the trace particle that is not part
                # of the simulation and can be positioned with the mouse
                st_aux.mass = blackHole._pAuxState.mass / 10.0
                st.x = 5000 if idx == 0 else -5000
                st.y = 5000 if idx == 0 else -5000

                self.GetOrbitalVelocity(blackHole, ParticleData(st, st_aux))
            else:
                st_aux.mass = 0.76 + 100 * random.random()
                rad = 1200 + k * 100
                st.x = rad * math.sin(2 * math.pi * l / 100.0)
                st.y = rad * math.cos(2 * math.pi * l / 100.0)
                self.GetOrbitalVelocity(blackHole, ParticleData(st, st_aux))

            # determine the size of the area including all particles
            self._max.x = max(self._max.x, st.x)
            self._max.y = max(self._max.y, st.y)
            self._min.x = min(self._min.x, st.x)
            self._min.y = min(self._min.y, st.y)

            self._center.x += st.x * st_aux.mass
            self._center.y += st.y * st_aux.mass
            mass += st_aux.mass
            ct += 1

    self._center.x /= mass
    self._center.y /= mass

    self._roi = 1.5 * max(self._max.x - self._min.x, self._max.y - self._min.y)

    # compute the center of the region including all particles
    self._min.x = self._center.x - self._roi
    self._max.x = self._center.x + self._roi
    self._min.y = self._center.y - self._roi
    self._max.y = self._center.y + self._roi

    print("Initial particle distribution area")
    print("----------------------------------")
    print("Particle spread:")
    print(f"  xmin   = {self._min.x}, ymin={self._min.y}")
    print(f"  xmax   = {self._max.x}, ymax={self._max.y}")
    print("Bounding box:")
    print(f"  center = {self._center.x}, cy  ={self._center.y}")
    print(f"  roi    = {self._roi}")
