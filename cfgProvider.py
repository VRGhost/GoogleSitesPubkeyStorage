import os

import ConfigReader

ROOT_DIR = os.path.realpath(os.path.dirname(__file__))

def getCfgDir():
    return os.path.join(ROOT_DIR, "cfg")

def getCfgFname(fname):
    return os.path.join(getCfgDir(), fname)

def getGeneralCfg():
    return ConfigReader.General.loadFile(getCfgFname("general.json"))

def getAuthCfg():
    return ConfigReader.Auth(getCfgFname("auth.json"))

# vim: set sts=4 sw=4 et :
