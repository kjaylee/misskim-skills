# OpenAPI → MCP Research & Audit (2026-02-16)

## 0) 방법

원래 `web_search` 기반으로 조사하려 했으나 Brave API 429(쿼터 초과)로 실패.
대체로 GitHub API + raw README/manifest fetch로 리서치를 진행했다.

- 실패 사유: `Brave Search API error (429) QUOTA_LIMITED`
- 대체 수단: `api.github.com/search/repositories`, `raw.githubusercontent.com/*`

---

## 1) Research: 주요 프로젝트 스캔

### A. OpenAPI → MCP 직접 변환/브릿지 계열

| Repo | Stars | Lang | License | 관찰 |
|---|---:|---|---|---|
| `open-webui/mcpo` | 3972 | Python | MIT | MCP↔OpenAPI 프록시(역방향에 가까움), 운영성 강점 |
| `janwilmake/openapi-mcp-server` | 872 | TypeScript | MIT | OpenAPI 검색/탐색 중심 MCP 서버 |
| `harsha-iiiv/openapi-mcp-generator` | 517 | TypeScript | MIT | OpenAPI→MCP 코드 생성 CLI (TS) |
| `higress-group/openapi-to-mcpserver` | 232 | Go | Apache-2.0 | OpenAPI→MCP config 생성 (Higress 친화) |
| `ivo-toby/mcp-openapi-server` | 223 | TypeScript | MIT | OpenAPI endpoint를 MCP tool로 노출 |
| `abutbul/openapi-mcp-generator` | 28 | Python | MIT | Python 생성기(템플릿 기반) |

추가 참고:
- `tadata-org/fastapi_mcp` (11532★, Python, MIT): OpenAPI 변환기라기보다 FastAPI native MCP 노출 패턴.

### B. 생성 패턴 공통점

1. `paths` + HTTP method 순회
2. `operationId` 우선 tool naming
3. `parameters` + `requestBody`를 MCP input schema로 매핑
4. `securitySchemes`를 env 기반 credential로 런타임 주입
5. stdio 또는 HTTP/SSE transport 지원

### C. GitHub trend 성격 관찰

`mcp openapi` 키워드 검색 시 2025~2026에 다수 신생 repo 등장.
다만 품질 편차가 크고, "생성기"와 "프록시"가 혼재되어 있어 선택적 흡수가 필요.

---

## 2) Audit: 품질/보안/라이선스

### 코드 품질 신호

- CI/Workflow 확인:
  - 있음: `open-webui/mcpo`, `harsha-iiiv/openapi-mcp-generator`, `higress-group/openapi-to-mcpserver`, `ivo-toby/mcp-openapi-server`, `abutbul/openapi-mcp-generator`
  - 상대적으로 약함: `janwilmake/openapi-mcp-server` (간결 구조, 테스트/CI 신호 적음)

### 보안 관점 체크포인트

1. 인증정보 처리: env 주입 방식이 표준적이나, 로그에 헤더/토큰 노출 위험
2. 도구 과다 노출: 모든 endpoint를 무차별 노출하면 파괴적 API까지 노출 가능
3. 입력 검증: path/query/body 스키마가 느슨하면 오용 가능
4. SSRF/URL 조작: base URL/경로 조합 로직 검증 필요

### 라이선스

- 대부분 MIT, 일부 Apache-2.0
- 패턴 참조/재작성에 적합

### 의존성 최소화 가능성

- TS 기반 생성기 다수는 의존성이 비교적 큼 (swagger-parser, zod, mcp sdk 등)
- Python 재작성 시 stdlib 중심으로 경량화 가능
  - 필수: stdlib
  - 선택: PyYAML (YAML 입력 파싱)

### MiniPC/Mac Studio 호환성

- Python 3.10+ 환경 기준으로 문제 없음
- Node/Go 런타임 강제하지 않는 구현이 운영 단순성에서 유리

---

## 3) 비판적 흡수 4질문 결과

1. **실제로 필요한가?**
   - Yes. 외부 REST API를 MCP tool로 전환하는 반복 작업을 제거.

2. **기존 것으로 충분한가?**
   - 완전 충분하지 않음.
   - 기존에는 프록시/탐색 서버가 많고, 우리 워크스페이스에 맞는 Python 코드 생성 스캐폴드는 부재.

3. **비용 대비 효과?**
   - 금전 비용은 사실상 0, 개발 시간 절약 효과 큼.

4. **과대포장 위험?**
   - 있음. 따라서 “범용 완벽 변환기”가 아니라 **실전형 최소 기능 생성기**로 범위를 명확히 제한.

---

## 4) Rewrite 결정

외부 프로젝트를 가져오지 않고, 다음만 흡수:

- OpenAPI operation → MCP tool 매핑 패턴
- security scheme env 주입 패턴
- stdio transport 및 tools/list/tools/call 골격

그리고 내부 구현으로 재작성:

- `scripts/openapi-to-mcp.py`
- `templates/mcp_server_stdio.py.tmpl`
- `examples/*`

재작성 원칙:

- Python 3.10+
- stdlib 우선
- 인증 스텁 포함 (Bearer/API key/OAuth)
- 코드 생성 결과를 즉시 py_compile 가능 상태로 제공
