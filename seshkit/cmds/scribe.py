import click
from seshkit.settings import *


@click.command(name="scribe")
@click.option(
    "--config-path",
    "-p",
    type=click.Path(),
    default=DEFAULT_SESHKIT_CONFIG_PATH,
    help="The path from which to read configuration",
)


# @click.option(
#     "--config-path",
#     "-p",
#     "sesh_config_path",
#     type=click.Path(),
#     default=DEFAULT_SESHKIT_CONFIG_PATH,
#     help="The path from which to read and write seshkit configuration",
# )
# # TODO: allow --source to point to S3 URI or web URL for single files? Or make user download
# # remote files themselves?
# @click.option(
#     '--source',
#     '-s',
#     type=str,
#     help="""A local path, pointing to a file; or a glob thingy TKTK; Required for starting a new job""",
# )

# @click.option(
#     '--name',
#     '-n',
#     'job_name',
#     type=str,
#     help="""The name of the job to create or to check on.
#     Can be either:
#         - a regular string, e.g. 'my-interview', in which case --bucket or profile.default_bucket is assumed
#         - a S3 URI that represents an existing or intended project folder e.g. s3://some-other-bucket/my-interview/

#     If this is left empty and --source is not (i.e. you're trying to create a new job), by default it will be derived from the base name of --source""",
# )

# @click.option(
#     '--dest',
#     '-d',
#     help="""A local subdir to copy a finished remote job and process it...?TKTK"""
# )
def command(**kwargs):
    """
    Initiate, and/or update and/or finish a sesh job.

    - Establishes a local project folder
    - syncs it to remote service
    - runs transcription API
    - syncs results back to local
    - makes produced transcript.json and other finishing files
    TKTK
    """
    click.echo("Nothing to see here! TKTK")
