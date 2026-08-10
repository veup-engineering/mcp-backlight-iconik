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

## Repo-Local Wrapper Requirement
If a client repo wraps the shared `scripts/iconik-mcp.sh`, the wrapper must export:
- `ICONIK_PROFILE_FILE`
- `ICONIK_PROFILES_INDEX`

Those should point at repo-local files before delegating to the shared script. If not, commands like `status`, `ensure`, and `profile use` can silently read the workspace-wide active profile instead of the client repo profile.

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

## Asset Player Timecode Metadata
Iconik's player-visible source timecode can be reconstructed from file format metadata:

```bash
GET /API/files/v1/assets/{asset_id}/versions/{version_id}/formats/?per_page=100
```

Use the video stream component, usually the component where `format=ProRes`, rather than only the
container-level metadata. Useful component metadata fields include:
- `delay_string[4]`: start timecode displayed by the player, for example `13:00:57;39`
- `delay_string[5]`: UI-friendly start, for example `13:00:57.708 (13:00:57;39)`
- `delay`, `delay_dropframe`, and `delay_settings`
- `frame_rate`, `framerate_num`, `framerate_den`
- `frame_count`
- `duration_string[4]`

To match Iconik's displayed end timecode for a file, compute `start_frame + frame_count - 1`.
For run-of-day matching against external logs, compare the visible wall-clock timecode value first;
do not let drop-frame math create large noon/afternoon drift when one source uses `:` and the other
uses `;`.

## Segment Timing Interpretation

Read comments and timed metadata together from:

```bash
GET /API/assets/v1/assets/{asset_id}/segments/?page=1&per_page=100
```

- The response `objects` can mix `COMMENT`, `GENERIC`, and other segment types.
- A point comment normally has equal `time_start_milliseconds` and `time_end_milliseconds`.
- A `GENERIC` timed-metadata row can be an interval around an event mark. Do not treat its start as
  the event time. For a symmetric interval, compare the midpoint with the point comment; otherwise
  read the source mark from the segment metadata view.
- Page size may be capped by the API. Count returned objects and paginate instead of assuming a large
  `per_page` value returned the complete asset timeline.

## Troubleshooting
1. If startup fails, inspect:
```bash
tail -n 200 ./.iconik-mcp.log
```
2. If health briefly succeeds and then drops inside Codex/agent execution:
  - verify whether the daemon was reaped after the parent command exited
  - re-test with a foreground run (`cd mcp-backlight-iconik && uv run mcp-iconik`) to separate credential issues from process-lifecycle issues
2. If auth is wrong after switching profile:
  - Confirm active profile in `./.iconik-profile`
  - Re-run profile switch
  - Verify using `iconik_get_connection_context`

## Registry Tracking
Local wrapper supports per-profile registry CSV sync for IDs and mappings.

- Auto-sync triggers:
  - `./scripts/iconik-mcp.sh ensure [profile]`
  - `./scripts/iconik-mcp.sh profile use <name>`
- Manual sync:
  - `./scripts/iconik-mcp.sh registry sync [profile]`
- Output path:
  - `docs/iconik/registry/iconik_registry_<profile>.csv`
- Disable auto-sync:
  - `ICONIK_AUTO_SYNC_REGISTRY=0`


## External Storage Attachment
For Backblaze and other S3-compatible buckets, the safe workflow is:

1. Keep raw credentials out of git and load them from a local secrets file or Keychain.
2. Inspect the local OpenAPI spec in `docs/iconik_swagger_defs/files.json`:
  - `POST /API/files/v1/storages/verifications/access/`
  - `POST /API/files/v1/storages/`
  - `POST /API/files/v1/storages/{storage_id}/default/`
3. Preflight the candidate settings with `storages/verifications/access`.
4. Create the storage only after access verification passes.
5. Set the created storage as the default for its purpose by storage ID.
6. Read back `GET /API/files/v1/storages/?per_page=100` and `GET /API/files/v1/storages/{purpose}/default/` to confirm tenant state.

Known-good pattern:
- Backblaze can work either as S3-compatible `S3` or native `B2`.
- For native `B2`, the working live mapping is `account_id` => Backblaze application key ID and `authorization_token` => Backblaze application key.
- Do not assume `authorization_token` means a short-lived token from `b2_authorize_account`; that failed live validation for persistent storage creation.
- Do not assume `method: B2` or `method: S3` without verification against the credential shape you actually have.
