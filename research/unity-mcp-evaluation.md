# Unity MCP 평가 보고서

> 조사일: 2026-01-31
> 대상:
>   - CoderGamester/mcp-unity (⭐3.5k+, MIT)
>   - IvanMurzak/Unity-MCP (⭐1.5k+, v0.43+)
> 현재 상태: Unity 미사용 (Godot 4 사용 중)

## 1. 두 구현 비교

### CoderGamester/mcp-unity
- **아키텍처:** AI Client → Node.js MCP Server → WebSocket :8090 → Unity Editor
- **Unity:** 6.0+ 필수
- **25+ 도구:** GameObject CRUD, 컴포넌트, 머티리얼, 씬, 에셋, 프리팹, 테스트, 콘솔, 패키지
- **배치 실행:** 여러 작업을 하나의 요청으로
- **IDE 통합:** PackedCache를 워크스페이스에 추가 → 자동완성 개선

### IvanMurzak/Unity-MCP (더 성숙)
- **아키텍처:** AI Client → C# Binary MCP Server → WebSocket → Unity Plugin
- **Unity:** 2022.3+ 지원 (더 넓은 호환)
- **50+ 도구:** 위 전부 + Reflection, Roslyn C# 동적 컴파일, 런타임 AI
- **핵심 차별점:**
  - ✅ **런타임 AI** — 빌드된 게임 내에서 LLM 상호작용 (NPC AI, 디버깅)
  - ✅ **Reflection** — 프로젝트 전체 코드의 모든 메서드/프로퍼티 접근
  - ✅ **커스텀 MCP Tool** — 프로젝트별 확장 도구 작성 가능
  - ✅ **크로스 플랫폼 바이너리** — Win/Mac/Linux, x64/ARM64
- **추가 플러그인:** Animation, ParticleSystem, ProBuilder

## 2. 핵심 패턴 분석

### 패턴 1: 게임 에디터 자동화 via 소켓/MCP
```
AI Agent → 프로토콜 서버 → 에디터 소켓 → 엔진 API
```
이 패턴은 **Blender MCP, Unity MCP, 우리 blender-interactive 모두 동일**.
엔진 종류(Blender/Unity/Godot)만 다를 뿐 아키텍처는 일관됨.

→ **Godot 4에도 동일 패턴 적용 가능** (향후 godot-interactive 스킬)

### 패턴 2: 런타임 AI (IvanMurzak)
```
빌드된 게임 → MCP Server (in-game) → LLM → 실시간 NPC 행동
```
- 게임 내에서 AI가 실시간으로 NPC를 제어
- 디버깅: 빌드된 게임 상태를 AI가 검사
- **참고 가치 높음** — 향후 게임에 AI NPC 도입 시 핵심 패턴

### 패턴 3: Reflection 기반 만능 접근
```
method-find → 코드베이스 전체 메서드 검색 (private 포함)
method-call → 아무 메서드나 호출 (파라미터 포함)
```
- 도구를 일일이 정의하지 않아도 엔진 전체 API에 접근
- **위험하지만 강력** — 개발 환경에서만 사용

### 패턴 4: 배치 실행 (CoderGamester)
```json
{
  "tool": "batch_execute",
  "operations": [
    {"tool": "create_gameobject", "params": {"name": "Enemy_1"}},
    {"tool": "create_gameobject", "params": {"name": "Enemy_2"}},
    {"tool": "create_gameobject", "params": {"name": "Enemy_3"}}
  ]
}
```
- 라운드트립 감소 → 성능 향상
- 선택적 롤백 (하나 실패 시 전부 취소)
- **우리 blender-interactive에도 적용 가능**

## 3. 흡수할 개념

### ⭐ 에디터 자동화 아키텍처 패턴
- AI → 프로토콜 서버 → 소켓 → 엔진 API
- **이미 blender-interactive에 구현됨**
- Godot 4에도 동일 패턴 적용 가능 (GDScript EditorPlugin + TCP socket)

### 👍 배치 실행 패턴
- 여러 명령을 하나의 요청으로 묶기
- blender-interactive의 execute_code로 이미 가능하지만, 명시적 배치 API가 편리
- **향후 blender-interactive 업데이트 시 고려**

### 👍 런타임 AI 통합 패턴 (장기)
- 게임 내 AI NPC 제어
- 현재는 불필요하지만 "AI 게임" 트렌드에 핵심
- **장기 참고자료로 보관**

### 🤷 MCP 프로토콜 래핑
- Unity/Claude Desktop 통합용 — 우리 환경(Clawdbot)에서 불필요
- 우리는 nodes.run으로 직접 제어

### 🤷 Reflection 만능 접근
- Unity C# 전용 — Godot/Blender에 직접 적용 불가
- 하지만 execute_code가 같은 역할 (임의 Python/GDScript 실행)

## 4. Godot 4 적용 가능성

현재 MiniPC에 Godot 4.6이 설치되어 있음. Unity MCP 패턴을 Godot에 적용하면:

```
Clawdbot → nodes.run → Godot headless → GDScript 실행
```

**가능한 도구들:**
- 씬 생성/수정 (tscn 파일 조작)
- 노드 추가/삭제 (GDScript via CLI)
- 리소스 관리 (.tres 파일)
- 빌드 자동화 (`godot4 --headless --export-release`)
- 테스트 실행

**현재는 Godot를 직접 스크립팅+빌드로 사용 중** → 소켓 서버 불필요.
하지만 프로젝트가 복잡해지면 Unity MCP처럼 인터랙티브 제어가 유용할 수 있음.

## 5. 결론

| 항목 | 판정 |
|------|------|
| Unity MCP 코드 직접 사용 | ❌ (Unity 미사용) |
| 에디터 자동화 패턴 | ✅ 이미 blender-interactive에 구현됨 |
| 배치 실행 패턴 | 👍 blender-interactive 향후 업데이트 참고 |
| 런타임 AI 패턴 | 👍 장기 참고자료 (AI NPC 게임) |
| Godot 자동화 확장 | 🤷 현재 불필요, 프로젝트 복잡화 시 고려 |
| Unity 도입 시 참고 | ✅ IvanMurzak/Unity-MCP가 정석 (더 성숙, 런타임 지원) |

**최종:** 코드 흡수 대상 없음. 패턴/아키텍처만 기록해두고 향후 참고.
배치 실행 개념을 blender-interactive에 추가하는 것만 실제 개선 사항.
