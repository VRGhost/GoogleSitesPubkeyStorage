from . import base

class SshKeySourceSite(base.BaseConfigReader):
    
    keyProto = {
        "site": {"constructor": str},
        "domain": {"constructor": str},
        "path": {"constructor": str},
    }

    def getCabinets(self):
        import cabinet
        return (
            cabinet.FileCabinet.fromSiteDomain(
                site=self.site,
                domain=self.domain,
                path=self.path,
            ),
        )

class OutputRecord(base.BaseConfigReader):

    keyProto = {
        "type": {"constructor": str},
    }

    def getOutputObject(self):
        import outputAdapters
        _classes = {
            "AuthorizedKeys": outputAdapters.AutorizedKeys,
            "Bitbucket": outputAdapters.Bitbucket,
        }

        _kw = dict(self._data)
        _type = _kw.pop("type")

        if _type in _classes:
            _cls = _classes[self.type]
            return _cls(**_kw)
        else:
            raise RuntimeError("Unknown output adapter type {0!r}.".format(self.type))

class KeyOutputs(base.ListConfigReader):

    keyProto = {"constructor": OutputRecord}

class General(base.BaseConfigReader):

    keyProto = {
        "ssh-key-source-site": {"constructor": SshKeySourceSite},
        "outputs": {"constructor": KeyOutputs},
    }


# vim: set sts=4 sw=4 et :
