import random
import sys
sys.path.append('../')


from mlab_tools.animation import Animation, Stop, StopAndRemove
from mlab_tools.polyhedron import Polyhedron
from mlab_tools.polyline import AnimatedPolyLine


def animate_shield(shield, frame_no):
    shield.transform(rotate=frame_no, translate=(0,0,0.1))
    new_color = (random.random(), random.random(), random.random())
    shield.update_properties(color=new_color)
    if frame_no > 10: Stop()

def animate_pipe(pipe, frame_no):
    angle = 360/20
    pipe.transform(rotate=(0,angle,0))
    if frame_no > 20: StopAndRemove()

def run_animation():
    animation = Animation(640, 480)

    pipe = Polyhedron.from_OFF('volumes/beampipe.off')
    pipe.transform(translate=1, scale=1e-3)

    shield = Polyhedron.from_OFF('volumes/shield.off')
    shield.transform(translate=3, scale=1e-3)

    polyline = AnimatedPolyLine([(0,0,0), (0,5,0), (2,2,0), (0,2,2), (2,2,7)])

    animation.add_animated_object(pipe, animate_pipe, opacity=0.5)
    animation.add_animated_object(shield, animate_shield, color=(0,0,1))
    animation.add_object(polyline, color=(1,0,0))

    animation.run(delay=300)


if __name__ == '__main__':
    run_animation()

