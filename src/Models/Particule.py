from Point import Point

class Particule:

    def __init__(self, position: Point, vitesse, acceleration, masse):
        self.position = position
        self.vitesse = vitesse
        self.acceleration = acceleration
        self.masse = masse