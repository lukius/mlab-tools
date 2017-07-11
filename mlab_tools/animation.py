import glob
import os
import random
import shutil

from mayavi import mlab
from tvtk.api import tvtk
from tvtk.tools import visual

from camera import Camera


class AnimationException(Exception):

    def __init__(self):
        raise self

class StopAnimation(AnimationException):

    pass

class Stop(AnimationException):

    pass

class StopAndRemove(AnimationException):

    pass



class Animation(object):

    def __init__(self, width, height):
        figure = mlab.figure(size=(width, height))
        visual.set_viewer(figure)
        
        self.width = width
        self.height = height
        
        self.camera = Camera()
        
        self.frame_callbacks = [self.on_frame]
        self.obj_animations = dict()

    def _add_actor(self, actor):
        viewer = visual.get_viewer()
        viewer.scene.add_actors(actor)

    def _remove_actor(self, actor):
        viewer = visual.get_viewer()
        viewer.scene.remove_actors(actor)
        
    def get_camera(self):
        return self.camera
        
    def update_camera(self, focalpoint=None, distance=None,
                      azimuth=None, elevation=None, roll=None):
        self.camera.update(focalpoint=focalpoint,
                           distance=distance,
                           azimuth=azimuth,
                           elevation=elevation,
                           roll=roll)

    def add_object(self, obj, **props):
        default_animation = obj.default_animation()
        self.add_animated_object(obj, default_animation, **props)

    def add_animated_object(self, obj, anim, **props):
        actor = obj.get_actor()

        obj.update_properties(**props)

        self._add_actor(actor)

        self.obj_animations[obj] = anim

    def remove_object(self, obj):
        if obj in self.obj_animations:
            del self.obj_animations[obj]
        self._remove_actor(obj.get_actor())

    def _assemble_video(self, directory, filename, tmp_dir, framerate):
        import cv2

        video = cv2.VideoWriter('%s/%s.avi' % (directory, filename),
                                cv2.cv.CV_FOURCC(*'XVID'),
                                framerate,
                                (self.width, self.height - 50))

        frames = glob.glob('%s/*.png' % tmp_dir)

        for i in xrange(1, len(frames)+1):
            frame_img = cv2.imread('%s/%s_%d.png' % (tmp_dir, filename, i))
            video.write(frame_img)

        video.release()

    def _render_frame(self, frame_no, frame_name):
        should_stop = True

        for obj, anim in self.obj_animations.items():
            actor = obj.get_actor()

            try:
                anim(obj, frame_no)
            except (Stop, StopAndRemove) as action:
                del self.obj_animations[obj]
                if isinstance(action, StopAndRemove):
                    self._remove_actor(actor)
            else:
                should_stop = False
                self._add_actor(actor)

        for index, callback in enumerate(self.frame_callbacks):
            try:
                callback(frame_no)
            except Stop:
                del self.frame_callbacks[index]
            else:
                should_stop = False

        if frame_name:
            mlab.savefig('%s_%d.png' % (frame_name, frame_no))

        if should_stop:
            StopAnimation()

    def run(self, delay=30, save_to=None, framerate=30):

        frame_name = None

        if save_to is not None:
            try:
                import cv2
            except Exception:
                print 'Python bindings for OpenCV needed to save animations!'
                save_to = None
            else:
                directory, filename = os.path.split(save_to)
                if not directory:
                    directory = '.'
                tmp_dir = '%s/tmp_%d' % (directory, random.randint(1,10**6))
                os.mkdir(tmp_dir)

                frame_name = '%s/%s' % (tmp_dir, filename)

        @mlab.animate(delay=delay, ui=False)
        def _run():
            frame_no = 1

            while True:
                try:
                    self._render_frame(frame_no, frame_name)
                except StopAnimation:
                    mlab.close(all=True)
                    break

                yield

                frame_no += 1

        self.initialize()
        _ = _run()
        mlab.show()

        if save_to is not None:
            self._assemble_video(directory, filename,
                                 tmp_dir,
                                 framerate)
            shutil.rmtree(tmp_dir)

    def initialize(self):
        pass

    def on_frame(self, frame_no):
        Stop()