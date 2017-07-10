from mayavi import mlab


class Camera(object):
    
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
        mlab.view(azimuth=self.azimuth,
                  elevation=self.elevation,
                  distance=self.distance,
                  focalpoint=self.focalpoint,
                  roll=self.roll)
        
    def parameters(self):
        self.azimuth, self.elevation, self.distance, self.focalpoint = mlab.view()
        self.roll = mlab.roll()

        return {'focalpoint' : self.focalpoint,
                'distance' : self.distance,
                'azimuth' : self.azimuth,
                'elevation' : self.elevation,
                'roll' : self.roll}
        
    def update(self, focalpoint=None, distance=None,
               azimuth=None, elevation=None, roll=None):
        self.focalpoint = focalpoint or self.focalpoint
        self.distance = self.distance + (distance or 0)
        self.azimuth = self.azimuth + (azimuth or 0)
        self.elevation = self.elevation + (elevation or 0)
        self.roll = self.roll + (roll or 0)
        self._set_view()