"""Collection tools for Iconik MCP."""

from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..client import IconikClient


def register_collection_tools(mcp: FastMCP, client: IconikClient) -> None:
    """Register collection-related tools."""

    @mcp.tool()
    async def iconik_list_collections(
        page: int = 1,
        per_page: int = 50,
        sort: Optional[str] = None,
    ) -> dict:
        """List collections in Iconik. Returns paginated list of collections.

        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 50, max: 100)
            sort: Sort field (e.g., 'date_created', '-title')
        """
        return await client.list_collections(page=page, per_page=per_page, sort=sort)

    @mcp.tool()
    async def iconik_get_collection(collection_id: str) -> dict:
        """Get detailed information about a specific collection.

        Args:
            collection_id: The unique ID of the collection
        """
        return await client.get_collection(collection_id)

    @mcp.tool()
    async def iconik_create_collection(
        title: str,
        description: Optional[str] = None,
        parent_id: Optional[str] = None,
    ) -> dict:
        """Create a new collection in Iconik.

        Args:
            title: Title of the collection
            description: Description of the collection
            parent_id: Parent collection ID for nested collections
        """
        data = {"title": title}
        if description is not None:
            data["description"] = description
        if parent_id is not None:
            data["parent_id"] = parent_id
        return await client.create_collection(data)

    @mcp.tool()
    async def iconik_update_collection(
        collection_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> dict:
        """Update an existing collection's properties.

        Args:
            collection_id: The unique ID of the collection
            title: New title for the collection
            description: New description for the collection
        """
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        return await client.update_collection(collection_id, data)

    @mcp.tool()
    async def iconik_delete_collection(collection_id: str) -> dict:
        """Delete a collection from Iconik.

        Args:
            collection_id: The unique ID of the collection to delete
        """
        return await client.delete_collection(collection_id)

    @mcp.tool()
    async def iconik_get_collection_contents(
        collection_id: str,
        page: int = 1,
        per_page: int = 50,
    ) -> dict:
        """Get the contents (assets and sub-collections) of a collection.

        Args:
            collection_id: The unique ID of the collection
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
        """
        return await client.get_collection_contents(collection_id, page=page, per_page=per_page)

    @mcp.tool()
    async def iconik_add_to_collection(
        collection_id: str,
        object_ids: list[str],
        object_type: str = "assets",
    ) -> dict:
        """Add assets or collections to a collection.

        Args:
            collection_id: The collection to add items to
            object_ids: List of asset or collection IDs to add
            object_type: Type of objects being added (assets or collections)
        """
        return await client.add_to_collection(collection_id, object_ids, object_type)
