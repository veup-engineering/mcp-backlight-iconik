# PR Summary: Iconik MCP Hardening + Schema Helpers

## What This PR Does
- Adds schema helper tools that read local Iconik Swagger/OpenAPI JSON definitions.
- Adds a connection-context tool to confirm active account/domain context without browser inspection.
- Enables structured output for all existing tools so MCP clients can consume `outputSchema` + `structuredContent`.
- Extends `/openapi.json` metadata to include each tool's input/output schema.
- Adds a canonical runbook under `docs/runbooks/`.

## New Tools
- `iconik_get_connection_context`
- `iconik_list_api_specs`
- `iconik_list_api_operations`
- `iconik_get_api_operation_schema`
- `iconik_get_api_component_schema`
- `iconik_resolve_api_ref`

## Key Implementation Notes
- Spec directory auto-resolution order:
  1. `ICONIK_OPENAPI_DIR`
  2. `docs/iconik_swagger_defs`
  3. `docs/iconik`
  4. workspace fallback paths
- Missing credentials are now reported on API request execution (not on module import), preserving startup compatibility.
- Existing tool names and request arguments remain unchanged.

## Validation Performed
- `uv run python -m compileall src`
- Runtime tool registration check (`tool_count` and new tools present)
- Spec catalog resolution check confirms `docs/iconik_swagger_defs` is selected by default when present

## Backward Compatibility
- Existing tool names preserved.
- Existing tool parameters preserved.
- Response format now includes structured output metadata; content remains compatible.

## Suggested Follow-Up
- Add lightweight tests for spec catalog parsing and schema helper tool behavior.
- Add sample prompt snippets in README for common schema lookup tasks.
