"""Generic API tools for Iconik MCP."""

from mcp.types import Tool

GENERIC_TOOLS = [
    Tool(
        name="iconik_api_request",
        description="""Make a generic API request to any Iconik endpoint. Use this for endpoints not covered by other tools.

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

Refer to Iconik API documentation for full endpoint details.""",
        inputSchema={
            "type": "object",
            "properties": {
                "method": {
                    "type": "string",
                    "description": "HTTP method (GET, POST, PUT, PATCH, DELETE)",
                    "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"],
                },
                "path": {
                    "type": "string",
                    "description": "API path (e.g., /API/assets/v1/assets/)",
                },
                "params": {
                    "type": "object",
                    "description": "Query parameters as key-value pairs",
                    "additionalProperties": True,
                },
                "body": {
                    "type": "object",
                    "description": "Request body for POST/PUT/PATCH requests",
                    "additionalProperties": True,
                },
            },
            "required": ["method", "path"],
        },
    ),
    Tool(
        name="iconik_get_acls",
        description="Get access control list (permissions) for an object.",
        inputSchema={
            "type": "object",
            "properties": {
                "object_type": {
                    "type": "string",
                    "description": "Type of object (assets, collections)",
                    "enum": ["assets", "collections"],
                },
                "object_id": {
                    "type": "string",
                    "description": "The unique ID of the object",
                },
            },
            "required": ["object_type", "object_id"],
        },
    ),
    Tool(
        name="iconik_update_acls",
        description="Update access control list (permissions) for an object.",
        inputSchema={
            "type": "object",
            "properties": {
                "object_type": {
                    "type": "string",
                    "description": "Type of object (assets, collections)",
                    "enum": ["assets", "collections"],
                },
                "object_id": {
                    "type": "string",
                    "description": "The unique ID of the object",
                },
                "acl_entries": {
                    "type": "array",
                    "description": "List of ACL entries with user/group IDs and permissions",
                    "items": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "group_id": {"type": "string"},
                            "permissions": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                    },
                },
            },
            "required": ["object_type", "object_id", "acl_entries"],
        },
    ),
]
