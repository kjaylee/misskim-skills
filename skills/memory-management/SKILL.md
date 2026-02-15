---
name: memory-management
description: >
  AI 에이전트의 세션 간 기억 관리 스킬. openclaw-mem CLI 기반 5-Layer 메모리 아키텍처 운용,
  세션 라이프사이클(시작/중간/종료) 기억 작업, 프로젝트 Brain 관리, 기억 위생 유지.
  memory, context, handoff, working memory, decision log, RAG, LanceDB 관련 작업 시 사용.
metadata:
  author: misskim
  version: "1.0"
---

# Memory Management

openclaw-mem 기반 세션 간 기억 관리. 에이전트는 세션이 끝나면 모든 걸 잊는다 — 이 스킬이 기억을 구조화한다.

## 환경 설정

```bash
export OPENCLAW_MEM_ROOT=$WORKSPACE/.openclaw/workspace
MEM=$WORKSPACE/.openclaw/workspace/openclaw-mem/.venv/bin/openclaw-mem
```

모든 명령어에서 `$MEM` 은 위 경로를 가리킨다.

---

## 1. 5-Layer 기억 구조

| Layer | 파일/시스템 | 특성 | 크기 제한 |
|-------|------------|------|----------|
| **L0** | `memory/core.md` | 핫캐시, 항상 로드 | **<2KB 엄수** |
| **L1** | `memory/working-memory.md` | 현재 작업 포커스, 휘발성 | 자유 |
| **L2** | `memory/decisions.md` | Master 결정 로그, append-only | 무제한 (주기적 아카이브) |
| **L3** | `memory/YYYY-MM-DD.md` + `memory/handoffs/` | 에피소드 기억 | 최근 7일 유지 |
| **L4** | LanceDB (`rag/lancedb/`) | 시맨틱 검색, 전체 워크스페이스 | 자동 관리 |

**읽기 순서:** L0 → L1 → L2(최근) → 필요 시 L3/L4 검색

---

## 2. 세션 라이프사이클

### 세션 시작 (MUST)

```bash
# 1. 이전 세션 핸드오프 읽기
$MEM handoff read

# 2. 워킹 메모리 확인
$MEM working-memory show

# 3. 최근 결정 확인
$MEM decision list --last 5
```

세 명령의 출력으로 "지금 뭘 하고 있었는지" 파악 후 작업 시작.

### 세션 중간

중요 결정 발생 시 **즉시** 기록:

```bash
# Master가 결정한 사항
$MEM decision log "Rust+Godot 전용, JS/TS 금지" --tag master

# 에이전트 학습/인사이트
$MEM observe "LanceDB 인덱싱은 --changed가 --all보다 10x 빠름" --tag learning

# 에러 기록
$MEM observe "Godot export 시 --headless 필수" --tag error
```

워킹 메모리가 변경된 경우:

```bash
$MEM working-memory set "현재 포커스: NAS 마이그레이션 Phase 2"
$MEM working-memory update "추가: DNS 전파 대기 중"
```

### 세션 종료 (MUST)

```bash
# 1. 핸드오프 노트 작성 (다음 세션 자신에게)
$MEM handoff write "블로그 배포 완료. 남은 작업: 게임 페이지 스크린샷 4장"

# 2. 워킹 메모리 갱신
$MEM working-memory set "다음: 게임 스크린샷 촬영 → 블로그 게임 포스트 완성"

# 3. 변경된 파일 인덱싱
$MEM index --changed
```

---

## 3. Brain 관리

Brain = `memory/projects/{name}.md` — 프로젝트별 영속 컨텍스트.

### 생성

```bash
cat > memory/projects/eastsea-blog.md << 'EOF'
# eastsea-blog Brain
## Stack: Hugo + GitHub Pages
## Repo: eastsea-blog/
## Deploy: git push → GitHub Actions → pages
## 주의: baseURL은 https://eastsea.xyz
EOF
```

### 업데이트 원칙

- 사실이 바뀌면 **즉시** Brain 수정 (stale 정보는 해로움)
- 크기 < 1KB 유지 — 서브에이전트 컨텍스트에 전체 주입되므로
- 결정 사항은 Brain이 아닌 L2(decisions.md)에 기록

### 서브에이전트에 Brain 주입

서브에이전트 스폰 시:
1. Brain 파일을 읽어서 프롬프트에 포함
2. "먼저 Brain 읽고 시작" 이 아닌, **직접 내용을 주입**
3. 전체 AGENTS.md 주입 금지 — Brain + 작업별 규칙만

---

## 4. 기억 위생

### L0 핫캐시 관리 (core.md < 2KB)

```bash
wc -c memory/core.md  # 2048 초과 시 정리 필요
```

초과 시: 오래된/덜 중요한 항목을 L2 또는 L4로 이동.

### 아카이브

```bash
# 드라이런 (무엇이 아카이브될지 확인)
$MEM archive --days 30

# 실행
$MEM archive --days 30 --execute

# 아카이브 후 재인덱싱
$MEM archive --reindex
```

### RAG 재인덱싱 시점

| 이벤트 | 명령 |
|--------|------|
| 매일 01:00 KST (크론) | `$MEM index --changed` |
| 대량 파일 변경 후 | `$MEM index --all` |
| 아카이브 실행 후 | `$MEM archive --reindex` |
| 특정 파일 수동 추가 | `$MEM index path/to/file.md` |

### 에피소드 정리

`memory/YYYY-MM-DD.md` 는 7일 이후 아카이브 대상. `memory/handoffs/`도 동일.

---

## 5. openclaw-mem CLI 레퍼런스

### search — 시맨틱 검색 (Progressive Disclosure)

```bash
$MEM search "배포 프로세스" --top-k 5     # 기본 검색
$MEM search "배포" --index                 # Step 1: 요약만
$MEM search --detail "chunk:0:abc123"      # Step 2: 전체 내용
$MEM search "에러" --tag error             # 태그 필터
$MEM search "Godot" --source memory --raw  # 소스 필터 + 사람 읽기용
```

### index — 벡터 DB 인덱싱

```bash
$MEM index --changed          # 변경된 파일만 (일상용)
$MEM index --all              # 전체 재인덱싱
$MEM index path/to/file.md   # 단일 파일
```

### observe — 구조화된 관찰 기록

```bash
$MEM observe "텍스트" --tag learning   # learning|decision|error|insight
```

### working-memory — 휘발성 작업 버퍼

```bash
$MEM working-memory show               # 현재 상태
$MEM working-memory set "새 포커스"     # 전체 교체
$MEM working-memory update "추가 내용"  # 덧붙이기
$MEM working-memory clear              # 초기화
```

### decision — 결정 로그 (append-only)

```bash
$MEM decision log "결정 내용" --tag master  # 기록
$MEM decision list --last 10               # 최근 10개
$MEM decision search "Rust"                # 키워드 검색
```

### handoff — 세션 핸드오프

```bash
$MEM handoff write "핸드오프 내용"   # 작성
$MEM handoff read                   # 최신 읽기
$MEM handoff history                # 히스토리
```

### archive — 콜드 스토리지

```bash
$MEM archive                        # 드라이런
$MEM archive --execute              # 실행
$MEM archive --reindex              # 아카이브 인덱싱
$MEM archive --days 14 --execute    # 14일 기준
```

### auto-capture — 세션 트랜스크립트에서 자동 추출

```bash
$MEM auto-capture --since 6h        # 최근 6시간
$MEM auto-capture --file session.md # 특정 파일
$MEM auto-capture --dry-run         # 미리보기
```

---

## 금기 사항

- ❌ core.md에 2KB 초과 내용 쓰기
- ❌ decisions.md 항목 수정/삭제 (append-only)
- ❌ 핸드오프 없이 세션 종료
- ❌ 서브에이전트에 전체 memory/ 덤프
- ❌ `--all` 인덱싱 남용 (변경 없는데 전체 인덱싱)
