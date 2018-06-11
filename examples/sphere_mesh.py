import sys
sys.path.append('../')

from mlab_tools.animation import Animation, StopAnimation
from mlab_tools.geometry import GeometryParser
from mlab_tools.polyline import AnimatedPolyLine


class SphereMeshAnimation(Animation):
    
    """This example shows how to use a VTK geometry file to render a 3D polyhedron mesh."""
    
    def initialize(self):
        self.parse_volumes()
        self.parse_trajectory()
        volume_names = map(lambda (time, volume): volume, self.volumes)
        
        parser = GeometryParser.from_VTK('data/sphere.vtk')
        self.geometry = parser.parse()
        
        for name, polyhedron in self.geometry:
            if name not in volume_names:
                continue
            polyhedron.transform(scale=100)
            polyhedron.transform(translate=0.1)
            self.add_object(polyhedron, opacity=0.01)
            
        self.update_camera(focalpoint=[10, -30, 10],
                           distance=1000,
                           azimuth=0,
                           elevation=180,
                           roll=0)
            
    def parse_volumes(self):
        self.volumes = list()
        
        with open('data/retQSS_volumes', 'r') as _file:
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
        
        with open('data/retQSS_trajectory', 'r') as _file:
            lines = _file.readlines()
            for line in lines:
                time, x, y, z = map(float, line.split())
                points.append((x,y,z))
                self.times.append(time)
                
        self.trajectory = AnimatedPolyLine(points)
        self.add_object(self.trajectory, color=(0,0,1))                
            
    def on_frame(self, frame_no):
        current_point_idx = self.trajectory.current_point()
        time = self.times[current_point_idx]
        
        self.update_camera(roll=0.1, distance=-0.7, elevation=-0.1)
        
        volume_name = self.volumes[self.current_volume_idx][1]
        if volume_name == 'World':
            StopAnimation()
            
        while time >= self.volumes[self.current_volume_idx][0]:
            if self.last_polyhedron is not None:
                self.last_polyhedron.update_properties(color=(0.5,0,0), opacity=0.05)
                
            volume_name = self.volumes[self.current_volume_idx][1]
            print 'Entering volume {}...'.format(volume_name)
            
            polyhedron = self.geometry.get_polyhedron(volume_name)
            polyhedron.update_properties(color=(0.7,0,0), opacity=0.3)
            
            self.current_volume_idx += 1
            self.last_polyhedron = polyhedron
        

def run_animation():
    animation = SphereMeshAnimation(640, 480)
    animation.run(delay=300, save_to='sphere')


if __name__ == '__main__':
    run_animation()

