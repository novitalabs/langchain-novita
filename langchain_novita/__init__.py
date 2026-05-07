from importlib import metadata

from langchain_novita.sandbox import NovitaSandbox

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    __version__ = ""
del metadata

__all__ = ["NovitaSandbox", "__version__"]
