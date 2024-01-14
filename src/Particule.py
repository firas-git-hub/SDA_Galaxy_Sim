from Point import Point

class Particule:

    def __init__(self, position: Point, vitesse: Point, acceleration: Point, masse):
        self.etat = Etat(position, vitesse)
        self.etatDeriv = EtatDeriv(vitesse, acceleration)
        self.masse = masse
        
    def __str__(self):
        return str("Etat Particule : \n"
                   + "Position : " 
                   + str(self.etat.position.x) 
                   + ", " 
                   + str(self.etat.position.y) 
                   + "Vitesse : "
                   + str(self.etat.vitesse.x)
                   + ", "
                   + str(self.etat.vitesse.y)
                   + "\nEtat Derivee du Particule : \n"
                   + "Vitesse : "
                   + str(self.etatDeriv.vitesse.x)
                   + ", "
                   + str(self.etatDeriv.vitesse.y)
                   + "Acceleration : \n"
                   + str(self.etatDeriv.acceleration.x)
                   + ", "
                   + str(self.etatDeriv.acceleration.y))
        
class Etat:
    def __init__(self, position: Point, vitesse: Point):
        self.position = position
        self.vitesse = vitesse
    
class EtatDeriv:
    def __init__(self, vitesse: Point, acceleration: Point):
        self.vitesse = vitesse
        self.acceleration = acceleration