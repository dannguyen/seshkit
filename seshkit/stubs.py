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
    default_bucket = my-seshkit-output-bucket
    """

    VALID_ATTRIBUTES = (
        "service",
        "service_creds_path",
        "service_profile",
        "default_bucket",
    )

    @staticmethod
    def get_active_profile_dict(config: ConfigParser) -> dict:
        """
        given a ConfigParser object that has read in the data, get the default/first profile
            and return a dict

        TODO: should be looking for 'default' first, not just the first profile
        """
        return list(config._sections.values())[0]

    def __init__(self, src: typeUnion[dict, StdPath, str], profile: str = None):
        self._original = src
        if isinstance(src, dict):
            _pdata = src
        elif isinstance(src, (StdPath, str)):
            inpath = str(StdPath(src).expanduser())
            _ini = ConfigParser()
            _ini.read(inpath)
            if profile:
                _pdata = _ini._sections[profile]
            else:
                _pdata = self.get_active_profile_dict(_ini)
        else:
            raise TypeError(f"Can't process src of type: {type(src)}")

        _pdata = {k: _pdata.get(k) for k in self.VALID_ATTRIBUTES}
        super().__init__(_pdata)
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

    @property
    def creds_safe(self) -> dict:
        """
        produces a dict that has the cred values sanitized for logging purposes
        """

        def _santiize(txt):
            return txt[0:4] + "*****" + txt[-2:]

        c = {k: _santiize(v) for k, v in self.creds.items()}
        return c


def get_active_profile(config: ConfigParser) -> SeshProfile:
    """
    given a ConfigParser object that has read in the data, get the default/first profile and
    instantiate a SeshProfile object
    """
    d = SeshProfile.get_active_profile_dict(config)
    return SeshProfile(d)
