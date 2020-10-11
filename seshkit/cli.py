"""Console script for seshkit."""
import sys
import click


@click.group()
def top(args=None):
    """seshkit.cli top"""
    return 0


def main():
    from seshkit.cmds.config import command as cmd_config
    top.add_command(cmd_config)
    top()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
