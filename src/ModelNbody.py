from BHTreeNode import BHTreeNode
from Particle import Particle

class Point2D:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y


class Point3D:
    def __init__(self, x:float, y:float, z:float):
        self.x = x
        self.y = y
        self.z = z

class PODState:
    def __init__(self, x:float, y:float, vx:float, vy:float):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

class PODAuxState:
    def __init__(self, masse:float):
        self.masse = masse

class PODDeriv:
    def __init__(self, vx, vy, ax, ay):
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay

class Constants:
    def __init__(self):
        self.MassOfSun = 1.988435e30
        self.ParsecInMeter = 3.08567758129e16
        self.Gamma = 6.67428e-11


class ModelNbody:
    def __init__(self):
        constants = Constants()
        self.pInitial = PODState()
        self.pAux = PODAuxState()
        self.root = BHTreeNode(Point2D(), Point2D())
        self.min = Point2D()
        self.max = Point2D()
        self.centre = Point2D()
        self.camDir = Point3D()
        self.camPos = Point3D()
        self.roi = 1.0
        self.timeStep = 1.0
        self.gamma_1 = constants.Gamma / (constants.ParsecInMeter ** 3) * constants.MassOfSun * (365.25 * 86400) ** 2
        self.num = 0
        self.bVerbose = False
    


    def eval(self, a_state, a_time, a_deriv):
        pState = PODState()
        pDeriv = PODDeriv()

        all = Particle(pState, self.pAux)

        self.CalcBHArea(all)
        self.BuiltTree(all)

        for i in range(1, self.num):
            p = Particle(pState[i], self.pAux[i])
            acc = self.root.CalcForce(p)
            pDeriv[i].ax = acc.x
            pDeriv[i].ay = acc.y
            pDeriv[i].vx = pState[i].vx
            pDeriv[i].vy = pState[i].vy


        self.root.StatReset()
        
        p = Particle(pState[0], self.pAux[0]) #Pas sur
        acc = self.root.CalcForce(p)
        pDeriv[0].ax = acc.x
        pDeriv[0].ay = acc.y
        pDeriv[0].vx = pState[0].vx
        pDeriv[0].vy = pState[0].vy


        self.camPos.x = self.root.GetCenterOfMass().x
        self.camPos.y = self.root.GetCenterOfMass().y


    def BuildTree(self, all:Particle):
        self.root.Reset(Point2D(self.centre.x - self.roi, self.centre.y - self.roi), Point2D(self.centre.x + self.roi, self.centre.y + self.roi))
        
        ct = 0
        for i in range(self.num):
            try:
                p = Particle(all._pState[i], all._pAuxState[i])

                self.root.Insert(p, 0)
                ct += 1
            except Exception as exc:
                '''
                print(exc)
                print(f"Particle {i} ({st.x}, {st.y}) is outside the roi (skipped).")
                print(f"  roi size   =   {m_roi}")
                print(f"  roi center = ({m_center.x}, {m_center.y})")
                '''
        self.root.ComputeMassDistribution()

        if self.bVerbose:
            print("Tree Dump")
            print("---------")
            self.root.DumpNode(-1, 0)
            print("\n\n")

        self.centre = self.root.GetCenterOfMass()
"""

void ModelNBody::BuiltTree(const ParticleData &all)
{
    // Reset the quadtree, make sure only particles inside the roi
    // are handled. The renegade ones may live long and prosper
    // outside my simulation
    _root.Reset(Vec2D(_center.x - _roi, _center.y - _roi),
                Vec2D(_center.x + _roi, _center.y + _roi));

    // build the quadtree
    int ct = 0;
    for (int i = 0; i < _num; ++i)
    {
        try
        {
            // extract data for a single particle
            ParticleData p(&(all._pState[i]),
                           &(all._pAuxState[i]));

            // insert the particle, but only if its inside the roi
            _root.Insert(p, 0);
            ++ct;
        }
        catch (std::exception &exc)
        {
            /*
                  std::cout << exc.what() << "\n";
                  std::cout << "Particle " << i << " (" << st->x << ", " << st->y << ") is outside the roi (skipped).\n";
                  std::cout << "  roi size   =   " << m_roi << "\n";
                  std::cout << "  roi center = (" << m_center.x << ", " << m_center.y << ")\n";
            */
        }
    }

    //  std::cout << ct << " particles added sucessfully\n";

    // compute masses and center of mass on all scales of the tree
    _root.ComputeMassDistribution();
    if (_bVerbose)
    {
        std::cout << "Tree Dump\n";
        std::cout << "---------\n";
        _root.DumpNode(-1, 0);
        std::cout << "\n\n";
    }

    // update the center of mass
    _center = _root.GetCenterOfMass();
}


"""






"""
void ModelNBody::Eval(double *a_state, double a_time, double *a_deriv)
{
    // wrap the complete particle data together for easier treatment
    // in the following algorithms
    PODState *pState = reinterpret_cast<PODState *>(a_state);
    PODDeriv *pDeriv = reinterpret_cast<PODDeriv *>(a_deriv);
    ParticleData all(pState, _pAux);

    CalcBHArea(all);
    BuiltTree(all);

#pragma omp parallel for
    for (int i = 1; i < _num; ++i)
    {
        ParticleData p(&pState[i], &_pAux[i]);
        Vec2D acc = _root.CalcForce(p);
        pDeriv[i].ax = acc.x;
        pDeriv[i].ay = acc.y;
        pDeriv[i].vx = pState[i].vx;
        pDeriv[i].vy = pState[i].vy;
    }

    // Particle 0 is calculated last, because the statistics
    // data relate to this particle. They would be overwritten
    // otherwise
    _root.StatReset();
    ParticleData p(&pState[0], &_pAux[0]);
    Vec2D acc = _root.CalcForce(p);
    pDeriv[0].ax = acc.x;
    pDeriv[0].ay = acc.y;
    pDeriv[0].vx = pState[0].vx;
    pDeriv[0].vy = pState[0].vy;

    // Save vectors for camera orientations
    //  m_camDir.x = pState[0].x - pState[4000].x;
    //  m_camDir.y = pState[0].y - pState[4000].y;
    _camPos.x = _root.GetCenterOfMass().x;
    _camPos.y = _root.GetCenterOfMass().y;
}









---------------------
    PODState *_pInitial;        ///< The initial state
    PODAuxState *_pAux;         ///< Auxilliary state information

    BHTreeNode _root;           ///< The root node of the barnes hut tree
    Vec2D _min;                 ///< Upper left corner of the bounding box containing all particles
    Vec2D _max;                 ///< Lower right corner of the bounding box containing all particles
    Vec2D _center;              ///< The center of the simulation, the barnes hut tree is centered at this point
    Vec3D _camDir;              ///< Direction of the camera
    Vec3D _camPos;              ///< Position of the camera
    double _roi;
    double _timeStep;

    static constexpr double gamma_1 = Constants::Gamma / (Constants::ParsecInMeter * Constants::ParsecInMeter * Constants::ParsecInMeter) * Constants::MassOfSun * (365.25 * 86400) * (365.25 * 86400);
  
    int _num;
    bool _bVerbose;
----------------------------
"""



"""
import concurrent.futures

class ModelNBody:
    # ... autres parties de la classe ...

    def Eval(self, a_state, a_time, a_deriv):
        p_state = a_state
        p_deriv = a_deriv
        all_data = ParticleData(p_state, self._pAux)

        self.CalcBHArea(all_data)
        self.BuiltTree(all_data)

        def calculate_force(i):
            p = ParticleData(p_state[i], self._pAux[i])
            acc = self._root.CalcForce(p)
            p_deriv[i].ax = acc.x
            p_deriv[i].ay = acc.y
            p_deriv[i].vx = p_state[i].vx
            p_deriv[i].vy = p_state[i].vy

        # Utilisation de ThreadPoolExecutor pour paralléliser la boucle for
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(calculate_force, range(1, self._num))

        # Calculer pour la particule 0 après la parallélisation
        self._root.StatReset()
        p = ParticleData(p_state[0], self._pAux[0])
        acc = self._root.CalcForce(p)
        p_deriv[0].ax = acc.x
        p_deriv[0].ay = acc.y
        p_deriv[0].vx = p_state[0].vx
        p_deriv[0].vy = p_state[0].vy

        # Enregistrez les vecteurs pour les orientations de la caméra
        # m_camDir.x = p_state[0].x - p_state[4000].x
        # m_camDir.y = p_state[0].y - p_state[4000].y
        self._camPos.x = self._root.GetCenterOfMass().x
        self._camPos.y = self._root.GetCenterOfMass().y

"""