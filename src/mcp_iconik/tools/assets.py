"""Asset tools for Iconik MCP."""

from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..client import IconikClient


def register_asset_tools(mcp: FastMCP, client: IconikClient) -> None:
    """Register asset-related tools."""

    @mcp.tool()
    async def iconik_list_assets(
        page: int = 1,
        per_page: int = 50,
        sort: Optional[str] = None,
    ) -> dict:
        """List assets in Iconik. Returns paginated list of assets with their metadata.

        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 50, max: 100)
            sort: Sort field (e.g., 'date_created', '-date_created' for descending)
        """
        return await client.list_assets(page=page, per_page=per_page, sort=sort)

    @mcp.tool()
    async def iconik_get_asset(asset_id: str) -> dict:
        """Get detailed information about a specific asset by its ID.

        Args:
            asset_id: The unique ID of the asset
        """
        return await client.get_asset(asset_id)

    @mcp.tool()
    async def iconik_create_asset(
        title: str,
        description: Optional[str] = None,
        type: Optional[str] = None,
        status: str = "ACTIVE",
    ) -> dict:
        """Create a new asset in Iconik.

        Args:
            title: Title of the asset
            description: Description of the asset
            type: Type of asset (VIDEO, AUDIO, IMAGE, DOCUMENT, OTHER)
            status: Status of the asset (ACTIVE, INACTIVE)
        """
        data = {"title": title}
        if description is not None:
            data["description"] = description
        if type is not None:
            data["type"] = type
        if status != "ACTIVE":
            data["status"] = status
        return await client.create_asset(data)

    @mcp.tool()
    async def iconik_update_asset(
        asset_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ) -> dict:
        """Update an existing asset's properties.

        Args:
            asset_id: The unique ID of the asset to update
            title: New title for the asset
            description: New description for the asset
            status: New status (ACTIVE, INACTIVE)
        """
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if status is not None:
            data["status"] = status
        return await client.update_asset(asset_id, data)

    @mcp.tool()
    async def iconik_delete_asset(asset_id: str) -> dict:
        """Delete an asset from Iconik. This moves the asset to the delete queue.

        Args:
            asset_id: The unique ID of the asset to delete
        """
        return await client.delete_asset(asset_id)
