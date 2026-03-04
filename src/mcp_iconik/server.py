"""MCP server for Iconik API with SSE and Streamable HTTP transport support.

This module sets up the FastMCP server with both Streamable HTTP and SSE transports
for use with OpenWebUI, Claude Code, and other MCP-compatible clients.
"""

import contextlib

import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from mcp.server.transport_security import TransportSecuritySettings
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response
from starlette.routing import Mount, Route

from .client import IconikClient
from .config import settings
from .tools import register_all_tools

# Transport security settings - disable DNS rebinding protection for browser clients
# We're behind a reverse proxy and need to accept requests from any origin
security_settings = TransportSecuritySettings(
    enable_dns_rebinding_protection=False,
)

# Create FastMCP instance with stateless HTTP mode and permissive security
mcp = FastMCP(
    name="mcp-iconik",
    stateless_http=True,
    transport_security=security_settings,
)

# Initialize shared Iconik client (singleton pattern)
iconik_client = IconikClient()

# Register all tools with the MCP server
register_all_tools(mcp, iconik_client)

# Get the MCP ASGI app for Streamable HTTP transport
mcp_app = mcp.streamable_http_app()

# SSE transport for Claude Code and other SSE-based clients
sse_transport = SseServerTransport("/sse/messages/")


async def handle_sse(request):
    """Handle SSE connection requests.

    Clients connect to /sse to establish an SSE stream, then POST messages
    to /sse/messages/?session_id=xxx to communicate with the server.
    """
    async with sse_transport.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await mcp._mcp_server.run(
            streams[0],
            streams[1],
            mcp._mcp_server.create_initialization_options(),
        )
    return Response()


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    """Lifespan context manager to initialize MCP session manager."""
    async with mcp.session_manager.run():
        yield


async def health(request):
    """Health check / liveness probe endpoint."""
    return JSONResponse({"status": "healthy"})


async def ready(request):
    """Readiness probe endpoint."""
    return JSONResponse({"status": "ready"})


async def openapi_json(request):
    """OpenAPI schema endpoint for OpenWebUI compatibility.

    Returns a minimal OpenAPI spec that describes the MCP server.
    OpenWebUI may check this endpoint when connecting to MCP servers.
    """
    tools = []
    for tool in mcp._tool_manager.list_tools():
        tools.append({
            "name": tool.name,
            "description": tool.description or "",
            "input_schema": tool.parameters,
            "output_schema": tool.output_schema,
        })

    return JSONResponse({
        "openapi": "3.1.0",
        "info": {
            "title": "Iconik MCP Server",
            "description": "MCP server exposing 45+ Iconik tools via HTTP and SSE",
            "version": "1.0.0",
        },
        "servers": [{"url": "/"}],
        "paths": {
            "/mcp": {
                "post": {
                    "summary": "Streamable HTTP MCP endpoint",
                    "description": "Streamable HTTP MCP endpoint for tool invocation (OpenWebUI)",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"type": "object"}
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "MCP response (JSON or SSE stream)"}
                    },
                }
            },
            "/sse": {
                "get": {
                    "summary": "SSE MCP endpoint",
                    "description": "SSE MCP endpoint for Claude Code",
                    "responses": {
                        "200": {
                            "description": "SSE stream with MCP messages",
                            "content": {"text/event-stream": {}},
                        }
                    },
                }
            },
        },
        "x-mcp-tools": tools,
    })


# CORS middleware for browser-based clients like OpenWebUI and Claude Code
cors_middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Cache-Control",
            "mcp-protocol-version",
            "mcp-session-id",
        ],
        expose_headers=["mcp-session-id", "Content-Type"],
    )
]

# Create the main app with health routes and MCP mounted
app = Starlette(
    routes=[
        Route("/health", health),
        Route("/ready", ready),
        Route("/openapi.json", openapi_json),
        # SSE transport endpoints for Claude Code compatibility
        Route("/sse", endpoint=handle_sse),
        Mount("/sse/messages/", app=sse_transport.handle_post_message),
        # Streamable HTTP transport (default)
        Mount("/", app=mcp_app),
    ],
    middleware=cors_middleware,
    lifespan=lifespan,
)


def main() -> None:
    """Run the MCP server with both Streamable HTTP and SSE transports."""
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
    )


if __name__ == "__main__":
    main()
