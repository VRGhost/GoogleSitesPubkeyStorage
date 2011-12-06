import urllib2

class Base(object):

    def getAuthCred(self, recordName):
        import cfgProvider
        _cfg = cfgProvider.getAuthCfg()
        return _cfg.getAuthRecord(recordName)

    def getUserPass(self, recordName):
        _rec = self.getAuthCred(recordName)
        return (_rec["username"], _rec["password"])

# vim: set sts=4 sw=4 et :
