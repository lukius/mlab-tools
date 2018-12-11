import sys
sys.path.append('../')

from mlab_tools.animation import Animation, StopAnimation
from mlab_tools.geometry import GeometryParser
from mlab_tools.polyline import AnimatedPolyLine


class CubeMeshAnimation(Animation):
    
    """This example shows how to use a VTK geometry file to render a 3D polyhedron mesh."""
    
    def initialize(self):
        self.parse_volumes()
        self.parse_trajectory()
        
        parser = GeometryParser.from_VTK('data/cube.vtk')
        self.geometry = parser.parse()
        self.polys = list()
        
        for _, polyhedron in self.geometry:
            self.polys.append(polyhedron)
            self.add_object(polyhedron, opacity=0.1)
            
        self.update_camera(focalpoint=[0,-30,120],
                           distance=2700,
                           azimuth=0,
                           elevation=90,
                           roll=-90)
            
    def parse_volumes(self):
        self.volumes = list()
        self.boundary = list()
        
        with open('data/retQSS_volumes_cube', 'r') as _file:
            lines = _file.readlines()
            for line in lines:
                fields = line.split()
                time = float(fields[0])
                volume = fields[1]
                self.volumes.append((time, volume))
                
        self.current_volume_idx = 0
        self.last_polyhedron = None
                
    def parse_trajectory(self):
        points = list()
        self.times = list()
        
        with open('data/retQSS_trajectory_cube', 'r') as _file:
            lines = _file.readlines()
            for line in lines:
                time, x, y, z = map(float, line.split()[:-1])
                points.append((x,y,z))
                self.times.append(time)
                
        self.trajectory = AnimatedPolyLine(points)
        self.add_object(self.trajectory, color=(0,0,1))                
            
    def on_frame(self, frame_no):
        current_point_idx = self.trajectory.current_point()
        time = self.times[current_point_idx]
        
        for poly in self.polys:
            poly.transform(rotate=(0,0,0.3))
        self.trajectory.transform(rotate=(0,0,0.3))
        
        dist = self.get_camera().parameters()['distance']
        if dist > 525:
            self.update_camera(distance=-10)
        
        while self.current_volume_idx < len(self.volumes) and\
              time >= self.volumes[self.current_volume_idx][0]:
            if self.last_polyhedron is not None:
                self.last_polyhedron.update_properties(color=(0.5,0,0), opacity=0.05)
                
            volume_name = self.volumes[self.current_volume_idx][1]
            print 'Entering volume {}...'.format(volume_name)
            
            polyhedron = self.geometry.get_polyhedron(volume_name)
            polyhedron.update_properties(color=(0.7,0,0), opacity=0.3)
            self.last_polyhedron = polyhedron
            
            self.current_volume_idx += 1
            
        if current_point_idx == self.trajectory.num_points()-1:
            StopAnimation()
        

def run_animation():
    animation = CubeMeshAnimation(640, 480)
    animation.run(delay=20, save_to='cube')


if __name__ == '__main__':
    run_animation()

