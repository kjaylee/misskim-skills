# Test Report — openapi-tool-scaffold

Date: 2026-02-16

## Test 1: Petstore 변환

Command:

```bash
python3 skills/openapi-tool-scaffold/scripts/openapi-to-mcp.py \
  "https://petstore3.swagger.io/api/v3/openapi.json" \
  --output skills/openapi-tool-scaffold/examples/petstore-mcp-server.py \
  --server-name petstore_mcp \
  --max-tools 8
```

Output (요약):

```json
{
  "status": "ok",
  "server_name": "petstore_mcp",
  "base_url": "https://petstore3.swagger.io/api/v3",
  "tool_count": 8,
  "security_scheme_count": 2
}
```

검증 포인트:
- 최소 3개 endpoint 변환 조건 충족 (8개 생성)

## Test 2: 로컬 YAML 변환

Command:

```bash
python3 skills/openapi-tool-scaffold/scripts/openapi-to-mcp.py \
  skills/openapi-tool-scaffold/examples/todo-mini-openapi.yaml \
  --output skills/openapi-tool-scaffold/examples/todo-mini-mcp-server.py \
  --server-name todo_mini_mcp
```

Output (요약):

```json
{
  "status": "ok",
  "server_name": "todo_mini_mcp",
  "base_url": "https://api.todo-mini.example.com",
  "tool_count": 4,
  "security_scheme_count": 3
}
```

## Test 3: 생성 코드 문법 검증

Command:

```bash
python3 -m py_compile \
  skills/openapi-tool-scaffold/scripts/openapi-to-mcp.py \
  skills/openapi-tool-scaffold/examples/petstore-mcp-server.py \
  skills/openapi-tool-scaffold/examples/todo-mini-mcp-server.py
```

Result:
- exit code 0 (syntax OK)

## Test 4: MCP 프로토콜 스모크 테스트

- 대상: `petstore-mcp-server.py`
- 절차: `initialize` → `tools/list` → `tools/call`
- 결과:
  - `initialize`/`tools/list` 정상 응답
  - `tools/call`에서 OAuth 토큰 미설정 시 예상된 auth stub 에러 반환 (`isError: true`)

결론:
- 생성 서버의 기본 MCP 루프 + tool 노출 + 인증 훅 동작 확인
