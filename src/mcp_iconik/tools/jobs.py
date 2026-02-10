"""Job tools for Iconik MCP."""

from mcp.types import Tool

JOB_TOOLS = [
    Tool(
        name="iconik_list_jobs",
        description="List jobs in Iconik (uploads, transcodes, analysis, etc.).",
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
                "status": {
                    "type": "string",
                    "description": "Filter by status (PENDING, IN_PROGRESS, FINISHED, FAILED)",
                    "enum": ["PENDING", "IN_PROGRESS", "FINISHED", "FAILED"],
                },
            },
        },
    ),
    Tool(
        name="iconik_get_job",
        description="Get details of a specific job including its progress and status.",
        inputSchema={
            "type": "object",
            "properties": {
                "job_id": {
                    "type": "string",
                    "description": "The unique ID of the job",
                },
            },
            "required": ["job_id"],
        },
    ),
    Tool(
        name="iconik_create_job",
        description="Create a new job in Iconik.",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title/name of the job",
                },
                "type": {
                    "type": "string",
                    "description": "Type of job (UPLOAD, TRANSCODE, ANALYSIS, etc.)",
                },
                "object_id": {
                    "type": "string",
                    "description": "ID of the object this job is for",
                },
                "object_type": {
                    "type": "string",
                    "description": "Type of object (assets, collections)",
                },
                "metadata": {
                    "type": "object",
                    "description": "Additional job metadata",
                },
            },
            "required": ["title", "type"],
        },
    ),
    Tool(
        name="iconik_update_job",
        description="Update a job's status or progress.",
        inputSchema={
            "type": "object",
            "properties": {
                "job_id": {
                    "type": "string",
                    "description": "The unique ID of the job",
                },
                "status": {
                    "type": "string",
                    "description": "New status for the job",
                    "enum": ["PENDING", "IN_PROGRESS", "FINISHED", "FAILED"],
                },
                "progress": {
                    "type": "number",
                    "description": "Progress percentage (0-100)",
                    "minimum": 0,
                    "maximum": 100,
                },
                "message": {
                    "type": "string",
                    "description": "Status message or error description",
                },
            },
            "required": ["job_id"],
        },
    ),
]
