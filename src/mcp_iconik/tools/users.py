"""User, group, share, project, and webhook tools for Iconik MCP."""

from mcp.server.fastmcp import FastMCP

from ..client import IconikClient


def register_user_tools(mcp: FastMCP, client: IconikClient) -> None:
    """Register user, group, share, project, and webhook tools."""

    @mcp.tool()
    async def iconik_list_users(
        page: int = 1,
        per_page: int = 50,
    ) -> dict:
        """List users in the Iconik domain.

        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
        """
        return await client.list_users(page=page, per_page=per_page)

    @mcp.tool()
    async def iconik_get_user(user_id: str) -> dict:
        """Get details of a specific user.

        Args:
            user_id: The unique ID of the user
        """
        return await client.get_user(user_id)

    @mcp.tool()
    async def iconik_get_current_user() -> dict:
        """Get details of the currently authenticated user."""
        return await client.get_current_user()

    @mcp.tool()
    async def iconik_list_groups(
        page: int = 1,
        per_page: int = 50,
    ) -> dict:
        """List groups in the Iconik domain.

        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
        """
        return await client.list_groups(page=page, per_page=per_page)

    @mcp.tool()
    async def iconik_get_group(group_id: str) -> dict:
        """Get details of a specific group.

        Args:
            group_id: The unique ID of the group
        """
        return await client.get_group(group_id)

    @mcp.tool()
    async def iconik_list_shares(
        page: int = 1,
        per_page: int = 50,
    ) -> dict:
        """List shares created by the current user.

        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
        """
        return await client.list_shares(page=page, per_page=per_page)

    @mcp.tool()
    async def iconik_get_share(share_id: str) -> dict:
        """Get details of a specific share.

        Args:
            share_id: The unique ID of the share
        """
        return await client.get_share(share_id)

    @mcp.tool()
    async def iconik_list_projects(
        page: int = 1,
        per_page: int = 50,
    ) -> dict:
        """List projects in Iconik.

        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
        """
        return await client.list_projects(page=page, per_page=per_page)

    @mcp.tool()
    async def iconik_get_project(project_id: str) -> dict:
        """Get details of a specific project.

        Args:
            project_id: The unique ID of the project
        """
        return await client.get_project(project_id)

    @mcp.tool()
    async def iconik_list_webhooks(
        page: int = 1,
        per_page: int = 50,
    ) -> dict:
        """List webhooks configured in Iconik.

        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
        """
        return await client.list_webhooks(page=page, per_page=per_page)

    @mcp.tool()
    async def iconik_get_webhook(webhook_id: str) -> dict:
        """Get details of a specific webhook.

        Args:
            webhook_id: The unique ID of the webhook
        """
        return await client.get_webhook(webhook_id)
