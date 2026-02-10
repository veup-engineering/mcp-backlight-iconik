"""MCP server for Iconik API with SSE and HTTP transport support."""

import asyncio
import json
import logging
import os
import sys
from contextlib import asynccontextmanager
from typing import Any

from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.server.streamable_http import StreamableHTTPServerTransport
from mcp.types import TextContent, Tool
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Mount, Route

from .client import IconikClient
from .tools import ALL_TOOLS

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("mcp-iconik")


class IconikMCPServer:
    """MCP server providing Iconik API tools."""

    def __init__(self):
        self.server = Server("mcp-iconik")
        self.client: IconikClient | None = None
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up MCP server handlers."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Return list of available tools."""
            return ALL_TOOLS

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """Handle tool calls."""
            try:
                result = await self._execute_tool(name, arguments)
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            except Exception as e:
                logger.exception(f"Error executing tool {name}")
                return [TextContent(type="text", text=json.dumps({"error": str(e)}))]

    async def _get_client(self) -> IconikClient:
        """Get or create the Iconik client."""
        if self.client is None:
            self.client = IconikClient()
        return self.client

    async def _execute_tool(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        """Execute a tool by name with given arguments."""
        client = await self._get_client()

        # Asset tools
        if name == "iconik_list_assets":
            return await client.list_assets(
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
                sort=args.get("sort"),
            )
        elif name == "iconik_get_asset":
            return await client.get_asset(args["asset_id"])
        elif name == "iconik_create_asset":
            data = {k: v for k, v in args.items() if v is not None}
            return await client.create_asset(data)
        elif name == "iconik_update_asset":
            asset_id = args.pop("asset_id")
            data = {k: v for k, v in args.items() if v is not None}
            return await client.update_asset(asset_id, data)
        elif name == "iconik_delete_asset":
            return await client.delete_asset(args["asset_id"])

        # Collection tools
        elif name == "iconik_list_collections":
            return await client.list_collections(
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
                sort=args.get("sort"),
            )
        elif name == "iconik_get_collection":
            return await client.get_collection(args["collection_id"])
        elif name == "iconik_create_collection":
            data = {k: v for k, v in args.items() if v is not None}
            return await client.create_collection(data)
        elif name == "iconik_update_collection":
            collection_id = args.pop("collection_id")
            data = {k: v for k, v in args.items() if v is not None}
            return await client.update_collection(collection_id, data)
        elif name == "iconik_delete_collection":
            return await client.delete_collection(args["collection_id"])
        elif name == "iconik_get_collection_contents":
            return await client.get_collection_contents(
                args["collection_id"],
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
            )
        elif name == "iconik_add_to_collection":
            return await client.add_to_collection(
                args["collection_id"],
                args["object_ids"],
                args.get("object_type", "assets"),
            )

        # Search tools
        elif name == "iconik_search":
            return await client.search(
                query=args.get("query"),
                filter_data=args.get("filter"),
                doc_types=args.get("doc_types"),
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
                sort=args.get("sort"),
            )
        elif name == "iconik_list_saved_searches":
            return await client.list_saved_searches(
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
            )
        elif name == "iconik_get_saved_search":
            return await client.get_saved_search(
                args["search_id"],
                include_results=args.get("include_results", True),
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
            )
        elif name == "iconik_create_saved_search":
            return await client.create_saved_search(args["name"], args["criteria"])
        elif name == "iconik_delete_saved_search":
            return await client.delete_saved_search(args["search_id"])

        # File tools
        elif name == "iconik_list_storages":
            return await client.list_storages(
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
            )
        elif name == "iconik_get_storage":
            return await client.get_storage(args["storage_id"])
        elif name == "iconik_get_asset_files":
            return await client.get_asset_files(
                args["asset_id"],
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
            )
        elif name == "iconik_get_asset_formats":
            return await client.get_asset_formats(
                args["asset_id"],
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
            )
        elif name == "iconik_get_asset_proxies":
            return await client.get_asset_proxies(args["asset_id"])
        elif name == "iconik_get_asset_keyframes":
            return await client.get_asset_keyframes(args["asset_id"])

        # Metadata tools
        elif name == "iconik_list_metadata_views":
            return await client.list_metadata_views(
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
            )
        elif name == "iconik_get_metadata_view":
            return await client.get_metadata_view(args["view_id"])
        elif name == "iconik_get_asset_metadata":
            return await client.get_asset_metadata(args["asset_id"])
        elif name == "iconik_update_asset_metadata":
            return await client.update_asset_metadata(
                args["asset_id"],
                args["view_id"],
                {"metadata_values": args["metadata_values"]},
            )

        # Job tools
        elif name == "iconik_list_jobs":
            return await client.list_jobs(
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
                status=args.get("status"),
            )
        elif name == "iconik_get_job":
            return await client.get_job(args["job_id"])
        elif name == "iconik_create_job":
            data = {k: v for k, v in args.items() if v is not None}
            return await client.create_job(data)
        elif name == "iconik_update_job":
            job_id = args.pop("job_id")
            data = {k: v for k, v in args.items() if v is not None}
            return await client.update_job(job_id, data)

        # User tools
        elif name == "iconik_list_users":
            return await client.list_users(
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
            )
        elif name == "iconik_get_user":
            return await client.get_user(args["user_id"])
        elif name == "iconik_get_current_user":
            return await client.get_current_user()
        elif name == "iconik_list_groups":
            return await client.list_groups(
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
            )
        elif name == "iconik_get_group":
            return await client.get_group(args["group_id"])
        elif name == "iconik_list_shares":
            return await client.list_shares(
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
            )
        elif name == "iconik_get_share":
            return await client.get_share(args["share_id"])
        elif name == "iconik_list_projects":
            return await client.list_projects(
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
            )
        elif name == "iconik_get_project":
            return await client.get_project(args["project_id"])
        elif name == "iconik_list_webhooks":
            return await client.list_webhooks(
                page=args.get("page", 1),
                per_page=args.get("per_page", 50),
            )
        elif name == "iconik_get_webhook":
            return await client.get_webhook(args["webhook_id"])

        # Generic tools
        elif name == "iconik_api_request":
            return await client.api_request(
                method=args["method"],
                path=args["path"],
                params=args.get("params"),
                body=args.get("body"),
            )
        elif name == "iconik_get_acls":
            return await client.get_acls(args["object_type"], args["object_id"])
        elif name == "iconik_update_acls":
            return await client.update_acls(
                args["object_type"],
                args["object_id"],
                {"acl_entries": args["acl_entries"]},
            )

        else:
            raise ValueError(f"Unknown tool: {name}")

    async def cleanup(self):
        """Clean up resources."""
        if self.client:
            await self.client.close()


# Global server instance
mcp_server = IconikMCPServer()


def create_sse_app() -> Starlette:
    """Create Starlette app with SSE transport."""
    sse_transport = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> Response:
        """Handle SSE connections."""
        async with sse_transport.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await mcp_server.server.run(
                streams[0], streams[1], mcp_server.server.create_initialization_options()
            )
        return Response()

    async def handle_messages(request: Request) -> Response:
        """Handle SSE messages."""
        await sse_transport.handle_post_message(request.scope, request.receive, request._send)
        return Response()

    @asynccontextmanager
    async def lifespan(app: Starlette):
        """App lifespan handler."""
        logger.info("Starting MCP Iconik server (SSE mode)")
        yield
        await mcp_server.cleanup()
        logger.info("Shutting down MCP Iconik server")

    return Starlette(
        debug=os.getenv("DEBUG", "").lower() == "true",
        lifespan=lifespan,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Route("/messages/", endpoint=handle_messages, methods=["POST"]),
        ],
    )


def create_http_app() -> Starlette:
    """Create Starlette app with streamable HTTP transport."""

    async def handle_mcp(request: Request) -> Response:
        """Handle MCP HTTP requests."""
        transport = StreamableHTTPServerTransport(
            mcp_session_id=request.headers.get("mcp-session-id"),
        )

        async with transport.connect(
            request.scope, request.receive, request._send
        ) as streams:
            await mcp_server.server.run(
                streams[0], streams[1], mcp_server.server.create_initialization_options()
            )
        return Response()

    async def health_check(request: Request) -> JSONResponse:
        """Health check endpoint."""
        return JSONResponse({"status": "healthy", "service": "mcp-iconik"})

    @asynccontextmanager
    async def lifespan(app: Starlette):
        """App lifespan handler."""
        logger.info("Starting MCP Iconik server (HTTP mode)")
        yield
        await mcp_server.cleanup()
        logger.info("Shutting down MCP Iconik server")

    return Starlette(
        debug=os.getenv("DEBUG", "").lower() == "true",
        lifespan=lifespan,
        routes=[
            Route("/mcp", endpoint=handle_mcp, methods=["POST"]),
            Route("/health", endpoint=health_check, methods=["GET"]),
        ],
    )


def create_combined_app() -> Starlette:
    """Create Starlette app supporting both SSE and HTTP transports."""
    sse_transport = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> Response:
        """Handle SSE connections."""
        async with sse_transport.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await mcp_server.server.run(
                streams[0], streams[1], mcp_server.server.create_initialization_options()
            )
        return Response()

    async def handle_messages(request: Request) -> Response:
        """Handle SSE messages."""
        await sse_transport.handle_post_message(request.scope, request.receive, request._send)
        return Response()

    async def handle_mcp(request: Request) -> Response:
        """Handle MCP HTTP requests."""
        transport = StreamableHTTPServerTransport(
            mcp_session_id=request.headers.get("mcp-session-id"),
        )

        async with transport.connect(
            request.scope, request.receive, request._send
        ) as streams:
            await mcp_server.server.run(
                streams[0], streams[1], mcp_server.server.create_initialization_options()
            )
        return Response()

    async def health_check(request: Request) -> JSONResponse:
        """Health check endpoint."""
        return JSONResponse({
            "status": "healthy",
            "service": "mcp-iconik",
            "transports": ["sse", "http"],
        })

    @asynccontextmanager
    async def lifespan(app: Starlette):
        """App lifespan handler."""
        logger.info("Starting MCP Iconik server (combined SSE + HTTP mode)")
        yield
        await mcp_server.cleanup()
        logger.info("Shutting down MCP Iconik server")

    return Starlette(
        debug=os.getenv("DEBUG", "").lower() == "true",
        lifespan=lifespan,
        routes=[
            # SSE transport endpoints
            Route("/sse", endpoint=handle_sse),
            Route("/messages/", endpoint=handle_messages, methods=["POST"]),
            # Streamable HTTP transport endpoint
            Route("/mcp", endpoint=handle_mcp, methods=["POST"]),
            # Health check
            Route("/health", endpoint=health_check, methods=["GET"]),
        ],
    )


# Create the combined app for uvicorn
app = create_combined_app()


def main():
    """Run the MCP server."""
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    logger.info(f"Starting MCP Iconik server on {host}:{port}")
    logger.info("SSE endpoint: /sse")
    logger.info("HTTP endpoint: /mcp")
    logger.info("Health check: /health")

    uvicorn.run(
        "mcp_iconik.server:app",
        host=host,
        port=port,
        reload=os.getenv("RELOAD", "").lower() == "true",
    )


if __name__ == "__main__":
    main()
