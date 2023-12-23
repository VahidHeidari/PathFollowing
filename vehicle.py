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
        #    /|\ '',. p (o)
        #     |    .
        #     | __.
        #     |  /| (n)
        #     | /
        #     |/
        #    (s)
        #

        # Segment vector
        NUM_SEGS = len(path_segs)
        ed_idx = (self.idx + 1) % NUM_SEGS
        s = vector.Sub(path_segs[self.idx], path_segs[ed_idx])
        n = vector.Normalize(s)

        # Front vector
        f = vector.Add(self.xy, vector.MultNorm(FRONT, self.velocity))

        # Projection to segment length
        p = vector.Dot(n, vector.Sub(path_segs[self.idx], f))
        if abs(p) > vector.Len(s):
            self.idx = (self.idx + 1) % NUM_SEGS        # Next Segment

        # Path aligned vector
        v = vector.MultNorm(MAX_SPEED / 2.0, vector.Mult(abs(p), n))
        new_vel = vector.Add(self.velocity, v)

        # Path perpendicular vector
        spn = vector.Add(path_segs[self.idx], vector.Mult(p, n))
        o = vector.Sub(f, spn)
        ort_vel = vector.Add(new_vel, o)

        # Apply result.
        self.velocity = vector.MultNorm(MAX_SPEED, ort_vel)

