from Point import Point

class Particule:

    def __init__(self, position: Point, vitesse: Point, acceleration: Point, masse):
        self.position = position
        self.vitesse = vitesse
        self.acceleration = acceleration
        self.masse = masse
        
    def __str__(self):
        return str("Position : "
              + str(self.position.x)
              + ", "
              + str(self.position.y)
              + "\nVitesse : "
              + str(self.vitesse.x)
              + ", "
              + str(self.vitesse.y)
              + "\nAcceleration : "
              + str(self.acceleration.x)
              + ", "
              + str(self.acceleration.y))