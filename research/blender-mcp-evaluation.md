# Blender MCP 패턴 평가

**날짜:** 2026-01-31
**대상:** https://github.com/ahujasid/blender-mcp (v1.5.5)
**목적:** 패턴/개념 흡수 → 자체 스킬 작성 (코드 복사 금지)

## 아키텍처 분석

### 2-컴포넌트 구조
1. **Blender Addon (addon.py)** — Blender 내부에서 TCP 소켓 서버 실행
2. **MCP Server (server.py)** — Claude Desktop/Cursor와 통신하는 MCP 프로토콜 브릿지

### 통신 프로토콜
- **전송:** TCP 소켓, JSON 기반
- **요청:** `{"type": "command_name", "params": {...}}`
- **응답:** `{"status": "success|error", "result": {...}}`
- **버퍼링:** 수신 데이터를 누적하다가 유효한 JSON이 완성되면 파싱
- **타임아웃:** 180초 (복잡한 작업 대비)

### 스레드 모델
- 소켓 서버: 별도 daemon 스레드에서 실행
- 클라이언트 연결: 각각 별도 스레드
- **핵심 패턴:** `bpy.app.timers.register(callback, first_interval=0.0)` — 
  워커 스레드에서 받은 명령을 Blender 메인 스레드로 마샬링
- Blender의 bpy API는 메인 스레드에서만 안전하게 호출 가능

### 지원 명령어
| 명령 | 설명 |
|------|------|
| `get_scene_info` | 씬 전체 상태 (오브젝트 목록, 위치, 개수) |
| `get_object_info` | 특정 오브젝트 상세 (메시 정보, 머티리얼, 바운딩박스) |
| `get_viewport_screenshot` | 뷰포트 스크린샷 캡처 (GUI 모드 전용) |
| `execute_code` | 임의 Python 코드 실행 (가장 강력) |
| `get_polyhaven_categories` | Poly Haven 카테고리 조회 |
| `search_polyhaven_assets` | Poly Haven 에셋 검색 |
| `download_polyhaven_asset` | Poly Haven 에셋 다운로드 + 임포트 |
| `set_texture` | 다운받은 텍스처를 오브젝트에 적용 |

## Poly Haven API 구조

**베이스 URL:** `https://api.polyhaven.com`
**라이선스:** CC0 (완전 무료, 상용 포함)
**User-Agent 필수:** 모든 요청에 User-Agent 헤더 필요

### 주요 엔드포인트
| 엔드포인트 | 설명 |
|------------|------|
| `GET /types` | 에셋 타입 목록 (hdris, textures, models) |
| `GET /assets?type=...&categories=...` | 에셋 목록 (필터링 가능) |
| `GET /categories/{type}` | 카테고리 목록 + 개수 |
| `GET /info/{id}` | 개별 에셋 메타데이터 |
| `GET /files/{id}` | 다운로드 URL (해상도/포맷별 트리 구조) |

### 에셋 타입
- **HDRIs** — 환경 조명 맵 (hdr, exr 포맷)
- **Textures** — PBR 텍스처 (diffuse, normal, roughness, displacement 등)
- **Models** — 3D 모델 (gltf, fbx 포맷)

## 강점

1. **양방향 통신** — 명령 실행 + 결과 수신, 반복 작업 가능
2. **씬 상태 조회** — 현재 상태 기반 의사결정 가능
3. **임의 코드 실행** — 사전 정의 안 된 작업도 수행 가능
4. **Poly Haven 통합** — 무료 CC0 에셋 즉시 활용
5. **뷰포트 캡처** — 빠른 프리뷰 (렌더링 없이)

## 약점 / 우리 환경 차이

1. **GUI 의존** — viewport screenshot은 3D View 영역 필요 (headless 불가)
2. **MCP 프로토콜** — Claude Desktop/Cursor 전용, Clawdbot에서 불필요
3. **단일 세션** — 하나의 Blender 인스턴스와만 통신
4. **보안** — execute_code는 위험할 수 있음 (우리는 제어된 환경이라 괜찮)
5. **텔레메트리** — 우리는 필요 없음

## 우리 환경 적응 전략

### 환경
- **MiniPC** (Linux, headless)
- **Blender 5.0.1** (snap 설치)
- **접근:** Clawdbot `nodes.run` → MiniPC

### 설계 결정

| 원본 | 우리 적응 |
|------|----------|
| Blender GUI addon | headless 백그라운드 스크립트 |
| MCP 서버 (server.py) | 불필요 — `nodes.run`으로 직접 통신 |
| viewport screenshot | offscreen 렌더링 (Cycles CPU) |
| 로컬 소켓 (localhost) | 0.0.0.0 바인딩 (원격 접근) 또는 localhost + 클라이언트 스크립트 |
| `bpy.app.timers` | 동일 — headless에서도 작동 |

### 핵심 변경점
1. **소켓 서버를 Blender background 스크립트로 실행** (addon 등록 불필요)
2. **클라이언트 스크립트**로 명령 전송 (`nodes.run`으로 실행)
3. **오프스크린 렌더링**으로 프리뷰 (viewport 대신)
4. **기존 blender-pipeline 스킬과 상호보완** — pipeline은 배치/파이프라인, interactive는 실시간 조작

## 기존 blender-pipeline 스킬과의 관계

### blender-pipeline (기존)
- **강점:** 배치 처리, 포맷 변환, 스프라이트 시트, 프로시저럴 생성
- **패턴:** 1회성 스크립트 실행 (`blender -b --python script.py`)
- **유지:** 그대로 유지

### blender-interactive (신규)
- **강점:** 양방향 실시간 통신, 씬 상태 조회, 반복 조작
- **패턴:** 상주 소켓 서버 + 명령 전송
- **추가:** Poly Haven 통합, 오프스크린 프리뷰

### 상호보완
- 단순 변환/배치 → blender-pipeline
- 복잡한 씬 구축, 반복 조작 → blender-interactive
- Poly Haven 에셋 + 씬 조합 → blender-interactive

## 결론

**추천: 자체 스킬 작성 ✅**

패턴은 건전하고 우리 환경에 잘 적응 가능. MCP 계층은 불필요하므로 제거하고,
소켓 서버 + 클라이언트 패턴만 headless에 맞게 자체 구현.
Poly Haven API 통합은 큰 가치 — CC0 무료 에셋을 게임 파이프라인에 활용 가능.
