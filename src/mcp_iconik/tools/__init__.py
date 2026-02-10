"""Iconik API tools for MCP."""

from .assets import ASSET_TOOLS
from .collections import COLLECTION_TOOLS
from .files import FILE_TOOLS
from .jobs import JOB_TOOLS
from .metadata import METADATA_TOOLS
from .search import SEARCH_TOOLS
from .users import USER_TOOLS
from .generic import GENERIC_TOOLS

ALL_TOOLS = (
    ASSET_TOOLS
    + COLLECTION_TOOLS
    + FILE_TOOLS
    + JOB_TOOLS
    + METADATA_TOOLS
    + SEARCH_TOOLS
    + USER_TOOLS
    + GENERIC_TOOLS
)

__all__ = ["ALL_TOOLS"]
