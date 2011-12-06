import os

from . import base

class AutorizedKeys(base.Base):

    def __init__(self, output_file):
        self._outFname = output_file

    def writeKeys(self, keys):
        _fname = os.path.expanduser(self._outFname)

        _fobj = open(_fname, "wb")
        _fobj.write("\n".join(keys))
        _fobj.close()

    def __repr__(self):
        return "<{0} file={1!r}>".format(self.__class__.__name__, self._outFname)

# vim: set sts=4 sw=4 et :
