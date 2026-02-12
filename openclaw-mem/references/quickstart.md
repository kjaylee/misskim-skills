# openclaw-mem Quickstart (3분 가이드 / 3-Minute Guide)

## 1. 설치 / Install

```bash
pip install openclaw-mem
```

> Python 3.10+ 필요 / Requires Python 3.10+
> 첫 실행 시 임베딩 모델 (~90MB) 자동 다운로드 / Embedding model (~90MB) auto-downloads on first run

## 2. 워크스페이스 초기화 / Initialize Workspace

```bash
cd your-project/
openclaw-mem init
```

다음 구조가 생성됩니다 / This creates:

```
memory/
├── core.md           # 핵심 메모리 / Core memory
├── observations.md   # 관찰 기록 / Observations log
└── projects/         # 프로젝트별 Brain / Per-project Brain files
.env                  # 환경변수 설정 / Environment config
```

## 3. 관찰 기록 / Record Observations

```bash
# 의사결정 기록 / Record a decision
openclaw-mem observe "Redis 캐시 TTL을 1시간으로 설정" --tag decision

# 배운 점 기록 / Record a lesson
openclaw-mem observe "Always run --dry-run before archive" --tag learning
```

## 4. 인덱싱 / Index Files

```bash
# 모든 파일 인덱싱 / Index all files
openclaw-mem index --all

# 변경된 파일만 / Changed files only
openclaw-mem index --changed
```

## 5. 검색 / Search

```bash
# 시맨틱 검색 / Semantic search
openclaw-mem search "배포 프로세스"
openclaw-mem search "deployment process"

# Progressive Disclosure (2단계 검색)
openclaw-mem search "캐시 설정" --index     # Step 1: 요약 / summaries
openclaw-mem search --detail "chunk:0:abc"  # Step 2: 전문 / full content
```

## 6. Brain 디렉토리 / Brain Directories

프로젝트별 컨텍스트를 영속적으로 관리합니다.
Manage persistent per-project context.

```bash
# Brain 파일 생성 / Create a Brain file
cat > memory/projects/my-api.md << 'EOF'
# my-api Brain

## Architecture
- FastAPI + PostgreSQL
- Redis for caching

## Decisions
- JWT auth with 24h expiry
EOF

# 인덱싱 후 검색 가능 / Index and search
openclaw-mem index memory/projects/my-api.md
openclaw-mem search "my-api architecture"
```

## 7. 자동 캡처 / Auto-Capture

세션 기록에서 자동으로 관찰을 추출합니다.
Automatically extract observations from session transcripts.

```bash
# 최근 6시간 세션에서 추출 / Extract from last 6h
openclaw-mem auto-capture --since 6h

# Brain으로 자동 라우팅 / Auto-route to Brain files
openclaw-mem auto-capture --since 6h --route-to-brain

# 미리보기 (실행 안 함) / Preview (dry run)
openclaw-mem auto-capture --since 6h --dry-run
```

## 다음 단계 / Next Steps

- `openclaw-mem brain-check` — Brain 파일 보안 검사 / Security scan
- `openclaw-mem archive --execute` — 오래된 메모리 아카이브 / Archive old memory
- 환경변수로 커스터마이징 → `openclaw-mem help` 참조 / Customize via env vars

---

**GitHub:** [github.com/kjaylee/openclaw-mem](https://github.com/kjaylee/openclaw-mem)
**License:** MIT
