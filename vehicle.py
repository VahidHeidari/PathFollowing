import random

import vector



MAX_SPEED = 50
FRONT = 20

IS_INIT_RANDOM = True
#IS_INIT_RANDOM = False



class Vehicle:
    def __init__(self):
        if IS_INIT_RANDOM:
            rnd = random.uniform(20, 300), random.uniform(20, 300)
            self.xy = rnd
            rnd = random.uniform(-1, 1), random.uniform(-1, 1)
            self.velocity = vector.MultNorm(MAX_SPEED, rnd)
        else:
            self.xy = (100, 30)
            self.velocity = vector.MultNorm(MAX_SPEED, (100, 15))

        self.idx = 0


    @staticmethod
    def FindNearestStartSegment(path_segs):
        idx = 0
        dist = vector.Len2(vector.Sub(self.xy, path_segs[0]))
        NUM_SEGS = len(path_segs)
        for i in range(1, NUM_SEGS):
            d = vector.Len2(vector.Sub(self.xy, path_segs[i]))
            if dist > d:
                idx = i
                dist = d
        return idx


    def Update(self, dt):
        self.xy = vector.Add(self.xy, vector.Mult(dt, self.velocity))


    def FollowPath(self, path_segs):
        #
        #              (e)
        #              .
        #    (f)      .
        #     ;,,    .
        #    /|\ '',. p
        #     |    .
        #     | __.
        #     |  /| (n)
        #     | /
        #     |/
        #    (s)
        #
        NUM_SEGS = len(path_segs)
        ed_idx = (self.idx + 1) % NUM_SEGS
        s = vector.Sub(path_segs[self.idx], path_segs[ed_idx])
        n = vector.Normalize(s)
        f = vector.Add(self.xy, vector.MultNorm(FRONT, self.velocity))
        p = abs(vector.Dot(n, vector.Sub(path_segs[self.idx], f)))
        if p > vector.Len(s):
            self.idx = (self.idx + 1) % NUM_SEGS        # Next Segment
        v = vector.MultNorm(MAX_SPEED / 2.0, vector.Mult(p, n))
        new_vel = vector.MultNorm(MAX_SPEED, vector.Add(self.velocity, v))
        self.velocity = new_vel

