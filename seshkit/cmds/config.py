from configparser import ConfigParser
from copy import deepcopy
from io import StringIO
from pathlib import Path
from typing import NoReturn as typeNoReturn

import click


DEFAULT_CREDS_PATHS = {
    'aws': '~/.aws/credentials'
}

for k, p in DEFAULT_CREDS_PATHS.items():
    DEFAULT_CREDS_PATHS[k] = str(Path(p).expanduser().resolve())
DEFAULT_SESHKIT_CONFIG_PATH = str(Path('~/.seshkitrc').expanduser().resolve())

SERVICES = ('aws', )

"""
creds_path = ~/sample/.aws/credentials
profile = seshkituser
input_bucket = my-seshkit-input-bucket
output_bucket = my-seshkit-output-bucket
"""
@click.command(name='config')
@click.option('--config-path', '-p', type=click.Path(), default=DEFAULT_SESHKIT_CONFIG_PATH, help="The path from which to read and write seshkit configuration")
@click.option('--profile', 'sesh_profile_name', type=str, help="The seshkit config profile to write/update")
def command(config_path, sesh_profile_name, **kwargs):
    """
    View and/or edit your seshkit configuration profiles and settings
    """

    do_edit_mode = True if sesh_profile_name else False
    sesh_profile_name = sesh_profile_name or 'default'

    config = ConfigParser()
    if Path(config_path).exists():
        config.read(config_path)
        sesh_profiles = config._sections
    else:
        do_edit_mode = True
        sesh_profiles = {}

    if do_edit_mode:
        if sesh_profiles.get(sesh_profile_name):
            click.echo(f"Editing '{sesh_profile_name}' configuration...", err=True)
            prof = sesh_profiles[sesh_profile_name]
        else:
            click.echo(f"Creating '{sesh_profile_name}' configuration...", err=True)
            prof = {}

        sesh_profiles[sesh_profile_name] = interactive_profile_editor(prof)
        config.read_dict(sesh_profiles)

    with StringIO() as ctxt:
        config.write(ctxt)
        ctxt.seek(0)
        config_text = ctxt.read()
        click.echo(click.style(f'Contents of {config_path}:', fg='green', bg='black'), err=True)
        click.echo(config_text)

        if do_edit_mode:
            with open(config_path, 'w') as outs:
                outs.write(config_text)


def interactive_profile_editor(profile:dict) -> dict:
    prof = deepcopy(profile)

    _dv = prof.get('service', 'aws')
    prof['service'] = click.prompt('Which service?', default=_dv, type=click.Choice(SERVICES, case_sensitive=False))

    _dv = prof.get('service_creds_path', DEFAULT_CREDS_PATHS[prof['service']])
    prof['service_creds_path'] = _credspath = click.prompt(f'What is the file path for service credentials?', default=_dv, type=click.Path())

    # attempt to open creds path
    _pcreds = ConfigParser()
    _pcreds.read(_credspath)
    _credprofiles = _pcreds.sections()
    _defaultpcredname = 'default' if 'default' in _credprofiles else _credprofiles[0]

    _dv = prof.get('service_profile', _defaultpcredname)
    prof['service_profile'] = click.prompt('Which account profile?', type=click.Choice(_credprofiles),  default=_dv,)

    # _dv = prof.get('input_bucket', '')
    # prof['input_bucket'] = click.prompt("What is the name/id of the default input bucket? e.g. 'my-input-bucket'", type=str, default=_dv)

    _dv = prof.get('output_bucket', '')
    prof['output_bucket'] = click.prompt("What is the name/id of the default output bucket? e.g. 'my-output-bucket'", type=str, default=_dv)

    return prof
