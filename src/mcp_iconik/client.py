"""Iconik API client wrapper."""

import base64
import hashlib
import json
import os
from typing import Any

import httpx


class IconikClient:
    """Client for interacting with the Iconik API."""

    def __init__(
        self,
        base_url: str | None = None,
        app_id: str | None = None,
        auth_token: str | None = None,
        api_token: str | None = None,
    ):
        """Initialize the Iconik client.

        Args:
            base_url: Iconik API base URL (default: https://app.iconik.io)
            app_id: Application ID for authentication
            auth_token: Authentication token
            api_token: JWT API token (alternative to app_id/auth_token)
        """
        self.base_url = (base_url or os.getenv("ICONIK_URL", "https://app.iconik.io")).rstrip("/")

        # Support both JWT token and app_id/auth_token authentication
        if api_token or os.getenv("ICONIK_API"):
            token = api_token or os.getenv("ICONIK_API", "")
            payload = self._decode_jwt_payload(token)
            self.app_id = payload.get("app_id", "")
            # Use the full JWT as the Auth-Token
            self.auth_token = token
            self.auth_mode = "jwt"
        else:
            self.app_id = app_id or os.getenv("ICONIK_APP_ID", "")
            self.auth_token = auth_token or os.getenv("ICONIK_AUTH_TOKEN", "")
            self.auth_mode = "app_token"

        self.has_credentials = bool(self.app_id and self.auth_token)

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self._get_headers(),
            timeout=60.0,
        )

    def _decode_jwt_payload(self, token: str) -> dict[str, Any]:
        """Decode JWT payload without verification."""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return {}
            payload = parts[1]
            # Add padding if needed
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += "=" * padding
            decoded = base64.urlsafe_b64decode(payload)
            return json.loads(decoded)
        except Exception:
            return {}

    def _get_headers(self) -> dict[str, str]:
        """Get default headers for API requests."""
        return {
            "App-ID": self.app_id,
            "Auth-Token": self.auth_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _token_fingerprint(self) -> str:
        """Get a short token fingerprint for profile verification."""
        return hashlib.sha256(self.auth_token.encode("utf-8")).hexdigest()[:12]

    async def get_connection_context(self, include_current_user: bool = True) -> dict[str, Any]:
        """Return non-secret auth/runtime context to verify active account."""
        context: dict[str, Any] = {
            "base_url": self.base_url,
            "auth_mode": self.auth_mode,
            "app_id": self.app_id,
            "token_fingerprint": self._token_fingerprint(),
            "has_credentials": self.has_credentials,
        }

        if self.auth_mode == "jwt":
            payload = self._decode_jwt_payload(self.auth_token)
            context["jwt_claims"] = {
                "app_id": payload.get("app_id"),
                "exp": payload.get("exp"),
                "sys": payload.get("sys"),
                "id": payload.get("id"),
            }

        if include_current_user:
            user = await self.get_current_user()
            context["current_user"] = {
                "id": user.get("id"),
                "email": user.get("email"),
                "username": user.get("username"),
                "name": user.get("name"),
            }

        return context

    async def request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an API request.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            path: API path (e.g., /API/assets/v1/assets/)
            params: Query parameters
            json_data: JSON request body

        Returns:
            API response as dictionary
        """
        if not self.has_credentials:
            raise ValueError(
                "Iconik credentials are missing. Set ICONIK_API or ICONIK_APP_ID and ICONIK_AUTH_TOKEN."
            )

        # Ensure path starts with /API/
        if not path.startswith("/API/"):
            path = f"/API/{path.lstrip('/')}"

        # Ensure path ends with /
        if not path.endswith("/") and "?" not in path:
            path = f"{path}/"

        response = await self._client.request(
            method=method.upper(),
            url=path,
            params=params,
            json=json_data,
        )

        if response.status_code == 204:
            return {"success": True, "status_code": 204}

        try:
            return response.json()
        except Exception:
            return {
                "status_code": response.status_code,
                "text": response.text,
            }

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()

    # Assets API
    async def list_assets(
        self,
        page: int = 1,
        per_page: int = 50,
        sort: str | None = None,
    ) -> dict[str, Any]:
        """List assets."""
        params = {"page": page, "per_page": per_page}
        if sort:
            params["sort"] = sort
        return await self.request("GET", "/API/assets/v1/assets/", params=params)

    async def get_asset(self, asset_id: str) -> dict[str, Any]:
        """Get a specific asset."""
        return await self.request("GET", f"/API/assets/v1/assets/{asset_id}/")

    async def create_asset(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new asset."""
        return await self.request("POST", "/API/assets/v1/assets/", json_data=data)

    async def update_asset(self, asset_id: str, data: dict[str, Any]) -> dict[str, Any]:
        """Update an asset."""
        return await self.request("PATCH", f"/API/assets/v1/assets/{asset_id}/", json_data=data)

    async def delete_asset(self, asset_id: str) -> dict[str, Any]:
        """Delete an asset."""
        return await self.request("DELETE", f"/API/assets/v1/assets/{asset_id}/")

    # Collections API
    async def list_collections(
        self,
        page: int = 1,
        per_page: int = 50,
        sort: str | None = None,
    ) -> dict[str, Any]:
        """List collections."""
        params = {"page": page, "per_page": per_page}
        if sort:
            params["sort"] = sort
        return await self.request("GET", "/API/assets/v1/collections/", params=params)

    async def get_collection(self, collection_id: str) -> dict[str, Any]:
        """Get a specific collection."""
        return await self.request("GET", f"/API/assets/v1/collections/{collection_id}/")

    async def create_collection(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new collection."""
        return await self.request("POST", "/API/assets/v1/collections/", json_data=data)

    async def update_collection(self, collection_id: str, data: dict[str, Any]) -> dict[str, Any]:
        """Update a collection."""
        return await self.request(
            "PATCH", f"/API/assets/v1/collections/{collection_id}/", json_data=data
        )

    async def delete_collection(self, collection_id: str) -> dict[str, Any]:
        """Delete a collection."""
        return await self.request("DELETE", f"/API/assets/v1/collections/{collection_id}/")

    async def get_collection_contents(
        self,
        collection_id: str,
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        """Get collection contents."""
        params = {"page": page, "per_page": per_page}
        return await self.request(
            "GET", f"/API/assets/v1/collections/{collection_id}/contents/", params=params
        )

    async def add_to_collection(
        self, collection_id: str, object_ids: list[str], object_type: str = "assets"
    ) -> dict[str, Any]:
        """Add objects to a collection."""
        data = {"object_ids": object_ids, "object_type": object_type}
        return await self.request(
            "POST", f"/API/assets/v1/collections/{collection_id}/contents/", json_data=data
        )

    # Search API
    async def search(
        self,
        query: str | None = None,
        filter_data: dict[str, Any] | None = None,
        doc_types: list[str] | None = None,
        page: int = 1,
        per_page: int = 50,
        sort: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        """Search for assets and collections."""
        data: dict[str, Any] = {}
        if query:
            data["query"] = query
        if filter_data:
            data["filter"] = filter_data
        if doc_types:
            data["doc_types"] = doc_types
        if sort:
            data["sort"] = sort

        params = {"page": page, "per_page": per_page}
        return await self.request("POST", "/API/search/v1/search/", params=params, json_data=data)

    async def list_saved_searches(
        self,
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        """List saved searches."""
        params = {"page": page, "per_page": per_page}
        return await self.request("GET", "/API/search/v1/search/saved/", params=params)

    async def get_saved_search(
        self,
        search_id: str,
        include_results: bool = True,
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        """Get saved search and optionally its results."""
        params = {
            "page": page,
            "per_page": per_page,
            "include_results": str(include_results).lower(),
        }
        return await self.request("GET", f"/API/search/v1/search/saved/{search_id}/", params=params)

    async def create_saved_search(self, name: str, criteria: dict[str, Any]) -> dict[str, Any]:
        """Create a saved search."""
        data = {"name": name, "criteria": criteria}
        return await self.request("POST", "/API/search/v1/search/saved/", json_data=data)

    async def delete_saved_search(self, search_id: str) -> dict[str, Any]:
        """Delete a saved search."""
        return await self.request("DELETE", f"/API/search/v1/search/saved/{search_id}/")

    # Files API
    async def list_storages(self, page: int = 1, per_page: int = 50) -> dict[str, Any]:
        """List storage locations."""
        params = {"page": page, "per_page": per_page}
        return await self.request("GET", "/API/files/v1/storages/", params=params)

    async def get_storage(self, storage_id: str) -> dict[str, Any]:
        """Get storage details."""
        return await self.request("GET", f"/API/files/v1/storages/{storage_id}/")

    async def get_asset_files(
        self,
        asset_id: str,
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        """Get files for an asset."""
        params = {"page": page, "per_page": per_page}
        return await self.request(
            "GET", f"/API/files/v1/assets/{asset_id}/files/", params=params
        )

    async def get_asset_formats(
        self,
        asset_id: str,
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        """Get formats for an asset."""
        params = {"page": page, "per_page": per_page}
        return await self.request(
            "GET", f"/API/files/v1/assets/{asset_id}/formats/", params=params
        )

    async def get_asset_proxies(self, asset_id: str) -> dict[str, Any]:
        """Get proxies for an asset."""
        return await self.request("GET", f"/API/files/v1/assets/{asset_id}/proxies/")

    async def get_asset_keyframes(self, asset_id: str) -> dict[str, Any]:
        """Get keyframes for an asset."""
        return await self.request("GET", f"/API/files/v1/assets/{asset_id}/keyframes/")

    # Metadata API
    async def list_metadata_views(self, page: int = 1, per_page: int = 50) -> dict[str, Any]:
        """List metadata views."""
        params = {"page": page, "per_page": per_page}
        return await self.request("GET", "/API/metadata/v1/views/", params=params)

    async def get_metadata_view(self, view_id: str) -> dict[str, Any]:
        """Get a metadata view."""
        return await self.request("GET", f"/API/metadata/v1/views/{view_id}/")

    async def get_asset_metadata(self, asset_id: str) -> dict[str, Any]:
        """Get metadata for an asset."""
        return await self.request("GET", f"/API/metadata/v1/assets/{asset_id}/views/")

    async def update_asset_metadata(
        self, asset_id: str, view_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update metadata for an asset."""
        return await self.request(
            "PUT", f"/API/metadata/v1/assets/{asset_id}/views/{view_id}/", json_data=data
        )

    # Jobs API
    async def list_jobs(
        self,
        page: int = 1,
        per_page: int = 50,
        status: str | None = None,
    ) -> dict[str, Any]:
        """List jobs."""
        params = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status
        return await self.request("GET", "/API/jobs/v1/jobs/", params=params)

    async def get_job(self, job_id: str) -> dict[str, Any]:
        """Get job details."""
        return await self.request("GET", f"/API/jobs/v1/jobs/{job_id}/")

    async def create_job(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a job."""
        return await self.request("POST", "/API/jobs/v1/jobs/", json_data=data)

    async def update_job(self, job_id: str, data: dict[str, Any]) -> dict[str, Any]:
        """Update a job."""
        return await self.request("PATCH", f"/API/jobs/v1/jobs/{job_id}/", json_data=data)

    # Users API
    async def list_users(self, page: int = 1, per_page: int = 50) -> dict[str, Any]:
        """List users."""
        params = {"page": page, "per_page": per_page}
        return await self.request("GET", "/API/users/v1/users/", params=params)

    async def get_user(self, user_id: str) -> dict[str, Any]:
        """Get user details."""
        return await self.request("GET", f"/API/users/v1/users/{user_id}/")

    async def get_current_user(self) -> dict[str, Any]:
        """Get current user details."""
        return await self.request("GET", "/API/users/v1/users/current/")

    async def list_groups(self, page: int = 1, per_page: int = 50) -> dict[str, Any]:
        """List groups."""
        params = {"page": page, "per_page": per_page}
        return await self.request("GET", "/API/users/v1/groups/", params=params)

    async def get_group(self, group_id: str) -> dict[str, Any]:
        """Get group details."""
        return await self.request("GET", f"/API/users/v1/groups/{group_id}/")

    # Shares API
    async def list_shares(self, page: int = 1, per_page: int = 50) -> dict[str, Any]:
        """List shares."""
        params = {"page": page, "per_page": per_page}
        return await self.request("GET", "/API/assets/v1/shares/", params=params)

    async def get_share(self, share_id: str) -> dict[str, Any]:
        """Get share details."""
        return await self.request("GET", f"/API/assets/v1/shares/{share_id}/")

    async def create_share(
        self, object_type: str, object_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a share."""
        return await self.request(
            "POST", f"/API/assets/v1/{object_type}/{object_id}/shares/", json_data=data
        )

    async def delete_share(self, object_type: str, object_id: str, share_id: str) -> dict[str, Any]:
        """Delete a share."""
        return await self.request(
            "DELETE", f"/API/assets/v1/{object_type}/{object_id}/shares/{share_id}/"
        )

    # Projects API
    async def list_projects(self, page: int = 1, per_page: int = 50) -> dict[str, Any]:
        """List projects."""
        params = {"page": page, "per_page": per_page}
        return await self.request("GET", "/API/assets/v1/projects/", params=params)

    async def get_project(self, project_id: str) -> dict[str, Any]:
        """Get project details."""
        return await self.request("GET", f"/API/assets/v1/projects/{project_id}/")

    async def create_project(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a project."""
        return await self.request("POST", "/API/assets/v1/projects/", json_data=data)

    # Transcode API
    async def list_transcode_jobs(self, page: int = 1, per_page: int = 50) -> dict[str, Any]:
        """List transcode jobs."""
        params = {"page": page, "per_page": per_page}
        return await self.request("GET", "/API/transcode/v1/transcode/", params=params)

    async def create_transcode_job(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a transcode job."""
        return await self.request("POST", "/API/transcode/v1/transcode/", json_data=data)

    # ACLs API
    async def get_acls(self, object_type: str, object_id: str) -> dict[str, Any]:
        """Get ACLs for an object."""
        return await self.request("GET", f"/API/acls/v1/{object_type}/{object_id}/acls/")

    async def update_acls(
        self, object_type: str, object_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update ACLs for an object."""
        return await self.request(
            "PUT", f"/API/acls/v1/{object_type}/{object_id}/acls/", json_data=data
        )

    # Webhooks/Notifications API
    async def list_webhooks(self, page: int = 1, per_page: int = 50) -> dict[str, Any]:
        """List webhooks."""
        params = {"page": page, "per_page": per_page}
        return await self.request("GET", "/API/notifications/v1/webhooks/", params=params)

    async def get_webhook(self, webhook_id: str) -> dict[str, Any]:
        """Get webhook details."""
        return await self.request("GET", f"/API/notifications/v1/webhooks/{webhook_id}/")

    async def create_webhook(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a webhook."""
        return await self.request("POST", "/API/notifications/v1/webhooks/", json_data=data)

    async def delete_webhook(self, webhook_id: str) -> dict[str, Any]:
        """Delete a webhook."""
        return await self.request("DELETE", f"/API/notifications/v1/webhooks/{webhook_id}/")

    # Generic request method for any endpoint
    async def api_request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a generic API request to any Iconik endpoint.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            path: Full API path (e.g., /API/assets/v1/assets/)
            params: Query parameters
            body: JSON request body

        Returns:
            API response
        """
        return await self.request(method, path, params=params, json_data=body)
