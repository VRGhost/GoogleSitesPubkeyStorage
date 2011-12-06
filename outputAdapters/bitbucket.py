import lib.bitbucket as bitbucket

from . import base

class Bitbucket(base.Base):

    def __init__(self, output_auth_record):
        self._userRecord = output_auth_record

    def writeKeys(self, keys):
        (_login, _pass) = self.getUserPass(self._userRecord)
        _bb = bitbucket.api.BitBucket(_login, _pass)
        _bb_keys = _bb.ssh_keys

        _oldKeys = dict((_el["key"], _el["pk"]) for _el in _bb_keys.get())

        _allKeys = set(_oldKeys.keys())
        _allKeys.update(keys)

        for _key in _allKeys:
            if _key in _oldKeys and _key not in keys:
                _bb_keys.delete(_oldKeys[_key])
            elif _key in keys and _key not in _oldKeys:
                _bb_keys.add(_key)

# vim: set sts=4 sw=4 et :
