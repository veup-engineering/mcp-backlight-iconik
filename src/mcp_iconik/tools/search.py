"""Search tools for Iconik MCP."""

from typing import Any, Optional

from mcp.server.fastmcp import FastMCP

from ..client import IconikClient


def register_search_tools(mcp: FastMCP, client: IconikClient) -> None:
    """Register search-related tools."""

    @mcp.tool(structured_output=True)
    async def iconik_search(
        query: Optional[str] = None,
        doc_types: Optional[list[str]] = None,
        filter: Optional[dict[str, Any]] = None,
        sort: Optional[list[dict[str, str]]] = None,
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        """Search for assets and collections in Iconik using various criteria.

        Supports text search, filters, and facets.

        Args:
            query: Text search query
            doc_types: Document types to search (assets, collections)
            filter: Filter criteria object with 'operator' (AND/OR) and 'terms' array
            sort: Sort criteria array of objects with 'name' and 'order' (asc/desc)
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
        """
        return await client.search(
            query=query,
            filter_data=filter,
            doc_types=doc_types,
            page=page,
            per_page=per_page,
            sort=sort,
        )

    @mcp.tool(structured_output=True)
    async def iconik_list_saved_searches(
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        """List all saved searches in Iconik.

        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
        """
        return await client.list_saved_searches(page=page, per_page=per_page)

    @mcp.tool(structured_output=True)
    async def iconik_get_saved_search(
        search_id: str,
        include_results: bool = True,
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        """Get a saved search and optionally execute it to get results.

        Args:
            search_id: The unique ID of the saved search
            include_results: Whether to include search results (default: true)
            page: Page number for results (default: 1)
            per_page: Items per page for results (default: 50)
        """
        return await client.get_saved_search(
            search_id, include_results=include_results, page=page, per_page=per_page
        )

    @mcp.tool(structured_output=True)
    async def iconik_create_saved_search(
        name: str,
        criteria: dict[str, Any],
    ) -> dict[str, Any]:
        """Create a new saved search with specified criteria.

        Args:
            name: Name for the saved search
            criteria: Search criteria object containing query, filter, doc_types, etc.
        """
        return await client.create_saved_search(name, criteria)

    @mcp.tool(structured_output=True)
    async def iconik_delete_saved_search(search_id: str) -> dict[str, Any]:
        """Delete a saved search.

        Args:
            search_id: The unique ID of the saved search to delete
        """
        return await client.delete_saved_search(search_id)
