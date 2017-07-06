from mayavi import mlab
from tvtk.api import tvtk
from tvtk.tools import visual


class StopAnimation(Exception):

    pass


class Animation(object):

    def __init__(self, width, height):
        figure = mlab.figure(size=(width, height))
        visual.set_viewer(figure)
        self.obj_animations = dict()

    def _add_actor(self, actor):
        viewer = visual.get_viewer()
        viewer.scene.add_actors(actor)

    def add_object(self, obj, **props):
        default_animation = obj.default_animation()
        self.add_animated_object(obj, default_animation, **props)

    def add_animated_object(self, obj, anim, **props):
        actor = obj.get_actor()

        properties = tvtk.Property(**props)
        actor.property = properties
        actor.mapper.update()

        self._add_actor(actor)

        self.obj_animations[obj] = anim

    def run(self, frame_callback=None, delay=30):
        @mlab.show
        @mlab.animate(delay=delay)
        def _run():
            frame_no = 1

            while True:

                should_stop = True

                for obj, anim in self.obj_animations.items():
                    if anim(obj, frame_no):
                        del self.obj_animations[obj]
                    else:
                        should_stop = False
                    self._add_actor(obj.get_actor())

                if frame_callback is not None:
                    try:
                        frame_callback(frame_no)
                    except StopAnimation:
                        should_stop = True

                if should_stop:
                    break

                frame_no += 1

                yield

        _run()
        

