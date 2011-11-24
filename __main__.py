import os
import argparse
import re
import logging

# from .
import lib.autoEnv

ROOT_DIR = os.path.dirname(__file__)

logging.basicConfig()
_logger = logging.getLogger()
_logger.setLevel(logging.DEBUG)

def setupEnv():
    _dir = os.path.join(ROOT_DIR, "tmp", "env")
    _env = lib.autoEnv.Environment(_dir, True)
    _env.activate()
    _env.install("gdata")

    logging.basicConfig()
    logging.getLogger('').setLevel(logging.DEBUG)

def get_cabinet(args):
    import cabinet
    _uri = args.uri
    _re = re.compile(r"^(?:http(?:s)?://)?(\w+)\.([^/]+)(/.*)$")
    (_site, _domain, _path) = _re.match(_uri).groups()
    return cabinet.FileCabinet.fromSiteDomain(_site, _domain, path=_path)

def get_parser():
    _parser = argparse.ArgumentParser(description="Create and update your `authorized_keys` file from a file cabinet on Google Sites.")
    _parser.add_argument("--uri", help="Cabinet URI", required=True)
    _parser.add_argument("--keys-file", help="`authorized_keys` file location",
        default=os.path.expanduser("~/.ssh/authorized_keys"))
    return _parser

def get_keyfile_line_tail(siteFile):
    return "|| {0!r}".format(siteFile.getPropDict())

def need_to_regenerate_keyfile(keyfile, siteFiles):
    if os.path.exists(keyfile):
        _expectedTails = set(get_keyfile_line_tail(_file) for _file in siteFiles)
        _file = open(keyfile, "r")
        try:
            for _line in _file:
                _line = _line.strip()
                for _tail in tuple(_expectedTails):
                    if _line.endswith(_tail):
                        _expectedTails.remove(_tail)
                        break
                else:
                    return True
        finally:
            _file.close()
        return len(_expectedTails) != 0
    else:
        return True

def get_ssh_pubkey(cabinetFile):
    _txt = cabinetFile.getContents()
    return " ".join(_line.strip() for _line in _txt.splitlines())

if __name__ == "__main__":
    _parser = get_parser()
    _args = _parser.parse_args()
    setupEnv()

    _cabinet = get_cabinet(_args)
    _files = _cabinet.ls()
    if need_to_regenerate_keyfile(_args.keys_file, _files):
        print "Regenerating file..."
        _records = ["{0} {1}".format(get_ssh_pubkey(_file), get_keyfile_line_tail(_file))
            for _file in _files]
        _out = open(_args.keys_file, "w")
        _out.write("\n".join(_records))
        _out.close()

# vim: set sts=4 sw=4 et :
