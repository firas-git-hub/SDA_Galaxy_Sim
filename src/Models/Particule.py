from Point import Point

class Particule:

    def __init__(self, position: Point, vitesse: Point, acceleration: Point, masse):
        self.etat = etatParticule(position, vitesse)
        self.etatDeriv = etatDerivParticule(vitesse, acceleration)
        self.masse = masse
        
    def __str__(self):
        return str("Etat Particule : \n"
                   + "Position : " 
                   + str(self.etat.position.x) 
                   + ", " 
                   + str(self.etat.position.y) 
                   + "\nVitesse : "
                   + str(self.etat.vitesse.x)
                   + ", "
                   + str(self.etat.vitesse.y)
                   + "Etat Derivee du Particule : \n"
                   + "\nVitesse : "
                   + str(self.etatDeriv.vitesse.x)
                   + ", "
                   + str(self.etatDeriv.vitesse.y)
                   + "\nAcceleration : "
                   + str(self.etatDeriv.acceleration.x)
                   + ", "
                   + str(self.etatDeriv.acceleration.y))
        
class etatParticule:
    def __init__(self, position: Point, vitesse: Point):
        self.position = position
        self.vitesse = vitesse
    
class etatDerivParticule:
    def __init__(self, vitesse: Point, acceleration: Point):
        self.vitesse = vitesse
        self.acceleration = acceleration