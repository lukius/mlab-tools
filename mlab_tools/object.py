from tvtk.api import tvtk

from animation import Stop


class Object(object):
    
    """Base class for objects that can be placed into the scene."""

    def _set_actor(self):
        self.actor = tvtk.Actor(mapper=self.mapper)
        self.actor.mapper.update()

    def get_actor(self):
        return self.actor

    def default_animator(self):
        """Returns the default animator, which leaves the object still."""
        return lambda obj, frame_no: Stop()

    def update_properties(self, **props):
        """Updates the object properties, such as opacity, color, etc. (see VTK
        documentation for further details)."""
        properties = tvtk.Property(**props)
        self.actor.property = properties

    def _to_tuple(self, value):
        if isinstance(value, (list, tuple)):
            return value[:3]
        elif isinstance(value, (int, float)):
            return value, value, value

    def transform(self, translate=None, scale=None, rotate=None):
        """Applies an affine transformation to the current object.
        
        Keyword arguments are self explanatory. They can be a tuple or list
        representing the three-dimensional vector or a single number to use
        for each of the three components.
        """
        transform = self.actor.user_transform or tvtk.Transform()

        if translate is not None:
            transform.translate(self._to_tuple(translate))

        if scale is not None:
            transform.scale(self._to_tuple(scale))

        if rotate is not None:
            rotate = self._to_tuple(rotate)
            transform.rotate_x(rotate[0])
            transform.rotate_y(rotate[1])
            transform.rotate_z(rotate[2])
        
        self.actor.user_transform = transform


class PolyObject(Object):
    
    """Base class for objects based on vtkPolyData."""

    def _set_actor(self):
        self.mapper = tvtk.PolyDataMapper()
        self.mapper.set_input_data(self.poly_data)
        Object._set_actor(self)