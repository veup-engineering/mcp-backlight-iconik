"""Job tools for Iconik MCP."""

from typing import Any, Optional

from mcp.server.fastmcp import FastMCP

from ..client import IconikClient


def register_job_tools(mcp: FastMCP, client: IconikClient) -> None:
    """Register job-related tools."""

    @mcp.tool()
    async def iconik_list_jobs(
        page: int = 1,
        per_page: int = 50,
        status: Optional[str] = None,
    ) -> dict:
        """List jobs in Iconik (uploads, transcodes, analysis, etc.).

        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
            status: Filter by status (PENDING, IN_PROGRESS, FINISHED, FAILED)
        """
        return await client.list_jobs(page=page, per_page=per_page, status=status)

    @mcp.tool()
    async def iconik_get_job(job_id: str) -> dict:
        """Get details of a specific job including its progress and status.

        Args:
            job_id: The unique ID of the job
        """
        return await client.get_job(job_id)

    @mcp.tool()
    async def iconik_create_job(
        title: str,
        type: str,
        object_id: Optional[str] = None,
        object_type: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict:
        """Create a new job in Iconik.

        Args:
            title: Title/name of the job
            type: Type of job (UPLOAD, TRANSCODE, ANALYSIS, etc.)
            object_id: ID of the object this job is for
            object_type: Type of object (assets, collections)
            metadata: Additional job metadata
        """
        data: dict[str, Any] = {"title": title, "type": type}
        if object_id is not None:
            data["object_id"] = object_id
        if object_type is not None:
            data["object_type"] = object_type
        if metadata is not None:
            data["metadata"] = metadata
        return await client.create_job(data)

    @mcp.tool()
    async def iconik_update_job(
        job_id: str,
        status: Optional[str] = None,
        progress: Optional[float] = None,
        message: Optional[str] = None,
    ) -> dict:
        """Update a job's status or progress.

        Args:
            job_id: The unique ID of the job
            status: New status for the job (PENDING, IN_PROGRESS, FINISHED, FAILED)
            progress: Progress percentage (0-100)
            message: Status message or error description
        """
        data: dict[str, Any] = {}
        if status is not None:
            data["status"] = status
        if progress is not None:
            data["progress"] = progress
        if message is not None:
            data["message"] = message
        return await client.update_job(job_id, data)
