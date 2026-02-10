"""Collection tools for Iconik MCP."""

from mcp.types import Tool

COLLECTION_TOOLS = [
    Tool(
        name="iconik_list_collections",
        description="List collections in Iconik. Returns paginated list of collections.",
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
                    "description": "Sort field (e.g., 'date_created', '-title')",
                },
            },
        },
    ),
    Tool(
        name="iconik_get_collection",
        description="Get detailed information about a specific collection.",
        inputSchema={
            "type": "object",
            "properties": {
                "collection_id": {
                    "type": "string",
                    "description": "The unique ID of the collection",
                },
            },
            "required": ["collection_id"],
        },
    ),
    Tool(
        name="iconik_create_collection",
        description="Create a new collection in Iconik.",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the collection",
                },
                "description": {
                    "type": "string",
                    "description": "Description of the collection",
                },
                "parent_id": {
                    "type": "string",
                    "description": "Parent collection ID for nested collections",
                },
            },
            "required": ["title"],
        },
    ),
    Tool(
        name="iconik_update_collection",
        description="Update an existing collection's properties.",
        inputSchema={
            "type": "object",
            "properties": {
                "collection_id": {
                    "type": "string",
                    "description": "The unique ID of the collection",
                },
                "title": {
                    "type": "string",
                    "description": "New title for the collection",
                },
                "description": {
                    "type": "string",
                    "description": "New description for the collection",
                },
            },
            "required": ["collection_id"],
        },
    ),
    Tool(
        name="iconik_delete_collection",
        description="Delete a collection from Iconik.",
        inputSchema={
            "type": "object",
            "properties": {
                "collection_id": {
                    "type": "string",
                    "description": "The unique ID of the collection to delete",
                },
            },
            "required": ["collection_id"],
        },
    ),
    Tool(
        name="iconik_get_collection_contents",
        description="Get the contents (assets and sub-collections) of a collection.",
        inputSchema={
            "type": "object",
            "properties": {
                "collection_id": {
                    "type": "string",
                    "description": "The unique ID of the collection",
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
            "required": ["collection_id"],
        },
    ),
    Tool(
        name="iconik_add_to_collection",
        description="Add assets or collections to a collection.",
        inputSchema={
            "type": "object",
            "properties": {
                "collection_id": {
                    "type": "string",
                    "description": "The collection to add items to",
                },
                "object_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of asset or collection IDs to add",
                },
                "object_type": {
                    "type": "string",
                    "description": "Type of objects being added (assets or collections)",
                    "enum": ["assets", "collections"],
                    "default": "assets",
                },
            },
            "required": ["collection_id", "object_ids"],
        },
    ),
]
