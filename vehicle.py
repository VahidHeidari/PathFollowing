import vector



class Vehicle:
    def __init__(self):
        self.xy = (30, 20)
        self.velocity = vector.Mult(10, (5, 7))


    def Update(self, dt):
        self.xy = vector.Add(self.xy, vector.Mult(dt, self.velocity))

