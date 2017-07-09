from sphere import Sphere


def Point(x, y, z, thickness=1e-2):
    return Sphere(center=(x,y,z), radius=thickness)