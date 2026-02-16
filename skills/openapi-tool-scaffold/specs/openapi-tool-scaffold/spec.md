# Spec — openapi-tool-scaffold

## Problem
외부 REST API를 MCP tool로 붙일 때 수작업이 반복되고 인증/파라미터 매핑 오류가 잦다.

## Goal
OpenAPI 3.x(JSON/YAML) 입력으로 Python MCP stdio 서버 코드를 자동 생성한다.

## Scope
- OpenAPI 3.x 파싱
- endpoint → MCP tool 변환
- Bearer/API key/OAuth stub 인증 패턴
- 생성 코드 템플릿 기반 출력
- 예시/테스트 제공

## Non-Goals
- 완전한 OpenAPI serialization(style/explode) 100% 커버
- OAuth 토큰 발급/refresh 자동 구현
- 외부 `$ref` URL 전부 dereference

## Functional Requirements
1. URL/파일 입력 지원
2. JSON/YAML 지원 (YAML은 PyYAML 사용)
3. `paths`의 각 operation을 tool로 변환
4. `tools/list`, `tools/call` 처리 가능한 stdio MCP 서버 생성
5. securitySchemes 해석 + env credential 주입
6. Python 3.10+ 호환

## Test Cases
### Spec validation tests
- [x] OpenAPI 3.0/3.1 문서 입력 시 성공
- [x] OpenAPI 2.0 입력 시 실패
- [x] `paths` 누락 시 실패

### User-scenario tests
- [x] Petstore URL 입력 -> 3개 이상 tool 생성
- [x] 로컬 YAML 입력 -> tool 생성
- [x] 생성 코드 `py_compile` 통과
- [x] MCP `initialize`, `tools/list` 응답
