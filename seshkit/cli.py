"""Console script for seshkit."""
import sys
import click
from typing import NoReturn as typeNoReturn
from seshkit import __version__ as seshkit_version


def _print_version(ctx=None, param=None, value=None) -> typeNoReturn:
    """
    https://click.palletsprojects.com/en/3.x/options/#callbacks-and-eager-options
    """
    if not ctx:
        click.echo(seshkit_version)
    else:
        # this is being used as a callback
        if not value or ctx.resilient_parsing:
            return
        click.echo(seshkit_version)
        ctx.exit()


@click.group(name="sesh")
@click.option(
    "--version",
    callback=_print_version,
    is_eager=True,
    is_flag=True,
    help="Print seshkit version",
)
def top(args=None, **kwargs):
    pass


def main():
    # TODO: use importlib and DRY it up
    from seshkit.cmds.config import command as cmd_config
    from seshkit.cmds.scribe import command as cmd_scribe
    from seshkit.cmds.whoami import command as cmd_whoami

    top.add_command(cmd_config)
    top.add_command(cmd_scribe)
    top.add_command(cmd_whoami)

    top()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
