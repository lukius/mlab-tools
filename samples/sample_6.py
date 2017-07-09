import random
import sys
sys.path.append('../')

from mlab_tools.animation import Animation, StopAnimation
from mlab_tools.primitive import Cube


def rand_color():
    return (random.random(), random.random(), random.random())

def animate_obj(obj, frame_no):
    obj.transform(rotate=(1,1,1))

def frame_callback(frame_no, animation):
    if frame_no == 1:
        cube = Cube(length=10)
        animation.add_object(cube, color=(1,1,1), opacity=0.1)
    
    elif frame_no < 20:
        cube = Cube(length=random.random())
        offset = lambda: random.random() + random.randint(-3,3)
        cube.transform(translate=(offset(), offset(), offset()))
        color = rand_color()
        
        rot = random.randint(-5,5)
        animation.add_animated_object(cube,
                                      lambda obj, frame_no: obj.transform(rotate=rot),
                                      color=color)
        
    elif frame_no > 50: StopAnimation()

def run_animation():
    animation = Animation(800, 600)
    animation.run(frame_callback=frame_callback, delay=200)


if __name__ == '__main__':
    run_animation()

