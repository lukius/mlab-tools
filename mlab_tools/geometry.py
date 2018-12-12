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
            cell_type, cell = cell[0], cell[1:]           
                
            if cell_type == 10:
                poly, name = self._build_tetrahedron(cell, points)
            elif cell_type == 11:
                poly, name = self._build_voxel(cell, points)

            geometry.add_named_polyhedron(poly, name)
        
        return geometry
    
    def _get_cell_points(self, cell, points):
        cell_points = tvtk.Points()
        
        for idx in cell:
            vertex = points[idx]
            cell_points.insert_next_point(vertex)
            
        return cell_points
    
    def _build_tetrahedron(self, cell, points):
        faces = tvtk.CellArray()
        
        for i0,i1,i2 in [(0,1,2), (0,3,1), (0,2,3), (1,3,2)]:
            polygon = tvtk.Polygon()
            polygon.point_ids.number_of_ids = 3
            polygon.point_ids.set_id(0, i0)
            polygon.point_ids.set_id(1, i1)
            polygon.point_ids.set_id(2, i2)          
            faces.insert_next_cell(polygon)

        cell_points = self._get_cell_points(cell, points)
        
        poly = Polyhedron(cell_points, faces)
        name = 'Tetra-{}-{}-{}-{}'.format(*cell)
        
        return poly, name
        
    def _build_voxel(self, cell, points):
        faces = tvtk.CellArray()
        
        for i0,i1,i2,i3 in [(0,1,3,2), (1,3,7,5), (5,7,6,4), (4,0,2,6),
                            (6,2,3,7), (0,1,5,4)]:
            polygon = tvtk.Polygon()
            polygon.point_ids.number_of_ids = 4
            polygon.point_ids.set_id(0, i0)
            polygon.point_ids.set_id(1, i1)
            polygon.point_ids.set_id(2, i2)
            polygon.point_ids.set_id(3, i3)     
            faces.insert_next_cell(polygon)
        
        cell_points = self._get_cell_points(cell, points)
        
        poly = Polyhedron(cell_points, faces)
        name = 'Voxel-{}-{}-{}-{}-{}-{}-{}-{}'.format(*cell)
        
        return poly, name
    
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
                    
                    cell = list(map(int, match[1:]))
                    
                    cells.append(cell)
                    
                if i == n_points+n_cells+6:
                    match = re.match(cell_types_regexp, line)
                    
                    if match is None:
                        raise Exception('Line {}: wrong cell types declaration format!'.format(i+k))
                    
                if i > n_points+n_cells+6:
                    match = re.findall('\d+', line)
                    
                    if len(match) == 0:
                        raise Exception('Line {}: wrong cell type format!'.format(i+k))
                    
                    cell_type = int(match[0])
                    if cell_type not in [10,11]:
                        raise Exception('Line {}: only tetrahedral or voxel cell types (10,11) supported!'.format(i+k))
                    
                    cells[i-n_points-n_cells-7].insert(0, cell_type)
                    
                i += 1
                    
        return self._build_geometry(points, cells)