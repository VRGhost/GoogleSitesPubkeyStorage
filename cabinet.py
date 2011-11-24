import os

# from .
import sitesClient

def _print(el):
    for _el in dir(el):
        if _el.startswith("_"):
            continue
        _rv = getattr(el, _el)
        try:
            if callable(_rv):
                _rv = "()->{0}".format(_rv())
        except:
            pass
        print "{0}: {1!r}".format(_el, _rv)

class FileAuthor(sitesClient.Client):

    name = property(lambda s: s._rec.name.text)
    email = property(lambda s: s._rec.email.text)

    def __init__(self, client, record):
        super(FileAuthor, self).__init__(client)
        self._rec = record

    def __repr__(self):
        return "<{0} name={1!r} email={2!r}>".format(self.__class__.__name__, self.name, self.email)

class FileAttachment(sitesClient.Client):

    fileName = property(lambda s: s._rec.title.text)
    summary = property(lambda s: s._rec.summary.text)
    rev = property(lambda s: s._rec.revision.text)
    published = property(lambda s: s._rec.published.text)
    author = property(lambda s: FileAuthor(s._client, s._rec.author[0]))

    def __init__(self, client, feedRecord):
        super(FileAttachment, self).__init__(client)
        self._rec = feedRecord
   
    @property
    def folder(self):
        for _cat in self._rec.category:
            if _cat.scheme.endswith("#folder"):
                return _cat.term
        return None

    @property
    def fullName(self):
        _path = []
        _folder = self.folder
        if _folder:
            _path.append(_folder)
        _path.append(self.fileName)
        return os.sep.join(_path)

    def getContents(self):
        _uri = self._rec.content.src
        return self._client._get_file_content(_uri)

    def getPropDict(self):
        _out = {}
        for _attr in ("fullName", "summary", "rev", "published", "author"):
            _val = getattr(self, _attr)
            _out[_attr] = _val
        return _out

    def __repr__(self):
        _attrs = " ".join("{0}={1!r}".format(*_el) for _el in self.getPropDict().items())
        return "<{0} {1}>".format(self.__class__.__name__, _attrs)

class FileCabinet(sitesClient.Client):

    def __init__(self, client, path):
        super(FileCabinet, self).__init__(client)
        assert path.startswith("/")
        self._cabinetPath = path

    def _getThisCabinet(self):
        _ans = self.getFeed(path=self._cabinetPath, kind="filecabinet")
        _cabinets = _ans.GetFileCabinets()
        assert len(_cabinets) == 1, "Only one file cabinet is expected."
        return _cabinets[0]

    def ls(self):
        _cab = self._getThisCabinet()
        _out = []
        for _rec in self.getFeed(parent=_cab.GetNodeId()).GetAttachments():
            _out.append(FileAttachment(self._client, _rec))
        return _out

# vim: set sts=4 sw=4 et :
