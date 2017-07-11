import random
import sys
sys.path.append('../')

from mlab_tools.animation import Animation, Stop, StopAnimation
from mlab_tools.polyhedron import Polyhedron
from mlab_tools.polyline import AnimatedPolyLine


class PolyhedronAndLines(Animation):

    def rand_color(self):
        return (random.random(), random.random(), random.random())
    
    def animate_shield(self, shield, frame_no):
        shield.transform(rotate=frame_no, translate=(0,0,0.1))
        shield.update_properties(color=self.rand_color())
        if frame_no > 20: Stop()
        
    def initialize(self):
        self.lines = list()
        
        shield = Polyhedron.from_OFF('volumes/shield.off')
        shield.transform(scale=1e-2)
    
        self.add_animated_object(shield, self.animate_shield, color=(0,0,1))
    
    def on_frame(self, frame_no):
        def rand():
            return random.randint(-3,3)
    
        if frame_no <= 10:
            rand_points = [(rand(), rand(), rand()) for _ in xrange(10)]
            polyline = AnimatedPolyLine(rand_points, initial_frame=frame_no)
            self.add_object(polyline, color=self.rand_color())
            self.lines.append(polyline)
    
        if frame_no == 7:
            for line_no in xrange(7):
                self.remove_object(self.lines[line_no])
    
        if frame_no > 20: StopAnimation()


def run_animation():
    animation = PolyhedronAndLines(640, 480)
    animation.run(delay=500)


if __name__ == '__main__':
    run_animation()

