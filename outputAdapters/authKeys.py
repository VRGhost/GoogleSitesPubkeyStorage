import os
import subprocess
import tempfile

from . import base

class AuthorizedKeys(base.Base):

    def __init__(self, output_file):
        self._outFname = output_file

    def writeKeys(self, keys):
        _fname = os.path.expanduser(self._outFname)

        _fobj = open(_fname, "wb")
        _fobj.write("\n".join(keys))
        _fobj.close()

    def __repr__(self):
        return "<{0} file={1!r}>".format(self.__class__.__name__, self._outFname)

class AuthorizedKeysShell(base.Base):
    def __init__(self, command):
        self._command = command

    def writeKeys(self, keys):
        with tempfile.NamedTemporaryFile() as _fobj:
            _fobj.write("\n".join(keys))
            _fobj.flush()
            assert os.path.isfile(_fobj.name)
            _cmd = self._command.format(SRC_FILE=_fobj.name)
            print repr(_cmd)
            subprocess.check_call(_cmd, shell=True)

    def __repr__(self):
        return "<{0} file={1!r}>".format(self.__class__.__name__, self._outFname)

# vim: set sts=4 sw=4 et :
