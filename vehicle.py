import vector



class Vehicle:
    def __init__(self):
        self.xy = (30, 20)
        self.velocity = vector.Mult(10, (10, 15))


    def Update(self, dt):
        self.xy = vector.Add(self.xy, vector.Mult(dt, self.velocity))

