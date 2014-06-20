# coding=UTF-8

"""
Pasta
******

API for paths.

Biblioteca de gerenciamento de paths.
Mais informações sobre esta biblioteca podem ser encontradas em
https://github.com/phillipecavalcante/pasta.
"""

try:
    import os
except ImportError:
    raise

def join(path_a, path_b):
    return os.path.join(path_a, path_b)
    
class Path(object):
    
    def __init__(self, path, path_type):
        
        if not os.path.isabs(path):
            raise FilePathException("Path is not a absolute path.")
        
        self.path = path
        self.dir_path = os.path.split(self.path)[0]
        self.path_type = path_type
        
    def __repr__(self):
        return "<%s: '%s'>" % (self.__class__.__name__, self.path)
    
    def __str__(self):
        return self.path
    
class FilePath(Path):
    
    def __init__(self, path):
    
        if not os.path.isfile(path):
            raise FilePathException("Path is not a file path.")
        
        super(FilePath, self).__init__(path, "file")
        
        self.__setup()
        
    def __setup(self):
        
        self.extension = os.path.splitext(self.path)[1].replace(".", "")
        self.fullname = os.path.split(self.path)[1]
        self.name = self.fullname.split(".")[0]

class DirPath(Path):
    
    def __init__(self, path):
        
        if not os.path.isdir(path):
            raise DirPathException("Path is not a directory path.")
        
        super(DirPath, self).__init__(path, "dir")
        self.name = os.path.basename(self.path)
        
    def files(self):
        return [FilePath(join(self.path, f)) for f in os.listdir(self.path) if os.path.isfile(join(self.path, f))]
    
    def dirs(self):
        return [DirPath(join(self.path, d)) for d in os.listdir(self.path) if os.path.isdir(join(self.path, d))]
        
    def filter(self, exts):
        return [f for f in self.files() if f.extension in exts]
    
    def create_inside(self, dirname):
        os.mkdir(join(self.path, dirname))
    
    def create_beside(self, dirname):
        os.mkdir(join(self.dir_path, dirname))
    

class FilePathException(Exception):
    pass

class DirPathException(Exception):
    pass