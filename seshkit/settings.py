from pathlib import Path


def resolve_path(path) -> str:
    return str(Path(path).expanduser().resolve())


AVAILABLE_SERVICES = ("aws",)


DEFAULT_SESHKIT_PROFILE_PATH = "~/.seshkitrc"
# TODO: why is this here? Instead of settings?
DEFAULT_CREDS_PATHS = {"aws": "~/.aws/credentials"}

for k, p in DEFAULT_CREDS_PATHS.items():
    DEFAULT_CREDS_PATHS[k] = resolve_path(p)
DEFAULT_SESHKIT_CONFIG_PATH = resolve_path("~/.seshkitrc")
