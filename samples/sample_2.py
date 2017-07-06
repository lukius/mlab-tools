import sys
sys.path.append('../')

from mlab_tools.animation import Animation, StopAnimation
from mlab_tools.polyhedron import Polyhedron
from mlab_tools.polyline import AnimatedPolyLine

def transform_shield(shield, frame_no):
    shield.transform(rotate=frame_no, translate=(0,0,0.5))
    return frame_no > 6

def run_animation():
    animation = Animation(640, 480)

    pipe = Polyhedron.from_OFF('volumes/beampipe.off')
    pipe.transform(translate=1, scale=1e-3)

    shield = Polyhedron.from_OFF('volumes/shield.off')
    shield.transform(translate=3, scale=1e-3)

    polyline = AnimatedPolyLine([(0,0,0), (0,5,0), (2,2,0), (0,2,2), (2,2,7)])

    animation.add_object(pipe, opacity=0.5)
    animation.add_animated_object(shield, transform_shield, color=(0,0,1))
    animation.add_object(polyline, color=(1,0,0))

    animation.run(delay=300)


if __name__ == '__main__':
    run_animation()

