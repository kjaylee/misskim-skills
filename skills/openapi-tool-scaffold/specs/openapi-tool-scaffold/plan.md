# Plan — openapi-tool-scaffold

1. Research
   - OpenAPI→MCP 관련 레포/도구 조사
   - 생성/프록시 패턴 분리

2. Audit
   - 라이선스/의존성/CI/보안 관점 점검
   - Python 경량 재작성 가능성 판단

3. Design
   - 변환기(`scripts/openapi-to-mcp.py`) 구조 설계
   - 템플릿(`templates/mcp_server_stdio.py.tmpl`) 분리
   - 입력/스키마/보안 매핑 규칙 정의

4. Implement
   - OpenAPI 로더(JSON/YAML)
   - local `$ref` resolver
   - operation->tool 매퍼
   - 인증 훅 생성 로직
   - MCP stdio 서버 코드 렌더링

5. Verify
   - Petstore 변환
   - 로컬 YAML 변환
   - py_compile
   - MCP 루프 smoke test

6. Document
   - SKILL.md 사용법
   - examples + research/audit + test report
