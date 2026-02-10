"""Asset tools for Iconik MCP."""

from mcp.types import Tool

ASSET_TOOLS = [
    Tool(
        name="iconik_list_assets",
        description="List assets in Iconik. Returns paginated list of assets with their metadata.",
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
                    "description": "Items per page (default: 50, max: 100)",
                    "default": 50,
                },
                "sort": {
                    "type": "string",
                    "description": "Sort field (e.g., 'date_created', '-date_created' for descending)",
                },
            },
        },
    ),
    Tool(
        name="iconik_get_asset",
        description="Get detailed information about a specific asset by its ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "asset_id": {
                    "type": "string",
                    "description": "The unique ID of the asset",
                },
            },
            "required": ["asset_id"],
        },
    ),
    Tool(
        name="iconik_create_asset",
        description="Create a new asset in Iconik.",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the asset",
                },
                "description": {
                    "type": "string",
                    "description": "Description of the asset",
                },
                "type": {
                    "type": "string",
                    "description": "Type of asset (VIDEO, AUDIO, IMAGE, DOCUMENT, OTHER)",
                    "enum": ["VIDEO", "AUDIO", "IMAGE", "DOCUMENT", "OTHER"],
                },
                "status": {
                    "type": "string",
                    "description": "Status of the asset (ACTIVE, INACTIVE)",
                    "default": "ACTIVE",
                },
            },
            "required": ["title"],
        },
    ),
    Tool(
        name="iconik_update_asset",
        description="Update an existing asset's properties.",
        inputSchema={
            "type": "object",
            "properties": {
                "asset_id": {
                    "type": "string",
                    "description": "The unique ID of the asset to update",
                },
                "title": {
                    "type": "string",
                    "description": "New title for the asset",
                },
                "description": {
                    "type": "string",
                    "description": "New description for the asset",
                },
                "status": {
                    "type": "string",
                    "description": "New status (ACTIVE, INACTIVE)",
                },
            },
            "required": ["asset_id"],
        },
    ),
    Tool(
        name="iconik_delete_asset",
        description="Delete an asset from Iconik. This moves the asset to the delete queue.",
        inputSchema={
            "type": "object",
            "properties": {
                "asset_id": {
                    "type": "string",
                    "description": "The unique ID of the asset to delete",
                },
            },
            "required": ["asset_id"],
        },
    ),
]
