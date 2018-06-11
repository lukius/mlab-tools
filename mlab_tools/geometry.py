import re

from polyhedron import Polyhedron

from tvtk.api import tvtk


class Geometry(object):

    def __init__(self):
        self.polys = dict()
        
    def add_named_polyhedron(self, poly, name):
        if name in self.polys:
            raise Exception('Polyhedron {} already registered!'.format(name))
        self.polys[name] = poly
        
    def get_polyhedron(self, name):
        return self.polys.get(name)
    
    def __iter__(self):
        return self.polys.iteritems()
    
    
class GeometryParser(object):
    
    @classmethod
    def from_VTK(cls, filename):
        return VTKParser(filename)
    
    def __init__(self, filename):
        self.filename = filename
    
    def parse(self):
        raise NotImplementedError
    
    
class VTKParser(GeometryParser):
    
    def _build_geometry(self, points, cells):
        geometry = Geometry()
        
        for cell in cells:
            cell_points = tvtk.Points()
            faces = tvtk.CellArray()           
            
            vertex0 = points[cell[0]]
            vertex1 = points[cell[1]]
            vertex2 = points[cell[2]]
            vertex3 = points[cell[3]]
            
            cell_points.insert_next_point(vertex0)
            cell_points.insert_next_point(vertex1)
            cell_points.insert_next_point(vertex2)
            cell_points.insert_next_point(vertex3)
            
            polygon = tvtk.Polygon()
            polygon.point_ids.number_of_ids = 3
            polygon.point_ids.set_id(0, 0)
            polygon.point_ids.set_id(1, 1)
            polygon.point_ids.set_id(2, 2)          
            faces.insert_next_cell(polygon)
              
            polygon = tvtk.Polygon()
            polygon.point_ids.number_of_ids = 3
            polygon.point_ids.set_id(0, 0)
            polygon.point_ids.set_id(1, 3)
            polygon.point_ids.set_id(2, 1)          
            faces.insert_next_cell(polygon)
              
            polygon = tvtk.Polygon()
            polygon.point_ids.number_of_ids = 3
            polygon.point_ids.set_id(0, 0)
            polygon.point_ids.set_id(1, 2)
            polygon.point_ids.set_id(2, 3)          
            faces.insert_next_cell(polygon)
              
            polygon = tvtk.Polygon()
            polygon.point_ids.number_of_ids = 3
            polygon.point_ids.set_id(0, 1)
            polygon.point_ids.set_id(1, 3)
            polygon.point_ids.set_id(2, 2)          
            faces.insert_next_cell(polygon)
            
            polyhedron = Polyhedron(cell_points, faces)
            name = 'Tetra-{}-{}-{}-{}'.format(*cell)
            
            geometry.add_named_polyhedron(polyhedron, name)
        
        return geometry
    
    def parse(self):
        points = list()
        cells = list()
        
        point_regexp = 'POINTS\s+(\d+)\s+([a-zA-Z]+)'
        cell_regexp = 'CELLS\s+(\d+)'
        cell_types_regexp = 'CELL_TYPES\s+(\d+)'

        with open(self.filename, 'r') as _file:
            lines = _file.readlines()
            
            i = k = 0
            n_points = n_cells = 0
            
            for line in lines:
                line = line.strip()
                
                if i == 0:
                    if line != '# vtk DataFile Version 2.0':
                        raise Exception('Wrong format!')
                    i += 1
                    continue
                    
                if not line or line[0] == '#':
                    k += 1
                    continue
                
                if i == 2:
                    if line != 'ASCII':
                        raise Exception('Binary input not supported!')
                    
                if i == 3:
                    if line != 'DATASET UNSTRUCTURED_GRID':
                        raise Exception('VTK dataset must be unstructured grid!')
                    
                if i == 4:
                    match = re.match(point_regexp, line)
                    
                    if match is None:
                        raise Exception('Line {}: wrong point declaration format!'.format(i+k))
                    
                    n_points, _ = match.groups()
                    
                    try:
                        n_points = int(n_points)
                    except Exception:
                        raise Exception('Line {}: wrong number of points!'.format(i+k))
                    
                if i >= 5 and len(points) < n_points:
                    try:
                        values = map(float, line.split())
                    except Exception:
                        raise Exception('Line {}: invalid point coordinates!'.format(i+k))
                        
                    points.append(tuple(values))
                    
                if i == n_points+5:
                    match = re.match(cell_regexp, line)
                    
                    if match is None:
                        raise Exception('Line {}: wrong cell declaration format!'.format(i+k))
                    
                    n_cells = match.groups()[0]
                    
                    try:
                        n_cells = int(n_cells)
                    except Exception:
                        raise Exception('Line {}: wrong number of cells!'.format(i+k))
                    
                if i > n_points+5 and len(cells) < n_cells:
                    match = re.findall('\d+', line)
                    
                    if len(match) == 0:
                        raise Exception('Line {}: wrong cell format!'.format(i+k))
                    
                    n_points_in_cell = int(match[0])
                    
                    if len(match) != 1+n_points_in_cell:
                        raise Exception('Line {}: wrong cell format!'.format(i+k))
                    
                    cell = tuple(map(int, match[1:]))
                    
                    cells.append(cell)
                    
                if i == n_points+n_cells+6:
                    match = re.match(cell_types_regexp, line)
                    
                    if match is None:
                        raise Exception('Line {}: wrong cell types declaration format!'.format(i+k))
                    
                if i > n_points+n_cells+6:
                    match = re.findall('\d+', line)
                    
                    if len(match) == 0:
                        raise Exception('Line {}: wrong cell type format!'.format(i+k))
                    
                    if int(match[0]) != 10:
                        raise Exception('Line {}: only tetrahedral cell type (10) supported!'.format(i+k))
                    
                i += 1
                    
        return self._build_geometry(points, cells)