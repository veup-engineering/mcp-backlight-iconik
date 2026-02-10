"""File and storage tools for Iconik MCP."""

from mcp.types import Tool

FILE_TOOLS = [
    Tool(
        name="iconik_list_storages",
        description="List all storage locations configured in Iconik.",
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
        name="iconik_get_storage",
        description="Get details of a specific storage location.",
        inputSchema={
            "type": "object",
            "properties": {
                "storage_id": {
                    "type": "string",
                    "description": "The unique ID of the storage",
                },
            },
            "required": ["storage_id"],
        },
    ),
    Tool(
        name="iconik_get_asset_files",
        description="Get all files associated with an asset.",
        inputSchema={
            "type": "object",
            "properties": {
                "asset_id": {
                    "type": "string",
                    "description": "The unique ID of the asset",
                },
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
            "required": ["asset_id"],
        },
    ),
    Tool(
        name="iconik_get_asset_formats",
        description="Get all format definitions for an asset (ORIGINAL, PROXY, etc.).",
        inputSchema={
            "type": "object",
            "properties": {
                "asset_id": {
                    "type": "string",
                    "description": "The unique ID of the asset",
                },
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
            "required": ["asset_id"],
        },
    ),
    Tool(
        name="iconik_get_asset_proxies",
        description="Get proxy files for an asset (video previews, thumbnails).",
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
        name="iconik_get_asset_keyframes",
        description="Get keyframe images for a video asset.",
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
]
