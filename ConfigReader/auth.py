import json

class Auth(object):

    def __init__(self, fname):
        self.fname = fname

    def _readRecord(self, name):
        _fp = open(self.fname, "rb")
        try:
            _data = json.load(_fp)
            return _data[name]
        finally:
            _fp.close()

    def getAuthRecord(self, name):
        _rec = self._readRecord(name)
        if "password_rot13" in _rec:
            assert "password" not in _rec, "You can ether pass password in plain text (field 'password' or in 'rot13' encryption. But not both"
            _r13 = _rec.pop("password_rot13")
            _rec["password"] = _r13.decode("rot13")
        return _rec

    def __repr__(self):
        return "<{0} file={1!r}>".format(self.__class__.__name__, self.fname)

# vim: set sts=4 sw=4 et :
