from tvtk.api import tvtk

from animation import Stop
from object import PolyObject
from primitive import Sphere


class PolyLine(PolyObject):
    
    """Class that represents a polyline (i.e., a continuous line that is made
    up of several linear segments).
    """
    
    def __init__(self, points):
        """Build a polyline from a given list of points.
        
        Arguments:
        
        :points: a list of points of the form (x, y, z) or objects returned by
        the Point function.
        """
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
        
    def num_points(self):
        return len(self.points)

    def add_point(self, point):
        """Adds a point to the polyline.
        
        Arguments:
        
        :point: a point of the form (x, y, z) or an object returned by the
        Point function. 
        """
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
    
    """An animated polyline (see PolyLine class for further details).
    
    Points in the this polyline will be progressively added frame after frame.
    This is achieved by a custom animator provided by the `default_animator`
    method.
    """

    def __init__(self, points, initial_frame=1):
        """Build an animated polyline from a given list of points.
        
        Arguments:
        
        :points: a list of points of the form (x, y, z) or objects returned by
        the Point function.
        
        :initial_frame: number of the first frame on which this polyline
        appears on scene (defaults to 1).
        """        
        PolyLine.__init__(self, points)
        self.initial_frame = initial_frame
        self.current_point_idx = 0

    def _configure(self, points):
        PolyLine._configure(self, self.points[:1])

    def default_animator(self):

        def anim(obj, abs_frame_no):
            # Compute frame number relative to the starting point of this line.
            frame_no = abs_frame_no - self.initial_frame
            if frame_no >= len(self.points): Stop()
            self.add_point(self.points[frame_no])
            self.current_point_idx = frame_no

        return anim
    
    def current_point(self):
        return self.current_point_idx
