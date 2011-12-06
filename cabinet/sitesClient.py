import gdata.sites.data
import gdata.sites.client
import gdata.sample_util

class Client(object):

    def __init__(self, client):
        self._client = client

    @classmethod
    def fromSiteDomain(cls, site, domain, **kw):
        return cls(gdata.sites.client.SitesClient(site=site, domain=domain), **kw)

    def getFeed(self, **props):
        _cl = self._client
        _tail = "&".join("{0}={1}".format(*_el) for _el in props.items())
        _uri = "{0}?{1}".format(_cl.MakeContentFeedUri(), _tail)
        return _cl.GetContentFeed(uri=_uri)

# vim: set sts=4 sw=4 et :
