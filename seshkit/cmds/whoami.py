import click
from configparser import ConfigParser
from seshkit.settings import *
from seshkit.stubs import get_active_profile


@click.command(name="whoami")
@click.option(
    "--config-path",
    "-p",
    type=click.Path(exists=True),
    default=DEFAULT_SESHKIT_CONFIG_PATH,
    help="The path from which to read and write seshkit configuration",
)
def command(config_path, **kwargs):
    """
    Print current sesh profile/configuration, and its authentication status
    """

    # TODO: DRY this and config.py functionality
    config = ConfigParser()
    config.read(config_path)

    profile = get_active_profile(config)

    for k, v in profile.items():
        click.echo(f"{k}: {v}")
        # click.style(f"Contents of {config_path}:", fg="green", bg="black"), err=True

    click.echo("creds:")
    for k, v in profile.creds_safe.items():
        click.echo(f"  {k}: {v}")
    # TODO:
    # test authentication with service
    # test r/w status of default_bucket
