from primitive import Sphere


def Point(x, y, z, thickness=1e-2):
    """Sphere wrapper to represent points."""
    return Sphere(center=(x,y,z), radius=thickness)