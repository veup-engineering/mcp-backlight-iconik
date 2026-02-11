"""Iconik API tools for MCP."""

from mcp.server.fastmcp import FastMCP

from ..client import IconikClient
from .assets import register_asset_tools
from .collections import register_collection_tools
from .files import register_file_tools
from .generic import register_generic_tools
from .jobs import register_job_tools
from .metadata import register_metadata_tools
from .search import register_search_tools
from .users import register_user_tools


def register_all_tools(mcp: FastMCP, client: IconikClient) -> None:
    """Register all Iconik tool modules with the MCP server."""
    register_asset_tools(mcp, client)
    register_collection_tools(mcp, client)
    register_file_tools(mcp, client)
    register_job_tools(mcp, client)
    register_metadata_tools(mcp, client)
    register_search_tools(mcp, client)
    register_user_tools(mcp, client)
    register_generic_tools(mcp, client)
