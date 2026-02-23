# Skill Intake Gate Report

- Path: `/Users/kjaylee/.openclaw/workspace/misskim-skills/skills/openapi-tool-scaffold`
- Risk: **medium** (score=13)
- Recommendation: `quarantine_then_rewrite`

## Matches by category
- network: 34
- doc_url: 6

## Top findings
- `SKILL.md:53` [doc_url] `"https://petstore3.swagger.io/api/v3/openapi.json" \`
- `references/test-report.md:11` [doc_url] `"https://petstore3.swagger.io/api/v3/openapi.json" \`
- `references/test-report.md:23` [doc_url] `"base_url": "https://petstore3.swagger.io/api/v3",`
- `references/test-report.md:49` [doc_url] `"base_url": "https://api.todo-mini.example.com",`
- `examples/todo-mini-mcp-server.py:13` [network] `import urllib.error`
- `examples/todo-mini-mcp-server.py:14` [network] `import urllib.parse`
- `examples/todo-mini-mcp-server.py:15` [network] `import urllib.request`
- `examples/todo-mini-mcp-server.py:20` [network] `BASE_URL = 'https://api.todo-mini.example.com'`
- `examples/todo-mini-mcp-server.py:84` [network] `'flows': {'authorizationCode': {'authorizationUrl': 'https://auth.todo-mini.example.com/oauth/authorize',`
- `examples/todo-mini-mcp-server.py:85` [network] `'tokenUrl': 'https://auth.todo-mini.example.com/oauth/token',`
- `examples/todo-mini-mcp-server.py:346` [network] `encoded = urllib.parse.quote(str(value), safe="")`
- `examples/todo-mini-mcp-server.py:381` [network] `query_string = urllib.parse.urlencode(query, doseq=True)`
- `examples/todo-mini-mcp-server.py:385` [network] `req = urllib.request.Request(url=url, data=body_data, headers=headers, method=method)`
- `examples/todo-mini-mcp-server.py:392` [network] `with urllib.request.urlopen(req, timeout=timeout) as resp:`
- `examples/todo-mini-mcp-server.py:396` [network] `except urllib.error.HTTPError as exc:`
- `examples/todo-mini-openapi.yaml:6` [network] `- url: https://api.todo-mini.example.com`
- `examples/todo-mini-openapi.yaml:86` [network] `authorizationUrl: https://auth.todo-mini.example.com/oauth/authorize`
- `examples/todo-mini-openapi.yaml:87` [network] `tokenUrl: https://auth.todo-mini.example.com/oauth/token`
- `examples/petstore-mcp-server.py:13` [network] `import urllib.error`
- `examples/petstore-mcp-server.py:14` [network] `import urllib.parse`
- `examples/petstore-mcp-server.py:15` [network] `import urllib.request`
- `examples/petstore-mcp-server.py:20` [network] `BASE_URL = 'https://petstore3.swagger.io/api/v3'`
- `examples/petstore-mcp-server.py:22` [network] `OPENAPI_SOURCE = 'https://petstore3.swagger.io/api/v3/openapi.json'`
- `examples/petstore-mcp-server.py:234` [network] `'flows': {'implicit': {'authorizationUrl': 'https://petstore3.swagger.io/oauth/authorize',`
- `examples/petstore-mcp-server.py:497` [network] `encoded = urllib.parse.quote(str(value), safe="")`
- `examples/petstore-mcp-server.py:532` [network] `query_string = urllib.parse.urlencode(query, doseq=True)`
- `examples/petstore-mcp-server.py:536` [network] `req = urllib.request.Request(url=url, data=body_data, headers=headers, method=method)`
- `examples/petstore-mcp-server.py:543` [network] `with urllib.request.urlopen(req, timeout=timeout) as resp:`
- `examples/petstore-mcp-server.py:547` [network] `except urllib.error.HTTPError as exc:`
- `examples/README.md:6` [doc_url] `- `https://petstore3.swagger.io/api/v3/openapi.json``
- `examples/README.md:12` [doc_url] `"https://petstore3.swagger.io/api/v3/openapi.json" \`
- `scripts/openapi-to-mcp.py:21` [network] `import urllib.parse`
- `scripts/openapi-to-mcp.py:22` [network] `import urllib.request`
- `scripts/openapi-to-mcp.py:31` [network] `parsed = urllib.parse.urlparse(value)`
- `scripts/openapi-to-mcp.py:37` [network] `req = urllib.request.Request(`
- `scripts/openapi-to-mcp.py:44` [network] `with urllib.request.urlopen(req, timeout=30) as resp:`
- `scripts/openapi-to-mcp.py:337` [network] `parsed = urllib.parse.urlparse(url)`
- `scripts/openapi-to-mcp.py:341` [network] `base = urllib.parse.urlparse(input_ref)`
- `scripts/openapi-to-mcp.py:343` [network] `return urllib.parse.urljoin(origin, url)`
- `scripts/openapi-to-mcp.py:346` [network] `return "https://api.example.com"`
