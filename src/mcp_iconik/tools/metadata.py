"""Metadata tools for Iconik MCP."""

from typing import Any

from mcp.server.fastmcp import FastMCP

from ..client import IconikClient


def register_metadata_tools(mcp: FastMCP, client: IconikClient) -> None:
    """Register metadata-related tools."""

    @mcp.tool()
    async def iconik_list_metadata_views(
        page: int = 1,
        per_page: int = 50,
    ) -> dict:
        """List all metadata views (schemas) configured in Iconik.

        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
        """
        return await client.list_metadata_views(page=page, per_page=per_page)

    @mcp.tool()
    async def iconik_get_metadata_view(view_id: str) -> dict:
        """Get details of a specific metadata view including its fields.

        Args:
            view_id: The unique ID of the metadata view
        """
        return await client.get_metadata_view(view_id)

    @mcp.tool()
    async def iconik_get_asset_metadata(asset_id: str) -> dict:
        """Get all metadata values for an asset across all views.

        Args:
            asset_id: The unique ID of the asset
        """
        return await client.get_asset_metadata(asset_id)

    @mcp.tool()
    async def iconik_update_asset_metadata(
        asset_id: str,
        view_id: str,
        metadata_values: dict[str, Any],
    ) -> dict:
        """Update metadata values for an asset in a specific view.

        Args:
            asset_id: The unique ID of the asset
            view_id: The unique ID of the metadata view
            metadata_values: Object with field names as keys and values to set
        """
        return await client.update_asset_metadata(
            asset_id, view_id, {"metadata_values": metadata_values}
        )
