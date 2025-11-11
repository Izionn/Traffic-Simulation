from math import pi


def degToRad(deg):
    return ((deg / 180) * pi) % (2 * pi)


def radToDeg(rad):
    return (rad * 180 / pi) % (360)
