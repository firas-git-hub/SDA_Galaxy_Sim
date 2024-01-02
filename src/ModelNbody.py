from f import BHTreeNode

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class ModelNbody:
    def __init__(self):
        #pAux
        self.root = BHTreeNode(Point2D(), Point2D())
        self.min = Point2D()
        self.max = Point2D()
        self.centre = Point2D()
        self.camDir = Point3D()
        self.camPos = Point3D()
        self.roi = 1.0
        self.timeStep = 1.0
        #self.gamma_1 = Constants.Gamma / (Constants.ParsecInMeter ** 3) * Constants.MassOfSun * (365.25 * 86400) ** 2
        self.num = 0
        self.bVerbose:bool
        

"""
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
"""