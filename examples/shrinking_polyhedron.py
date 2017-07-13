import sys
sys.path.append('../')

from mlab_tools.animation import Animation, StopAnimation
from mlab_tools.polyhedron import Polyhedron


class ShrinkingPolyhedron(Animation):
    
    """Basic animation that shrinks a polyhedron by 20% on each frame."""
    
    def animate_polyhedron(self, polyhedron, frame_no):
        polyhedron.transform(scale=0.8)
        if frame_no > 10: StopAnimation()
    
    def initialize(self):
        polyhedron = Polyhedron.from_OFF('volumes/beampipe.off')
        polyhedron.transform(translate=1, scale=1e-3, rotate=20)
    
        self.add_animated_object(polyhedron, self.animate_polyhedron, opacity=0.5)


def run_animation():
    animation = ShrinkingPolyhedron(640, 480)
    animation.run(delay=300)


if __name__ == '__main__':
    run_animation()

