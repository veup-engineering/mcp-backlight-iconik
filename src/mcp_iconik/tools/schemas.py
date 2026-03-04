"""OpenAPI schema and connection-context tools for Iconik MCP."""

from typing import Any, Optional

from mcp.server.fastmcp import FastMCP

from ..client import IconikClient
from ..spec_catalog import IconikSpecCatalog


def register_schema_tools(mcp: FastMCP, client: IconikClient) -> None:
    """Register tools that expose API shapes and active auth context."""

    @mcp.tool(structured_output=True)
    async def iconik_get_connection_context(
        include_current_user: bool = True,
    ) -> dict[str, Any]:
        """Return non-secret runtime/auth context for the currently running Iconik MCP server.

        Use this to confirm which account/domain/profile the MCP is actually using.

        Args:
            include_current_user: When true, includes current user identity from the API.
        """
        return await client.get_connection_context(include_current_user=include_current_user)

    @mcp.tool(structured_output=True)
    async def iconik_list_api_specs() -> dict[str, Any]:
        """List bundled Iconik OpenAPI spec groups available for schema lookup.

        Returns:
            Available spec names and resolved source directory.
        """
        catalog = IconikSpecCatalog()
        specs = catalog.list_specs()
        return {
            "source_dir": str(catalog.spec_dir),
            "spec_count": len(specs),
            "specs": sorted(specs.keys()),
        }

    @mcp.tool(structured_output=True)
    async def iconik_list_api_operations(
        spec: str,
        path_prefix: Optional[str] = None,
        limit: int = 200,
    ) -> dict[str, Any]:
        """List operation stubs for one OpenAPI spec.

        Args:
            spec: Spec name such as assets, search, files, metadata.
            path_prefix: Optional path filter, e.g. '/v1/assets/'.
            limit: Maximum number of operations to return.
        """
        operations = IconikSpecCatalog().list_operations(spec=spec, path_prefix=path_prefix, limit=limit)
        return {
            "spec": spec.removesuffix(".json"),
            "operation_count": len(operations),
            "operations": operations,
        }

    @mcp.tool(structured_output=True)
    async def iconik_get_api_operation_schema(
        spec: str,
        path: str,
        method: str = "get",
    ) -> dict[str, Any]:
        """Get request/response schema details for a specific API operation.

        Args:
            spec: Spec name such as assets, search, files, metadata.
            path: OpenAPI path key exactly as defined in the spec (e.g. '/v1/assets/').
            method: HTTP method (GET, POST, PUT, PATCH, DELETE).
        """
        return IconikSpecCatalog().get_operation(spec=spec, path=path, method=method)

    @mcp.tool(structured_output=True)
    async def iconik_get_api_component_schema(
        spec: str,
        schema_name: str,
    ) -> dict[str, Any]:
        """Get a named component schema from an Iconik OpenAPI spec.

        Args:
            spec: Spec name such as assets, search, files, metadata.
            schema_name: Schema name under components.schemas.
        """
        return IconikSpecCatalog().get_component_schema(spec=spec, schema_name=schema_name)

    @mcp.tool(structured_output=True)
    async def iconik_resolve_api_ref(
        spec: str,
        ref: str,
    ) -> dict[str, Any]:
        """Resolve a local OpenAPI $ref pointer from a spec.

        Args:
            spec: Spec name such as assets, search, files, metadata.
            ref: Local JSON pointer ref (e.g. '#/components/schemas/AssetBaseSchema').
        """
        return IconikSpecCatalog().resolve_ref(spec=spec, ref=ref)
