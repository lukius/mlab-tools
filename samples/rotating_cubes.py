import random
import sys
sys.path.append('../')

from mlab_tools.animation import Animation, StopAnimation
from mlab_tools.primitive import Cube


class RotatingCubes(Animation):

    def rand_color(self):
        return (random.random(), random.random(), random.random())
    
    def initialize(self):
        self.update_camera(distance=30)
    
    def on_frame(self, frame_no):
        self.update_camera(distance=0.1, elevation=5)
        
        if frame_no == 1:
            cube = Cube(length=10)
            self.add_object(cube, color=(1,1,1), opacity=0.1)
        
        elif frame_no < 20:
            cube = Cube(length=random.random())
            offset = lambda: random.random() + random.randint(-3,3)
            cube.transform(translate=(offset(), offset(), offset()))
            color = self.rand_color()
            
            rot = random.randint(-5,5)
            self.add_animated_object(cube,
                                     lambda obj, frame_no: obj.transform(rotate=rot),
                                     color=color)
            
        elif frame_no > 50: StopAnimation()


def run_animation():
    animation = RotatingCubes(800, 600)
    animation.run(delay=200)


if __name__ == '__main__':
    run_animation()

