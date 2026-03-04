"""File and storage tools for Iconik MCP."""

from typing import Any

from mcp.server.fastmcp import FastMCP

from ..client import IconikClient


def register_file_tools(mcp: FastMCP, client: IconikClient) -> None:
    """Register file and storage tools."""

    @mcp.tool(structured_output=True)
    async def iconik_list_storages(
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        """List all storage locations configured in Iconik.

        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
        """
        return await client.list_storages(page=page, per_page=per_page)

    @mcp.tool(structured_output=True)
    async def iconik_get_storage(storage_id: str) -> dict[str, Any]:
        """Get details of a specific storage location.

        Args:
            storage_id: The unique ID of the storage
        """
        return await client.get_storage(storage_id)

    @mcp.tool(structured_output=True)
    async def iconik_get_asset_files(
        asset_id: str,
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        """Get all files associated with an asset.

        Args:
            asset_id: The unique ID of the asset
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
        """
        return await client.get_asset_files(asset_id, page=page, per_page=per_page)

    @mcp.tool(structured_output=True)
    async def iconik_get_asset_formats(
        asset_id: str,
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        """Get all format definitions for an asset (ORIGINAL, PROXY, etc.).

        Args:
            asset_id: The unique ID of the asset
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
        """
        return await client.get_asset_formats(asset_id, page=page, per_page=per_page)

    @mcp.tool(structured_output=True)
    async def iconik_get_asset_proxies(asset_id: str) -> dict[str, Any]:
        """Get proxy files for an asset (video previews, thumbnails).

        Args:
            asset_id: The unique ID of the asset
        """
        return await client.get_asset_proxies(asset_id)

    @mcp.tool(structured_output=True)
    async def iconik_get_asset_keyframes(asset_id: str) -> dict[str, Any]:
        """Get keyframe images for a video asset.

        Args:
            asset_id: The unique ID of the asset
        """
        return await client.get_asset_keyframes(asset_id)
