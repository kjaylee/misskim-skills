#!/usr/bin/env python3
"""
OpenAPI 3.x -> MCP stdio server code generator.

- Input: OpenAPI spec URL or local JSON/YAML file path
- Output: Python MCP stdio server code
- Transport: stdio (newline JSON-RPC, with optional Content-Length output)

No blind external installs: uses Python stdlib + optional PyYAML when parsing YAML.
Python 3.10+.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import pprint
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

HTTP_METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]
PATH_ITEM_NON_OP_KEYS = {"summary", "description", "servers", "parameters"}


def is_url(value: str) -> bool:
    parsed = urllib.parse.urlparse(value)
    return parsed.scheme in {"http", "https"}


def load_text(input_ref: str) -> str:
    if is_url(input_ref):
        req = urllib.request.Request(
            input_ref,
            headers={
                "User-Agent": "openapi-to-mcp-generator/1.0",
                "Accept": "application/json, application/yaml, text/yaml, */*",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
        return raw.decode("utf-8", errors="replace")

    path = pathlib.Path(input_ref)
    return path.read_text(encoding="utf-8")


def parse_json_or_yaml(text: str, input_ref: str) -> Dict[str, Any]:
    stripped = text.lstrip()
    if stripped.startswith("{") or stripped.startswith("["):
        return json.loads(text)

    # Try JSON first even for non-obvious cases
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "YAML spec detected but PyYAML is not installed. "
            "Install with: pip install pyyaml"
        ) from exc

    parsed = yaml.safe_load(text)
    if not isinstance(parsed, dict):
        raise ValueError(f"OpenAPI document must be an object: {input_ref}")
    return parsed


def deep_get(root: Dict[str, Any], parts: List[str]) -> Any:
    cur: Any = root
    for part in parts:
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            raise KeyError("/".join(parts))
    return cur


def resolve_refs(node: Any, root: Dict[str, Any], seen: Optional[set[str]] = None) -> Any:
    if seen is None:
        seen = set()

    if isinstance(node, dict):
        if "$ref" in node and isinstance(node["$ref"], str):
            ref = node["$ref"]
            if ref.startswith("#/"):
                if ref in seen:
                    return {k: v for k, v in node.items() if k != "$ref"}
                seen_next = set(seen)
                seen_next.add(ref)
                target = deep_get(root, ref[2:].split("/"))
                resolved_target = resolve_refs(target, root, seen_next)
                overlay = {k: v for k, v in node.items() if k != "$ref"}
                if isinstance(resolved_target, dict):
                    merged = dict(resolved_target)
                    merged.update(resolve_refs(overlay, root, seen_next))
                    return merged
                return resolve_refs(overlay, root, seen_next) or resolved_target
            # External refs are intentionally not auto-fetched.
            return {k: resolve_refs(v, root, seen) for k, v in node.items() if k != "$ref"}

        return {k: resolve_refs(v, root, seen) for k, v in node.items()}

    if isinstance(node, list):
        return [resolve_refs(item, root, seen) for item in node]

    return node


def normalize_schema(schema: Any, root: Dict[str, Any]) -> Dict[str, Any]:
    if schema is None:
        return {"type": "string"}

    resolved = resolve_refs(schema, root)
    if not isinstance(resolved, dict):
        return {"type": "string"}

    out: Dict[str, Any] = {}

    passthrough_keys = [
        "type",
        "format",
        "enum",
        "default",
        "nullable",
        "minimum",
        "maximum",
        "exclusiveMinimum",
        "exclusiveMaximum",
        "minLength",
        "maxLength",
        "pattern",
        "description",
        "title",
        "example",
        "examples",
    ]
    for key in passthrough_keys:
        if key in resolved:
            out[key] = resolved[key]

    if "properties" in resolved and isinstance(resolved["properties"], dict):
        out.setdefault("type", "object")
        out["properties"] = {
            prop_name: normalize_schema(prop_schema, root)
            for prop_name, prop_schema in resolved["properties"].items()
        }
        required = resolved.get("required")
        if isinstance(required, list):
            out["required"] = [item for item in required if isinstance(item, str)]

    if "items" in resolved:
        out.setdefault("type", "array")
        out["items"] = normalize_schema(resolved.get("items"), root)

    if "oneOf" in resolved and isinstance(resolved["oneOf"], list):
        out["oneOf"] = [normalize_schema(x, root) for x in resolved["oneOf"]]
    if "anyOf" in resolved and isinstance(resolved["anyOf"], list):
        out["anyOf"] = [normalize_schema(x, root) for x in resolved["anyOf"]]
    if "allOf" in resolved and isinstance(resolved["allOf"], list):
        out["allOf"] = [normalize_schema(x, root) for x in resolved["allOf"]]

    if "additionalProperties" in resolved:
        ap = resolved["additionalProperties"]
        if isinstance(ap, dict):
            out["additionalProperties"] = normalize_schema(ap, root)
        elif isinstance(ap, bool):
            out["additionalProperties"] = ap

    if not out:
        return {"type": "object"}
    return out


def sanitize_identifier(raw: str, fallback: str = "tool") -> str:
    name = re.sub(r"[^a-zA-Z0-9_]+", "_", raw.strip())
    name = re.sub(r"_+", "_", name).strip("_")
    if not name:
        name = fallback
    if name[0].isdigit():
        name = f"_{name}"
    return name[:64]


def default_tool_name(method: str, path: str) -> str:
    clean_path = path.strip("/") or "root"
    clean_path = clean_path.replace("{", "").replace("}", "")
    return sanitize_identifier(f"{method.lower()}_{clean_path}", fallback="op").lower()


def unique_name(name: str, used: set[str]) -> str:
    candidate = name
    idx = 2
    while candidate in used:
        suffix = f"_{idx}"
        candidate = (name[: max(1, 64 - len(suffix))] + suffix)[:64]
        idx += 1
    used.add(candidate)
    return candidate


def merge_parameters(path_params: Any, op_params: Any) -> List[Dict[str, Any]]:
    merged: Dict[Tuple[str, str], Dict[str, Any]] = {}

    for bucket in [path_params, op_params]:
        if not isinstance(bucket, list):
            continue
        for raw in bucket:
            if not isinstance(raw, dict):
                continue
            key = (str(raw.get("name", "")), str(raw.get("in", "query")))
            merged[key] = raw

    return list(merged.values())


def extract_body_schema(operation: Dict[str, Any], root: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str], bool]:
    if "requestBody" not in operation:
        return None, None, False

    request_body = resolve_refs(operation.get("requestBody"), root)
    if not isinstance(request_body, dict):
        return None, None, False

    content = request_body.get("content")
    if not isinstance(content, dict) or not content:
        return None, None, bool(request_body.get("required"))

    if "application/json" in content:
        media_type = "application/json"
    else:
        media_type = next(iter(content.keys()))

    media_obj = resolve_refs(content.get(media_type), root)
    required = bool(request_body.get("required"))

    if not isinstance(media_obj, dict):
        return {"type": "string", "description": f"Raw request body ({media_type})"}, media_type, required

    schema = media_obj.get("schema")
    if schema is None:
        return {"type": "string", "description": f"Raw request body ({media_type})"}, media_type, required

    if media_type.startswith("application/json"):
        return normalize_schema(schema, root), media_type, required

    normalized = {
        "type": "string",
        "description": f"Raw request body for content-type '{media_type}'",
    }
    return normalized, media_type, required


def pick_security(operation: Dict[str, Any], root: Dict[str, Any], global_security: Any) -> List[Dict[str, List[str]]]:
    if "security" in operation:
        selected = operation.get("security")
    else:
        selected = global_security

    selected = resolve_refs(selected, root)

    if selected is None:
        return []
    if selected == []:
        return []
    if not isinstance(selected, list):
        return []

    out: List[Dict[str, List[str]]] = []
    for entry in selected:
        if not isinstance(entry, dict):
            continue
        entry_out: Dict[str, List[str]] = {}
        for scheme_name, scopes in entry.items():
            if isinstance(scopes, list):
                clean_scopes = [x for x in scopes if isinstance(x, str)]
            else:
                clean_scopes = []
            entry_out[str(scheme_name)] = clean_scopes
        out.append(entry_out)
    return out


def parse_security_schemes(spec: Dict[str, Any], root: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    components = spec.get("components")
    if not isinstance(components, dict):
        return {}

    schemes = components.get("securitySchemes")
    if not isinstance(schemes, dict):
        return {}

    out: Dict[str, Dict[str, Any]] = {}
    for name, raw in schemes.items():
        resolved = resolve_refs(raw, root)
        if not isinstance(resolved, dict):
            continue

        scheme_type = str(resolved.get("type", "")).strip()
        entry: Dict[str, Any] = {"type": scheme_type}

        if scheme_type == "http":
            entry["scheme"] = resolved.get("scheme")
            if "bearerFormat" in resolved:
                entry["bearerFormat"] = resolved["bearerFormat"]
        elif scheme_type == "apiKey":
            entry["in"] = resolved.get("in")
            entry["name"] = resolved.get("name")
        elif scheme_type in {"oauth2", "openIdConnect"}:
            if "flows" in resolved:
                entry["flows"] = resolved.get("flows")
            if "openIdConnectUrl" in resolved:
                entry["openIdConnectUrl"] = resolved.get("openIdConnectUrl")

        out[str(name)] = entry

    return out


def choose_base_url(spec: Dict[str, Any], override: Optional[str], input_ref: str) -> str:
    if override:
        return override

    servers = spec.get("servers")
    if isinstance(servers, list):
        for server in servers:
            if isinstance(server, dict) and isinstance(server.get("url"), str):
                url = str(server["url"])
                parsed = urllib.parse.urlparse(url)
                if parsed.scheme in {"http", "https"}:
                    return url
                if is_url(input_ref):
                    base = urllib.parse.urlparse(input_ref)
                    origin = f"{base.scheme}://{base.netloc}"
                    return urllib.parse.urljoin(origin, url)
                return url

    return "https://api.example.com"


def build_tools(spec: Dict[str, Any], include_deprecated: bool = False, max_tools: int = 0) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    paths = spec.get("paths")
    if not isinstance(paths, dict):
        raise ValueError("OpenAPI spec has no valid 'paths' object")

    root = spec
    global_security = spec.get("security")

    used_names: set[str] = set()
    tools: List[Dict[str, Any]] = []
    runtime_map: Dict[str, Dict[str, Any]] = {}

    for path, path_item_raw in paths.items():
        if not isinstance(path_item_raw, dict):
            continue

        path_item = resolve_refs(path_item_raw, root)
        path_params = path_item.get("parameters") if isinstance(path_item, dict) else None

        for method, operation_raw in path_item.items():
            if method in PATH_ITEM_NON_OP_KEYS or method.lower() not in HTTP_METHODS:
                continue
            if not isinstance(operation_raw, dict):
                continue

            operation = resolve_refs(operation_raw, root)
            if not isinstance(operation, dict):
                continue

            if operation.get("deprecated") and not include_deprecated:
                continue

            op_id = operation.get("operationId")
            if isinstance(op_id, str) and op_id.strip():
                tool_name_seed = sanitize_identifier(op_id.strip(), fallback="op").lower()
            else:
                tool_name_seed = default_tool_name(method, str(path))
            tool_name = unique_name(tool_name_seed, used_names)

            summary = str(operation.get("summary") or "").strip()
            description = str(operation.get("description") or "").strip()
            doc = summary or description or f"{method.upper()} {path}"
            if summary and description and description != summary:
                doc = f"{summary} — {description}"

            merged_params = merge_parameters(path_params, operation.get("parameters"))

            properties: Dict[str, Dict[str, Any]] = {}
            required: List[str] = []
            runtime_params: List[Dict[str, Any]] = []

            used_arg_names: set[str] = set()
            for raw_param in merged_params:
                param = resolve_refs(raw_param, root)
                if not isinstance(param, dict):
                    continue

                param_name = str(param.get("name") or "param")
                param_in = str(param.get("in") or "query").lower()
                arg_name = sanitize_identifier(param_name, fallback="param").lower()
                if arg_name in used_arg_names:
                    arg_name = sanitize_identifier(f"{arg_name}_{param_in}", fallback="param").lower()
                arg_name = unique_name(arg_name, used_arg_names)

                schema = normalize_schema(param.get("schema"), root)
                desc = str(param.get("description") or "").strip()
                loc_note = f"OpenAPI parameter ({param_in}: {param_name})"
                schema["description"] = f"{desc} | {loc_note}" if desc else loc_note
                properties[arg_name] = schema

                is_required = bool(param.get("required")) or param_in == "path"
                if is_required:
                    required.append(arg_name)

                runtime_params.append(
                    {
                        "arg": arg_name,
                        "name": param_name,
                        "in": param_in,
                        "required": is_required,
                    }
                )

            body_schema, body_content_type, body_required = extract_body_schema(operation, root)
            body_arg: Optional[str] = None
            if body_schema is not None:
                body_arg = "body"
                if body_arg in properties:
                    body_arg = unique_name("request_body", set(properties.keys()))
                properties[body_arg] = body_schema
                if body_required:
                    required.append(body_arg)

            security = pick_security(operation, root, global_security)

            input_schema: Dict[str, Any] = {
                "type": "object",
                "properties": properties,
                "additionalProperties": False,
            }
            if required:
                input_schema["required"] = sorted(set(required))

            tool_def = {
                "name": tool_name,
                "description": doc,
                "inputSchema": input_schema,
            }
            tools.append(tool_def)

            runtime_map[tool_name] = {
                "method": method.upper(),
                "path": path,
                "parameters": runtime_params,
                "body_arg": body_arg,
                "body_content_type": body_content_type,
                "security": security,
            }

            if max_tools and len(tools) >= max_tools:
                return tools, runtime_map

    return tools, runtime_map


def render_server(
    template_path: pathlib.Path,
    output_path: pathlib.Path,
    server_name: str,
    base_url: str,
    source_ref: str,
    tools: List[Dict[str, Any]],
    runtime_map: Dict[str, Dict[str, Any]],
    security_schemes: Dict[str, Dict[str, Any]],
) -> None:
    template = template_path.read_text(encoding="utf-8")

    generator_meta = {
        "name": "openapi-to-mcp.py",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
    }

    replacements = {
        "__SERVER_NAME_JSON__": repr(server_name),
        "__BASE_URL_JSON__": repr(base_url),
        "__GENERATOR_META_JSON__": pprint.pformat(generator_meta, width=100, sort_dicts=False),
        "__OPENAPI_SOURCE_JSON__": repr(source_ref),
        "__TOOLS_JSON__": pprint.pformat(tools, width=100, sort_dicts=False),
        "__TOOL_RUNTIME_JSON__": pprint.pformat(runtime_map, width=100, sort_dicts=False),
        "__SECURITY_SCHEMES_JSON__": pprint.pformat(security_schemes, width=100, sort_dicts=False),
    }

    content = template
    for key, value in replacements.items():
        content = content.replace(key, value)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def validate_openapi_3(spec: Dict[str, Any]) -> None:
    version = spec.get("openapi")
    if not isinstance(version, str):
        raise ValueError("Missing OpenAPI version ('openapi' field)")
    if not version.startswith("3."):
        raise ValueError(f"Only OpenAPI 3.x is supported, got: {version}")


def default_server_name(spec: Dict[str, Any]) -> str:
    info = spec.get("info")
    title = None
    if isinstance(info, dict):
        title = info.get("title")
    if isinstance(title, str) and title.strip():
        return sanitize_identifier(title, fallback="openapi_bridge").lower()
    return "openapi_bridge"


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    script_dir = pathlib.Path(__file__).resolve().parent
    default_template = script_dir.parent / "templates" / "mcp_server_stdio.py.tmpl"

    parser = argparse.ArgumentParser(description="Generate MCP stdio server code from OpenAPI 3.x spec")
    parser.add_argument("input", help="OpenAPI spec URL or local file path (JSON/YAML)")
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output Python file path for generated MCP server",
    )
    parser.add_argument("--server-name", help="Override generated MCP server name")
    parser.add_argument("--base-url", help="Override base API URL (defaults to first OpenAPI server URL)")
    parser.add_argument(
        "--template",
        default=str(default_template),
        help=f"Server template path (default: {default_template})",
    )
    parser.add_argument(
        "--include-deprecated",
        action="store_true",
        help="Include deprecated OpenAPI operations",
    )
    parser.add_argument(
        "--max-tools",
        type=int,
        default=0,
        help="Optional cap on number of generated tools (0 = no limit)",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    input_ref = args.input
    output_path = pathlib.Path(args.output).resolve()
    template_path = pathlib.Path(args.template).resolve()

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    text = load_text(input_ref)
    spec = parse_json_or_yaml(text, input_ref)

    validate_openapi_3(spec)

    server_name = args.server_name or default_server_name(spec)
    server_name = sanitize_identifier(server_name, fallback="openapi_bridge").lower()

    base_url = choose_base_url(spec, args.base_url, input_ref)

    tools, runtime_map = build_tools(
        spec,
        include_deprecated=args.include_deprecated,
        max_tools=max(0, int(args.max_tools or 0)),
    )
    security_schemes = parse_security_schemes(spec, spec)

    render_server(
        template_path=template_path,
        output_path=output_path,
        server_name=server_name,
        base_url=base_url,
        source_ref=input_ref,
        tools=tools,
        runtime_map=runtime_map,
        security_schemes=security_schemes,
    )

    print(
        json.dumps(
            {
                "status": "ok",
                "output": str(output_path),
                "server_name": server_name,
                "base_url": base_url,
                "tool_count": len(tools),
                "security_scheme_count": len(security_schemes),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
