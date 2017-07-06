import sys
sys.path.append('../')

from mlab_tools.animation import Animation, StopAnimation
from mlab_tools.polyhedron import Polyhedron
from mlab_tools.polyline import AnimatedPolyLine


def run_animation():
    animation = Animation(640, 480)

    polyhedron = Polyhedron.from_OFF('volumes/beampipe.off')
    polyhedron.transform(translate=1, scale=1e-3)

    polyline = AnimatedPolyLine([(0,0,0), (0,5,0), (2,2,0), (0,2,2), (2,2,7)])

    animation.add_object(polyhedron, opacity=0.5)
    animation.add_object(polyline, color=(1,0,0))

    animation.run(delay=300)


if __name__ == '__main__':
    run_animation()

