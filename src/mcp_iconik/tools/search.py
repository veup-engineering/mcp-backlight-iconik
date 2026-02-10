"""Search tools for Iconik MCP."""

from mcp.types import Tool

SEARCH_TOOLS = [
    Tool(
        name="iconik_search",
        description="Search for assets and collections in Iconik using various criteria. Supports text search, filters, and facets.",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Text search query",
                },
                "doc_types": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Document types to search (assets, collections)",
                    "default": ["assets"],
                },
                "filter": {
                    "type": "object",
                    "description": "Filter criteria object with 'operator' (AND/OR) and 'terms' array",
                },
                "sort": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "order": {"type": "string", "enum": ["asc", "desc"]},
                        },
                    },
                    "description": "Sort criteria array",
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
        },
    ),
    Tool(
        name="iconik_list_saved_searches",
        description="List all saved searches in Iconik.",
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
        name="iconik_get_saved_search",
        description="Get a saved search and optionally execute it to get results.",
        inputSchema={
            "type": "object",
            "properties": {
                "search_id": {
                    "type": "string",
                    "description": "The unique ID of the saved search",
                },
                "include_results": {
                    "type": "boolean",
                    "description": "Whether to include search results (default: true)",
                    "default": True,
                },
                "page": {
                    "type": "integer",
                    "description": "Page number for results (default: 1)",
                    "default": 1,
                },
                "per_page": {
                    "type": "integer",
                    "description": "Items per page for results (default: 50)",
                    "default": 50,
                },
            },
            "required": ["search_id"],
        },
    ),
    Tool(
        name="iconik_create_saved_search",
        description="Create a new saved search with specified criteria.",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name for the saved search",
                },
                "criteria": {
                    "type": "object",
                    "description": "Search criteria object containing query, filter, doc_types, etc.",
                    "properties": {
                        "query": {"type": "string"},
                        "doc_types": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "filter": {"type": "object"},
                    },
                },
            },
            "required": ["name", "criteria"],
        },
    ),
    Tool(
        name="iconik_delete_saved_search",
        description="Delete a saved search.",
        inputSchema={
            "type": "object",
            "properties": {
                "search_id": {
                    "type": "string",
                    "description": "The unique ID of the saved search to delete",
                },
            },
            "required": ["search_id"],
        },
    ),
]
