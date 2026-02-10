"""Metadata tools for Iconik MCP."""

from mcp.types import Tool

METADATA_TOOLS = [
    Tool(
        name="iconik_list_metadata_views",
        description="List all metadata views (schemas) configured in Iconik.",
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
        name="iconik_get_metadata_view",
        description="Get details of a specific metadata view including its fields.",
        inputSchema={
            "type": "object",
            "properties": {
                "view_id": {
                    "type": "string",
                    "description": "The unique ID of the metadata view",
                },
            },
            "required": ["view_id"],
        },
    ),
    Tool(
        name="iconik_get_asset_metadata",
        description="Get all metadata values for an asset across all views.",
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
        name="iconik_update_asset_metadata",
        description="Update metadata values for an asset in a specific view.",
        inputSchema={
            "type": "object",
            "properties": {
                "asset_id": {
                    "type": "string",
                    "description": "The unique ID of the asset",
                },
                "view_id": {
                    "type": "string",
                    "description": "The unique ID of the metadata view",
                },
                "metadata_values": {
                    "type": "object",
                    "description": "Object with field names as keys and values to set",
                    "additionalProperties": True,
                },
            },
            "required": ["asset_id", "view_id", "metadata_values"],
        },
    ),
]
