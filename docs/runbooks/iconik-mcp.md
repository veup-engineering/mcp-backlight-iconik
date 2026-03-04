# Iconik MCP Runbook (Canonical)

## Scope
This runbook is the canonical operational guide for the `mcp-backlight-iconik` server.

## Startup And Health
1. Start/ensure local server from workspace root:
```bash
./scripts/iconik-mcp.sh ensure
```
2. Check health:
```bash
curl -sS http://localhost:8000/health
```
3. Check MCP endpoint:
```bash
curl -sS -o /tmp/iconik_mcp_http.out -w '%{http_code}\n' http://localhost:8000/mcp
```

## Profile/Account Verification
After switching profiles, verify active account context through MCP:
- Tool: `iconik_get_connection_context`
- Includes:
  - `base_url`
  - `auth_mode`
  - `app_id`
  - `token_fingerprint`
  - optional `current_user`

This makes account mismatches detectable without opening browser devtools.

## Schema Inspection (No Browser Needed)
Use schema tools to inspect request/response shapes from local OpenAPI specs:
- `iconik_list_api_specs`
- `iconik_list_api_operations`
- `iconik_get_api_operation_schema`
- `iconik_get_api_component_schema`
- `iconik_resolve_api_ref`

Default spec source resolution order:
1. `ICONIK_OPENAPI_DIR` (if set)
2. `mcp-backlight-iconik/docs/iconik_swagger_defs`
3. `mcp-backlight-iconik/docs/iconik`
4. workspace root `docs/iconik_swagger_defs` / `docs/iconik`

## Troubleshooting
1. If startup fails, inspect:
```bash
tail -n 200 ./.iconik-mcp.log
```
2. If auth is wrong after switching profile:
  - Confirm active profile in `./.iconik-profile`
  - Re-run profile switch
  - Verify using `iconik_get_connection_context`
