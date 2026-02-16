# OpenAPI Tool Scaffold Examples

## 1) Petstore (public OpenAPI URL)

Source:
- `https://petstore3.swagger.io/api/v3/openapi.json`

Generate:

```bash
python3 ../scripts/openapi-to-mcp.py \
  "https://petstore3.swagger.io/api/v3/openapi.json" \
  --output ./petstore-mcp-server.py \
  --server-name petstore_mcp \
  --max-tools 8
```

Result summary:
- Generated tools: **8**
- Sample tool names:
  - `updatepet`
  - `addpet`
  - `findpetsbystatus`
  - `findpetsbytags`
  - `getpetbyid`

## 2) Todo Mini (local YAML)

Source:
- `./todo-mini-openapi.yaml`

Generate:

```bash
python3 ../scripts/openapi-to-mcp.py \
  ./todo-mini-openapi.yaml \
  --output ./todo-mini-mcp-server.py \
  --server-name todo_mini_mcp
```

Result summary:
- Generated tools: **4**
- Tool names:
  - `listtodos`
  - `createtodo`
  - `gettodobyid`
  - `getprofile`

## Syntax check

```bash
python3 -m py_compile ./petstore-mcp-server.py ./todo-mini-mcp-server.py
```

## MCP smoke test (newline JSON-RPC)

```bash
python3 ./petstore-mcp-server.py
```

Then send:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

The server returns valid JSON-RPC responses and lists generated tools.
