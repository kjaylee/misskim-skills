# Blender MCP 평가 보고서

> 조사일: 2026-01-31
> 대상: https://github.com/ahujasid/blender-mcp (v1.5.5, ⭐6.8k+)
> 비교 대상: 자체 blender-interactive 스킬

## 1. 아키텍처 비교

### Blender MCP (ahujasid)
```
AI Client → FastMCP Server (Python/uvx) → TCP Socket :9876 → Blender Addon
```
- MCP 프로토콜 표준 (FastMCP)
- uvx로 서버 실행 (npm 아닌 Python 생태계)
- Claude Desktop / Cursor / VS Code 통합

### 우리 blender-interactive
```
Clawdbot → nodes.run → TCP Socket :9876 → Blender Addon (headless)
```
- 커스텀 TCP 프로토콜 (JSON over TCP)
- Clawdbot nodes.run으로 직접 제어
- MiniPC headless Blender

### 핵심 차이

| 항목 | Blender MCP | 우리 시스템 |
|------|-------------|-------------|
| **프로토콜** | MCP (FastMCP) | 커스텀 TCP/JSON |
| **실행 환경** | 로컬 GUI Blender | MiniPC headless |
| **뷰포트 스크린샷** | ✅ (GUI 필수) | ❌ (headless 제한) |
| **렌더링** | 명시적 도구 없음 | ✅ render_preview/render_to_file |
| **오브젝트 조작** | execute_code로 간접 | ✅ 직접 API (create/delete/modify) |
| **Poly Haven** | ✅ addon 내장 | ✅ 독립 스크립트 |
| **Sketchfab** | ✅ 검색/다운로드 | ❌ |
| **AI 3D 생성** | ✅ Hyper3D + Hunyuan3D | ❌ |
| **텔레메트리** | ⚠️ 익명 수집 | ❌ 없음 |

## 2. 흡수할 개념

### ⭐ Sketchfab 모델 검색/다운로드
- **가치:** 무료 3D 모델 수천 개 접근 → 게임 에셋 획득
- **패턴:** API로 검색 → 다운로드 URL 획득 → glTF/FBX 임포트
- **구현:** polyhaven.py처럼 독립 스크립트로 추가 가능
- **API:** `https://api.sketchfab.com/v3/search?type=models&q={query}&downloadable=true`

### ⭐ AI 3D 생성 API 통합 (Hyper3D Rodin / Hunyuan3D)
- **가치:** 텍스트→3D 모델 자동 생성 → 게임 에셋 파이프라인 자동화
- **Hyper3D Rodin:** fal.ai 기반, 프리 티어 제한 있음
- **Hunyuan3D:** Tencent 오픈소스, 로컬 실행 가능성
- **패턴:** 프롬프트 제출 → 폴링 → 결과 다운로드 → Blender 임포트
- **우선순위:** Gemini 이미지 생성처럼 MiniPC에서 API 호출

### 🤷 MCP 프로토콜 래핑
- 우리는 Clawdbot nodes.run으로 직접 제어 → MCP 래퍼 불필요
- FastMCP는 Claude Desktop/Cursor 통합용 → 우리 환경에 맞지 않음

### ❌ 텔레메트리
- 익명이라 해도 데이터 외부 전송 = 거부

## 3. 우리 시스템의 장점

1. **Headless 렌더링** — 우리만의 강점. render_preview로 시각적 확인 가능
2. **세분화된 오브젝트 API** — create_object, modify_object 등 직접 조작
3. **모델 임포트/익스포트** — glTF/FBX/OBJ/STL 지원
4. **텔레메트리 없음** — 프라이버시 보장
5. **MiniPC 자동화** — 서버 24/7 가동 가능 (systemd)

## 4. 결론

| 항목 | 판정 |
|------|------|
| Blender MCP 코드 직접 사용 | ❌ 금지 (텔레메트리, MCP 종속) |
| Sketchfab API 패턴 흡수 | ⭐ 자체 스크립트로 재작성 |
| AI 3D 생성 패턴 흡수 | ⭐ 향후 구현 참고 |
| MCP 래퍼 | 🤷 불필요 |
| blender-interactive 현행 유지 | ✅ 이미 더 나은 부분 많음 |

**최종:** blender-interactive 스킬에 Sketchfab 검색 기능 추가. AI 3D 생성은 별도 참고자료로 기록.
