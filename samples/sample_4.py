import random
import sys
sys.path.append('../')

from mlab_tools.animation import Animation, Stop, StopAnimation
from mlab_tools.polyhedron import Polyhedron
from mlab_tools.polyline import AnimatedPolyLine


lines = list()


def rand_color():
    return (random.random(), random.random(), random.random())

def animate_shield(shield, frame_no):
    shield.transform(rotate=frame_no, translate=(0,0,0.1))
    shield.update_properties(color=rand_color())
    if frame_no > 20: Stop()

def frame_callback(frame_no, animation):
    global lines

    def rand():
        return random.randint(-3,3)

    if frame_no <= 10:
        rand_points = [(rand(), rand(), rand()) for _ in xrange(10)]
        polyline = AnimatedPolyLine(rand_points, initial_frame=frame_no)
        animation.add_object(polyline, color=rand_color())
        lines.append(polyline)

    if frame_no == 7:
        for line_no in xrange(7):
            animation.remove_object(lines[line_no])

    if frame_no > 20: StopAnimation()

def run_animation():
    animation = Animation(640, 480)

    shield = Polyhedron.from_OFF('volumes/shield.off')
    shield.transform(scale=1e-2)

    animation.add_animated_object(shield, animate_shield, color=(0,0,1))

    animation.run(frame_callback=frame_callback, delay=500)


if __name__ == '__main__':
    run_animation()

