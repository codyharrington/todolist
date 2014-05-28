__author__ = 'cody'

class LocalBase(dict):
    """This LocalBase class is just a container for a JSON-decoded dict representing a database object. All the
    real storage stuff goes on behind the database REST API. Each local version of the database object will
    inherit from this class"""

    def __init__(self, data=None):
        super().__init__()
        if data is not None:
            super().update(data)



