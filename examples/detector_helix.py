import math
import sys
sys.path.append('../')

from mlab_tools.animation import Animation, StopAnimation
from mlab_tools.polyline import AnimatedPolyLine
from mlab_tools.polyhedron import Polyhedron
from mlab_tools.point import Point


class HelixInDetector(Animation):
    
    """A more complex animation that shows a small fragment of a particle
    detector, zooming into it to reveal a particle describing a helicoidal
    trajectory inside. Some points are distinguished in the trajectory;
    they represent boundary points in the geometry."""
    
    INIT_ROLL    = 2.588
    INIT_DIST    = 18555.628
    INIT_ELEV    = 27.673
    INIT_AZIMUTH = 12.699
    INIT_FOCAL   = (-1000,0,0)
    
    POLYHEDRON_COLOR = (0.8, 0.8, 0.8)
    TRAJECTORY_COLOR = (1, 0, 0)
    POINTS_COLOR     = (0, 0, 1)
    
    def distance(self, i, j):
        point1 = self.points[i]
        point2 = self.int_points[j]
        
        x = point1[0] - point2[0]
        y = point1[1] - point2[1]
        z = point1[2] - point2[2]
        
        return math.sqrt(x**2 + y**2 + z**2)
    
    def initialize(self):
        self.points = list()
        self.int_points = list()
        
        self.first_zoom_done = False
        self.rotation_done = False
        self.second_zoom_done = False
        self.wait_done = False
        self.wait_frame = 0        
        
        with open('data/points', 'r') as _file:
            for line in _file.readlines():
                point = map(float, line.strip().split(' '))
                self.points.append(point)
                
        with open('data/int_points', 'r') as _file:
            for line in _file.readlines():
                point = map(float, line.strip().split(' '))
                self.int_points.append(point)        
        
        with open('data/volumes', 'r') as _file:
            for line in _file.readlines():
                filename = line.strip()
                poly = Polyhedron.from_OFF(filename)
                self.add_object(poly, color=self.POLYHEDRON_COLOR, opacity=0.7)
                
        trajectory = AnimatedPolyLine(list(self.points))
        self.add_object(trajectory, color=self.TRAJECTORY_COLOR)
        
        self.update_camera(roll=self.INIT_ROLL,
                           distance=self.INIT_DIST,
                           elevation=self.INIT_ELEV,
                           azimuth=self.INIT_AZIMUTH,
                           focalpoint=self.INIT_FOCAL)        
    
    def on_frame(self, frame_no):
        if self.points and self.int_points and self.distance(0,0) < 1e-2:
            int_point = self.int_points.pop(0)
            point = Point(*int_point, thickness=5)
            self.add_object(point, color=self.POINTS_COLOR)
        if self.points:
            self.points.pop(0)
        
        params = self.camera.parameters()
        distance = params['distance']
        azimuth = params['azimuth']
        elevation = params['elevation']
        x, y, z = params['focalpoint']
        
        if distance < 4000:
            self.first_zoom_done = True
        if self.first_zoom_done and azimuth > 170:
            self.rotation_done = True
        if self.rotation_done and distance < 300:
            self.second_zoom_done = True
        if self.second_zoom_done and\
           self.wait_frame != 0 and\
           frame_no - self.wait_frame > 60:
            self.wait_done = True
        if self.wait_done and distance >= 15000:
            StopAnimation()
        
        if not self.first_zoom_done:
            self.update_camera(distance=-100)
        elif not self.rotation_done:
            self.update_camera(azimuth=3)
        elif not self.second_zoom_done:
            if elevation < 130:
                self.update_camera(distance=-20, elevation=2)
            else:
                self.update_camera(distance=-20)
        elif not self.wait_done:
            if self.wait_frame == 0:
                self.wait_frame = frame_no
        else:
            self.update_camera(distance=250,
                               focalpoint=(x-20, y+20, z+20))
        
    
def run_animation():
    animation = HelixInDetector(1024, 768)
    animation.run(delay=50)


if __name__ == '__main__':
    run_animation()