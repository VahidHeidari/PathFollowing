import math



def Len(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2)


def Normalize(vec):
    vec_dist = Len(vec)
    return (vec[0] / vec_dist, vec[1] / vec_dist)


def Neg(vec):
    return (-vec[0], -vec[1])


def Mult(amt, vec):
    return (vec[0] * amt, vec[1] * amt)


def Add(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])


def Orth(vec):
    return (-vec[1], vec[0])

