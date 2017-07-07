from tvtk.api import tvtk

from animation import Stop


class PolyObject(object):

    def _set_actor(self):
        self.mapper = tvtk.PolyDataMapper()
        self.mapper.set_input_data(self.poly_data)

        self.actor = tvtk.Actor(mapper=self.mapper)
        self.actor.mapper.update()

    def _to_tuple(self, value):
        if isinstance(value, (list, tuple)):
            return value[:3]
        elif isinstance(value, (int, float)):
            return value, value, value

    def get_actor(self):
        return self.actor

    def default_animation(self):
        return lambda obj, frame_no: Stop()

    def update_properties(self, **props):
        properties = tvtk.Property(**props)
        self.actor.property = properties

    def transform(self, translate=None, scale=None, rotate=None):
        transform = tvtk.Transform()

        if translate is not None:
            transform.translate(self._to_tuple(translate))

        if scale is not None:
            transform.scale(self._to_tuple(scale))

        if rotate is not None:
            rotate = self._to_tuple(rotate)
            transform.rotate_x(rotate[0])
            transform.rotate_y(rotate[1])
            transform.rotate_z(rotate[2])
        
        current = self.actor.user_transform or tvtk.Transform()
        transform.concatenate(current)
        self.actor.user_transform = transform
