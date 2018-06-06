import sys
sys.path.append('../')

from mlab_tools.animation import Animation, StopAnimation
from mlab_tools.geometry import GeometryParser


class SphereMeshAnimation(Animation):
    
    """This example shows how to use a VTK geometry file to render a 3D polyhedron mesh."""
    
    def initialize(self):
        parser = GeometryParser.from_VTK('data/sphere.vtk')
        polyhedrons = parser.parse()
        
        for polyhedron in polyhedrons:
            self.add_object(polyhedron, opacity=0.5, color=(0.8,0,0.1))
            
    def on_frame(self, frame_no):
        if frame_no > 400: StopAnimation()


def run_animation():
    animation = SphereMeshAnimation(300, 200)
    animation.run(delay=50)


if __name__ == '__main__':
    run_animation()

