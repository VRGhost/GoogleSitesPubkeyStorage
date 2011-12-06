import json

from collections import defaultdict

def _recursive_defaultdict():
    return defaultdict(_recursive_defaultdict)

def _recursive_dict(baseData):
    _out = _recursive_defaultdict()

    for (_key, _value) in baseData.items():
        if isinstance(_value, dict):
            _value = _recursive_dict(_value)
        _out[_key] = _value

    return _out

class KeyNotFound(KeyError):

    def __init__(self, key, path = ()):
        self.key = key
        self.path = tuple(path)

        _msg = "Key {0!r} not found".format(key)
        if self.path:
            _msg += " while accessing {0!r}".format(".".join(self.path))
        _msg += "."

        KeyError.__init__(self, _msg)

    @classmethod
    def encapsulate(cls, prevErr, extraPath):
        _newPath = (extraPath, ) + prevErr.path
        return cls(prevErr.key, _newPath)

class ConfigKey(object):

    def __init__(self, key, constructor, required=True):
        self.key = key
        self.required = required
        self.constructor = constructor


class BaseConfigReader(object):

    _data = None

    parent = None

    keyProto = {
        # List of config key prototypes
    }

    def __init__(self, data):
        self._data =  _recursive_dict(data)
        for (_key, _value) in self.keyProto.items():
            self._valueToFieldDict(_key, _value)

    def _valueToFieldDict(self, key, value):
        _data = self._data

        _cfgKey = ConfigKey(key=key, **value)
        _key = _cfgKey.key
        _constructor = _cfgKey.constructor
        if _key not in _data:
            if _cfgKey.required:
                raise KeyNotFound(_key)
            _newValueFn = lambda: _constructor(parent=self)
        else:
            _newValueFn = lambda: _constructor(_data[_key])
        try:
            _data[_key] = _newValueFn()
        except KeyNotFound, _err:
            raise KeyNotFound.encapsulate(_err, _key)

    def __getitem__(self, name):
        try:
            return self._data[name]
        except KeyNotFound, _err:
            raise KeyNotFound.encapsulate(_err, name)
    
    def __getattr__(self, name):
        return self[name]

    @classmethod
    def load(cls, fobj):
        return cls(json.load(fobj))

    @classmethod
    def loadFile(cls, fname):
        return cls.load(open(fname))

    def __iter__(self):
        _keys = sorted(self._data.keys())
        for _el in _keys:
            yield self._data[_el]

    def __repr__(self):
        return "<{0}: {1!r}>".format(self.__class__.__name__, self._data)

class ListConfigReader(BaseConfigReader):

    def __init__(self, data):
        assert isinstance(data, list), "List expected"
        
        self._data = dict(_el for _el in enumerate(data))

        for (_id, _el) in enumerate(data):
            self._valueToFieldDict(_id, self.keyProto.copy())

    def __repr__(self):
        return "<{0}: {1!r}>".format(self.__class__.__name__, list(self))

# vim: set sts=4 sw=4 et :
