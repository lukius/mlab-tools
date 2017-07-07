import glob
import os
import random
import shutil

from mayavi import mlab
from tvtk.api import tvtk
from tvtk.tools import visual


class StopAnimation(Exception):

    pass


class AnimatorException(Exception):

    def __init__(self):
        raise self


class Stop(AnimatorException):

    pass


class StopAndRemove(AnimatorException):

    pass


class Animation(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        figure = mlab.figure(size=(width, height))
        visual.set_viewer(figure)
        self.obj_animations = dict()

    def _add_actor(self, actor):
        viewer = visual.get_viewer()
        viewer.scene.add_actors(actor)

    def _remove_actor(self, actor):
        viewer = visual.get_viewer()
        viewer.scene.remove_actors(actor)

    def add_object(self, obj, **props):
        default_animation = obj.default_animation()
        self.add_animated_object(obj, default_animation, **props)

    def add_animated_object(self, obj, anim, **props):
        actor = obj.get_actor()

        obj.update_properties(**props)

        self._add_actor(actor)

        self.obj_animations[obj] = anim

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

    def _save_frame(self, tmp_dir, filename, frame_no):
        mlab.savefig('%s/%s_%d.png' % (tmp_dir, filename, frame_no))

    def run(self, frame_callback=None, delay=30, save_to=None, framerate=30):

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

        @mlab.animate(delay=delay, ui=False)
        def _run():
            frame_no = 1

            while True:
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

                if frame_callback is not None:
                    try:
                        frame_callback(frame_no)
                    except StopAnimation:
                        should_stop = True

                if save_to is not None:
                    self._save_frame(tmp_dir, filename, frame_no)

                if should_stop:
                    mlab.close(all=True)
                    break

                yield

                frame_no += 1

        _ = _run()
        mlab.show()

        if save_to is not None:
            self._assemble_video(directory, filename,
                                 tmp_dir,
                                 framerate)
            shutil.rmtree(tmp_dir)
