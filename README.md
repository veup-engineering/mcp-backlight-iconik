# MCP Iconik

MCP (Model Context Protocol) server providing tools for the [Iconik](https://iconik.io) media asset management API.

## Features

- **Dual Transport Support**: Both SSE (Server-Sent Events) and Streamable HTTP transports
- **Docker Ready**: Runs as a containerized service
- **Comprehensive API Coverage**: Tools for all major Iconik API endpoints
- **Claude Code CLI Compatible**: Works with Claude Code CLI
- **LMStudio Compatible**: Works with LMStudio via HTTP transport

## Available Tools

### Assets
- `iconik_list_assets` - List assets with pagination
- `iconik_get_asset` - Get asset details
- `iconik_create_asset` - Create new asset
- `iconik_update_asset` - Update asset properties
- `iconik_delete_asset` - Delete an asset

### Collections
- `iconik_list_collections` - List collections
- `iconik_get_collection` - Get collection details
- `iconik_create_collection` - Create new collection
- `iconik_update_collection` - Update collection
- `iconik_delete_collection` - Delete collection
- `iconik_get_collection_contents` - Get collection contents
- `iconik_add_to_collection` - Add items to collection

### Search
- `iconik_search` - Search assets and collections
- `iconik_list_saved_searches` - List saved searches
- `iconik_get_saved_search` - Get/execute saved search
- `iconik_create_saved_search` - Create saved search
- `iconik_delete_saved_search` - Delete saved search

### Files & Storage
- `iconik_list_storages` - List storage locations
- `iconik_get_storage` - Get storage details
- `iconik_get_asset_files` - Get asset files
- `iconik_get_asset_formats` - Get asset formats
- `iconik_get_asset_proxies` - Get asset proxies
- `iconik_get_asset_keyframes` - Get asset keyframes

### Metadata
- `iconik_list_metadata_views` - List metadata views
- `iconik_get_metadata_view` - Get metadata view
- `iconik_get_asset_metadata` - Get asset metadata
- `iconik_update_asset_metadata` - Update asset metadata

### Jobs
- `iconik_list_jobs` - List jobs
- `iconik_get_job` - Get job details
- `iconik_create_job` - Create job
- `iconik_update_job` - Update job

### Users & Groups
- `iconik_list_users` - List users
- `iconik_get_user` - Get user details
- `iconik_get_current_user` - Get current user
- `iconik_list_groups` - List groups
- `iconik_get_group` - Get group details
- `iconik_list_shares` - List shares
- `iconik_get_share` - Get share details
- `iconik_list_projects` - List projects
- `iconik_get_project` - Get project details
- `iconik_list_webhooks` - List webhooks
- `iconik_get_webhook` - Get webhook details

### Generic
- `iconik_api_request` - Make generic API requests
- `iconik_get_acls` - Get object ACLs
- `iconik_update_acls` - Update object ACLs

## Quick Start

### Using Docker Compose

1. Create a `.env` file with your Iconik credentials:

```bash
# Option 1: Use JWT API token
ICONIK_API=your_jwt_token_here

# Option 2: Use App ID and Auth Token
ICONIK_APP_ID=your_app_id
ICONIK_AUTH_TOKEN=your_auth_token

# Optional: Custom Iconik URL (default: https://app.iconik.io)
ICONIK_URL=https://app.iconik.io
```

2. Build and run:

```bash
docker-compose up -d
```

3. The server will be available at:
   - SSE endpoint: `http://localhost:8000/sse`
   - HTTP endpoint: `http://localhost:8000/mcp`
   - Health check: `http://localhost:8000/health`

### Using Docker Directly

```bash
docker build -t mcp-iconik .
docker run -d \
  -p 8000:8000 \
  -e ICONIK_API=your_jwt_token \
  --name mcp-iconik \
  mcp-iconik
```

### Local Development

```bash
# Install dependencies
pip install -e .

# Run the server
python -m mcp_iconik.server
```

## Configuration with Claude Code CLI

Add to your Claude Code configuration (`~/.claude/mcp.json`):

```json
{
  "mcpServers": {
    "iconik": {
      "url": "http://localhost:8000/sse",
      "transport": "sse"
    }
  }
}
```

Or for HTTP transport:

```json
{
  "mcpServers": {
    "iconik": {
      "url": "http://localhost:8000/mcp",
      "transport": "http"
    }
  }
}
```

## Configuration with LMStudio

LMStudio uses HTTP transport. Configure the MCP server URL as:

```
http://localhost:8000/mcp
```

## API Endpoints

| Endpoint | Transport | Description |
|----------|-----------|-------------|
| `/sse` | SSE | Server-Sent Events connection |
| `/messages/` | SSE | SSE message handler |
| `/mcp` | HTTP | Streamable HTTP transport |
| `/health` | HTTP | Health check endpoint |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ICONIK_API` | JWT API token (preferred) | - |
| `ICONIK_APP_ID` | Application ID | - |
| `ICONIK_AUTH_TOKEN` | Auth token | - |
| `ICONIK_URL` | Iconik base URL | `https://app.iconik.io` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Enable debug mode | `false` |

## Getting Iconik Credentials

1. Log in to your Iconik instance
2. Go to Admin Panel > Settings > Application Tokens
3. Create a new application or use an existing one
4. Create a new authentication token
5. Copy the App ID and token

## License

MIT
