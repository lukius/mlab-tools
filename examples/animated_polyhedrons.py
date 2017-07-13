import random
import sys
sys.path.append('../')

from mlab_tools.animation import Animation, Stop, StopAndRemove
from mlab_tools.polyhedron import Polyhedron


class TwoPolyhedrons(Animation):
    
    """Basic animation that moves two OFF-based polyhedrons."""
    
    def animate_shield(self, shield, frame_no):
        shield.transform(rotate=frame_no, translate=(0,0,0.1))
        new_color = (random.random(), random.random(), random.random())
        shield.update_properties(color=new_color)
        if frame_no > 15: Stop()
        
    def animate_pipe(self, pipe, frame_no):
        pipe.transform(scale=1.1)
        if frame_no > 10: StopAndRemove()

    def initialize(self):
        # The animation is set up here. Note that no frame callback is defined
        # as the on_frame method is not overriden. This means that the
        # animation flow is completely controlled by the two animators of 
        # the polyhedrons.
        pipe = Polyhedron.from_OFF('volumes/beampipe.off')
        pipe.transform(translate=1, scale=1e-3)
    
        shield = Polyhedron.from_OFF('volumes/shield.off')
        shield.transform(translate=3, scale=1e-3)
    
        self.add_animated_object(pipe, self.animate_pipe, opacity=0.5)
        self.add_animated_object(shield, self.animate_shield, color=(0,0,1))
    

def run_animation():
    animation = TwoPolyhedrons(640, 480)
    # The animation will also be saved to a video named 'polyhedrons.avi' and
    # will feature two frames per second.
    animation.run(delay=300, save_to='polyhedrons', framerate=2)


if __name__ == '__main__':
    run_animation()

