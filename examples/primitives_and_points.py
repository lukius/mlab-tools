import random
import sys
sys.path.append('../')

from mlab_tools.animation import Animation, StopAnimation
from mlab_tools.point import Point
from mlab_tools.polyline import AnimatedPolyLine
from mlab_tools.primitive import Sphere, Box, Cone, Cylinder


class PrimitivesAndPoints(Animation):
    
    """This animation uses some primitives (namely, sphere, cube, cone and
    cylinder) and animated polylines on a random set of points."""

    def rand_color(self):
        return (random.random(), random.random(), random.random())
    
    def animate_obj(self, obj, frame_no):
        obj.transform(rotate=(1,1,1))
        
    def initialize(self):
        # Animation state can be preserved in instance variables.
        self.points = list()
        
        sphere = Sphere(center=(1,1,1), radius=1, theta_res=20, phi_res=20)
        
        cone = Cone(radius=0.4, height=0.5, resolution=20)
        cone.transform(translate=1)
        
        cylinder = Cylinder(radius=0.1, height=0.5, resolution=20)
        cylinder.transform(translate=1.3)
        
        box = Box(0.2,0.2,1)
        box.transform(translate=1.8)
    
        # Note that the same animator is used for every primitive.
        self.add_animated_object(sphere, self.animate_obj, color=(0,1,0), opacity=0.5)
        self.add_animated_object(box, self.animate_obj, color=(1,1,0))
        self.add_animated_object(cone, self.animate_obj, color=(1,0,1))
        self.add_animated_object(cylinder, self.animate_obj, color=(0,0,1))
    
    def on_frame(self, frame_no):
        def rand_point():
            point = (random.random()+2, random.random()+2, random.random()+2)
            return Point(*point)
    
        # Generate a random point for the first 30 frames.
        if frame_no < 30:
            point = rand_point()
            self.add_object(point, color=self.rand_color())
            self.points.append(point)
    
        # On frame 30, render a polyline that will progressively join the 
        # randomly generated points above.
        if frame_no == 30:
            line = AnimatedPolyLine(self.points, initial_frame=frame_no)
            self.add_object(line, color=(0,0,0))
    
        # Leave enough time for the polyline to join the whole set of 30 points.
        if frame_no > 60: StopAnimation()


def run_animation():
    animation = PrimitivesAndPoints(800, 600)
    animation.run(delay=200)


if __name__ == '__main__':
    run_animation()

