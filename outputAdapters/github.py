import lib.github3 as github3

from . import base

class GitHub(base.Base):

    def __init__(self, output_auth_record):
        self._userRecord = output_auth_record

    def writeKeys(self, keys):
        _myKeys = []
        for _key in keys:
            (_key, _name) = _key.rsplit(" ", 1)
            _myKeys.append({"name": _name.strip(), "key": _key.strip()})

        (_login, _pass) = self.getUserPass(self._userRecord)
        _hub = github3.api.Github(_login, _pass)
        _myUser = _hub.users

        _hubKeys = tuple(_myUser.get_keys())

        for _hubKey in _hubKeys:
            if _hubKey.key not in (_el["key"] for _el in _myKeys):
                _myUser.delete_key(_hubKey.id)

        for _myKey in _myKeys:
            if _myKey["key"] not in (_el.key for _el in _hubKeys):
                _myUser.create_key(
                    key = _myKey["key"],
                    title = _myKey["name"],
                )

# vim: set sts=4 sw=4 et :
