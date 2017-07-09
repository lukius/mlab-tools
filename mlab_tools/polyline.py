from tvtk.api import tvtk

from animation import Stop
from object import PolyObject
from sphere import Sphere


class PolyLine(PolyObject):
    
    def __init__(self, points):
        PolyObject.__init__(self)
        self.points = points
        self._configure(points)

    def _to_float_tuple(self, point):
        if isinstance(point, Sphere):
            point = point.center
        return point

    def _configure(self, points):
        self.vtk_points = tvtk.Points()
        self.lines = tvtk.CellArray()

        for point in points:
            self.vtk_points.insert_next_point(self._to_float_tuple(point))
         
        for i in xrange(len(points)-1):
            line = tvtk.Line()
            line.point_ids.set_id(0, i)
            line.point_ids.set_id(1, i+1)
            self.lines.insert_next_cell(line)
         
        self.poly_data = tvtk.PolyData(points=self.vtk_points, lines=self.lines)

        self._set_actor()

    def add_point(self, point):
        idx = len(self.vtk_points) - 1

        self.vtk_points.insert_next_point(self._to_float_tuple(point))
        
        line = tvtk.Line()
        line.point_ids.set_id(0, idx)
        line.point_ids.set_id(1, idx+1)
        self.lines.insert_next_cell(line)

        self.poly_data.update_traits()
        self.poly_data.modified()
        self.actor.mapper.update()


class AnimatedPolyLine(PolyLine):

    def __init__(self, points, initial_frame=1):
        PolyLine.__init__(self, points)
        self.initial_frame = initial_frame

    def _configure(self, points):
        PolyLine._configure(self, self.points[:1])

    def default_animation(self):

        def anim(obj, abs_frame_no):
            frame_no = abs_frame_no - self.initial_frame
            if frame_no >= len(self.points): Stop()
            self.add_point(self.points[frame_no])

        return anim
