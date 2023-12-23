import random

import vector



MAX_SPEED = 50
FRONT = 20



class Vehicle:
    def __init__(self):
        rnd = random.uniform(20, 300), random.uniform(20, 300)
        self.xy = rnd

        rnd = random.uniform(-1, 1), random.uniform(-1, 1)
        self.velocity = vector.MultNorm(MAX_SPEED, rnd)


    def Update(self, dt):
        self.xy = vector.Add(self.xy, vector.Mult(dt, self.velocity))


    def FollowPath(self, path_segs):
        idx = 0
        dist = vector.Len2(vector.Sub(self.xy, path_segs[0]))
        NUM_SEGS = len(path_segs)
        for i in range(1, NUM_SEGS):
            d = vector.Len2(vector.Sub(self.xy, path_segs[i]))
            if dist > d:
                idx = i
                dist = d

        ed_idx = (idx + 1) % NUM_SEGS
        n = vector.Normalize(vector.Sub(path_segs[idx], path_segs[ed_idx]))
        f = vector.Add(self.xy, vector.MultNorm(FRONT, self.velocity))
        p = vector.Dot(n, vector.Sub(path_segs[idx], f))
        v = vector.MultNorm(MAX_SPEED / 2.0, vector.Mult(p, n))
        new_vel = vector.MultNorm(MAX_SPEED, vector.Add(self.velocity, v))
        self.velocity = new_vel

        #v = vector.Sub(self.xy, path_segs[idx])
        #v = vector.MultNorm(MAX_SPEED / 2.0, v)
        #v = vector.Add(v, self.velocity)
        #v = vector.MultNorm(MAX_SPEED, v)
        #self.velocity = v

