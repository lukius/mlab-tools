import glob
import os
import random
import shutil

from mayavi import mlab
from tvtk.api import tvtk
from tvtk.tools import visual

try:
    import cv2
except ImportError:
    cv2 = None

from camera import Camera


class AnimationException(Exception):

    def __init__(self):
        raise self

class StopAnimation(AnimationException):
    
    """Stop the animation.
    Can be instanciated inside any animator callback to immediately end the
    animation.
    """

    pass

class Stop(AnimationException):
    
    """Stop the current animator.
    Note that this will not terminate the animation (see StopAnimation).
    """

    pass

class StopAndRemove(AnimationException):
    
    """Stop the current animator and remove the current object from the scene.
    Note that this will not terminate the animation (see StopAnimation).
    """

    pass



class Animation(object):
    
    """Base class for custom animations.
    An animation is a sequence of frames, which in turn consist of objects.
    Objects can be added to or removed from the scene at any point of the
    animation. When adding an object, an associated animator can be supplied.
    This animator, which defines the behavior of the object along the
    animation, will be automatically called for each frame. If no animator is
    provided, a default animator that (typically) leaves the object still
    will be chosen. Also, a frame callback controlling the global behavior of
    the animation will be called frame after frame.
    """

    def __init__(self, width, height, bgcolor=None):
        figure = mlab.figure(size=(width, height), bgcolor=bgcolor)
        visual.set_viewer(figure)
        
        self.width = width
        self.height = height
        
        self.camera = Camera()
        
        self.frame_callbacks = [self.on_frame]
        self.obj_animations = dict()

    def _add_actor(self, actor):
        viewer = visual.get_viewer()
        # Avoiding mlab.add_actor since it resets the zoom.
        viewer.scene.add_actors(actor)

    def _remove_actor(self, actor):
        viewer = visual.get_viewer()
        viewer.scene.remove_actors(actor)
        
    def get_camera(self):
        return self.camera
        
    def update_camera(self, focalpoint=None, distance=None,
                      azimuth=None, elevation=None, roll=None):
        """Updates the animation camera.
        Parameters are additive (e.g., if distance=d is supplied, the camera
        will have an increase of d in its distance after this call).
        
        Keyword arguments:
        
        :azimuth: the azimuthal angle (in degrees, 0-360), i.e. the angle
        subtended by the position vector on a sphere projected on to the x-y
        plane with the x-axis.
        
        :distance: a positive floating point number representing the distance
        from the focal point to place the camera.
        
        :elevation: the zenith angle (in degrees, 0-180), i.e. the angle
        subtended by the position vector and the z-axis.
        
        :focalpoint: an array of 3 floating point numbers representing the
        focal point of the camera. 
        
        :roll: the rotation of the camera around its axis.
        
        See mlab documentation for further details.
        """
        self.camera.update(focalpoint=focalpoint,
                           distance=distance,
                           azimuth=azimuth,
                           elevation=elevation,
                           roll=roll)

    def add_object(self, obj, **props):
        """Adds an object to the scene (using its default animator).
        
        Arguments:
        
        :obj: an instance of object.Object.
        
        :props: keyword arguments specifying the object properties, such as
        color, opacity, etc. See VTK documentation for futher details.
        """
        default_animator = obj.default_animator()
        self.add_animated_object(obj, default_animator, **props)

    def add_animated_object(self, obj, anim, **props):
        """Adds an object to the scene with an user-supplied animator.
        
        Arguments:
        
        :obj: an instance of object.Object.
        
        :anim: the animator that defines the behavior of this object during the
        animation. It should be a callable Python object expecting two
        arguments: an object (which will be `obj`) and a frame number. Note that
        the same animator can be reused for multiple objects.
        
        :props: keyword arguments specifying the object properties, such as
        color, opacity, etc. See VTK documentation for futher details.
        """        
        obj.update_properties(**props)

        self._add_actor(obj.get_actor())

        self.obj_animations[obj] = anim

    def remove_object(self, obj):
        """Removes an object from the scene.
        
        Arguments:
        
        :obj: an instance of object.Object.
        """
        if obj in self.obj_animations:
            del self.obj_animations[obj]
        self._remove_actor(obj.get_actor())
        
    def _get_image_resolution(self, tmp_dir, filename):
        img = cv2.imread('%s/%s_1.png' % (tmp_dir, filename))
        height, width, _ = img.shape
        return height, width

    def _assemble_video(self, directory, filename, tmp_dir, framerate):
        # Compiles the saved PNG frames into a video using the OpenCV library.
        # TODO: add support for OpenCV 3.0.
        if cv2 is None:
            raise RuntimeError('OpenCV not found! Video cannot be saved.')
        
        height, width = self._get_image_resolution(tmp_dir, filename)
        video = cv2.VideoWriter('%s/%s.avi' % (directory, filename),
                                cv2.cv.CV_FOURCC(*'XVID'),
                                framerate,
                                (width, height))

        frames = glob.glob('%s/*.png' % tmp_dir)

        for i in xrange(1, len(frames)+1):
            frame_filename = '%s/%s_%d.png' % (tmp_dir, filename, i)
            frame_img = cv2.imread(frame_filename)
            
            frame_height, frame_width, _ = frame_img.shape
            if frame_height != height or frame_width != width:
                msg = 'Frame %s has invalid resolution!' % frame_filename
                raise RuntimeError(msg)
            
            video.write(frame_img)

        video.release()

    def _render_frame(self, frame_no, frame_name):
        # Frame rendering method called during the animation loop.
        
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
        """Runs the animation.
        For each object in the scene, the associated animators are called in
        sequence with an increasing number that identifies the current frame.
        Then, the global frame callback is invoked. This animation loop ends
        whenever StopAnimation is raised or otherwise if no custom global
        frame callback is defined and every added object is stopped.
        
        A video of the animation can be optionally saved. In order to use this
        functionality, the Python bindings for OpenCV have to be installed.
        
        Keyword arguments:
        
        :delay: time interval in milliseconds between calls to the frame
        rendering loop (default: 30).
        
        :save_to: name to use for the video file of the animation (defaults to
        None, meaning that the video will not be saved).
        
        :framerate: framerate of the video (only valid is `save_to` is
        provided).
        """

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
        """Initialization method that is called before running the animation.
        Typically used for setting up the scene and the initial objects to be
        rendered.
        """
        pass

    def on_frame(self, frame_no):
        """Frame callback to control the global behavior of the animation. By
        default, it raises a Stop (which implies that the callback will no 
        longer be used after the first frame).
        
        Arguments:
        
        :frame_no: current frame number.
        """
        Stop()