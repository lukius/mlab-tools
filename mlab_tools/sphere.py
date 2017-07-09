from tvtk.api import tvtk
from tvtk.common import configure_input_data

from object import Object


class Sphere(Object):
    
    def __init__(self, center, radius):
        Object.__init__(self)
        self.center = center
        self.radius = radius
        self._configure()
        
    def _configure(self):
        self.sphere = tvtk.SphereSource(center=self.center, radius=self.radius)
        self.mapper = tvtk.PolyDataMapper()
        configure_input_data(self.mapper, self.sphere.output)
        self.sphere.update()
        
        self._set_actor()