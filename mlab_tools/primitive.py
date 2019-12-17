from tvtk.api import tvtk
from tvtk.common import configure_input_data

from object import Object


class Primitive(Object):
    
    """Base class for 'primitive' objects (i.e., those based on some of the
    vtkPolyDataAlgorithm subclasses).
    """
    
    def __init__(self, center):
        Object.__init__(self)
        self.center = center or (0,0,0)

    def _get_primitive(self):
        raise NotImplementedError
    
    def set_center(self, center):
        self.primitive.center = center
        self.primitive.update()

    def _configure(self):
        self.primitive = self._get_primitive()
        self.mapper = tvtk.PolyDataMapper()
        configure_input_data(self.mapper, self.primitive.output)
        self.primitive.update()
        
        self._set_actor()
        

class Sphere(Primitive):
    
    def __init__(self, center, radius, theta_res=8, phi_res=8):
        Primitive.__init__(self, center)
        self.radius = radius
        self.theta_res = theta_res
        self.phi_res = phi_res
        self._configure()
        
    def _get_primitive(self):
        return tvtk.SphereSource(center=self.center,
                                 radius=self.radius,
                                 theta_resolution=self.theta_res,
                                 phi_resolution=self.phi_res)

        
class Box(Primitive):

    def __init__(self, x_length, y_length, z_length, center=None):
        Primitive.__init__(self, center)
        self.x_length = x_length
        self.y_length = y_length
        self.z_length = z_length
        self._configure()
        
    def _get_primitive(self):
        return tvtk.CubeSource(center=self.center,
                               x_length=self.x_length,
                               y_length=self.y_length,
                               z_length=self.z_length)


class Cube(Box):
    
    def __init__(self, length, center=None):
        Box.__init__(self, length, length, length, center=center)
        
        
class Cone(Primitive):
    
    def __init__(self, radius, height, resolution=6, center=None, direction=None):
        Primitive.__init__(self, center)
        self.radius = radius
        self.height = height
        self.resolution = resolution
        self.direction = direction or (1,0,0)
        self._configure()
        
    def set_direction(self, direction):
        self.primitive.direction = direction
        self.primitive.update()
        
    def _get_primitive(self):
        return tvtk.ConeSource(center=self.center,
                               height=self.height,
                               radius=self.radius,
                               direction=self.direction,
                               resolution=self.resolution)
        
class Cylinder(Primitive):
    
    def __init__(self, radius, height, resolution=6, center=None):
        Primitive.__init__(self, center)
        self.radius = radius
        self.height = height
        self.resolution = resolution
        self._configure()
        
    def _get_primitive(self):
        return tvtk.CylinderSource(center=self.center,
                                   height=self.height,
                                   radius=self.radius,
                                   resolution=self.resolution)