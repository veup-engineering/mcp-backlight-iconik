"""Helpers for reading and querying bundled Iconik OpenAPI specs."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class IconikSpecError(ValueError):
    """Raised when requested OpenAPI spec data cannot be resolved."""


class IconikSpecCatalog:
    """OpenAPI spec catalog for exposing response/request shapes via MCP tools."""

    def __init__(self, spec_dir: str | Path | None = None):
        self.spec_dir = self._resolve_spec_dir(spec_dir)
        self._cache: dict[str, dict[str, Any]] = {}

    def _resolve_spec_dir(self, spec_dir: str | Path | None) -> Path:
        candidates: list[Path] = []
        if spec_dir is not None:
            candidates.append(Path(spec_dir).expanduser())

        env_dir = os.getenv("ICONIK_OPENAPI_DIR")
        if env_dir:
            candidates.append(Path(env_dir).expanduser())

        repo_root = Path(__file__).resolve().parents[2]
        workspace_root = Path(__file__).resolve().parents[3]
        candidates.append(repo_root / "docs" / "iconik_swagger_defs")
        candidates.append(repo_root / "docs" / "iconik")
        candidates.append(workspace_root / "docs" / "iconik_swagger_defs")
        candidates.append(workspace_root / "docs" / "iconik")

        for candidate in candidates:
            if candidate.is_dir():
                return candidate

        raise IconikSpecError(
            "Could not locate Iconik OpenAPI specs. Set ICONIK_OPENAPI_DIR or add docs/iconik."
        )

    def list_specs(self) -> dict[str, str]:
        """List available spec files by logical name."""
        specs: dict[str, str] = {}
        for path in sorted(self.spec_dir.glob("*.json")):
            specs[path.stem] = str(path)
        if not specs:
            raise IconikSpecError(f"No .json spec files found in {self.spec_dir}")
        return specs

    def load_spec(self, spec: str) -> dict[str, Any]:
        """Load a spec by name (e.g. 'assets') or filename ('assets.json')."""
        key = spec.removesuffix(".json")
        if key in self._cache:
            return self._cache[key]

        path = self.spec_dir / f"{key}.json"
        if not path.is_file():
            available = ", ".join(sorted(self.list_specs().keys()))
            raise IconikSpecError(f"Unknown spec '{spec}'. Available: {available}")

        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise IconikSpecError(f"Invalid spec format in {path}")

        self._cache[key] = data
        return data

    def list_operations(
        self,
        spec: str,
        path_prefix: str | None = None,
        limit: int = 200,
    ) -> list[dict[str, Any]]:
        """List operation stubs for a given spec."""
        data = self.load_spec(spec)
        paths = data.get("paths", {})
        if not isinstance(paths, dict):
            return []

        operations: list[dict[str, Any]] = []
        for path, methods in paths.items():
            if path_prefix and not str(path).startswith(path_prefix):
                continue
            if not isinstance(methods, dict):
                continue

            for method, operation in methods.items():
                if method.lower() not in {"get", "post", "put", "patch", "delete", "head", "options"}:
                    continue
                if not isinstance(operation, dict):
                    continue
                operations.append(
                    {
                        "path": path,
                        "method": method.lower(),
                        "summary": operation.get("summary"),
                        "operation_id": operation.get("operationId"),
                        "tags": operation.get("tags", []),
                    }
                )
                if len(operations) >= limit:
                    return operations
        return operations

    def get_operation(self, spec: str, path: str, method: str) -> dict[str, Any]:
        """Get operation details for path + method."""
        data = self.load_spec(spec)
        paths = data.get("paths", {})
        if not isinstance(paths, dict):
            raise IconikSpecError(f"Spec '{spec}' does not contain a paths object")

        path_item = paths.get(path)
        if path_item is None:
            available = ", ".join(sorted(str(p) for p in paths.keys())[:20])
            raise IconikSpecError(f"Path '{path}' not found in spec '{spec}'. Examples: {available}")
        if not isinstance(path_item, dict):
            raise IconikSpecError(f"Path '{path}' has invalid shape in spec '{spec}'")

        normalized_method = method.lower()
        operation = path_item.get(normalized_method)
        if operation is None:
            available_methods = ", ".join(sorted(path_item.keys()))
            raise IconikSpecError(
                f"Method '{normalized_method}' not found for path '{path}'. Available: {available_methods}"
            )
        if not isinstance(operation, dict):
            raise IconikSpecError(f"Operation '{normalized_method} {path}' has invalid shape")

        return {
            "spec": spec.removesuffix(".json"),
            "path": path,
            "method": normalized_method,
            "operation_id": operation.get("operationId"),
            "summary": operation.get("summary"),
            "description": operation.get("description"),
            "tags": operation.get("tags", []),
            "parameters": operation.get("parameters", []),
            "request_body": operation.get("requestBody"),
            "responses": operation.get("responses", {}),
            "servers": data.get("servers", []),
        }

    def get_component_schema(self, spec: str, schema_name: str) -> dict[str, Any]:
        """Get a named component schema from a spec."""
        data = self.load_spec(spec)
        schemas = data.get("components", {}).get("schemas", {})
        if not isinstance(schemas, dict):
            raise IconikSpecError(f"Spec '{spec}' does not define components.schemas")

        schema = schemas.get(schema_name)
        if schema is None:
            available = ", ".join(sorted(str(name) for name in schemas.keys())[:30])
            raise IconikSpecError(
                f"Schema '{schema_name}' not found in spec '{spec}'. Examples: {available}"
            )

        return {
            "spec": spec.removesuffix(".json"),
            "schema_name": schema_name,
            "schema": schema,
        }

    def resolve_ref(self, spec: str, ref: str) -> dict[str, Any]:
        """Resolve a local JSON pointer reference (e.g. '#/components/schemas/User')."""
        if not ref.startswith("#/"):
            raise IconikSpecError("Only local refs are supported (expected '#/...')")

        data = self.load_spec(spec)
        cursor: Any = data
        for segment in ref[2:].split("/"):
            if not isinstance(cursor, dict):
                raise IconikSpecError(f"Could not resolve ref '{ref}'")
            cursor = cursor.get(segment)
            if cursor is None:
                raise IconikSpecError(f"Could not resolve ref '{ref}'")

        return {
            "spec": spec.removesuffix(".json"),
            "ref": ref,
            "resolved": cursor,
        }
