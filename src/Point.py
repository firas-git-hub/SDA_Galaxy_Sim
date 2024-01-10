class Point:
    
    def __init__(self, x: float = None, y: float = None):
        self.x = x
        self.y = y

    def __str__(self):
        return str("x: "
                   + str(self.x)
                   + ", y: "
                   + str(self.y))
