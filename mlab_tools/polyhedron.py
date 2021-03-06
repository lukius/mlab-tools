import re

from tvtk.api import tvtk

from object import PolyObject


class Polyhedron(PolyObject):
    
    """Class that represents arbitrary polyhedrons.
    
    Supports a subset of the OFF file format (basically, triangulated
    polyhedrons).
    """

    @classmethod
    def from_OFF(cls, filename):
        """Builds a `Polyhedron` instance from a given OFF file.
        
        Arguments:
        
        :filename: path to an OFF (Object File Format) file. Supports
        a basic subset of the format (polyhedrons with triangular faces).
        """
        faces, points = cls._parse_OFF(filename)
        return cls(points, faces)

    @classmethod
    def _parse_OFF(cls, filename):
        points = tvtk.Points()
        faces = tvtk.CellArray()

        n_read = False
        vertices_read = faces_read = 0

        fp_regexp = '(-?)(0[\.\d*]?|([1-9]\d*\.?\d*)|(\.\d+))([Ee][+-]?\d+)?'

        with open(filename, 'r') as _file:
            lines = _file.readlines()

            for i, line in enumerate(lines):
                line = line.strip()
    
                if i == 0 and line != 'OFF':
                    raise Exception('Wrong format!')
                elif i == 0:
                    continue

                if not line or line[0] == '#':
                    continue

                if n_read is False:
                    match = re.match('(\d+)\s+(\d+)\s+(\d+).*', line)

                    if match is None:
                        raise Exception('Wrong format!')

                    n_verts = int(match.groups()[0])
                    n_faces = int(match.groups()[1])

                    n_read = True

                    continue

                if vertices_read < n_verts:
                    match = re.findall(fp_regexp, line)

                    if not match:
                        raise Exception('Wrong format!')

                    x = float(match[0][1]) 
                    if match[0][0] == '-':
                        x = -x

                    y = float(match[1][1]) 
                    if match[1][0] == '-':
                        y = -y

                    z = float(match[2][1]) 
                    if match[2][0] == '-':
                        z = -z

                    points.insert_next_point((x,y,z))     
    
                    vertices_read += 1

                    continue   

                if faces_read < n_faces:
                    # TODO: add support for non-triangular faces.
                    match = re.match('(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*(\d+)?.*', line)

                    if match is None:
                        raise Exception('Wrong format!')

                    f_verts = int(match.groups()[0])
                    if f_verts not in [3,4]:
                        raise Exception('Faces should have three or four vertices!')
                    
                    vert0 = int(match.groups()[1])
                    vert1 = int(match.groups()[2])
                    vert2 = int(match.groups()[3])

                    polygon = tvtk.Polygon()
                    polygon.point_ids.number_of_ids = f_verts
                    polygon.point_ids.set_id(0, vert0)
                    polygon.point_ids.set_id(1, vert1)
                    polygon.point_ids.set_id(2, vert2)

                    if f_verts == 4:
                        vert3 = int(match.groups()[4])
                        polygon.point_ids.set_id(3, vert3)

                    faces.insert_next_cell(polygon)

                    faces_read += 1

                    continue

        return faces, points

    def __init__(self, points, faces):
        PolyObject.__init__(self)
        self.points = points
        self.faces = faces
        self._configure()

    def _configure(self):
        self.poly_data = tvtk.PolyData(points=self.points, polys=self.faces)
        self._set_actor()
