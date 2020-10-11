"""
small classes/utils that I haven't decided on a final name/structure for...
"""
from configparser import ConfigParser
from pathlib import Path as StdPath
from typing import Union as typeUnion


class Services(object):
    AWS = "aws"
    # GCLOUD = 'gcloud'

    ALL = (AWS,)

    @staticmethod
    def validate(txt) -> bool:
        t = txt.lower()
        return t in self.ALL


class SeshProfile(dict):
    """
    comes from a dict that is serialized like:

    [default]
    service = aws
    service_creds_path = ~/sample/.aws/credentials
    service_profile = seshkituser
    output_bucket = my-seshkit-output-bucket
    """

    VALID_ATTRIBUTES = (
        "service",
        "service_creds_path",
        "service_profile",
        "output_bucket",
    )

    def __init__(self, src: typeUnion[dict, StdPath, str], profile: str = None):
        self._original = src
        if isinstance(src, dict):
            _data = {k: src.get(k) for k in self.VALID_ATTRIBUTES}
        elif isinstance(src, (StdPath, str)):
            inpath = str(StdPath(src).expanduser())
            _ini = ConfigParser()
            _ini.read(inpath)
            if profile:
                _data = _ini._sections[profile]
            else:
                _data = list(_ini._sections.values())[0]
        else:
            raise TypeError(f"Can't process src of type: {type(src)}")
        super().__init__(_data)
        self._creds = None

    def __getattr__(self, name):
        if name in self.VALID_ATTRIBUTES:
            return self.get(name, None)
        else:
            return super().__getattribute__(name)

    def _get_creds(self):
        if not self._creds:
            if self.service == Services.AWS:
                with open(self.service_creds_path) as f:
                    _ini = ConfigParser()
                    _ini.read_string(f.read())
                    _cd = _ini._sections[self.service_profile]
                    # TODO: refactor aws key names later
                    parsedcreds = {
                        k: _cd[k]
                        for k in (
                            "aws_access_key_id",
                            "aws_secret_access_key",
                        )
                    }
            else:
                raise ValueError(
                    "Tried to parse a creds file for a service not yet implemented!"
                )

            self._creds = parsedcreds
        return self._creds

    @property
    def creds(self) -> dict:
        return self._get_creds()
