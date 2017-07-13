from mayavi import mlab


class Camera(object):
    
    """Class that wraps some of the mlab functions that manipulate the camera.
    A camera instance is automatically created by the animation.
    """
    
    def __init__(self, focalpoint=None, distance=None,
                 azimuth=None, elevation=None, roll=None):
        self.focalpoint = focalpoint or 'auto'
        self.distance = distance or 'auto'
        self.azimuth = azimuth or 0
        self.elevation = elevation or 0
        self.roll = roll or 0
        self._set_view()
        if self.distance == 'auto':
            _, _, self.distance, self.focalpoint = mlab.view()
        
    def _set_view(self):
        # Sets current camera state into the animation.
        mlab.view(azimuth=self.azimuth,
                  elevation=self.elevation,
                  distance=self.distance,
                  focalpoint=self.focalpoint,
                  roll=self.roll)
        
    def parameters(self):
        """Get current camera parameters.
        Returns a dictionary associating each parameter name (i.e., `azimuth`,
        `focalpoint`, `distance`, `elevation` and `roll`) to its current value.
        """
        self.azimuth, self.elevation, self.distance, self.focalpoint = mlab.view()
        self.roll = mlab.roll()

        return {'focalpoint' : self.focalpoint,
                'distance' : self.distance,
                'azimuth' : self.azimuth,
                'elevation' : self.elevation,
                'roll' : self.roll}
        
    def update(self, focalpoint=None, distance=None,
               azimuth=None, elevation=None, roll=None):
        """Updates the camera.
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
        self.focalpoint = focalpoint or self.focalpoint
        self.distance = self.distance + (distance or 0)
        self.azimuth = self.azimuth + (azimuth or 0)
        self.elevation = self.elevation + (elevation or 0)
        self.roll = self.roll + (roll or 0)
        self._set_view()