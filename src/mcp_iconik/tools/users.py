"""User and group tools for Iconik MCP."""

from mcp.types import Tool

USER_TOOLS = [
    Tool(
        name="iconik_list_users",
        description="List users in the Iconik domain.",
        inputSchema={
            "type": "object",
            "properties": {
                "page": {
                    "type": "integer",
                    "description": "Page number (default: 1)",
                    "default": 1,
                },
                "per_page": {
                    "type": "integer",
                    "description": "Items per page (default: 50)",
                    "default": 50,
                },
            },
        },
    ),
    Tool(
        name="iconik_get_user",
        description="Get details of a specific user.",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The unique ID of the user",
                },
            },
            "required": ["user_id"],
        },
    ),
    Tool(
        name="iconik_get_current_user",
        description="Get details of the currently authenticated user.",
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    Tool(
        name="iconik_list_groups",
        description="List groups in the Iconik domain.",
        inputSchema={
            "type": "object",
            "properties": {
                "page": {
                    "type": "integer",
                    "description": "Page number (default: 1)",
                    "default": 1,
                },
                "per_page": {
                    "type": "integer",
                    "description": "Items per page (default: 50)",
                    "default": 50,
                },
            },
        },
    ),
    Tool(
        name="iconik_get_group",
        description="Get details of a specific group.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "string",
                    "description": "The unique ID of the group",
                },
            },
            "required": ["group_id"],
        },
    ),
    Tool(
        name="iconik_list_shares",
        description="List shares created by the current user.",
        inputSchema={
            "type": "object",
            "properties": {
                "page": {
                    "type": "integer",
                    "description": "Page number (default: 1)",
                    "default": 1,
                },
                "per_page": {
                    "type": "integer",
                    "description": "Items per page (default: 50)",
                    "default": 50,
                },
            },
        },
    ),
    Tool(
        name="iconik_get_share",
        description="Get details of a specific share.",
        inputSchema={
            "type": "object",
            "properties": {
                "share_id": {
                    "type": "string",
                    "description": "The unique ID of the share",
                },
            },
            "required": ["share_id"],
        },
    ),
    Tool(
        name="iconik_list_projects",
        description="List projects in Iconik.",
        inputSchema={
            "type": "object",
            "properties": {
                "page": {
                    "type": "integer",
                    "description": "Page number (default: 1)",
                    "default": 1,
                },
                "per_page": {
                    "type": "integer",
                    "description": "Items per page (default: 50)",
                    "default": 50,
                },
            },
        },
    ),
    Tool(
        name="iconik_get_project",
        description="Get details of a specific project.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "The unique ID of the project",
                },
            },
            "required": ["project_id"],
        },
    ),
    Tool(
        name="iconik_list_webhooks",
        description="List webhooks configured in Iconik.",
        inputSchema={
            "type": "object",
            "properties": {
                "page": {
                    "type": "integer",
                    "description": "Page number (default: 1)",
                    "default": 1,
                },
                "per_page": {
                    "type": "integer",
                    "description": "Items per page (default: 50)",
                    "default": 50,
                },
            },
        },
    ),
    Tool(
        name="iconik_get_webhook",
        description="Get details of a specific webhook.",
        inputSchema={
            "type": "object",
            "properties": {
                "webhook_id": {
                    "type": "string",
                    "description": "The unique ID of the webhook",
                },
            },
            "required": ["webhook_id"],
        },
    ),
]
