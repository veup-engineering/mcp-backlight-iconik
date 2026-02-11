"""Generic API tools for Iconik MCP."""

from typing import Any, Optional

from mcp.server.fastmcp import FastMCP

from ..client import IconikClient


def register_generic_tools(mcp: FastMCP, client: IconikClient) -> None:
    """Register generic API tools."""

    @mcp.tool()
    async def iconik_api_request(
        method: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        body: Optional[dict[str, Any]] = None,
    ) -> dict:
        """Make a generic API request to any Iconik endpoint.

        Use this for endpoints not covered by other tools.

        Common API paths include:
        - /API/assets/v1/ - Assets, Collections, Shares, Projects
        - /API/search/v1/ - Search, Saved Searches
        - /API/files/v1/ - Files, Storages, Formats, Proxies
        - /API/metadata/v1/ - Metadata Views and Values
        - /API/jobs/v1/ - Jobs
        - /API/users/v1/ - Users and Groups
        - /API/acls/v1/ - Access Control Lists
        - /API/notifications/v1/ - Webhooks
        - /API/transcode/v1/ - Transcoding
        - /API/automations/v1/ - Automations
        - /API/ml/v1/ - Machine Learning features
        - /API/stats/v1/ - Statistics

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            path: API path (e.g., /API/assets/v1/assets/)
            params: Query parameters as key-value pairs
            body: Request body for POST/PUT/PATCH requests
        """
        return await client.api_request(method=method, path=path, params=params, body=body)

    @mcp.tool()
    async def iconik_get_acls(
        object_type: str,
        object_id: str,
    ) -> dict:
        """Get access control list (permissions) for an object.

        Args:
            object_type: Type of object (assets, collections)
            object_id: The unique ID of the object
        """
        return await client.get_acls(object_type, object_id)

    @mcp.tool()
    async def iconik_update_acls(
        object_type: str,
        object_id: str,
        acl_entries: list[dict[str, Any]],
    ) -> dict:
        """Update access control list (permissions) for an object.

        Args:
            object_type: Type of object (assets, collections)
            object_id: The unique ID of the object
            acl_entries: List of ACL entries with user/group IDs and permissions
        """
        return await client.update_acls(object_type, object_id, {"acl_entries": acl_entries})
