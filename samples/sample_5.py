import random
import sys
sys.path.append('../')

from mlab_tools.animation import Animation, StopAnimation
from mlab_tools.point import Point
from mlab_tools.polyline import AnimatedPolyLine
from mlab_tools.primitive import Sphere, Box, Cone, Cylinder


points = list()

def rand_color():
    return (random.random(), random.random(), random.random())

def animate_obj(obj, frame_no):
    obj.transform(rotate=(1,1,1))

def frame_callback(frame_no, animation):
    global points

    def rand_point():
        point = (random.random()+2, random.random()+2, random.random()+2)
        return Point(*point)

    if frame_no < 30:
        point = rand_point()
        animation.add_object(point, color=rand_color())
        points.append(point)

    if frame_no == 30:
        line = AnimatedPolyLine(points, initial_frame=frame_no)
        animation.add_object(line, color=(0,0,0))

    if frame_no > 60: StopAnimation()

def run_animation():
    animation = Animation(800, 600)

    sphere = Sphere(center=(1,1,1), radius=1, theta_res=20, phi_res=20)
    
    cone = Cone(radius=0.4, height=0.5, resolution=20)
    cone.transform(translate=1)
    
    cylinder = Cylinder(radius=0.1, height=0.5, resolution=20)
    cylinder.transform(translate=1.3)
    
    box = Box(0.2,0.2,1)
    box.transform(translate=1.8)

    animation.add_animated_object(sphere, animate_obj, color=(0,1,0), opacity=0.5)
    animation.add_animated_object(box, animate_obj, color=(1,1,0))
    animation.add_animated_object(cone, animate_obj, color=(1,0,1))
    animation.add_animated_object(cylinder, animate_obj, color=(0,0,1))

    animation.run(frame_callback=frame_callback, delay=200)


if __name__ == '__main__':
    run_animation()

