# Agent Skills 생태계 전체 평가 보고서

> 조사일: 2026-01-31
> 조사 범위: agentskills.io 표준, SkillKit npm 패키지, 172+ 스킬 (31+ 소스)

## 1. 생태계 개요

### agentskills.io 표준
- Anthropic이 주도, 독립 오픈 표준으로 발전
- SKILL.md (YAML frontmatter + Markdown instructions) 포맷
- Microsoft (VS Code, GitHub Copilot), Cursor, Goose, Amp, OpenCode 등 채택
- 핵심: 폴더 = 스킬, SKILL.md 필수, scripts/ + references/ + assets/ 선택

### SkillKit (npm skillkit)
- **저자:** rohitg00
- **기능:** 32개 에이전트 포맷 자동 변환 (SKILL.md → .mdc 등)
- **평가:** 🤷 불필요
  - 우리는 Clawdbot 단일 에이전트 → 변환 불필요
  - npm install 자체가 보안 리스크
  - 마켓플레이스 브라우징 기능은 web_search로 대체 가능

### skillsmp.com
- 71,000+ 스킬 인덱싱 (GitHub 자동 크롤링)
- 대부분 AGENTS.md/CLAUDE.md를 SKILL.md로 감싼 것
- 양은 많으나 품질 편차 큼

---

## 2. 소스별 스킬 카탈로그 + 평가

### 📦 Anthropic Official (16개)

| 스킬 | 설명 | 등급 | 이유 |
|------|------|------|------|
| algorithmic-art | p5.js 제너레이티브 아트 | 🤷 | 게임에서 부분 활용 가능하나 p5.js 특화 |
| brand-guidelines | Anthropic 브랜딩 가이드 | 🤷 | Anthropic 전용 |
| canvas-design | PNG/PDF 비주얼 아트 | 🤷 | 정적 디자인, 핵심이 아님 |
| doc-coauthoring | 문서 공동 편집 | 🤷 | 엔터프라이즈 기능 |
| docx | Word 문서 생성/편집 | 🤷 | 문서 조작 = 불필요 |
| **frontend-design** | **프론트엔드 UI/UX 디자인** | **⭐** | **Anti-AI-slop 디자인 원칙! 게임/웹앱 필수** |
| internal-comms | 상태 보고서/뉴스레터 | 🤷 | 기업 커뮤니케이션 |
| mcp-builder | MCP 서버 개발 가이드 | 👍 | MCP 참조용으로 유용 |
| pdf | PDF 처리 | 🤷 | PDF 특화 |
| pptx | PowerPoint 생성 | 🤷 | 프레젠테이션 = 불필요 |
| **skill-creator** | **스킬 작성 가이드** | **⭐** | **메타스킬! 우리 스킬 작성 표준** |
| slack-gif-creator | Slack용 GIF | 🤷 | Slack 특화 |
| theme-factory | 10개 테마 적용 | 🤷 | 이미 자체 처리 |
| **web-artifacts-builder** | **React+Tailwind HTML 아티팩트** | **👍** | **단일 HTML 번들링 패턴 참조** |
| **webapp-testing** | **Playwright 웹앱 테스트** | **⭐** | **MiniPC Playwright와 직결! 필수** |
| xlsx | Excel 처리 | 🤷 | 스프레드시트 = 불필요 |

### 📦 Vercel Labs (4개)

| 스킬 | 설명 | 등급 | 이유 |
|------|------|------|------|
| **react-best-practices** | **React/Next.js 57개 성능 규칙** | **👍** | **React 사용 시 참조 가치 높음** |
| vercel-deploy-claimable | Vercel 배포 | 🤷 | Vercel 특화 |
| web-design-guidelines | 웹 디자인 가이드 | 🤷 | frontend-design과 중복 |
| react-native-skills | React Native | 🤷 | RN 안 씀 |

### 📦 Remotion (1개)

| 스킬 | 설명 | 등급 | 이유 |
|------|------|------|------|
| **remotion** | **React 기반 영상 제작 종합 가이드** | **⭐** | **MiniPC Remotion과 직결! 26개 규칙 파일** |

### 📦 Stripe (2개)

| 스킬 | 설명 | 등급 | 이유 |
|------|------|------|------|
| **stripe-best-practices** | **Stripe 결제 통합 베스트 프랙티스** | **⭐** | **게임/앱 수익화 필수! CheckoutSessions, 구독, Connect** |
| upgrade-stripe | SDK 업그레이드 | 🤷 | 버전업 시 참조 |

### 📦 Supabase (1개)

| 스킬 | 설명 | 등급 | 이유 |
|------|------|------|------|
| **postgres-best-practices** | **PostgreSQL 성능 최적화 8개 범주** | **👍** | **DB 사용 시 참조 가치** |

### 📦 Cloudflare (7개)

| 스킬 | 설명 | 등급 | 이유 |
|------|------|------|------|
| agents-sdk | CF 에이전트 SDK | 🤷 | CF 미사용 |
| building-ai-agent | CF AI 에이전트 | 🤷 | CF 미사용 |
| building-mcp-server | CF MCP 서버 | 🤷 | CF 미사용 |
| commands | CF CLI 레퍼런스 | 🤷 | CF 미사용 |
| durable-objects | 상태 관리 | 🤷 | CF 미사용 |
| **web-perf** | **Core Web Vitals 감사** | **👍** | **웹 성능 최적화 참조용** |
| wrangler | Workers 배포 | 🤷 | CF 미사용 |

### 📦 HuggingFace (8개) → 전부 🤷

우리는 pre-trained 모델 사용자이지 훈련자가 아님. ML 워크플로우 불필요.

### 📦 Trail of Bits (22개)

| 주요 스킬 | 등급 | 이유 |
|-----------|------|------|
| static-analysis | 👍 | 코드 품질 분석 참조용 |
| property-based-testing | 🤷 | 과도하게 전문적 |
| 나머지 20개 | 🤷 | 보안 감사 전문 도구들 |

### 📦 Expo (3개) → 전부 🤷

React Native/Expo 안 씀.

### 📦 Google Labs/Stitch (2개) → 전부 🤷

Google Stitch 특화.

### 📦 Sentry (7개)

| 스킬 | 등급 | 이유 |
|------|------|------|
| commit | 👍 | 커밋 베스트 프랙티스 참조 가능 |
| code-review | 👍 | 코드 리뷰 패턴 참조 가능 |
| 나머지 5개 | 🤷 | Sentry 내부용 |

### 📦 obra/superpowers 커뮤니티 (19개)

| 스킬 | 설명 | 등급 | 이유 |
|------|------|------|------|
| **dispatching-parallel-agents** | **병렬 에이전트 디스패치** | **⭐** | **우리 서브에이전트 워크플로우 강화** |
| **systematic-debugging** | **체계적 디버깅 4단계** | **⭐** | **근본 원인 추적 방법론 필수** |
| **subagent-driven-development** | **서브에이전트 기반 개발** | **⭐** | **spec+quality 2단계 리뷰 패턴** |
| **verification-before-completion** | **완료 전 검증** | **⭐** | **"증거 없이 완료 주장 금지" 필수** |
| **test-driven-development** | **TDD 방법론** | **👍** | **철저한 Red-Green-Refactor** |
| brainstorming | 아이디어 생성 | 🤷 | 이미 자체 수행 |
| writing-plans | 전략 문서 작성 | 🤷 | ralph-loop에 이미 포함 |
| executing-plans | 계획 실행 | 🤷 | ralph-loop에 이미 포함 |
| sharing-skills | 스킬 공유 | 🤷 | 우리 환경에서 불필요 |
| using-git-worktrees | Git worktrees | 🤷 | 과도한 복잡도 |
| finishing-a-development-branch | 브랜치 완료 | 🤷 | 기본 Git 워크플로우 |
| requesting/receiving-code-review | 코드 리뷰 | 🤷 | subagent-dev에 통합 |
| root-cause-tracing | 근본 원인 추적 | 🤷 | systematic-debugging에 포함 |
| testing-anti-patterns | 테스트 안티패턴 | 🤷 | TDD에 포함 |
| condition-based-waiting | 조건 대기 | 🤷 | 기본 프로그래밍 |
| testing-skills-with-subagents | 서브에이전트 테스트 | 🤷 | subagent-dev에 포함 |

### 📦 기타 커뮤니티

| 스킬 | 등급 | 이유 |
|------|------|------|
| ComposioHQ/content-research-writer | 🤷 | 이미 web_search+web_fetch 가능 |
| coreyhaines31/marketingskills | 🤷 | 너무 범용적 |
| CloudAI-X/threejs-skills | 👍 | Three.js 3D 참조 가능 |
| NanoBanana-PPT-Skills | 🤷 | PPT = 불필요 |
| fal-ai skills (6개) | 🤷 | 자체 MLX+Gemini 이미지 생성 보유 |
| Better Auth (3개) | 🤷 | 특정 라이브러리 종속 |
| Notion skills | 🤷 | Notion 미사용 |

---

## 3. 최종 흡수 목록

### ⭐ 필수 흡수 (9개 → 자체 재작성)

1. **anti-slop-design** ← frontend-design (Anthropic)
2. **playwright-testing** ← webapp-testing (Anthropic)
3. **skill-authoring** ← skill-creator (Anthropic)
4. **remotion-video** ← remotion (Remotion)
5. **stripe-payments** ← stripe-best-practices (Stripe)
6. **parallel-agents** ← dispatching-parallel-agents (obra)
7. **systematic-debugging** ← systematic-debugging (obra)
8. **subagent-dev** ← subagent-driven-development (obra)
9. **verify-before-done** ← verification-before-completion (obra)

### 👍 유용 (4개 → 간소화 재작성)

10. **react-perf** ← react-best-practices (Vercel)
11. **postgres-perf** ← postgres-best-practices (Supabase)
12. **web-bundling** ← web-artifacts-builder (Anthropic)
13. **tdd-discipline** ← test-driven-development (obra)

---

## 4. 보안 평가

- **SKILL.md 파일 자체:** 안전 (마크다운 지침서, 코드 실행 없음)
- **SkillKit npm:** ❌ 위험 — npm install 자체가 supply chain 리스크
- **scripts/ 폴더:** ⚠️ 주의 — 셸 스크립트는 검토 필요
- **결론:** 개념만 흡수, 코드 복사 금지 원칙 유지

## 5. 핵심 인사이트

1. **표준 포맷 채택:** agentskills.io SKILL.md 포맷으로 우리 스킬도 작성 → 호환성 확보
2. **obra/superpowers가 가장 가치 높음:** 에이전트 자율성 관련 방법론이 우리 Clawdbot과 직결
3. **Anti-AI-slop 디자인 원칙:** 게임/웹앱 품질 차별화의 핵심
4. **Remotion 스킬:** MiniPC에 이미 설치된 Remotion 활용도 극대화
5. **Stripe 스킬:** 수익화 준비의 기반

---

*조사 방법: web_search + web_fetch (브라우저 미사용)*
*npm install 등 패키지 설치 없음*
*외부 코드 복사 없음 — 개념만 흡수*
