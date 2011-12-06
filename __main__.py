import os
import logging

# from .
import lib.autoEnv

ROOT_DIR = os.path.realpath(os.path.dirname(__file__))
VAR_DIR = os.path.join(ROOT_DIR, "var")
CFG_DIR = os.path.join(ROOT_DIR, "cfg")

logging.basicConfig()
_logger = logging.getLogger()
_logger.setLevel(logging.DEBUG)

def setupEnv():
    _dir = os.path.join(VAR_DIR, "env")
    _env =  lib.autoEnv.Bootstrap(_dir)
    _env.install("gdata")
    return _env

def get_cabinet_dump_fname(cabs):
    import hashlib

    _str = ""
    
    for _cab in cabs:
        _props = _cab.getPropDict()
        _keys = sorted(_props.keys())
        _str += "<[-.-]>".join(_props[_key] for _key in _keys)

    _fname = "{0}.cab.dump.json".format(hashlib.md5(_str).hexdigest())

    return os.path.join(VAR_DIR, _fname)

def get_file_props(cabs):
    _out = []
    for _cab in cabs:
        _out.extend(_el.getPropDict() for _el in _cab.ls())
    return _out

def files_updated(cabs):
    import json

    _fname = get_cabinet_dump_fname(cabs)
    
    if os.path.exists(_fname):
        _prevVal = json.load(open(_fname))
    else:
        _prevVal = None

    return _prevVal != get_file_props(cabs)

def save_cab_status(cabs):
    import json

    _fname = get_cabinet_dump_fname(cabs)
    json.dump(get_file_props(cabs), open(_fname, "wb"))

def collect_keys(cabinets):
    _out = []
    for _cab in cabinets:
        for _rec in _cab.ls():
            _contents = _rec.getContents().strip()
            assert len(_contents.split()) == 3, "id_rsa.pub has to contain three strings separated by spaces"
            _out.append(_contents)
    return _out

def sync_keys(outputCfg, cabinets):
    _keys = tuple(collect_keys(cabinets))

    for _outputRec in outputCfg:
        _outputObj = _outputRec.getOutputObject()
        _outputObj.writeKeys(_keys)

def run_program():
    import cfgProvider

    _generalCfg = cfgProvider.getGeneralCfg()

    _cabinets = _generalCfg["ssh-key-source-site"].getCabinets()
    if files_updated(_cabinets) or 1:
        sync_keys(_generalCfg.outputs, _cabinets)
        save_cab_status(_cabinets)

if __name__ == "__main__":
    setupEnv()
    run_program()

# vim: set sts=4 sw=4 et :
