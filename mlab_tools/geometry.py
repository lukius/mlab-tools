from collections import OrderedDict


class Geometry(object):

    def __init__(self):
        self.polys_by_id = OrderedDict()
        self.polys_by_name = dict()
        
    def add_named_polyhedron(self, poly, name, pid):
        if name in self.polys_by_name:
            raise Exception('Polyhedron {} already registered!'.format(name))
        if pid in self.polys_by_id:
            raise Exception('Polyhedron ID {} already exists!'.format(pid))
        
        self.polys_by_name[name] = poly
        self.polys_by_id[pid] = poly
        
    def get_polyhedron(self, name):
        return self.polys_by_name.get(name)
    
    def get_polyhedron_by_ID(self, pid):
        return self.polys_by_id.get(pid)
    
    def num_polyhedrons(self):
        return len(self.polys_by_id)
    
    def __iter__(self):
        return self.polys_by_id.iteritems()
    
    
class GeometryParser(object):
    
    @classmethod
    def from_VTK(cls, filename):
        from vtk_parser import VTKParser
        return VTKParser(filename)
    
    def __init__(self, filename):
        self.filename = filename
        self.current_id = 1
    
    def parse(self):
        raise NotImplementedError
    
    
