# MissKim Skills Intake Log


## 2026-02-25 08:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용, MiniPC relay 미연결로 browser.proxy 미사용.
- **수집 경로:** `web_fetch + r.jina.ai + direct HTTP(UA) + clawhub CLI/API`.
- **SkillsMP:** `skillsmp.com const skills=283,647` / `skills.sh All Time 73,867`.
- **MCP Market:** `web_fetch 429` 지속, direct HTTP 기준 `skillStats.totalCount=50,371`, mirror `6,409 MCP servers`.
- **SkillHub:** `4.9M Stars`, `22,030 Skills Collected`, sitemap `<loc> 1,979`.
- **ClawHub:** API `/api/v1/skills` `200` 회복(직전 429), CLI `search/explore` 정상.
- **VSCode Agent Skills:** `copilot-mcp 82.2K`, `agent-skills 1.9K`, `agent-skill-ninja 573`.
- **변화 판단:** 의미 있는 신규 변화 **2건**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillsMP 직접 흡수 | ⚠️ 참고만 | Q1 부분적, Q2 가능(대체 소스 존재), Q3 중간, Q4 높음(카운트 불일치). |
| MCP Market 상위군 즉시 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능(coding-agent/browser-cdp), Q3 낮음, Q4 중간. |
| SkillHub 상위군 신규 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능, Q3 낮음, Q4 중간. |
| ClawHub API 기반 intake 경로 강화 | ✅ 도입 | Q1 높음, Q2 일부 불가(API 신호 대체 어려움), Q3 높음, Q4 낮음. |
| VSCode Agent Skills 확장 직접 도입 | ⚠️ 참고만 | Q1 낮음(OpenClaw CLI 중심), Q2 가능, Q3 낮음, Q4 중간. |

**❌ 불필요 판정:** 5건

### ✅ Actions
1. ClawHub API 신호를 intake scorecard에 고정(Research→Audit→Rewrite).
2. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지.

### 📁 Full Report
- `intake-log/2026-02-25-08h-trend-sweep.md`
- `intake-log/2026-02-25-08h-trend-raw.json`

---


## 2026-02-25 04:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 경로:** direct HTTP + clawhub CLI + VSCode badge.
- **SkillsMP(=skills.sh):** `All Time 73,669`, sitemap `<loc> 4,000`.
- **MCP Market:** primary `429`(checkpoint), mirror `200` + `6,409 MCP servers` 신호 유지.
- **SkillHub:** `Stars 5.1M`, `Skills Collected 21564`.
- **ClawHub:** `search` 정상, `explore` 1회 재시도 후 정상, API `/api/v1/skills`는 `429`.
- **VSCode Agent Skills:** `copilot-mcp 82,193`, `agent-skills 1,881`, `agent-skill-ninja 573`.
- **변화 판단:** 의미 있는 신규 변화 **0건**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillsMP 직접 흡수 | ⚠️ 참고만 | Q1 부분적, Q2 가능(ClawHub/SkillHub 대체), Q3 중간, Q4 중간. |
| MCP Market 상위군 즉시 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능(coding-agent/browser-cdp), Q3 낮음, Q4 중간. |
| SkillHub 상위군 신규 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능, Q3 낮음, Q4 중간. |
| ClawHub 신규군 즉시 도입 | ⚠️ 참고만 | Q1 부분충족, Q2 대체 가능, Q3 낮음, Q4 중간 이상. |
| VSCode Agent Skills 확장 직접 도입 | ⚠️ 참고만 | Q1 낮음(OpenClaw CLI 중심), Q2 가능, Q3 낮음, Q4 중간. |

**❌ 불필요 판정:** 6건

### ✅ Actions
1. 신규 ✅ 도입 없음 (watchlist 유지)
2. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-25-04h-trend-sweep.md`
- `intake-log/2026-02-25-04h-trend-raw.json`

---


## 2026-02-25 00:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 경로:** direct HTTP + clawhub CLI/API + VSCode badge.
- **SkillsMP(=skills.sh):** `All Time 73,415` , sitemap `<loc> 4000`.
- **MCP Market:** primary `21,899 Servers` 확인, mirror(200) 유지.
- **SkillHub:** `Stars 5.0M`, `Skills Collected 21564`.
- **ClawHub:** search/explore 정상, API `/api/v1/skills` `200`.
- **VSCode Agent Skills:** `copilot-mcp 81.9K`, `agent-skills 1.9K`, `agent-skill-ninja 572`.
- **변화 판단:** 의미 있는 신규 변화 **0건**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillsMP 직접 흡수 | ⚠️ 참고만 | Q1 부분적, Q2 가능(ClawHub/SkillHub 대체), Q3 중간, Q4 중간. |
| MCP Market 상위군 즉시 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능(coding-agent/browser-cdp), Q3 낮음, Q4 중간. |
| SkillHub 상위군 신규 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능, Q3 낮음, Q4 중간. |
| ClawHub 신규군 즉시 도입 | ⚠️ 참고만 | Q1 부분충족, Q2 대체 가능, Q3 낮음, Q4 중간 이상. |
| VSCode Agent Skills 확장 직접 도입 | ⚠️ 참고만 | Q1 낮음(OpenClaw CLI 중심), Q2 가능, Q3 낮음, Q4 중간. |

**❌ 불필요 판정:** 6건

### ✅ Actions
1. 신규 ✅ 도입 없음 (watchlist 유지)
2. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-25-00h-trend-sweep.md`
- `intake-log/2026-02-25-00h-trend-raw.json`

---

## 2026-02-24 20:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 경로:** web_fetch + direct HTTP parse + clawhub CLI/API + VSCode badge.
- **SkillsMP(=skills.sh):** `All Time 73,274`, sitemap `<loc> 4,000`.
- **MCP Market:** `web_fetch 429` 지속이나 direct HTTP 파싱은 `21,857 Servers` 확인, mirror(200) 유지.
- **SkillHub:** `21.6K Skills / 5.1M Stars`, `21,564 Skills Collected`.
- **ClawHub:** 첫 호출 rate-limit 후 재시도 1회 내 `search/explore` 정상, API `/api/v1/skills` `200`.
- **VSCode Agent Skills:** `copilot-mcp ~81.9K`, `agent-skills ~1.8K~1.9K`, `agent-skill-ninja 573`.
- **변화 판단:** 의미 있는 신규 변화 **1건**(ClawHub 접근성 회복).

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillsMP 직접 흡수 | ⚠️ 참고만 | Q1 부분적, Q2 가능(ClawHub/SkillHub 대체), Q3 중간, Q4 중간. |
| MCP Market 상위군 즉시 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능(coding-agent/browser-cdp), Q3 낮음, Q4 중간. |
| SkillHub 상위군 신규 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능, Q3 낮음, Q4 중간. |
| ClawHub 신규군 즉시 도입 | ⚠️ 참고만 | Q1 부분충족, Q2 대체 가능, Q3 낮음, Q4 중간 이상. |
| VSCode Agent Skills 확장 직접 도입 | ⚠️ 참고만 | Q1 낮음(OpenClaw CLI 중심), Q2 가능, Q3 낮음, Q4 중간. |

**❌ 불필요 판정:** 6건

### ✅ Actions
1. 신규 ✅ 도입 없음 (watchlist 유지)
2. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-24-20h-trend-sweep.md`
- `intake-log/2026-02-24-20h-trend-raw.json`

---

## 2026-02-24 16:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 경로:** direct HTTP + clawhub CLI + VSCode Marketplace HTML 파싱.
- **SkillsMP(=skills.sh):** root 200 복구, leaderboard `All Time 73,042`, sitemap `<loc>` `4,000` 확인.
- **MCP Market:** primary `429` 지속, mirror(`market-mcp.com`) 200으로 상위군 신호만 유지.
- **SkillHub:** `21.6K Skills / 5.0M Stars` 확인.
- **ClawHub:** `search`는 응답, `explore`/API는 429(재시도 1회 후 중단).
- **VSCode Agent Skills:** `copilot-mcp 82,035`, `agent-skills 1,861`, `agent-skill-ninja 573`.
- **변화 판단:** 의미 있는 신규 변화 **1건**(SkillsMP 직접 접근/신호 복구).

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillsMP 직접 흡수 | ⚠️ 참고만 | Q1 부분적(탐색 신호 개선), Q2 가능(ClawHub/SkillHub로 대체), Q3 중간, Q4 중간 이상. |
| MCP Market 상위군 즉시 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능(coding-agent/browser-cdp), Q3 낮음(운영비), Q4 중간. |
| SkillHub 상위군 신규 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능, Q3 낮음, Q4 중간. |
| ClawHub 신규군 즉시 도입 | ⚠️ 참고만 | Q1 검증 부족(429), Q2 대체 가능, Q3 낮음, Q4 높음. |
| VSCode Agent Skills 확장 직접 도입 | ⚠️ 참고만 | Q1 낮음(OpenClaw CLI 중심), Q2 가능, Q3 낮음, Q4 중간. |

**❌ 불필요 판정:** 7건

### ✅ Actions
1. 신규 ✅ 도입 없음 (watchlist 유지)
2. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-24-16h-trend-sweep.md`
- `intake-log/2026-02-24-16h-trend-raw.json`

---

## 2026-02-24 12:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 경로:** direct HTTP + clawhub CLI/API + VSCode Marketplace API.
- **SkillsMP:** root 403 지속, `sitemap=684` 유지.
- **MCP Market:** primary 정상(`21,857` servers, updated 1 hour ago).
- **SkillHub:** `21,159` Skills Found 유지.
- **ClawHub:** API/CLI 429로 신규 노출 수집 실패(재시도 1회 후 중단).
- **VSCode Agent Skills:** `agent-skills 1,843`, `copilot-mcp 81,999`.
- **변화 판단:** 의미 있는 신규 변화 **0건**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillsMP 직접 흡수 | ⚠️ 참고만 | Q1 낮음(본문 차단), Q2 가능, Q3 낮음, Q4 높음. |
| MCP Market 상위군 즉시 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능(coding-agent/browser-cdp), Q3 중간 이하, Q4 중간. |
| SkillHub 상위군 신규 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능, Q3 낮음, Q4 중간. |
| ClawHub 신규군 즉시 도입 | ⚠️ 참고만 | Q1 검증 부족(429), Q2 대체 가능, Q3 낮음, Q4 높음(버즈 과대포장 가능). |
| VSCode Agent Skills 확장 직접 도입 | ⚠️ 참고만 | Q1 낮음(OpenClaw CLI 중심), Q2 가능, Q3 낮음, Q4 중간. |

**❌ 불필요 판정:** 6건

### ✅ Actions
1. 신규 ✅ 도입 없음 (watchlist 유지)
2. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-24-12h-trend-sweep.md`
- `intake-log/2026-02-24-12h-trend-raw.json`

---

## 2026-02-24 08:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 경로:** direct HTTP + clawhub CLI + VSCode Marketplace API.
- **SkillsMP:** root 403 지속, `sitemap=684` 유지.
- **MCP Market:** primary 정상(21,804 servers, updated 1 hour ago).
- **SkillHub:** `21,159 Skills Found` 유지.
- **ClawHub:** `explore` 정상(신규 노출은 버즈 중심, 검증 데이터 부족).
- **VSCode Agent Skills:** `agent-skills 1,838`, `copilot-mcp 81,961`.
- **변화 판단:** 의미 있는 신규 변화 **0건**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillsMP 직접 흡수 | ⚠️ 참고만 | Q1 낮음(본문 차단), Q2 가능, Q3 낮음, Q4 높음. |
| MCP Market 상위군 즉시 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능(coding-agent/browser-cdp), Q3 중간 이하, Q4 중간. |
| SkillHub 상위군 신규 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능, Q3 낮음, Q4 중간. |
| ClawHub 신규군 즉시 도입 | ⚠️ 참고만 | Q1 검증 부족, Q2 대체 가능, Q3 낮음, Q4 높음(버즈 과대포장 가능). |
| VSCode Agent Skills 확장 직접 도입 | ⚠️ 참고만 | Q1 낮음(OpenClaw CLI 중심), Q2 가능, Q3 낮음, Q4 중간. |

**❌ 불필요 판정:** 6건

### ✅ Actions
1. 신규 ✅ 도입 없음 (watchlist 유지)
2. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-24-08h-trend-sweep.md`
- `intake-log/2026-02-24-08h-trend-raw.json`

---

## 2026-02-24 04:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 경로:** direct HTTP + clawhub CLI + VSCode Marketplace API.
- **SkillsMP:** root 403 지속, `sitemap=684` 유지.
- **MCP Market:** primary 정상(21,804 servers, updated 1 hour ago), 상위 랭킹군 신호 유지.
- **SkillHub:** `21,159 Skills Found` 유지.
- **ClawHub:** `explore/search/inspect` 정상, `file-search` 업데이트(2026-02-23) 유지.
- **VSCode Agent Skills:** `agent-skills 1,837`, `copilot-mcp 81,938`.
- **변화 판단:** 의미 있는 신규 변화 **0건**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillsMP 직접 흡수 | ⚠️ 참고만 | 본문 차단(403) 지속으로 품질 검증 한계, 기존 소스로 1차 대체 가능. |
| MCP Market 상위군 즉시 도입 | ⚠️ 참고만 | 우리 핵심 병목 직접 해결도 제한, 기존 자동화 스택으로 대체 가능. |
| SkillHub 상위군 신규 도입 | ⚠️ 참고만 | 내부 유사 스택 다수, 도입/유지 비용 대비 순증 효과 불명확. |
| ClawHub 신규군 즉시 도입 | ⚠️ 참고만 | 최신 노출은 활발하나 신뢰 누적 데이터 부족, 과대포장 리스크 존재. |
| VSCode Agent Skills 확장 직접 도입 | ⚠️ 참고만 | OpenClaw CLI 중심 운영과 정합 낮음, 설치수 단독으로는 근거 부족. |

**❌ 불필요 판정:** 6건

### ✅ Actions
1. 신규 ✅ 도입 없음 (watchlist 유지)
2. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-24-04h-trend-sweep.md`
- `intake-log/2026-02-24-04h-trend-raw.json`

---

## 2026-02-24 00:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 경로:** `web_fetch + r.jina.ai + VSCode Marketplace API`.
- **SkillsMP:** `269,875` 신호 확인(직접 루트는 여전히 Cloudflare 차단).
- **MCP Market:** `mcpmarket.com` 429 유지, mirror(`market-mcp.com`) `6,409` 유지.
- **SkillHub:** `21,159 skills found` 유지.
- **ClawHub:** popular/highlighted 상위군 유지(`gog 33.7k`, `self-improving-agent 31.8k`).
- **VSCode Agent Skills:** `agent-skills 1,832`, `copilot-mcp 81,720`, `agent-skill-ninja 570`.
- **변화 판단:** 의미 있는 신규 변화 **0건**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillsMP 직접 흡수 | ⚠️ 참고만 | 실문제 직접 해결력 검증 신호가 약하고, 기존 소스(ClawHub/SkillHub/VSCode API)로 1차 대체 가능. |
| MCP Market 상위군 즉시 도입 | ⚠️ 참고만 | 기존 `coding-agent`/`browser-cdp-automation`로 대체 가능하며 운영·권한 비용 대비 ROI 불확실. |
| SkillHub 상위군 신규 도입 | ⚠️ 참고만 | 내부 유사 스킬 다수 존재, 신규 도입보다 기존 스택 고도화가 비용효율 우위. |
| ClawHub popular 신규 도입 | ⚠️ 참고만 | 직전 회차 대비 의미 있는 신규 후보 부재, 다운로드 지표 단독 채택은 과대평가 위험. |
| VSCode Agent Skills 확장군 | ⚠️ 참고만 | IDE 편의성은 있으나 OpenClaw CLI 중심 운영과 정합 낮음, 리뷰 모수도 작음. |

**❌ 불필요 판정:** 5건

### ✅ Actions
1. 신규 ✅ 도입 없음 (watchlist 유지)
2. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-24-00h-trend-sweep.md`
- `intake-log/2026-02-24-00h-trend-raw.json`

---

## 2026-02-23 20:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 우선순위:** `web_search + web_fetch` 우선 시도.
- **실제 상태:** `web_search` 429(quota/rate limit), MiniPC browser.proxy는 미사용(API/CLI로 수집 충족).
- **대체 경로:** `web_fetch + direct HTTP + clawhub CLI + VSCode Marketplace API`.
- **SkillsMP:** 루트는 Cloudflare 403, 대신 `robots/sitemap` 신호(684 URL)만 확보.
- **MCP Market:** `21,759 servers` 헤드라인 확인, 최신 항목 다수 0카운트.
- **SkillHub:** `21,159 skills found` 확인.
- **ClawHub:** `explore/search/inspect`로 후보 신속 검증 가능.
- **VSCode Agent Skills:** `agent-skills 1,829(리뷰 1)`, `copilot-mcp 81,834(리뷰 8)`.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `file-search` 패턴(내부 재작성) | ✅ 도입 | 대형 리포 탐색 병목을 직접 해결. 기존 보유 스킬과 중복이 낮고, 문서형 Rewrite라 도입비가 매우 작음. `inspect` 기반으로 사전 검증 가능. |
| MCP Market 상위군 | ⚠️ 참고만 | 랭킹 신호는 강하지만 기존 자동화 스택으로 1차 대체 가능. 신규 MCP 운영비 대비 ROI 미확정. |
| VSCode Agent Skills 확장군 | ⚠️ 참고만 | IDE 편의성은 있으나 현재 운영축(OpenClaw CLI)과 정합 낮음. 리뷰 모수도 작음. |
| SkillsMP 직접 흡수 | ⚠️ 참고만 | 본문 접근 차단으로 실품질 검증 불가. 교차검증 가능한 공식 데이터 확보 전 보류. |
| ClawHub `openclaw-token-optimizer` | ⚠️ 참고만 | 비용절감 문제는 맞지만 기존 운영과 중복 가능성 있음. 과장 문구 대비 A/B 검증 필요. |

**❌ 불필요 판정:** 12건

### ✅ Actions
1. `file-search` 계열을 `misskim-skills/skills/file-search-pro/`로 Research→Audit→Rewrite (macOS fallback 포함)
2. MCP/VSCode/SkillsMP는 재검토 트리거 기반 watchlist 유지
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-23-20h-trend-sweep.md`
- `intake-log/2026-02-23-20h-trend-raw.json`

---

## 2026-02-23 12:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 우선순위:** `web_search + web_fetch` 우선 시도.
- **실제 상태:** `web_search` 429(quota/rate limit), MiniPC browser.proxy는 이번 회차 미사용(필수 소스는 web/API/CLI로 충족).
- **대체 경로:** `web_fetch + r.jina.ai + clawhub CLI + VSCode Marketplace API`.
- **SkillsMP:** `269,875` skills (`Security 6,631`, `Mobile 4,817`, `LLM&AI 27,853`).
- **MCP Market:** `mcpmarket.com` 429 checkpoint, mirror(`market-mcp.com`) 기준 `6,409` 서버.
- **SkillHub:** `311 tools` (`233 MCP / 78 Skills`).
- **ClawHub:** 상위 `gog(32,958)`, `self-improving-agent(30,641)`, `tavily-search(27,112)`.
- **VSCode Agent Skills:** `copilot-mcp 81,749`, `agent-skills 1,818`, `agnix 28`.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| MCP Market `Microsandbox` 패턴(외부 설치 아님) | ✅ 도입 | 외부 스킬 intake의 실행계 보안검증 공백을 직접 해소. 기존 정적 리뷰만으로는 부족해 내부 sandbox gate로 재작성 시 비용 대비 보안효과가 큼. |
| SkillHub 상위(`Context7/Playwright/Notion`) | ⚠️ 참고만 | 기존 `context7-docs`/`playwright-testing`/현행 문서 파이프라인으로 1차 대체 가능. |
| MCP Market 상위(`Archon/Trigger.dev/Chrome DevTools`) | ⚠️ 참고만 | `coding-agent`/`parallel-agents`/`browser-cdp-automation`과 중복, 순증 ROI 불명확. |
| VSCode 확장군(`copilot-mcp/agent-skills/skill-ninja`) | ⚠️ 참고만 | installs 신호는 강하나 OpenClaw CLI 중심 운영축과 정합 낮음. |
| ClawHub `self-improving-agent`/`ontology` | ⚠️ 참고만 | 학습/메모리 가치는 있으나 현재 핵심 병목(intake security gate) 직접 해결도 낮음. |

**❌ 불필요 판정:** 9건

### ✅ Actions
1. `misskim-skills/skills/skill-intake-sandbox-gate/` 설계 착수 (Research → Audit → Rewrite)
2. 재검토 트리거: 문서/브라우저 워크플로 실패율 주간 2배↑ 또는 VSCode 협업비중 50%↑
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-23-12h-trend-sweep.md`
- `intake-log/2026-02-23-12h-trend-raw.json`

---

## 2026-02-23 08:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 우선순위:** `web_search + web_fetch` 우선 시도.
- **실제 상태:** `web_search` 429(quota/rate limit), MiniPC browser.proxy는 relay attach 미연결로 실사용 불가.
- **대체 경로:** `web_fetch + r.jina.ai + VSCode Marketplace API`.
- **SkillsMP:** `269,875` skills (`Security 6,631`, `Mobile 4,817`).
- **MCP Market:** `mcpmarket.com` 429, 대체 mirror(`market-mcp.com`) `6,409` 서버 신호 확보.
- **SkillHub:** `311 tools` 신호 유지.
- **ClawHub:** `gog 32.8k`, `self-improving-agent 30.3k`, `tavily-search 26.9k`.
- **VSCode Agent Skills:** `copilot-mcp 81,737`, `agent-skills 1,816`, `agnix 28`.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| agnix rulepack 흡수 (확장 설치 아님) | ✅ 도입 | 외부 스킬 intake에서 반복되는 정책/형식 편차를 직접 해결. 확장 설치 없이 룰셋만 내부 lint gate로 재작성해 저비용 고효율 확보. |
| SkillHub `Apple Docs MCP` 패턴 흡수 (직접 MCP 설치 아님) | ✅ 도입 | iOS/카메라앱 문서 탐색 정확도 병목을 줄이는 직접 해법. MCP 런타임 도입 없이 read-only 스킬로 재작성하여 유지비 최소화. |
| MCP Market 상위 자동화군 (`Chrome DevTools`, `Archon`) | ⚠️ 참고만 | 기존 `browser-cdp-automation`/`coding-agent`로 1차 대체 가능. 신규 MCP 운영 복잡도 대비 즉시 ROI 불명확. |
| VSCode `copilot-mcp` 직접 도입 | ⚠️ 참고만 | 설치 신호는 강하지만 현재 운영축(OpenClaw CLI)과 정합이 낮음. VSCode 협업 비중 상승 시 재검토. |
| ClawHub `self-improving-agent` | ⚠️ 참고만 | 개념은 유효하나 현재 핵심 병목은 품질게이트 일관성. 다운로드 신호만으로 도입 금지. |

**❌ 불필요 판정:** 7건

### ✅ Actions
1. `agnix` 룰셋을 내부 intake lint gate로 재작성 (Research → Audit → Rewrite)
2. `Apple Docs MCP` 패턴을 read-only 내부 스킬(`apple-dev-docs`)로 PoC 작성
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-23-08h-trend-sweep.md`
- `intake-log/2026-02-23-08h-trend-raw.json`

---

## 2026-02-23 04:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 우선순위:** `web_search + web_fetch` 우선 시도.
- **실제 상태:** `web_search` 429(quota/rate limit), MiniPC browser.proxy는 relay attach 미연결로 실사용 불가.
- **대체 경로:** `web_fetch + r.jina.ai + 검색 스니펫`.
- **SkillsMP:** `269,875` skills, peak `29,027`(@ 2026-02-19).
- **MCP Market:** `mcpmarket.com` 429 checkpoint로 직접 상세 수집 불가(리더보드/일간 랭킹 존재 신호만 확보).
- **SkillHub:** `311 tools`(`233 MCP / 78 Skills`).
- **ClawHub:** highlighted `Trello/Slack/Caldav/Answer Overflow`, popular `gog/ontology/summarize`.
- **VSCode Agent Skills:** `copilot-mcp 81.7k`, `agent-skills 1.8k`, `agnix 28`.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| agnix rulepack 흡수 (확장 설치 아님) | ✅ 도입 | 외부 스킬 intake의 설정/정책 lint 공백을 직접 해결. 확장은 설치하지 않고 룰셋만 추출해 내부 CLI 게이트로 재작성해 도입비를 최소화. |
| SkillHub `Context7 MCP` | ⚠️ 참고만 | 내부 `context7-docs` 보유로 즉시 순증 효과 제한. 문서 불일치가 주 3회+ 누적 시 재검토. |
| SkillHub `Playwright MCP` | ⚠️ 참고만 | 기존 `browser-cdp-automation`/`playwright-testing`과 중복. 브라우저 라인 안정성 저하 시 재검토. |
| ClawHub `Answer Overflow` | ⚠️ 참고만 | Discord 지식 검색은 유효하나 현재 핵심 병목 직접 해결도는 낮음. 재현 실패 반복 시 재검토. |
| VSCode `copilot-mcp` 계열 직접 도입 | ⚠️ 참고만 | OpenClaw CLI 중심 운영과 정합이 낮아 즉시 도입 보류. |

**❌ 불필요 판정:** 4건

### ✅ Actions
1. `agnix` 룰 아이디어를 내부 lint gate로 재작성 (Research → Audit → Rewrite)
2. `MCP/SkillHub/VSCode` 후보군은 재검토 트리거 기반 watchlist 유지
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-23-04h-trend-sweep.md`
- `intake-log/2026-02-23-04h-trend-raw.json`

---

## 2026-02-22 20:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 우선순위:** `web_search + web_fetch` 우선 시도.
- **실제 상태:** `web_search` 429(quota/rate limit), MiniPC browser.proxy는 불필요하여 미사용.
- **대체 경로:** `web_fetch + r.jina.ai`.
- **SkillsMP:** `261,145` skills, browse cap `5,000`.
- **MCP Market:** `mcpmarket.com` 429, 대체 `market-mcp.com`에서 `6,409` 서버(`100` 노출) 확인.
- **SkillHub:** `21.6K skills / 5.3M stars`, Trending Top5 급등 확인.
- **ClawHub:** API 429, home/popular mirror 기준 신호 수집.
- **VSCode Agent Skills:** marketplace API 기준 `copilot-mcp 81,666`, `agent-skills 1,805`, `agnix 27`.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| MCP Market 상위 자동화군 (`Archon`, `Trigger.dev`, `Chrome DevTools`) | ⚠️ 참고만 | 신호는 강하지만 현재 핵심 병목(일일 산출/QA 안정화) 직접 해결이 아님. 기존 `browser-cdp-automation`/`coding-agent`/OpenClaw 자동화로 1차 대체 가능. |
| ClawHub `ontology` | ⚠️ 참고만 | 구조화 메모리 니즈는 있으나 현재 병목은 메모리 스키마보다 실행 throughput. `openclaw-mem`/`memory-management`와 중복 가능성 큼. |
| VSCode 확장군 (`copilot-mcp`, `agent-skills`) | ⚠️ 참고만 | IDE 협업 환경엔 유효하나 현재 OpenClaw CLI 중심 운영축과 불일치. 설치수는 보조지표일 뿐 즉시 도입 근거로 부족. |
| SkillHub S-rank 군 (`systematic-debugging`, `file-search`, `skill-creator`) | ⚠️ 참고만 | 방법론 가치는 있으나 동일 계열 스킬/루틴을 이미 보유. 신규 채택보다 기존 루틴 고도화가 비용효율 우위. |

**✅ 도입:** 없음 (이번 회차)

**불필요 판정:** 4건

### ✅ Actions
1. 즉시 신규 도입 보류 (근거 부족)
2. `MCP/ClawHub/VSCode/SkillHub` 군은 재검토 트리거 기반 watchlist 유지
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-22-20h-trend-sweep.md`
- `intake-log/2026-02-22-20h-trend-raw.json`

---

## 2026-02-22 16:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 우선순위:** `web_search + web_fetch` 우선 시도.
- **실제 상태:** `web_search` 429(quota/rate limit), MiniPC browser.proxy는 불필요하여 미사용.
- **대체 경로:** `web_fetch + r.jina.ai`.
- **SkillsMP:** `261,145` skills, browse cap `5,000`.
- **MCP Market:** `mcpmarket.com` 429, 대체 `market-mcp.com`에서 `6,409` 서버(`100` 노출) 확인.
- **SkillHub:** `21.6K skills / 5.6M stars` + `542 skills / 55 sources / 111k downloads` 스냅샷 확인.
- **ClawHub:** API 1페이지 `24`개 기준, 상대 고신호 `capability-evolver (downloads 1,189 / installsCurrent 19 / stars 8)` 확인.
- **VSCode Agent Skills:** 공식 `chatSkills` 경로 + 설치 신호 `copilot-mcp 81,647`, `agent-skills 1,806`, `agnix 26` 확인.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `capability-evolver` 계열 | ⚠️ 참고만 | 품질개선 니즈는 있으나 현재 핵심 병목은 일일 산출/검증 루틴 안정화. `parallel-agents`/`subagent-dev`/`verify-before-done`로 1차 대체 가능하며, 신호는 있으나 장기 재현 데이터는 부족. |
| MCP Market 상위군 (`Archon`, `Trigger.dev`, `Chrome DevTools`) | ⚠️ 참고만 | 지표는 강하나 즉시 해결 못 하는 구체 병목이 아님. 기존 자동화 스택으로 대체 가능하고 MCP 운영복잡도 대비 ROI 불명확. |
| VSCode 확장군 (`copilot-mcp`, `agent-skills`) | ⚠️ 참고만 | IDE 협업 환경에는 유효하나 현재 OpenClaw CLI 중심 운영축과 불일치. 설치수는 보조지표일 뿐 즉시 도입 근거로 불충분. |

**✅ 도입:** 없음 (이번 회차)

**불필요 판정:** 4건

### ✅ Actions
1. 즉시 신규 도입 보류 (근거 부족)
2. `MCP/ClawHub/VSCode` 군은 재검토 트리거 기반 watchlist 유지
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-22-16h-trend-sweep.md`
- `intake-log/2026-02-22-16h-trend-raw.json`

---

## 2026-02-22 12:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 우선순위:** `web_search + web_fetch` 우선 시도.
- **실제 상태:** `web_search` 429(quota/rate limit), MiniPC browser.proxy는 불필요하여 미사용.
- **대체 경로:** `web_fetch + r.jina.ai`.
- **SkillsMP:** `261,145` skills, browse cap `5,000`.
- **MCP Market:** `mcpmarket.com` 429, 대체 `market-mcp.com`에서 `6,409` 서버(`100` 노출) 확인.
- **SkillHub:** `21.6K skills / 5.1M stars`, Trending 상단 `discord / nano-banana-pro / gifgrep / feishu-drive / model-usage`.
- **ClawHub:** newest/popular/API 교차 수집(`planning-with-files`, `browser-use`, `swarm`, `clawstats`, `website-monitor`).
- **VSCode Agent Skills:** 공식 docs의 `chatSkills`/slash command 경로 + 확장군(`copilot-mcp`, `agent-skills`, `agnix`) 기능 확인.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub 신규 운영/모니터링군 (`clawstats`, `website-monitor`) | ⚠️ 참고만 | 운영 니즈는 있으나 현재 핵심 병목(일일 게임/서비스 산출)과 직접 연결 약함. heartbeat+healthcheck로 1차 대체 가능하며 newest 신호(installsCurrent)도 약함. |
| ClawHub 계획/비용 최적화군 (`planning-with-files`, `swarm`) | ⚠️ 참고만 | 현재 운영정책(메인 오케스트레이션+서브에이전트)과 충돌 가능. 기존 subagent+cron+checkpoint 체계로 유사 기능 수행 중. |
| MCP Market 상위군 (`Archon`, `Trigger.dev`, `Chrome DevTools`) | ⚠️ 참고만 | 고신호이나 지금 즉시 해결 못 하는 병목은 아님. 기존 스택으로 대체 가능하고 MCP 운영복잡도 대비 ROI 불명확. |
| SkillHub Trending 급등군 | ⚠️ 참고만 | 상위 다수가 기존 보유 스킬과 중복. 단기 star 급등은 품질 보장 지표가 아님. |
| VSCode 확장군 (`copilot-mcp`, `agent-skills`, `agnix`) | ⚠️ 참고만 | IDE 협업 환경에는 유효하나 현재 OpenClaw CLI 중심 운영축과 불일치. VSCode 비중 상승 시 재검토. |
| SkillsMP 대규모 카탈로그 직접 흡수 | ⚠️ 참고만 | 검색 소스로는 유효하지만 대량 감사 비용이 큼. 품질/신뢰도 API 안정화 전까지 참고 유지. |

**✅ 도입:** 없음 (이번 회차)

**불필요 판정:** 19건

### ✅ Actions
1. 즉시 신규 도입 보류 (근거 부족)
2. `MCP/SkillHub/VSCode` 군은 재검토 트리거 기반으로 watchlist 유지
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-22-12h-trend-sweep.md`
- `intake-log/2026-02-22-12h-trend-raw.json`

---

## 2026-02-22 08:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 우선순위:** `web_search + web_fetch` 우선 시도.
- **실제 상태:** `web_search` 429(quota/rate limit), 브라우저 자동화는 불필요하여 MiniPC browser.proxy 미사용.
- **대체 경로:** `web_fetch + r.jina.ai`.
- **SkillsMP:** `261,145` skills, browse cap `5,000`.
- **MCP Market:** `mcpmarket.com` 429, 대체 `market-mcp.com`에서 `6,409` 서버(`100` 노출) 및 상위 signal 확인.
- **SkillHub:** `21.6K skills / 5.2M stars`, Trending 상단 `discord / nano-banana-pro / gifgrep / feishu-drive / model-usage`.
- **ClawHub:** API `api/v1/skills` 429, `skills?sort=newest` 텍스트 수집으로 신규군 확인.
- **VSCode Agent Skills:** 공식 docs에서 `chatSkills` + slash command 경로 확인, 설치 신호 `copilot-mcp 81.5K`, `agent-skills 1.8K`, `agnix 26`.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub newest 저신호 군 (`approvals-ui`, `summarize-file`, `prospairrow-websites-mcp`) | ⚠️ 참고만 | 일부 니즈는 있으나 현재 핵심 병목(일일 게임/서비스 생산)과 직접 정합이 약함. 신호(0~1)도 낮아 과대평가 위험. |
| MCP Market 상위군 (`Archon`, `Trigger.dev`, `Chrome DevTools`) | ⚠️ 참고만 | 숫자 신호는 강하나 `browser-cdp-automation`, `coding-agent` 등 기존 스택으로 대체 가능. MCP 운영 복잡도 대비 즉시 ROI 낮음. |
| VSCode 확장군 (`copilot-mcp`, `agent-skills`, `agnix`) | ⚠️ 참고만 | 설정 검증·유통 니즈는 유효하지만 현재 OpenClaw CLI 중심 운영축과 불일치. VSCode 비중 증가 시 재검토. |
| SkillsMP 대규모 카탈로그 직접 흡수 | ⚠️ 참고만 | 카탈로그 규모는 크지만 품질 신호 분리 비용이 큼. 신뢰도 점수/API 안정화 전까지 참고 유지. |

**✅ 도입:** 없음 (이번 회차)

**불필요 판정:** 17건

### ✅ Actions
1. 즉시 신규 도입 보류 (근거 부족)
2. 기존 도입안(`security-audit-toolkit` 패턴 흡수, VS Code `chatSkills` 병행 지원) 실행 지속
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-22-08h-trend-sweep.md`
- `intake-log/2026-02-22-08h-trend-raw.json`

---

## 2026-02-22 04:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 우선순위:** `web_search + web_fetch` 우선 시도.
- **실제 상태:** `web_search` 429(quota/rate limit), MiniPC browser.proxy는 openclaw profile start 실패 + chrome relay 미연결.
- **대체 경로:** MiniPC `system.run` Playwright + `r.jina.ai` + direct API/CLI.
- **SkillsMP:** `261,145` skills, browse cap `5,000` 확인.
- **MCP Market:** `21,654` servers(업데이트 `3 hours ago`), 상위 signal `Superpowers 56,294`, `Context7 46,347`, `Magic 4,283`, `Firecrawl 4,195`, `Browserbase 3,141`, `Godot 1,867`.
- **SkillHub:** `541 skills / 55 sources / 111k downloads`(홈 기준).
- **ClawHub:** `security-audit-toolkit` 실사용 신호(`downloads 1,765 / installsCurrent 6 / stars 4`) 확인.
- **VSCode Agent Skills:** 공식 `chatSkills` GA + 확장 설치 신호(`copilot-mcp 81.5K`, `agent-skills 1.8K`, `agnix 26`).

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `security-audit-toolkit` 패턴 흡수 (내부 보안 인테이크 게이트 v2) | ✅ 도입 | 외부 스킬 intake 보안 검수 병목을 직접 해결. 기존 규칙 분산 상태를 점수화 게이트로 통합 가능. 낮은 도입비 대비 리스크 절감 효과가 큼. |
| VS Code `chatSkills` 패키징 경로(공식 표준) 병행 지원 | ✅ 도입 | OpenClaw 외 협업 환경에서 스킬 재사용 장벽을 낮춤. clawhub 단일 경로의 유통 한계를 보완하며 공식 표준이라 신뢰성 높음. |
| SkillsMP 대규모 카탈로그 직접 흡수 | ⚠️ 참고만 | 규모는 크지만 노이즈/차단으로 정밀 필터 품질이 낮음. 카테고리 API/신뢰도 필드 안정화 시 재검토. |
| MCP Market 상위 서버 즉시 도입 | ⚠️ 참고만 | 지표는 강하나 기존 스택으로 1차 대체 가능. 동일 병목이 2주 연속 반복되면 재검토. |
| SkillHub Marketplace/Desktop 즉시 도입 | ⚠️ 참고만 | GUI 멀티툴 관리 가치는 있으나 CLI 중심 운영축과 정합 낮음. 협업 온보딩 수요 확정 시 재검토. |
| VSCode 서드파티 확장(`agent-skills`, `agnix`) 직접 도입 | ⚠️ 참고만 | 현재 운영축(OpenClaw CLI)과 불일치. VSCode 비중 50%+일 때 재검토. |

**불필요 판정:** 16건

### ✅ Actions
1. `security-audit-toolkit` 패턴을 내부형 보안 인테이크 게이트 v2로 재작성 (Research → Audit → Rewrite)
2. 핵심 스킬 3개를 VS Code `chatSkills` 포맷으로 PoC 패키징
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-22-04h-trend-sweep.md`
- `intake-log/2026-02-22-04h-trend-raw.json`

---

## 2026-02-22 00:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 우선순위:** `web_search + web_fetch` 우선 시도.
- **실제 상태:** `web_search` 429(quota), MiniPC browser.proxy는 node 점검 시 relay 미연결/프로필 시작 실패.
- **대체 경로:** `r.jina.ai + direct API + CLI`.
- **SkillsMP:** `239,658` skills, 평균 `1,826.2`, 피크 `29,797 @ 2026-02-19`, Security `5,913`, `security` 검색 `10,280`.
- **MCP Market:** `mcpmarket.com` 429 차단, `market-mcp.com` 대체 경로에서 `/mcp/*` `100`개 + 상위 signal(`archon 19,110`, `triggerdev 18,629`, `chrome-devtools 18,288`, `contextforge-gateway 4,009`).
- **SkillHub:** 홈페이지 `15,000+` 주장 + CLI JSON(trending/latest/search) 수집 성공.
- **VSCode Agent Skills:** `copilot-mcp` `81,558 installs`, `agent-skills` `1,796 installs`.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| SkillHub CLI non-interactive JSON fallback | ✅ 도입 | web_search 429 + proxy 미가용 시 discovery 중단을 직접 해소. clawhub 단일소스 중복 리스크 완화, npx 기반 저비용 적용 가능. |
| MCP Market detail-page signal harvester | ✅ 도입 | 메인 도메인 차단 시에도 MCP 후보의 수치 signal 확보 가능. 링크 나열이 아닌 숫자 기반 우선순위화로 즉시 효과. |
| MCP Market `contextforge-gateway` | ⚠️ 참고만 | 통합관리 니즈는 있으나 현재 OpenClaw gateway + mcporter로 대체 가능. MCP 운영 복잡도 증가 시 재검토. |
| VSCode `copilot-mcp / agent-skills` 확장군 | ⚠️ 참고만 | 설치 신호는 강하나 OpenClaw CLI 운영축과 정합 낮음. VSCode 비중 50%+ 전환 시 재검토. |
| ClawHub newest `kagi-fastgpt / kagi-summarizer` | ⚠️ 참고만 | fallback 니즈는 맞지만 실사용 신호(다운로드/설치/스타) 0으로 과대평가 위험. |

**불필요 판정:** 23건

### ✅ Actions
1. SkillHub CLI fallback 경로를 intake 루틴에 read-only로 편입 (Research → Audit → Rewrite)
2. MCP Market detail-page signal 파서를 추가해 상위 후보를 수치 기반으로 정렬
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-22-00h-trend-sweep.md`
- `intake-log/2026-02-22-00h-trend-raw.json`

---

## 2026-02-21 16:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 우선순위:** `web_search + web_fetch` 우선 시도.
- **실제 상태:** Brave `web_search` 429(quota), MCP Market 429(Vercel checkpoint), ClawHub API 429.
- **대체 경로:** `r.jina.ai + direct API`.
- **SkillsMP:** `239,658` skills, 평균 `1,762.2`, 피크 `19,898 @ Feb 4, 2026`, Security `5,913`.
- **SkillHub:** `21,564 skills / 5.1M stars`, Trending Top5 `discord/nano-banana-pro/gifgrep/feishu-drive/model-usage`.
- **ClawHub:** partial latest snapshot 확보 후 rate limit.
- **VSCode Agent Skills:** `copilot-mcp` `81,509 installs`, `agent-skills` `1,789 installs`.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| SkillHub `file-search` 패턴 | ✅ 도입 | 반복되는 코드 탐색 병목(과다 결과/컨텍스트 오염)을 직접 해소. 도구는 이미 있으나 실행 전략 스킬 부재. 저비용 내부 재작성 가능하며 효과는 최근 10개 작업 탐색시간 단축률로 검증 가능. |
| ClawHub `agent-rate-limiter` | ⚠️ 참고만 | 429 대응 니즈는 맞지만 기존 search-fallback 라인과 목적 중복. `installsCurrent=0`로 신뢰 신호 약함. |
| VSCode `AutomataLabs.copilot-mcp` | ⚠️ 참고만 | 설치 신호 강하지만 VSCode 종속 비용 큼. OpenClaw CLI 기반 운영으로 대체 가능. |
| MCP Market direct intake | ⚠️ 참고만 | 필요 소스이나 429 차단으로 이번 회차 품질 비교 불가. |

**불필요 판정:** 34건

### ✅ Actions
1. `misskim-skills/skills/code-search-playbook/` 내부 재작성 착수 (Research → Audit → Rewrite)
2. 최근 10개 코드 작업 기준 탐색 시간/오탐률 검증 계획 적용
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-21-16h-trend-sweep.md`
- `intake-log/2026-02-21-16h-trend-raw.json`

---

## 2026-02-21 12:10 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **수집 우선순위:** `web_search + web_fetch` 우선 시도.
- **실제 상태:** Brave `web_search` 429(quota), MCP Market 429(Vercel checkpoint)로 일부 차단.
- **대체 경로:** `r.jina.ai` + direct API/CLI로 수집 지속.
- **SkillsMP:** `239,658` skills, 평균 `1,762.2`, 피크 `19,898 @ Feb 4, 2026`, `security` 검색 `8,590`.
- **SkillHub:** `21.6K Skills / 4.8M Stars`, Trending Top5 `gifgrep/feishu-drive/model-usage/wacli/slack`.
- **ClawHub:** newest 30 / trending 29 샘플 수집.
- **VSCode Agent Skills:** relevance 필터 32개, 상위 `copilot-mcp` `81,492 installs`.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| SkillHub `file-search` 패턴 (ripgrep + ast-grep 워크플로) | ✅ 도입 | 코드 탐색 과다 결과/컨텍스트 오염 병목을 직접 해결. 도구는 있으나 실행 전략 스킬이 없어 재현성이 낮음. 저비용 재작성 가능, 효과는 최근 10개 작업 탐색시간 단축률로 검증. |
| VSCode `AutomataLabs.copilot-mcp` | ⚠️ 참고만 | MCP/skill 관리 니즈는 있으나 OpenClaw + clawhub CLI로 대체 가능. VSCode 종속 비용 대비 ROI 제한. |
| ClawHub newest 저신뢰 클러스터 | ⚠️ 참고만 | 일부 유용 가능성은 있으나 기존 스킬과 중복 다수 + 낮은 `installsCurrent`로 즉시 도입 근거 약함. |
| MCP Market direct intake | ⚠️ 참고만 | 필요하지만 이번 회차는 429 차단으로 품질 검증 자체가 불가. 접속 안정화 후 재검토. |

**불필요 판정:** 32건

### ✅ Actions
1. `misskim-skills/skills/code-search-playbook/` 설계 착수 (Research → Audit → Rewrite)
2. 최근 10개 코드 작업 기준 탐색 시간/오탐률 검증 계획 수립
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-21-12h-trend-sweep.md`
- `intake-log/2026-02-21-12h-trend-raw.json`

---

## 2026-02-21 08:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **MiniPC browser.proxy:** relay 탭 미연결로 부착 실패 → `web_fetch + r.jina.ai + direct API/CLI`로 대체.
- **web_search:** Brave API quota/rate limit(429) 지속.
- **SkillsMP:** `239,658` skills, timeline 평균 `1,762.2`, 피크 `19,898 @ Feb 4, 2026`, `security` 검색 `8,590`.
- **MCP Market:** direct sitemap 기준 `21,091 server URLs / 43,782 skill URLs` 확인.
- **SkillHub:** `21.6K Skills / 4.9M Stars`, Trending Top5 `gifgrep/feishu-drive/model-usage/wacli/slack`.
- **VSCode Agent Skills:** `copilot-mcp` `81,476 installs`.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| MCP Market `prodlint` 패턴 | ✅ 도입 | AI 생성 코드의 배포 전 보안/완성도 점검 병목을 직접 해결. 외부 서버 설치 없이 내부 규칙 스킬로 재작성 가능. |
| MCP Market `shellcheck` | ⚠️ 참고만 | 필요성은 높지만 MCP 없이 shellcheck CLI 게이트로 대체 가능. |
| ClawHub `clawd-zero-trust` | ⚠️ 참고만 | 보안 방향은 맞지만 `healthcheck` 축과 중복 + 실사용 신호 약함(installsCurrent=0). |
| SkillHub Trending Top5 | ⚠️ 참고만 | 대부분 기존 보유 스킬과 기능 중복. 스타 급증만으로 도입 근거 부족. |
| VSCode `copilot-mcp` | ⚠️ 참고만 | 설치 신호는 강하나 VSCode 종속. OpenClaw CLI 중심 운영과 정합 낮음. |
| SkillsMP `security` 클러스터 | ⚠️ 참고만 | 규모는 크지만 파생/중복 항목이 많아 즉시 흡수 품질 낮음. |

**불필요 판정:** 39건

### ✅ Actions
1. `misskim-skills/skills/production-readiness-gate/` 내부형 설계 착수 (Research → Audit → Rewrite)
2. 치명 이슈(시크릿/취약 패턴/환각 임포트) 기준의 dry-run 검증 템플릿 정의
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-21-08h-trend-sweep.md`
- `intake-log/2026-02-21-08h-trend-raw.json`

---

## 2026-02-21 04:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용.
- **web_search:** Brave API quota/rate limit(429)로 실패.
- **SkillsMP:** 카테고리 합 `254,084`, Security `5,913`.
- **MCP Market:** Vercel Security Checkpoint(429)로 직접 수집 차단.
- **MCP fallback(mcp.so):** `17,775` servers, `Search1API/Perplexity/Serper/Jina` 확인.
- **SkillHub:** `21.6K Skills / 4.6M Stars`, Trending 상단 `gifgrep/feishu-drive/model-usage/wacli/slack`.
- **VSCode Agent Skills:** 필터링 29개, `copilot-mcp` `81,453 installs`.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| mcp.so 검색군 기반 검색 fallback 브로커 패턴 | ✅ 도입 | `web_search` 429로 신규 탐색이 중단됨. `web_fetch` 단독 대체 불충분. 외부 코드 무설치 내부 재작성으로 즉시 복구 가능. |
| ClawHub `Ontology` | ⚠️ 참고만 | 구조화 메모리 장점은 있으나 현재 `openclaw-mem + memory-management`로 1차 대응 가능. |
| SkillsMP `Security` 대분류 확장 | ⚠️ 참고만 | 니즈는 높지만 범주가 넓어 저품질 혼입 가능. 탐지율 미달 시 재검토. |
| VSCode `copilot-mcp`/Agent Skills 확장군 | ⚠️ 참고만 | 설치수는 강하나 VSCode 종속. OpenClaw CLI 중심 운영과 정합 낮음. |
| ClawHub `.ai` latest 신규군 | ⚠️ 참고만 | 다수 `installsCurrent=0`로 실사용 신호 약함. |

**불필요 판정:** 37건

### ✅ Actions
1. `misskim-skills/skills/search-fallback-broker-lite/` 내부형 설계 착수 (Research → Audit → Rewrite)
2. `web_search` 정상 시 기본 경로 유지, `429/쿼터초과/타임아웃`에서만 fallback 발동
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-21-04h-trend-sweep.md`
- `intake-log/2026-02-21-04h-trend-raw.json`

---

## 2026-02-21 00:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **web_search:** Brave API quota/rate limit(429)로 탐색 불가.
- **MiniPC browser.proxy:** relay 탭 미연결로 브라우저 수집 실패(정책상 host 브라우저 미사용 유지).
- **SkillsMP:** `239,658` skills, Security `5,913` 확인.
- **MCP Market:** Vercel Security Checkpoint(429)로 직접 수집 차단.
- **SkillHub:** `21.6K Skills / 5.0M Stars`, Trending 상위 `gifgrep/feishu-drive/model-usage/wacli/slack`.
- **ClawHub:** 최근 신규군 다수 저신뢰(`apprentice` 2 downloads).
- **VSCode Agent Skills:** `copilot-mcp` `81,414 installs`, `agent-skills` `1,776 installs`.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| SkillHub CLI + ClawHub `search-cluster` 기반 멀티소스 검색 fallback 패턴 | ✅ 도입 | `web_search` 429로 discovery 중단. `web_fetch` 단독 대체 불충분. 외부 코드 무설치 내부 재작성으로 즉시 복구 가능. |
| VSCode `copilot-mcp / agent-skills` | ⚠️ 참고만 | 설치수 신호는 강하나 VSCode 의존. OpenClaw CLI 중심 운영과 정합 낮음. |
| SkillsMP `Security` 카테고리 확장 | ⚠️ 참고만 | 필요성은 높지만 범주가 넓고 저품질 혼입 가능. 탐지율 미달 시 재검토. |
| ClawHub `apprentice` | ⚠️ 참고만 | 컨셉은 유효하나 실사용 신호 약함(2 downloads / 0 current installs). |

**불필요 판정:** 14건

### ✅ Actions
1. `misskim-skills/skills/search-fallback-federation-lite/` 내부형 설계 착수 (Research → Audit → Rewrite)
2. `web_search` 정상 시 기본 경로 유지, `429/쿼터초과`에서만 fallback 발동
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-21-00h-trend-sweep.md`
- `intake-log/2026-02-21-00h-trend-raw.json`

---

## 2026-02-20 20:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **web_search:** Brave API quota 초과(429) 지속 → `web_fetch + direct API/CLI`로 대체.
- **SkillsMP:** `239,658` skills, 평균 `1,762.2`, 피크 `19,898`(Feb 4), Security `5,913`.
- **MCP Market:** Vercel Security Checkpoint(429)로 직접 수집 차단.
- **MCP fallback (mcp.so):** `search1api`, `perplexity`, `serper-mcp-server`, `brave-search` 노출.
- **SkillHub:** `21.6K Skills / 5.2M Stars`, Trending Today `gifgrep`, `feishu-drive`, `model-usage`, `wacli`, `slack`.
- **ClawHub:** newest 39개 샘플 재수집, 신규군 다수 `installsCurrent=0`.
- **VSCode Agent Skills:** 검색 `1,219` 결과, `copilot-mcp` `81,378 installs`, `agent-skills` `1,772 installs`.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| mcp.so `search1api/perplexity` 기반 검색 fallback 패턴 | ✅ 도입 | `web_search` 429로 discovery 중단. `web_fetch` 단독은 신규 탐색 대체 불충분. 외부 코드 무설치 내부 재작성으로 복구 가능. |
| SkillsMP `Security` 카테고리 확장 | ⚠️ 참고만 | 필요성은 높지만 기존 보안 스캔 라인과 중복. 재검토: 탐지율/오탐률 목표 미달 시. |
| ClawHub `x-twitter-scraper` | ⚠️ 참고만 | X 채널 집행 시 유효하지만 현재 핵심 KPI와 직접 정합 낮음. 재검토: X 퍼포먼스 실험 시작 시. |
| ClawHub `secureclaw-skill` | ⚠️ 참고만 | 보안 포지셔닝 대비 실사용 신호 약함(`downloads 5 / current installs 0`). 재검토: 내부 보안 커버리지 공백 확인 시. |
| VSCode `copilot-mcp / agent-skills` 확장군 | ⚠️ 참고만 | 설치 증가 신호는 있으나 OpenClaw CLI 중심 운영과 정합 낮음. 재검토: VSCode 협업 비중 50%+ 시. |

**불필요 판정:** 57건

### ✅ Actions
1. `misskim-skills/skills/search-fallback-mcp-lite/`로 fallback 라우팅 스킬 내부 재작성 착수(Research → Audit → Rewrite).
2. `web_search` 정상 시 기본 경로 유지, `429/쿼터초과`에서만 fallback 호출.
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지.

### 📁 Full Report
- `intake-log/2026-02-20-20h-trend-sweep.md`
- `intake-log/2026-02-20-20h-trend-raw.json`

---

## 2026-02-20 16:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **web_search:** Brave API quota 초과(429)로 본 회차 검색 불가 → `web_fetch + direct API`로 대체.
- **SkillsMP (r.jina.ai 우회):** `239,658` skills, 평균 `1,762.2`, 피크 `19,898`(Feb 4), Security `5,913`.
- **MCP Market:** `Vercel Security Checkpoint(429)`로 직접 수집 실패.
- **MCP fallback (mcp.so):** 상단 `edgeone-pages-mcp`, `mcpadvisor`, `puppeteer`, `postgres` 노출.
- **SkillHub:** `21.6K skills / 5.3M stars`, Trending Today `gifgrep`, `feishu-drive`, `model-usage`, `wacli`, `slack`.
- **ClawHub:** newest 39개 샘플 다수 `installsCurrent=0`.
- **VSCode Agent Skills:** 검색 결과 `1,218`; `copilot-mcp` 81,333 installs.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| mcp.so `perplexity` / `search1api` 계열 (검색 대체 MCP 패턴) | ✅ 도입 | `web_search` 429로 discovery가 실제 중단됨. `web_fetch` 단독으로는 대체 불충분. 외부 코드 설치 없이 fallback 라우팅 스킬로 내부 재작성 가능. |
| SkillsMP `security` 카테고리 확장 신호 | ⚠️ 참고만 | 필요성은 높지만 동일 축이 이미 진행 중(`agent-config-security-scan-lite`), 신규 도입보다 기존 트랙 완성이 우선. |
| ClawHub `openclaw-gateway-fd-fix` | ⚠️ 참고만 | 목적은 유효하나 증상 재현 로그 부족 + installsCurrent 0로 신뢰 신호 약함. |
| VSCode `copilot-mcp` / `agent-skills` / `agent-skill-ninja` | ⚠️ 참고만 | 생태계 신호는 강하지만 OpenClaw CLI 중심 운영과 정합 낮음. |
| SkillHub Trending 상위군 | ⚠️ 참고만 | 대부분 기존 보유 스택과 중복, 스타 증가는 도입 사유가 아님. |

**불필요 판정:** 51건

### ✅ Actions
1. `misskim-skills/skills/search-fallback-mcp-lite/` 설계 착수 (Research → Audit → Rewrite)
2. `web_search` 429/쿼터 초과 시에만 fallback 발동하는 조건부 라우팅 적용
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-20-16h-trend-sweep.md`
- `intake-log/2026-02-20-16h-trend-raw.json`

---

## 2026-02-20 08:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** `239,658` skills, 평균 `1,762.2`, 피크 `19,898`(Feb 4). Security 카테고리 `5,913`.
- **MCP Market:** 본회차 `Vercel Security Checkpoint(429)`로 직접 수집 실패.
- **MCP fallback (mcp.so):** `17,764` MCP servers 카탈로그 확인.
- **SkillHub:** `21.6K skills / 4.0M stars`, Trending Today 상단은 기존 보유군 중심.
- **ClawHub:** non-suspicious 상위 유지, newest는 다수 `0 current installs`.
- **VSCode Agent Skills:** `copilot-mcp` 81k installs(4.3/5, 8), `formulahendry.agent-skills` 1.8k installs(5.0/5, 1, Dec 2025 업데이트).

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| SkillsMP `security-scan` 패턴 | ✅ 도입 | 외부 스킬 intake의 설정/MCP/훅 보안 점검 자동화 공백을 직접 메움. 외부 코드 설치 없이 룰만 내부 재작성 가능. |
| ClawHub `counterclaw-core` | ⚠️ 참고만 | 방어 목적은 맞지만 기존 DLP/credential 게이트와 중복 + 실사용 신호 약함(8 downloads, 0 current installs). |
| ClawHub `sentry-issues` | ⚠️ 참고만 | 장애 분석 자동화는 유효하나 Sentry 표준 도입이 선행돼야 ROI 발생. |
| mcp.so `EdgeOne Pages MCP` | ⚠️ 참고만 | 배포 대안 가치는 있으나 현재 GitHub Pages 파이프라인으로 1차 대응 가능. |
| SkillHub `context-optimization` | ⚠️ 참고만 | `openclaw-mem`/내부 컨텍스트 규율과 중복, 즉시 실행효과 제한. |
| VSCode `copilot-mcp` / `agent-skills` | ⚠️ 참고만 | 생태계 신호는 강하나 OpenClaw CLI 운영축과 불일치. |

**불필요 판정:** 26건

### ✅ Actions
1. `misskim-skills/skills/agent-config-security-scan-lite/` 설계 착수 (Research → Audit → Rewrite)
2. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지
3. MCP Market 체크포인트 차단은 다음 회차 재검증(직접 수집 복구 전까지 차선 소스 병행)

### 📁 Full Report
- `intake-log/2026-02-20-08h-trend-sweep.md`

---

## 2026-02-20 04:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** `r.jina.ai` 우회로 **239,658 skills** 확인 (timeline 평균 **1,762.2**, 피크 **19,898 @ 2/4**).
- **MCP Market:** 원문 HTML 수집 기준 **21,507 servers**. Latest 상단 `NotebookLM`, `Marketer`, `Ocean`, `Substack Publisher`, `Rug Munch Intelligence`, `FastAPI`.
- **SkillHub (skillhub.club):** **21.6K skills / 4.0M stars**. Trending Today 상단 `coding-agent`, `feishu-drive`, `model-usage`, `wacli`, `slack`.
- **ClawHub:** `tavily-search` 신호 확인 (**downloads 23,180 / installsCurrent 133 / stars 71**), 최신 신규군은 저신뢰(0~1 installs 다수).
- **VSCode Agent Skills:** `copilot-mcp` **81,251 installs**, `formulahendry.agent-skills` **~1.75K installs**(v0.0.2, 2025-12-26).

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `tavily-search` | ✅ 도입 | Brave 검색 429/쿼터초과로 실제 공백 존재. `web_fetch`는 URL known 케이스만 가능해 대체 불완전. 도입비(API 키/소액비용) 대비 실패 재시도 시간 절감 효과 큼. 지표(23,180 downloads/133 current installs/71 stars)로 저신뢰 신규군과 구분 가능. |
| MCP Market `FastAPI` | ⚠️ 참고만 | API 자동화 수요는 있으나 `openapi-tool-scaffold`/기존 스택으로 1차 대응 가능. 재검토: API 프로젝트 동시 3개+ 병목 발생 시. |
| MCP Market `Substack Publisher` | ⚠️ 참고만 | 현재 핵심 병목(수익화/배포 자동화)과 직접 정합 낮음. 재검토: Substack 채널 KPI 승격 시. |
| VSCode `copilot-mcp` | ⚠️ 참고만 | 설치 신호는 강하나 OpenClaw CLI 중심 운영과 불일치. 재검토: VSCode 워크플로 비중 50%+ 시. |
| VSCode `formulahendry.agent-skills` | ⚠️ 참고만 | 멀티소스 탐색 장점은 있으나 업데이트 정체 + 평점 표본 부족. 재검토: 내부 탐색 리드타임 악화 시. |

**불필요 판정:** 18건

### ✅ Actions
1. `misskim-skills/skills/search-fallback-tavily-lite/` 설계 착수 (Research → Audit → Rewrite)
2. `web_search` 429/쿼터초과 시에만 fallback 발동하는 조건부 라우팅 규칙 적용
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-20-04h-trend-sweep.md`
- `intake-log/2026-02-20-04h-trend-raw.json`

---

## 2026-02-19 20:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** **239,658 skills**. recent 상단 `shadmin-feature-dev`, `nippo`, `check-tests-commit`, `maxxit-lazy-trading`, `audio-extractor` 확인.
- **MCP Market:** **21,362 servers**(updated just now). latest에 `Substack Publisher`, `DevOps Practices`, `LibreNMS`, `Gemini Search`, `Zen of Languages`, `MyInstants` 확인.
- **SkillHub (skillhub.club):** **21.6K skills / 4.0M stars**. Trending Today 상단 `coding-agent`, `feishu-drive`, `model-usage`, `wacli`, `slack` 확인.
- **ClawHub:** newest 30개 샘플에서 `guardian`, `openclaw-skillguard`, `agents-skill-security-audit` 확인.
- **VSCode Agent Skills:** 검색 `agent skills` **1,102 results**, `copilot-mcp` **81.1K installs**, `Agent Skills` **1.8K installs**, `agnix` **19 installs**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `guardian` (privacy-audit 패턴) | ✅ 도입 | 외부 스킬 재배포/내부화 시 개인정보/로컬데이터 누출 차단 게이트 공백을 직접 해소. |
| ClawHub `openclaw-skillguard` | ⚠️ 참고만 | 보안 스캔 방향은 유효하나 기존 추진 중 게이트와 범위 중복이 큼. |
| VSCode `agnix` | ⚠️ 참고만 | 룰셋 자산 가치는 높지만 VSCode 종속 도입은 현재 운영축과 불일치. |
| MCP Market `Substack Publisher` | ⚠️ 참고만 | 채널 확장 가치는 있으나 현재 핵심 병목(배포/수익화)과 직접 정합 낮음. |
| MCP Market `Gemini Search` | ⚠️ 참고만 | 검색 fallback 니즈는 유효하나 기존 fallback 라인과 중복 가능성 큼. |
| SkillsMP `check-tests-commit` 계열 | ⚠️ 참고만 | 내부 `verify-before-done` + SDD/TDD 규율로 핵심 수요를 이미 충족. |
| SkillHub 상위군(`coding-agent`/`feishu-drive`/`model-usage`) | ⚠️ 참고만 | 보유 스택과 기능 중복이 커 순증 가치가 낮음. |

**불필요 판정:** 72건

### ✅ Actions
1. `misskim-skills/skills/skill-package-privacy-gate/` 설계 착수 (Research → Audit → Rewrite)
2. Molt Road/molt.host/MoltHub **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-19-20h-trend-sweep.md`

---

## 2026-02-19 16:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** **239,658 skills**. recent 상단 `shadmin-feature-dev`, `nippo`, `check-tests-commit`, `maxxit-lazy-trading`, `audio-extractor` 확인.
- **MCP Market:** **21,362 servers**(updated just now). latest에 `Substack Publisher`, `DevOps Practices`, `LibreNMS`, `Gemini Search`, `Zen of Languages`, `MyInstants` 확인.
- **SkillHub (skillhub.club):** **21.6K skills / 4.1M stars**. Hot/Rankings 상단 `coding-agent`, `feishu-drive`, `model-usage`, `wacli`, `slack` 확인.
- **ClawHub:** newest 40개 샘플에서 `clawguarddevin`, `openclaw-cache-kit`, `agent-spawner` 확인. Molt 계열 노출은 정책 차단.
- **VSCode Agent Skills:** 검색 `agent skills` **1,103 results**, `copilot-mcp` **81.1K installs**, `Agent Skills` **1.8K installs**, `agnix` **18 installs**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `clawguarddevin` 패턴 | ✅ 도입 | 외부 스킬 intake의 악성패턴 자동 스캔 공백을 직접 해소. 수동 Audit만으로는 누락 리스크가 남음. |
| VSCode `agnix` 룰셋(패턴 흡수) | ✅ 도입 | SKILL.md/AGENTS/MCP 설정 검증 자동화가 현재 부재. 확장 자체가 아니라 룰셋만 내부 재작성 시 ROI가 큼. |
| MCP Market `Substack Publisher` | ⚠️ 참고만 | 채널 확장 가치는 있으나 현재 핵심 병목(배포/수익화)과 직접 정합 낮음. |
| MCP Market `Gemini Search` | ⚠️ 참고만 | 검색 fallback 니즈는 유효하나 기존 fallback 라인과 중복 가능성 큼. |
| SkillsMP `check-tests-commit` 계열 | ⚠️ 참고만 | 내부 `verify-before-done` + SDD/TDD 규율로 핵심 수요를 이미 충족. |
| SkillHub 상위군(`coding-agent`/`feishu-drive`/`model-usage`) | ⚠️ 참고만 | 보유 스택과 기능 중복이 커 순증 가치가 낮음. |
| ClawHub `openclaw-cache-kit` | ⚠️ 참고만 | 비용절감 잠재력은 있으나 설정 리스크 검증이 선행돼야 함. |

**불필요 판정:** 81건

### ✅ Actions
1. `misskim-skills/skills/skill-intake-malware-gate/` 설계 착수 (Research → Audit → Rewrite)
2. `misskim-skills/skills/agent-config-lint-gate/` 설계 착수 (Research → Audit → Rewrite)
3. Molt Road/molt.host/MoltHub/Moltbook **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-19-16h-trend-sweep.md`

---

## 2026-02-19 12:06 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** **239,658 skills**. recent 상단 `shadmin-feature-dev`, `nippo`, `check-tests-commit`, `maxxit-lazy-trading` 확인.
- **MCP Market:** **21,362 servers**(updated just now). latest에 `Substack Publisher`, `DevOps Practices`, `LibreNMS`, `Gemini Search`, `Zen of Languages`, `MyInstants` 확인.
- **SkillHub (skillhub.club):** **21.6K skills / 4.4M stars**, Trending Today `feishu-drive`, `model-usage`, `github`, `wacli`, `trello` 유지.
- **ClawHub:** newest 60개 샘플에서 `clawwall`, `memory-hygiene`, `reddit-insights` 확인. Molt 계열 노출은 정책 차단.
- **VSCode Agent Skills:** 검색 `agent skills` **1,103 results**, `copilot-mcp` **81.1K installs**, `formulahendry.agent-skills` **1.8K installs**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `clawwall` | ✅ 도입 | outbound secret/PII 유출 하드블록 공백을 직접 해소. 인기도가 아니라 리스크 갭 기반 채택. |
| MCP Market `Substack Publisher` | ⚠️ 참고만 | 배포 확장 가치는 있으나 현재 우선 채널과 직접 병목 정합이 낮음. |
| MCP Market `Gemini Search` | ⚠️ 참고만 | 검색 fallback 니즈는 유효하나 기존 fallback 경로와 중복 가능성 큼. |
| SkillsMP `check-tests-commit` 계열 | ⚠️ 참고만 | 내부 `verify-before-done` + SDD/TDD 규율로 핵심 기능 대체 가능. |
| SkillHub 상위군(`feishu-drive`/`model-usage`) | ⚠️ 참고만 | 대형 star는 확산 신호일 뿐 현재 운영 병목 해결과 거리 있음. |
| ClawHub `memory-hygiene` | ⚠️ 참고만 | `openclaw-mem` 및 내부 메모리 운영 규율과 기능 중복. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | 설치 신호는 강하나 OpenClaw CLI 중심 운영과 불일치. |

**불필요 판정:** 96건

### ✅ Actions
1. `misskim-skills/skills/outbound-dlp-gate/` 설계 착수 (Research → Audit → Rewrite)
2. Molt Road/molt.host/MoltHub/Moltbook **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-19-12h-trend-sweep.md`

---

## 2026-02-19 08:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 브라우저 수집 성공, **239,658 skills**. recent 상단에 `shadmin-feature-dev`, `nippo`, `check-tests-commit`, `maxxit-lazy-trading` 확인.
- **MCP Market:** 브라우저 수집 성공, **21,325 servers**. latest에 `DevOps Practices`, `LibreNMS`, `Gemini Search`, `Zen of Languages`, `MyInstants`, `Vigilo` 확인.
- **SkillHub (skillhub.club):** **21.6K skills / 4.3M stars**, Trending Today 상단 `feishu-drive`, `model-usage`, `github`, `wacli`, `trello` 노출.
- **ClawHub:** newest 59개 샘플에서 `credential-scanner`, `flowclaw`, `loopwind`, `gamer-news` 확인.
- **VSCode Agent Skills:** 검색 `agent skills` **1,102 results**, `copilot-mcp` **81K installs**, `formulahendry.agent-skills` **1,746 installs**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `credential-scanner` | ✅ 도입 | 외부 스킬 intake 단계의 secret leak 탐지 공백을 직접 메우며 도입비 대비 리스크 절감 효과가 큼. |
| ClawHub `flowclaw` | ⚠️ 참고만 | 멀티모델 라우팅 수요는 있으나 다중 인증/운영 복잡도가 높아 즉시 ROI 불명확. |
| MCP Market `Gemini Search` | ⚠️ 참고만 | 검색 백업 니즈는 유효하지만 `search-fallback-openrouter` 추진과 기능 중복 가능성 큼. |
| SkillsMP `check-tests-commit` 계열 | ⚠️ 참고만 | `verify-before-done` + `tdd-discipline`로 핵심 문제를 이미 커버 중. |
| SkillHub `context-optimization` | ⚠️ 참고만 | `openclaw-mem`/내부 메모리 규율과 중복. 비용 지표 악화 시 재검토. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | 설치 신호는 강하나 OpenClaw CLI 중심 운영과 정합이 낮음. |

**불필요 판정:** 19건

### ✅ Actions
1. `misskim-skills/skills/credential-leak-gate/` 설계 착수 (Research → Audit → Rewrite)
2. Molt Road/molt.host/MoltHub/Moltbook **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-19-08h-trend-sweep.md`

---

## 2026-02-19 04:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 브라우저 수집 성공, **239,658 skills**. recent 상단에 `shadmin-feature-dev`, `nippo`, `check-tests-commit` 확인.
- **MCP Market:** 브라우저 수집 성공, **21,325 servers**. latest에 `DevOps Practices`, `LibreNMS`, `Gemini Search`, `Zen of Languages`, `Vigilo` 확인.
- **SkillHub (skillhub.club):** **21.3K skills / 4.3M stars**, Trending Today 상단 `feishu-drive`, `model-usage`, `github` 노출.
- **ClawHub:** newest 38개 샘플에서 `memory-tools`, `proxymock`, `openrouter-perplexity`, `exa-tool` 확인. `moltbook-cli-tool` 노출.
- **VSCode Agent Skills:** 검색 `agent skills` **1,099 results**, `copilot-mcp` **81K installs**, `formulahendry.agent-skills` **1.7K installs**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `openrouter-perplexity` | ✅ 도입 | Brave 429/quota 공백을 메우는 검색 fallback 패턴으로 즉시 ROI가 높음. |
| ClawHub `memory-tools` | ⚠️ 참고만 | `openclaw-mem`/내부 메모리 규율과 기능 중복. 회상 실패 반복 시 재검토. |
| MCP Market `Gemini Search` | ⚠️ 참고만 | 검색 백업 니즈는 맞지만 `openrouter` fallback과 중복 가능성이 커 우선순위 낮음. |
| SkillsMP `check-tests-commit` 계열 | ⚠️ 참고만 | `verify-before-done` + `tdd-discipline`로 핵심 기능 이미 대응 중. |
| SkillHub `skill-creator` | ⚠️ 참고만 | 내부 `skill-authoring`/작성 규약과 중복. 제작 리드타임 악화 시 재검토. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | 설치 신호는 강하나 OpenClaw CLI 중심 운영과 불일치. |

**불필요 판정:** 18건

### ✅ Actions
1. `misskim-skills/skills/search-fallback-openrouter/` 설계 착수 (Research → Audit → Rewrite)
2. Molt Road/molt.host/MoltHub/Moltbook **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-19-04h-trend-sweep.md`

---

## 2026-02-19 00:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 브라우저 수집 성공, **239,658 skills**. recent 상단에 `shadmin-feature-dev`, `check-tests-commit`, `maxxit-lazy-trading` 등 확인.
- **MCP Market:** 브라우저 수집 성공, **21,325 servers**. latest에 `DevOps Practices`, `LibreNMS`, `Gemini Search`, `Vigilo` 확인(다수 0 usage).
- **SkillHub (skillhub.club):** **21.3K skills / 4.7M stars**, Hot에 `systematic-debugging`, `file-search`, `context-optimization` 지속 노출.
- **ClawHub:** newest 샘플에서 `ddg-web-search`, `agent-audit`, `lark-base` 확인.
- **VSCode Agent Skills:** 검색 `agent skills` **1,095 results**, `formulahendry.agent-skills` **1,741 installs**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `ddg-web-search` | ✅ 도입 | Brave 429로 반복되는 검색 공백을 직접 메우는 fallback 패턴. |
| MCP Market `Vigilo` | ⚠️ 참고만 | 감사 니즈는 유효하나 현재 세션/로그 체계로 1차 대응 가능. |
| SkillHub `context-optimization` | ⚠️ 참고만 | `openclaw-mem`/내부 메모리 규율과 중복. |
| SkillsMP `check-tests-commit` 계열 | ⚠️ 참고만 | 기존 `verify-before-done`/TDD 루틴으로 핵심 기능 대응 중. |
| VSCode `formulahendry.agent-skills` | ⚠️ 참고만 | IDE 편의성은 있으나 OpenClaw CLI 중심 운영과 불일치. |

**불필요 판정:** 17건

### ✅ Actions
1. `misskim-skills/skills/search-fallback-router/` 설계 착수 (Research → Audit → Rewrite)
2. Molt Road/molt.host/MoltHub **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-19-00h-trend-sweep.md`

---

## 2026-02-18 20:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 실시간 경로는 Cloudflare 403, `sitemap.xml`만 접근 가능(직접 신규 검증 제한).
- **MCP Market:** 홈 latest에서 `java-decompiler-1`, `dotnet-websearch`, `sql-sentinel`, `openwrt` 확인. sitemap 기준 **21,091 servers**.
- **SkillHub (skillhub.club):** **21.3K skills / 4.6M stars**, Hot에 `systematic-debugging`, `file-search`, `context-optimization` 노출.
- **ClawHub:** newest 샘플에서 `agent-audit`, `security-sentinel`, `fathom-meetings` 확인.
- **VSCode Agent Skills:** `formulahendry.agent-skills` **1,737 installs**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `agent-audit` | ✅ 도입 | 모델/크론/세션 비용-성과 감사의 수동 병목을 직접 해결. |
| ClawHub `security-sentinel` | ⚠️ 참고만 | 보안 니즈는 있으나 `healthcheck` 루틴과 중복 범위 큼. |
| MCP Market `SQL Sentinel` | ⚠️ 참고만 | DB 자동화 비중이 아직 낮아 즉시 ROI 제한. |
| SkillHub `context-optimization` | ⚠️ 참고만 | `openclaw-mem`/내부 메모리 규율과 핵심 기능 중복. |
| SkillsMP `mintlify` | ⚠️ 참고만 | 문서 자동화 가치는 있으나 현재 우선 병목과 정합 낮음. |
| VSCode `formulahendry.agent-skills` | ⚠️ 참고만 | IDE 편의성은 있으나 OpenClaw CLI 중심 운영과 불일치. |

**불필요 판정:** 15건

### ✅ Actions
1. `misskim-skills/skills/agent-cost-audit-gate/` 설계 착수 (Research → Audit → Rewrite)
2. Molt Road/molt.host/MoltHub **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-18-20h-trend-sweep.md`

---

## 2026-02-18 16:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 233,309 skills. 최신 노출에서 `mintlify`, `imsg`, `feishu-doc` 확인.
- **MCP Market:** 21,157 servers. latest에 `Java Decompiler`, `Dotnet Websearch`, `SQL Sentinel`, `OpenWrt`(0 usage 다수).
- **SkillHub (skillhub.club):** 21.3K skills / 4.8M stars. `context-optimization`, `systematic-debugging` 상위 노출.
- **ClawHub:** 8,222 skills. Newest에서 `Geepers Data`, `DeepReader`, `Audit OpenClaw Security` 확인.
- **VSCode Agent Skills:** `formulahendry.agent-skills` 1,733 installs, 5.0(1 review), v0.0.2.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `Geepers Data` | ✅ 도입 | Brave 검색 쿼터 제한으로 생기는 수집 공백을 직접 메움. |
| ClawHub `DeepReader` | ⚠️ 참고만 | URL 읽기 니즈는 있으나 `summarize`/`web_fetch`와 기능 중복. |
| MCP Market `Task Master` | ⚠️ 참고만 | 수요는 있으나 현 queue-manager + subagent 체계로 핵심 요구 충족. |
| MCP Market `Godot` MCP | ⚠️ 참고만 | 도메인 정합성은 높지만 현 godot 스택으로 1차 대응 가능. |
| SkillsMP `mintlify` | ⚠️ 참고만 | 문서 자동화 가치는 있으나 현재 우선 병목과 직접 정합 낮음. |
| SkillHub `context-optimization` | ⚠️ 참고만 | 컨텍스트 최적화 수요는 있으나 `openclaw-mem`/내부 메모리 루틴과 중복. |
| VSCode `formulahendry.agent-skills` | ⚠️ 참고만 | IDE 편의성은 있으나 OpenClaw CLI 중심 운영과 불일치. |

**불필요 판정:** 18건

### ✅ Actions
1. `misskim-skills/skills/data-source-fallback-bridge/` 설계 착수 (Research → Audit → Rewrite)
2. Molt Road/molt.host/MoltHub **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-18-16h-trend-sweep.md`

---

## 2026-02-18 12:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 233,309 skills. 상단 노출 `mintlify`, `feishu-doc`, `obsidian` 확인.
- **MCP Market:** 21,157 servers. latest에 `Java Decompiler`, `Dotnet Websearch`, `Turtle Noir`(0 usage 다수).
- **SkillHub.ai:** “Coming soon” 상태 유지.
- **ClawHub:** newest 20개 샘플에서 `faster-whisper`, `web-qa-bot`, `arc-compliance-checker` 확인.
- **VSCode Agent Skills:** 검색 1,095 결과. `copilot-mcp` 80.9K, `agent-skills` 1.7K installs.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `arc-compliance-checker` | ✅ 도입 | 외부 스킬 intake의 정책 준수 판정 자동화 병목과 직접 정합. |
| ClawHub `web-qa-bot` | ✅ 도입 | 기능 안정성 우선 운영 대비 스모크/접근성/시각 회귀 자동화 표준이 부재. |
| ClawHub `faster-whisper` | ⚠️ 참고만 | 속도 이점 가능성은 있으나 기존 Whisper 스택과 중복. SLA 초과 시 벤치마크 후 재검토. |
| MCP Market `Task Master` | ⚠️ 참고만 | 수요는 있으나 현행 queue-manager + subagent 체계로 핵심 요구 충족. |
| SkillsMP `query-data` 계열 | ⚠️ 참고만 | 분석 표준화 가치는 있으나 현재 최우선 병목(수익화/배포/QA)과 직접 정합 낮음. |
| VSCode `copilot-mcp` / `agent-skills` 확장군 | ⚠️ 참고만 | 설치 수치는 강하나 OpenClaw CLI 중심 운영과 불일치. |

**불필요 판정:** 13건

### ✅ Actions
1. `misskim-skills/skills/skill-intake-policy-gate/` 실행 전환 (Research → Audit → Rewrite)
2. `misskim-skills/skills/web-regression-guard/` 신규 설계 착수 (Research → Audit → Rewrite)
3. Molt Road/molt.host/MoltHub **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-18-12h-trend-sweep.md`

---

## 2026-02-18 08:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 233,309 skills. recent 상단에 `query-data`, `data-analysis`, `browsing-workflow` 확인.
- **MCP Market:** 21,135 servers. latest에 `Java Decompiler`, `Dotnet Websearch`, `AI Inspector` 노출(다수 0 usage).
- **SkillHub.ai:** 여전히 “Coming soon” 상태.
- **ClawHub:** newest 30개 샘플에서 `arc-compliance-checker`, `agent-self-assessment`, `SnapRender` 확인.
- **VSCode Agent Skills:** 검색 1,093 결과. `copilot-mcp` 80.8K, `agent-skills` 1.7K, `agnix` 17 installs.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `arc-compliance-checker` | ✅ 도입 | 외부 스킬 intake의 정책 준수 판정 자동화 병목과 직접 정합. |
| VSCode `avifenesh.agnix` | ⚠️ 참고만 | 규칙 lint 아이디어는 유효하나 VSCode 종속. CLI 룰팩 추출 가능 시 재검토. |
| MCP Market `AI Inspector` | ⚠️ 참고만 | 브라우저 자동화 스택 중복. 실패율/SLA 악화 시 재검토. |
| SkillsMP `query-data` | ⚠️ 참고만 | 분석 표준화는 유효하나 현 우선 병목(배포/수익화)과 직접 정합 낮음. |
| ClawHub `SnapRender` | ⚠️ 참고만 | 기능 중복. visual diff 운영 KPI화 시 재검토. |

**불필요 판정:** 8건

### ✅ Actions
1. `misskim-skills/skills/skill-intake-policy-gate/` 내부형 설계 착수 (Research → Audit → Rewrite)
2. Molt Road/molt.host/MoltHub **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-18-08h-trend-sweep.md`

---

## 2026-02-18 04:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 233,309 skills. recent에 `query-data`, `data-analysis`, `browsing-workflow` 등 2/17 신규 다수.
- **MCP Market:** 21,135 servers. latest 섹션에 `AI Inspector`, `Java Decompiler`, `Dotnet Websearch` 노출.
- **SkillHub:** 21.3K skills / 5.7M stars. Solopreneur Toolkit에 `requesthunt` 포함 유지.
- **ClawHub:** newest 30개 샘플 수집에서 `agents-skill-security-audit` 확인.
- **VSCode Agent Skills:** 검색 1,211 결과. `copilot-mcp` 80,815 installs, `agent-skills` 1,723 installs.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `agents-skill-security-audit` | ✅ 도입 | 외부 스킬 intake 수동 감사 공백을 직접 해소. 낮은 도입비 대비 리스크 감소 효과 큼. |
| SkillHub `requesthunt` | ✅ 도입 | 수요 신호 수집 자동화 공백 해결. 아이템 선정 속도 개선 기대. |
| VSCode `avifenesh.agnix` | ⚠️ 참고만 | 규칙 lint 아이디어 유효하나 VSCode 종속. CLI 추출 가능 시 재검토. |
| MCP Market `AI Inspector` | ⚠️ 참고만 | 현재 브라우저 자동화 스택과 중복. 실패율 악화 시 재검토. |
| SkillsMP `query-data` | ⚠️ 참고만 | 분석 니즈는 있으나 현 병목과 직접 정합 낮음. |
| VSCode `AutomataLabs.copilot-mcp` | ⚠️ 참고만 | 설치 신호 강하지만 OpenClaw CLI 중심 운영과 불일치. |

**불필요 판정:** 4건

### ✅ Actions
1. `misskim-skills/skills/skill-intake-security-audit-lite/` 내부형 설계 착수 (Research → Audit → Rewrite)
2. `misskim-skills/skills/request-signal-harvester/` 내부형 설계 착수 (Research → Audit → Rewrite)
3. Molt Road/molt.host/MoltHub **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-18-04h-trend-sweep.md`

---

## 2026-02-17 20:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 227,170 skills. recent 상단이 Android 분해형 대량 항목(2/17)으로 채워져 신호 대비 노이즈가 큼.
- **MCP Market:** 21,091 servers(약 1시간 전 업데이트). latest에 `ShellCheck`, `Appwrite`, `Mem0` 노출.
- **SkillHub:** 21.3K skills / 5.5M stars 표기, 랭킹/스택 중심 큐레이션 강화.
- **ClawHub:** 7,911 skills. 자동화·메모리·브라우저 계열 고다운로드 항목 재확인.
- **VSCode Agent Skills:** 검색 1,092 결과. `copilot-mcp` 80.7K installs, `formulahendry.agent-skills` 1.7K installs.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| VSCode `agnix - Agent Config Linter` | ✅ 도입 | 외부 스킬 intake 정적 검증 공백(SKILL.md/AGENTS.md)을 직접 메움. 규칙셋 패턴 흡수 비용 대비 품질 게이트 효과가 큼. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | 설치 신호는 강하지만 VSCode 중심. OpenClaw CLI 운영축과 직접 결합도 낮음. |
| MCP Market `Mem0` | ⚠️ 참고만 | `openclaw-mem` 검증 기간과 기능 중복. 회상 지표 악화 시 재검토. |
| MCP Market `Godot` | ⚠️ 참고만 | 도메인 적합성은 높으나 현재 godot 스택으로 1차 대응 가능. |
| SkillsMP recent Android cluster | ⚠️ 참고만 | 현재 핵심 파이프라인(웹게임/도구/마케팅 자동화)과 직접 정합 낮음. |
| ClawHub `Agent Browser` | ⚠️ 참고만 | 기존 `browser-cdp-automation` 및 OpenClaw browser tool과 기능 중복. |
| SkillHub `AI Video Ad Generator Stack` | ⚠️ 참고만 | 유료/크레딧 의존도가 높고 내부 파이프라인과 중복 구간 존재. |

**불필요 판정:** 19건

### ✅ Actions
1. `misskim-skills/skills/agent-config-lint-gate/` 내부형 설계 착수 (Research → Audit → Rewrite)
2. Molt Road/molt.host **ABSOLUTE BLOCK** 유지 (MoltHub 연계 항목 즉시 제외)
3. 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-17-20h-trend-sweep.md`

---

## 2026-02-17 16:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 227,170 skills, recent 상단이 Android 분해형 스킬 중심(2/17).
- **MCP Market:** 21,091 servers, latest에 `ShellCheck`, `Appwrite`, `Mem0` 등 신규 노출.
- **SkillHub:** Hot leaderboard 570 skills(6시간 주기 갱신).
- **ClawHub:** `explore` 최신에 `paypal`, `dependency-auditor`, `bitwarden-secrets` 등 확인.
- **VSCode Agent Skills:** `copilot-mcp` 80,690 installs(최신 0.0.91), `formulahendry.agent-skills` 1,714 installs.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| MCP Market `ShellCheck` MCP | ✅ 도입 | 쉘 스크립트 품질 게이트 공백을 직접 메움. 도입 비용 대비 회귀 방지 효과가 큼. |
| ClawHub `paypal` | ✅ 도입 | 직접결제 퍼널 강화(현재 수익화 우선순위)와 정합. 기존 스킬셋에 webhook 검증 템플릿 부재. |
| ClawHub `dependency-auditor` | ⚠️ 참고만 | 유용하지만 `healthcheck`/기존 검증 루프와 일부 중복. 의존성 이슈 재발 시 재검토. |
| SkillHub `audit-website` | ⚠️ 참고만 | `web-design-guidelines` + 내부 QA 루틴으로 1차 대응 가능. 유입 하락 시 재검토. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | 설치 신호는 강하지만 VSCode UI 중심이라 OpenClaw CLI 중심 운영과 불일치. |
| SkillsMP recent Android cluster | ⚠️ 참고만 | 현재 핵심 파이프라인(웹게임/도구/배포)과 직접 연관 약함. Android 네이티브 착수 시 재검토. |
| MCP Market `Mem0` | ⚠️ 참고만 | `openclaw-mem` 검증 기간과 기능 중복. 회상 지표 악화 시 재검토. |

**불필요 판정:** 12건

### ✅ Actions
1. `misskim-skills/skills/shell-script-guard/` 내부형 스킬 설계 착수 (Research → Audit → Rewrite)
2. `misskim-skills/skills/payments-paypal-funnel/` 신규 설계 착수 (Research → Audit → Rewrite)
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-17-16h-trend-sweep.md`

---

## 2026-02-17 12:07 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 227,170 skills. recent 상단은 Android 레포 분해형 신규 항목(2/17) 중심.
- **MCP Market:** 21,091 servers (약 1시간 전 업데이트). latest에 `ShellCheck`, `Dolex`, `K-Trendz`, `Appwrite`, `Mem0` 노출.
- **SkillHub:** 20,922 skills. `file-search`, `systematic-debugging`, `mcp-builder` 상위 유지.
- **ClawHub:** 7,834 skills. Newest에 `Arc Security MCP`, `Lily Memory`, `OpenClaw Backup Safe` 확인.
- **VSCode Agent Skills:** 검색 1,089 결과. `copilot-mcp` 80.7K installs, `Agent Skills` 1.7K installs.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| MCP Market `ShellCheck` MCP | ✅ 도입 | 쉘 스크립트 품질 게이트 공백을 직접 해소. 수동 점검 대비 도입 비용이 낮고 회귀 예방 ROI가 큼. |
| ClawHub `Arc Security MCP` | ⚠️ 참고만 | 문제정의(스킬 안전성)는 맞지만 신뢰 신호(별점/검증 사례) 부족. 외부 스킬 인테이크 병목 시 재검토. |
| SkillHub `mcp-builder` | ⚠️ 참고만 | MCP 제작 가이드는 유용하나 내부 `openapi-tool-scaffold`/`mcporter`로 1차 대체 가능. MCP 리드타임 지연 시 재검토. |
| VSCode `agnix` (Agent Config Linter) | ⚠️ 참고만 | lint 필요성은 높지만 VSCode 의존(17 installs)으로 현재 OpenClaw CLI 중심 운영과 불일치. |
| ClawHub `Lily Memory` | ⚠️ 참고만 | 메모리 문제 해결 주장 있으나 `openclaw-mem` 검증기간과 기능 중복. 회상 지표 악화 시 재검토. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | 설치 신호는 강하지만 IDE 확장 중심이라 현재 운영축과 불일치. IDE 표준화 시 재검토. |

**불필요 판정:** 14건

### ✅ Actions
1. `misskim-skills/skills/shell-script-guard/` 내부형 설계 착수 (Research → Audit → Rewrite)
2. Molt Road/molt.host **ABSOLUTE BLOCK** 유지 (Molt 계열 신규 항목 포함)
3. 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-17-12h-trend-sweep.md`

---

## 2026-02-17 08:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 브라우저 접근 정상. 총 227,170 skills, recent 상단은 레포 분해형(Android/React) 항목 비중이 높음.
- **MCP Market:** 21,087 servers. `Godot`, `Firecrawl`, `Browserbase` 등 고노출 항목 확인.
- **SkillHub:** 21.3K skills / 2.4M stars. `file-search(S 9.0)` 포함 고평가 스킬 노출.
- **ClawHub:** 브라우저/CLI 모두 정상. `openclaw-skill-observability`, `openclaw-watchdog` 등 최신 항목 확인.
- **VSCode Agent Skills:** 검색 1,089 결과. `copilot-mcp` 80.6K installs, `Agent Skills` 1.7K installs.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `openclaw-skill-observability` | ✅ 도입 | 24시간 비용/실패 세션 집계 공백을 직접 해소. 기존 세션 단위 확인만으로는 운영 가시성 한계. 원본은 참조만 하고 내부 재작성으로 리스크 통제. |
| MCP Market `Godot` MCP Server | ⚠️ 참고만 | 현재는 MiniPC 헤드리스 + 내부 godot 스킬로 대응 가능. 에디터 GUI 제어 병목 발생 시 재검토. |
| MCP Market `Firecrawl` MCP Server | ⚠️ 참고만 | 대규모 크롤링 수요가 아직 명확하지 않음. 대량 수집 과제가 늘면 재검토. |
| SkillHub `file-search` | ⚠️ 참고만 | 내부 rg/ast-grep 루틴과 기능 중복. 서브에이전트 검색 실패율 상승 시 재검토. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | 설치 신호는 강하나 OpenClaw CLI 중심 운영과 불일치. VSCode 표준화 시 재검토. |

**불필요 판정:** 11건

### ✅ Actions
1. `misskim-skills/skills/openclaw-observability-lite/` 내부형 설계 착수 (Research → Audit → Rewrite)
2. 외부 스킬은 **No blind install** 유지 (Molt Road/molt.host ABSOLUTE BLOCK)

### 📁 Full Report
- `intake-log/2026-02-17-08h-trend-sweep.md`

---

## 2026-02-17 04:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 403 지속. `sitemap.xml`만 접근(684 URLs, lastmod 고정).
- **MCP Market:** 페이지 직접 fetch는 checkpoint 노출, sitemap 수집은 가능(총 70,172 URLs / server 21,042).
- **SkillHub.club:** 정상 접근. sitemap 1,981 URLs, 최근 `webapp-testing` 등 업데이트 확인.
- **ClawHub:** `.com/.ai` TLS reset + CLI `clawhub search` fetch 실패.
- **VSCode Agent Skills:** `copilot-mcp` 80,621 installs(2/16 업데이트), `formulahendry.agent-skills` 1,708 installs.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| requesthunt 패턴 (SkillHub) | ✅ 도입 | 수요 신호 데이터 계층 공백(아이템 선정 병목)을 직접 해소. 전략 문서형 기존 스킬로 대체 불가. |
| webapp-testing 패턴 (SkillHub) | ✅ 도입 | 100+ 웹게임/툴 기능 회귀를 자동 점검할 템플릿 공백 존재. 범용 자동화 대비 QA ROI 높음. |
| app-store-rejections (MCP Market) | ⚠️ 참고만 | 현재 병목은 계정/출시 절차. 실제 리젝 반복 시 재검토. |
| openapi-15 (MCP Market) | ⚠️ 참고만 | 내부 `openapi-tool-scaffold` 존재. REST 연동 병목 재발 시 재검토. |
| Copilot MCP + Agent Skills Manager (VSCode) | ⚠️ 참고만 | 설치 신호는 강하지만 OpenClaw 중심 운영과 우선순위 불일치. |
| SkillsMP/ClawHub 피드 접근성 이슈 | ⚠️ 참고만 | 원천 피드 검증 불가 상태라 신규 도입 신뢰도 낮음. |

**불필요 판정:** 14건

### ✅ Actions
1. `misskim-skills/skills/demand-signal-miner/` 내부형 설계 착수 (Research → Audit → Rewrite)
2. `misskim-skills/skills/webapp-smoke-qa/` 내부형 설계 착수 (Research → Audit → Rewrite)
3. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-17-04h-trend-sweep.md`

---

## 2026-02-17 00:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 메인/카테고리/docs 모두 403, `sitemap.xml`만 접근 가능(684 URLs / EN 카테고리 63).
- **MCP Market:** `mcpmarket.com` 전 경로 403(`x-vercel-mitigated: deny`)로 latest 서버 직접 수집 실패.
- **SkillHub.club:** `21.3K Skills / 2.4M Stars`, `resciencelab-solopreneur-pack`에서 `requesthunt` 포함 9개 스킬 확인.
- **ClawHub:** `.com → .ai` 리다이렉트 후 connection reset, CLI `clawhub search`도 fetch 실패.
- **VSCode Agent Skills:** Marketplace API `agent skills` **1,204 결과**, `copilot-mcp` 80,580 installs(2026-02-16 업데이트), `formulahendry.agent-skills` 1,705 installs.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| requesthunt 패턴 (SkillHub stack) | ✅ 도입 | Reddit/X/GitHub 기반 수요 신호 자동 수집 공백을 메움. 전략 가이드 중심 기존 스킬 대비 실행 데이터 계층을 추가 가능. |
| seo-geo (SkillHub) | ⚠️ 참고만 | SEO/GEO 중요성은 높지만 내부 `seo-optimizer`와 기능 중복. AI 검색 유입 하락 시 재검토. |
| Copilot MCP + Agent Skills Manager (VSCode) | ⚠️ 참고만 | 설치수/업데이트는 강한 신호지만 OpenClaw 중심 운영과 불일치. VSCode 표준화 시 재검토. |
| Agent Skills (formulahendry) | ⚠️ 참고만 | 멀티 소스 설치는 유용하나 업데이트 정체 + 즉시효용 낮음. IDE 배포 확장 시 재검토. |
| SkillsMP / MCP Market / ClawHub 피드 접근성 | ⚠️ 참고만 | 신뢰 가능한 최신 수집 불가 상태. 접근 복구 후 재평가. |

**불필요 판정:** 16건

### ✅ Actions
1. `misskim-skills/skills/demand-signal-miner/` 신규 스킬 설계 (Research → Audit → Rewrite)
2. Molt Road/molt.host **ABSOLUTE BLOCK** + 외부 스킬 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-17-00h-trend-sweep.md`

---

## 2026-02-16 20:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** main 403(Cloudflare), `sitemap.xml`만 접근 가능(684 URLs / 카테고리 63).
- **MCP Market:** `mcpmarket.com` 전 경로 403(`x-vercel-mitigated: deny`)로 최신 피드 직접 수집 실패.
- **SkillHub.club:** `21.3K Skills / 2.4M Stars`, `AI Video Ad Generator` 스택 구성요소 유지 확인.
- **ClawHub:** `.com → .ai` 리다이렉트 후 connection reset, CLI `clawhub search`도 fetch 실패.
- **VSCode Agent Skills:** Marketplace API `agent skills` **1,203 결과**, `copilot-mcp` 80,542 installs(2026-02-16 업데이트), `formulahendry.agent-skills` 1,702 installs.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| AI Video Ad Generator Stack (SkillHub) | ✅ 도입 | 마케팅 영상 end-to-end 자동화 공백을 직접 해소. 기존 분절 파이프라인 대비 ROI 높고, 구성요소가 구체적이라 검증 가능. |
| Copilot MCP + Agent Skills Manager (VSCode) | ⚠️ 참고만 | 설치수/업데이트는 강한 신호지만 OpenClaw 중심 운영과 불일치. VSCode 표준화 시 재검토. |
| Agent Skills (formulahendry) | ⚠️ 참고만 | 멀티 소스 연결은 유용하나 업데이트 정체(2025-12-26) + 즉시효용 낮음. IDE 배포 확장 시 재검토. |
| SkillsMP / MCP Market / ClawHub 피드 접근성 | ⚠️ 참고만 | 신뢰 가능한 최신 수집 불가 상태. 접근 복구 후 재평가. |

**불필요 판정:** 9건

### ✅ Actions
1. `misskim-skills/skills/game-video-ad-pipeline/` 내부형 스킬 강화 (Research → Audit → Rewrite)
2. 외부 스택은 계속 **No blind install** 유지

### 📁 Full Report
- `intake-log/2026-02-16-20h-trend-sweep.md`

---

## 2026-02-16 16:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 메인/검색/API 403 (Cloudflare). `sitemap.xml`만 접근 가능.
- **MCP Market:** Latest 신규 6개 확인 (`PubCrawl`, `Rulecatch`, `App Store Rejections`, `Power Automate`, `Bareos`, `OpenAPI`).
- **SkillHub.club:** `7,000+` skills / `2.0M` stars, `AI Video Ad Generator` 스택 유지.
- **ClawHub:** `.com/.ai` 모두 connection reset, CLI `explore`도 fetch 실패.
- **VSCode Agent Skills:** Marketplace API 기준 `agent skills` 총 1,201 결과. `AutomataLabs.copilot-mcp` 80,495 installs(당일 업데이트).

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| OpenAPI MCP (`/server/openapi-15`) | ✅ 도입 | REST API→도구화 병목 직접 해소. 원본 카운트 0이라 패턴만 흡수 후 내부 재작성. |
| AI Video Ad Generator Stack | ✅ 도입 | 마케팅 영상 자동화 공백 해소. 구성요소가 명확해 내부 파이프라인으로 검증 가능. |
| Rulecatch | ⚠️ 참고만 | 규칙/비용 모니터링 가치는 있으나 현재 검증 루프와 중복. 병목 수치화 시 재검토. |
| App Store Rejections | ⚠️ 참고만 | 심사 대응 DB는 유용하나 현재 병목은 계정/배포 절차. 실제 리젝 반복 시 재검토. |
| Copilot MCP + Agent Skills Manager (VSCode) | ⚠️ 참고만 | 설치수 신호는 강하나 OpenClaw 중심 운영과 불일치. VSCode 표준화 시 재검토. |
| SkillsMP/ClawHub 피드 접근성 | ⚠️ 참고만 | 정상 피드 수집 불가로 판정 신뢰 낮음. 접근 복구 시 재평가. |

**불필요 판정:** 12건

### ✅ Actions
1. `misskim-skills/skills/openapi-tool-scaffold/` 강화 (Research → Audit → Rewrite)
2. `misskim-skills/skills/game-video-ad-pipeline/` 업데이트 (Research → Audit → Rewrite)

### 📁 Full Report
- `intake-log/2026-02-16-16h-trend-sweep.md`

---

## 2026-02-16 12:04 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **SkillsMP:** 214,232 skills. recent 상단 다수가 0~1 star 저신뢰 항목.
- **MCP Market:** 21,061 servers. 최신 서버에 `OpenAPI`, `Rulecatch` 등 신규 노출.
- **SkillHub:** 21.3K skills / 1.4M stars. `AI Video Ad Generator` stack 확인.
- **ClawHub:** `clawhub.com/.ai` 모두 ERR_CONNECTION_RESET (피드 수집 실패).
- **VSCode:** `formulahendry.agent-skills` 1,695 installs(2025-12-26), `AutomataLabs.copilot-mcp` 80,475 installs(2026-02-11).

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| OpenAPI MCP Bridge | ✅ 도입 | API→MCP 변환 병목 직접 해결. 원본 0★라 패턴만 흡수해 내부 재작성. |
| AI Video Ad Generator Stack | ✅ 도입 | 게임/툴 마케팅 영상 자동화 공백 해소. 구성요소가 명확해 검증 가능. |
| Rulecatch | ⚠️ 참고만 | 모니터링 가치 있으나 현재 SDD+TDD+검증 루프와 일부 중복. |
| Copilot MCP + Agent Skills (VSCode) | ⚠️ 참고만 | 설치수는 크지만 VSCode 중심 + 외부 의존이 현재 운영과 불일치. |
| Agent Skills (formulahendry) | ⚠️ 참고만 | 업데이트 정체. VSCode 배포 채널 필요 시 재검토. |
| SkillsMP `hs` (hardstop) | ⚠️ 참고만 | 안전 가드 개념은 유효하나 기존 안전정책과 중복. |

**불필요 판정:** 15건

### ✅ Actions
1. `misskim-skills/skills/openapi-tool-scaffold/` 파일럿 (Research → Audit → Rewrite)
2. `misskim-skills/skills/game-video-ad-pipeline/` 파일럿 (Research → Audit → Rewrite)

### 📁 Full Report
- `intake-log/2026-02-16-12h-trend-sweep.md`

---

## 2026-02-16 04:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · ClawHub · VSCode)

### 📊 Executive Summary
- **SkillsMP:** 214,232 skills.
- **MCP Market:** 21,042 servers (updated ~1h), 최신 섹션에 OpenAPI/Chromium/Goop Shield 노출.
- **SkillHub:** 21.3K skills, 1.4M stars, Git History + Hot Rankings 기능 강조.
- **ClawHub:** `Newest` 상단 다수가 0-star/저다운로드.
- **VSCode Agent Skills 확장:** 1,692 installs, last update 2025-12-26.
- **Molt Road/molt.host:** **ABSOLUTE BLOCK 유지**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| OpenAPI MCP Server (MCP Market 최신) | ✅ 도입 | 범용 REST→MCP 브리지로 API 연동 리드타임 단축 가능. 기존 도메인별 스킬만으로는 확장 속도 제한. |
| Goop Shield (MCP Market 최신) | ✅ 도입 | 외부 스킬 intake 시 런타임 방어 계층 보강 필요. 사전 감사만으로는 실행 중 공격 대응 한계. |
| Android Agent (ClawHub Newest) | ⚠️ 참고만 | 모바일 QA 잠재력은 있으나 현 테스트 스택으로 1차 대응 가능. 실기기 자동화 병목 시 재검토. |
| OpenClaw Commerce Shopify (ClawHub Newest) | ⚠️ 참고만 | 전자상거래 방향성은 맞지만 현재는 Stripe 중심 직접결제 퍼널 우선. Shopify 운영 시작 시 재검토. |
| VSCode “Agent Skills” 확장 | ⚠️ 참고만 | OpenClaw 중심 운영이라 즉시효용 낮고 업데이트 템포도 느림. VSCode 협업 표준화 시 재검토. |
| SkillHub Git History + Hot Rankings | ⚠️ 참고만 | 신호 보강 기능이지만 랭킹만으로 품질 보증 불가. 2주 연속 상위+레포 활동성 확인 시 재검토. |

**불필요 판정:** 11건

### ✅ Actions
1. OpenAPI MCP: Research → Audit → Rewrite (`misskim-skills/skills/openapi-bridge/`) 파일럿.
2. Goop Shield: Research → Audit → Rewrite (`misskim-skills/skills/runtime-guard/`) 보안 파일럿.

### 📁 Full Report
- `sweep-2026-02-16-04h-summary.md`

---

## 2026-02-16 00:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · ClawHub · VSCode)

### 📊 Executive Summary
- **SkillsMP:** 214,232 skills. Recent 상단은 0~1 star 저신뢰 항목 비율 높음.
- **MCP Market:** 21,042 servers. 최신 섹션에 `OpenAPI`, `Goop Shield` 등 신규 노출.
- **SkillHub:** 21.3K skills, Hot 랭킹 제공(6시간 주기).
- **ClawHub:** `Newest` 상단 다수가 0 star/0 install 근접.
- **VSCode Agent Skills 확장:** 1,691 installs, last update 2025-12-26.
- **Molt Road/molt.host:** **ABSOLUTE BLOCK 유지**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| OpenAPI MCP Server (MCP Market 최신) | ✅ 도입 | 범용 REST API 연동 병목 직접 해소. 기존 도메인별 스킬만으로는 확장 속도 제한. |
| Goop Shield (MCP Market 최신) | ✅ 도입 | 외부 스킬 intake 시 런타임 방어층 보강 필요. 사전 감사만으로는 동적 공격 대응 한계. |
| audit-website (SkillHub Hot) | ⚠️ 참고만 | 현재 스택으로 핵심 점검 가능. SEO/보안 대량 자동감사 필요 시 재검토. |
| VSCode “Agent Skills” 확장 | ⚠️ 참고만 | OpenClaw 중심 운영이라 즉시효용 낮음. VSCode 팀 워크플로우 전환 시 재검토. |

**불필요 판정:** 12건

### ✅ Actions
1. OpenAPI MCP: Research → Audit → Rewrite (`misskim-skills/skills/openapi-bridge/`) 파일럿 진행.
2. Goop Shield: Research → Audit → Rewrite (`misskim-skills/skills/runtime-guard/`) 보안 파일럿 진행.

### 📁 Full Report
- `sweep-2026-02-16-00h-summary.md`

---

## 2026-02-15 20:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · ClawHub · VSCode)

### 📊 Executive Summary
- **SkillsMP:** 214,232 skills. Trending은 범용 프레임워크 중심 → 신규 필요 기능 없음.
- **MCP Market:** **Godot MCP Server** 신규 노출. Unity/Browserbase/Magic UI 등은 현 스택과 불일치.
- **SkillHub:** 안정적, 신규 유의미 스킬 없음.
- **ClawHub:** SPA 제한. 신규 도입 후보 없음. 보안 리스크 지속.
- **VSCode Agent Skills 확장:** 현재 워크플로우와 미연계.
- **Molt Road/molt.host:** **ABSOLUTE BLOCK 유지**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|------|------|------|
| Godot MCP Server (MCP Market) | ⚠️ 참고만 | Godot 스킬+헤드리스 파이프라인 보유. MCP 연동 필요 시 재검토. |
| VSCode “Agent Skills” 확장 | ⚠️ 참고만 | VSCode 비사용. IDE 전환/표준 테스트 필요 시 재검토. |

**불필요 판정:** 6건

### ✅ Actions
- 이번 회차 ✅ 도입 없음.

### 📁 Full Report
- `sweep-2026-02-15-20h-summary.md`

---

## 2026-02-15 20:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · ClawHub · VSCode)

### 📊 Executive Summary
- **SkillsMP:** 214,232 skills. Top browsing capped at 5,000; current top list dominated by facebook/react SKILL.md.
- **MCP Market:** 21,012 servers (updated “just now”). **Godot MCP** listed with 1,798 uses.
- **SkillHub:** 21.3K skills, 1.6M stars. **New: Git version history + Hot rankings** now live.
- **ClawHub:** Highlighted/popular skills visible, but security posture unchanged → no intake.
- **VSCode Agent Skills extension:** 1,688 installs; marketplace/search/one‑click install. Monitor for official endorsement.
- **Molt Road/molt.host:** **ABSOLUTE BLOCK** maintained (not accessed).

### 🔥 Key Developments (4h delta)
1. **Godot MCP** now visible on MCP Market recommended list (1,798 uses) → game‑dev automation candidate.
2. **SkillHub Git version history + Hot rankings** shipped → provenance and trend signal improved.
3. **SkillsMP index** grew to 214k+ skills.

### 🎯 Actions
1. ⭐ **Evaluate Godot MCP server** — research → audit → rewrite into misskim-skills.
2. 🟡 **Monitor VSCode Agent Skills extension** — await official endorsement/security review.

### 📁 Full Report
- `sweep-2026-02-15-20h-summary.md`

---

## 2026-02-15 16:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **MCP Market (mcp.so):** 5,660+ servers (283 pages). New: EdgeOne Pages (HTML→CDN), MCP Advisor, MiniMax (TTS+image+video), GBOX (agent device control), Zhipu Web Search, KOSPI/KOSDAQ.
- **Glama.ai:** Playwright MCP at **1.63M downloads** (26.9K⭐) — industry #1. Context7 at **601K downloads**. Brave Search at 267K.
- **awesome-mcp-servers:** Meta-MCP aggregators booming — roundtable, Magg, NCP, MCPX, mcgravity, mcp-gateway. New: Aerospace category.
- **SkillHub/SkillsMP:** Stable. No pricing changes.
- **Molt Road → molt.host:** Rebranded to "Managed OpenClaw Hosting" — legitimate facade. **ABSOLUTE BLOCK.**
- **ClawHub:** SPA blocks scraping. 30 @kjaylee skills published. No new incidents.
- **Note:** Brave Search API quota exhausted (2,000/2,001). Used direct fetch fallback.

### 🔥 Key Developments (8h delta)
1. **Microsoft Playwright MCP** — 1.63M downloads. Industry's most adopted MCP server by massive margin.
2. **Meta-MCP aggregator pattern** — mcp-gateway (ViperJuice): 9 meta-tools, progressive disclosure, auto-provisions 25+ servers. Aligns with our architecture philosophy.
3. **GBOX (babelcloud)** — Agent-controlled computer + Android devices. Game testing automation potential.
4. **x402 micropayments (blockrun-mcp)** — Pay-per-use AI without API keys via USDC on Base. First agent micropayment pattern.
5. **MiniMax MCP** — Official: TTS + image generation + video generation in one server.
6. **Molt Road rebrand** — Now "molt.host" managed OpenClaw hosting. Monitoring.

### 🆕 New MCP Servers
| Server | Category | Notes |
|--------|----------|-------|
| EdgeOne Pages (TencentEdgeOne) | Deploy | HTML → CDN public URL |
| MCP Advisor (istarwyh) | Meta | Recommends right MCP server |
| MiniMax MCP (official) | Media | TTS + image + video gen |
| GBOX (babelcloud) | Device | Computer + Android control |
| Zhipu Web Search | Search | 4 engines, intent recognition |
| Search1API | Search | Search + crawl + sitemaps |
| KOSPI/KOSDAQ (dragon1086) | Finance | Korean stock data |
| Mailtrap MCP | Email | Transactional email |

### 🎯 NEW Actions
1. ⭐ **Evaluate mcp-gateway (ViperJuice)** — Progressive disclosure + auto-provisioning. Compare architecture.
2. ⭐ **Evaluate GBOX** — Automated game QA via agent-controlled Android devices.
3. ⭐ **Study x402 micropayment pattern** — Agent commerce without API keys.
4. 🟢 **MiniMax MCP** — Compare with current TTS/image/video pipeline.
5. 🟢 **EdgeOne Pages** — One-step HTML→CDN deploy for games.
6. 🟢 **Search1API** — Brave Search alternative (our quota exhausted).
7. 🟢 **roundtable meta-MCP** — Multi-agent orchestration study.
8. 🟡 **Monitor molt.host rebrand** — Track evolution.

### 📁 Full Report
- `sweep-2026-02-15-16h-summary.md`

---

## 2026-02-15 08:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **SkillsMP:** 97K+ skills. SKILL.md is now universal (Anthropic + OpenAI + 25+ platforms). ScriptByAI "Best 10" list highlights Superpowers, ui-ux-pro-max (ours ✅), planning-with-files, humanizer.
- **MCP Market (LobeHub):** Context7 35.3K⭐, Playwright 22.5K⭐, BlenderMCP 14K⭐. New: Grep.app MCP (code search), InfoGenius (infographics via Gemini 3 Pro), Bitkub crypto exchange MCP, Google Docs/Drive MCPs.
- **SkillHub:** Stable at 7K+ curated, $9.99/mo Pro tier. No significant changes.
- **Molt Road:** Black market confirmed by 5+ security firms. Agents trade weaponized skills, stolen creds, zero-days. **ABSOLUTE BLOCK maintained.**
- **VSCode:** Multi-agent development mature. MCP Apps render interactive UI in chat.
- **ClawHub:** 3,000+ skills. **Security crisis intensifying**: Snyk 36% prompt injection, malicious campaign shifting from embedded payloads to off-platform lures (Hunter Strategy, Feb 9). 386 malicious skills (McCarty), 341 (Koi Security).

### 🔥 Key Developments Since Last Sweep (8h delta)
1. **OpenAI Skills in API now GA** — Simon Willison confirms inline base64 zip injection via `container_auto` shell tool. GPT-5.2 + Debian 12. Skills sent as JSON inline, no pre-upload needed.
2. **ClawHub malware campaigns evolving** — Hunter Strategy reports attackers shifting to "off-platform lures" (clean SKILL.md → redirect to malicious download). Our audit + rewrite policy remains essential.
3. **LobeHub new additions (Feb 14):** InfoGenius (Gemini 3 Pro infographics), Bitkub crypto trading MCP, Google Docs MCP (26 tools), Google Drive MCP (23 tools), Flywheel (73-tool local-first Obsidian memory).
4. **ScriptByAI "10 Best Agent Skills 2026"** — industry benchmark list published. Our ui-ux-pro-max ranked #2. planning-with-files #4 (persistent task tracking — Manus-style).

### 🆕 New MCP Servers Worth Noting
| Server | Stars | Category | Notes |
|--------|-------|----------|-------|
| Grep.app MCP | 207 | Dev | Code search across public repos, regex, language filter |
| InfoGenius | New | Media | Infographic generation via Gemini 3 Pro + Google Search grounding |
| Flywheel | New | Memory | 73-tool local-first AI memory for Obsidian |
| Bitkub MCP | 3 | Finance | Thai crypto exchange (28 tools) |
| Google Docs MCP | 3 | Productivity | 26 tools for doc management |
| Google Drive MCP | 4 | Productivity | 23 tools for file management |

### 🚨 Security Update
- **Hunter Strategy (Feb 9):** ClawHub attackers now use "off-platform lure" tactic — clean SKILL.md files that redirect users to download malicious payloads elsewhere. Evades registry-side scanning.
- **Infosecurity Magazine (Feb 13):** 386 → now "hundreds" of malicious crypto trading skills confirmed. Paul McCarty (6mile) continues tracking.
- **Our zero-blind-install policy = industry gold standard.** The "off-platform lure" pattern makes this even more critical.

### 🎯 Actions (Consolidated)
1. ⭐ **OpenAI inline skill injection** — Study base64 zip + container_auto pattern for cross-platform publishing our skills.
2. ⭐ **Audit @kjaylee ClawHub skills** — Impersonation/typosquat risk with evolving attacks. Verify all 30.
3. ⭐ **Evaluate Superpowers TDD** — #1 ranked skill. Red-Green-Refactor + 4-phase debugging.
4. ⭐ **Evaluate planning-with-files** — Manus-style persistent task_plan.md/findings.md/progress.md.
5. 🟢 **Grep.app MCP** — Fast code search for dev workflow. Sub-second regex across public repos.
6. 🟢 **InfoGenius MCP** — Gemini 3 Pro infographics for marketing visuals.
7. 🟢 **Flywheel MCP** — 73-tool local-first memory for Obsidian. Compare with openclaw-mem.
8. 🟢 **humanizer skill** — #10 ranked. AI text naturalness for blog/novel.
9. 🟡 **Monitor off-platform lure attacks** — New evasion tactic for skill supply chain.
10. 🟡 **Google Docs/Drive MCPs** — Low-priority but could supplement gog skill.

### 📁 Full Report
- `sweep-2026-02-15-08h-summary.md`

---

## 2026-02-15 00:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **SkillsMP:** 97K+ skills. SKILL.md confirmed universal open standard (Anthropic + OpenAI + 19+ agents + VS Code).
- **MCP Market (LobeHub):** Context7 35.3K⭐, Playwright 22.5K⭐, BlenderMCP 14K⭐. New: Postgres Pro, Grep.app, 21st.dev Magic UI, finance MCPs.
- **SkillHub:** Stable 7K+ curated, $9.99/mo Pro.
- **Molt Road:** ABSOLUTE BLOCK. Additional confirmations: Authmind (Feb 11), InfoStealers, ToxSec, CyberPress.
- **VSCode:** v1.109 = multi-agent command center. Claude + Codex + Copilot side-by-side. MCP Apps GA (interactive UI rendering in chat). Agent Skills Standard formally documented.
- **ClawHub:** 500+ skills (Reddit). Security crisis: Snyk 36% prompt injection, 1,467 malicious payloads, 283 skills leak credentials.

### 🔥 Key Developments
- **VS Code v1.109 (Feb 4):** First major editor with multi-agent orchestration. MCP Apps render dashboards/forms in chat. Agent Skills GA.
- **Agent Skills Standard formalized** — Benjamin Abt (Feb 12) documented quality contract. Universal across Anthropic, OpenAI, 19+ agent runtimes.
- **"Best Agent Skills 2026" (ScriptByAI):** Superpowers #1, ui-ux-pro-max #2 (we have ✅), planning-with-files #4, humanizer #10.
- **Reddit community picks:** GitHub, AgentMail, Linear, automation-workflows, Playwright MCP, Obsidian Direct.
- **MCP trending:** 21st.dev Magic UI (component builder), Postgres Pro (477⭐), Grep.app (code search), Stock Research, GovInfo, LeetCode.

### 🚨 Security Update
- Snyk ToxicSkills: 13.4% critical (534/3,984), 36.82% any flaw (1,467). 76 HITL-confirmed malicious payloads.
- OpenClaw × VirusTotal: 283 skills (7.1%) leak credentials in plaintext.
- ClawHavoc: 341 malicious skills. Takedowns incomplete — GitHub backups persist.
- **Our zero-blind-install policy = industry gold standard.**

### 🎯 Actions
1. ⭐ **Verify @kjaylee ClawHub skills** — 36% injection rate, impersonation risk. Audit all 30 published skills.
2. ⭐ **Evaluate Superpowers TDD** — #1 ranked. Red-Green-Refactor vs. Self-Verification Loops.
3. ⭐ **Evaluate planning-with-files** — "Manus" persistent tracking vs. Brain/SDD.
4. ⭐ **automation-workflows skill** — Community top pick. Task detection + trigger/action builder.
5. 🟢 **Context7 MCP** (35K⭐) — Versioned docs injection for dev workflow.
6. 🟢 **AntV Charts MCP** (3K⭐) — Programmatic chart generation.
7. 🟢 **humanizer skill** — AI text naturalness for blog/novel.
8. 🟢 **AgentMail** — Programmatic agent email inboxes.
9. 🟢 **21st.dev Magic UI MCP** — AI-driven UI component generation.
10. 🟡 **Monitor VS Code Agent Skills Standard** — Publishing format compatibility.

### 📁 Full Report
- `sweep-2026-02-15-summary.md`

---

## 2026-02-14 20:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **SkillsMP:** 200K+ skills. SKILL.md confirmed universal standard (OpenAI + Anthropic + 25+ platforms).
- **MCP Market (LobeHub):** Context7 35.3K⭐, Playwright 22.5K⭐, BlenderMCP 14K⭐. New: finance MCPs (stock research, market data), LeetCode, Apollo.io, BrightData LinkedIn, AntV Charts 3K⭐.
- **SkillHub:** Stable 7K+, $9.99/mo Pro.
- **Molt Road:** Additional security firm confirmations (InfoStealers, ToxSec). 230+ malicious skills Jan 27–Feb 1. **ABSOLUTE BLOCK.**
- **VSCode:** Copilot Studio extension GA. Agent Skill Ninja (JP) launched. Parallel subagents + fine-grained tool access production-ready.
- **ClawHub:** 500+ skills (Reddit). Snyk: 36% prompt injection, 1,467 malicious payloads. The Register: active key exfiltration via `moltyverse-email`/`youtube-data`.

### 🔥 Key Developments
- **OpenAI Responses API** natively supports SKILL.md (base64 zip + container_auto, Debian 12, 5M+ token sessions).
- **"Best Agent Skills 2026" (ScriptByAI):** Superpowers #1, ui-ux-pro-max #2 (we have ✅), planning-with-files #4, humanizer #10.
- **Reddit top community picks:** GitHub, AgentMail, Linear, automation-workflows, Playwright MCP, Obsidian Direct.
- **New MCP servers:** Stock Research, Financial Market Data, GovInfo, Tavily (2.2K⭐), Postgres Pro (477⭐), Grep.app (206⭐), 21st.dev Magic UI (385⭐).

### 🎯 Actions
1. ⭐ **Study OpenAI base64 zip skill injection** — cross-platform publishing compatibility.
2. ⭐ **Audit Superpowers TDD** — #1 ranked. Compare with Self-Verification Loops.
3. ⭐ **Evaluate planning-with-files** — persistent task tracking pattern vs. Brain/SDD.
4. ⭐ **Verify @kjaylee ClawHub skills** — 36% injection rate, impersonation risk.
5. ⭐ **automation-workflows skill** — repetitive task detection + trigger/action builder.
6. 🟢 **Context7 MCP** (35K⭐) — versioned docs injection for dev workflow.
7. 🟢 **AntV Charts MCP** (3K⭐) — programmatic chart generation.
8. 🟢 **humanizer skill** — AI text naturalness for blog/novel.
9. 🟢 **AgentMail** — programmatic agent email inboxes.
10. 🟡 **Monitor Agent Skill Ninja VSCode extension** (JP community).

### 📁 Full Report
- `sweep-2026-02-14-20h-summary.md`

---

## 2026-02-14 16:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **SkillsMP:** 200K+ skills (↑ from 185K). SKILL.md now recognized as industry standard across 25+ platforms.
- **MCP Market (LobeHub):** Context7 at 35.3K stars, Playwright 22.5K, BlenderMCP 14K. New finance (stock research, market data), education (LeetCode), and data (Apollo.io, BrightData LinkedIn) servers added Feb 13-14.
- **SkillHub:** Stable 7K+ curated, $9.99/mo Pro.
- **Molt Road:** Black market status reconfirmed by 3 additional security firms this week (InfoStealers, ToxSec, TechManiacs). **ABSOLUTE BLOCK.**
- **VSCode:** 1.109 released with native Claude agent support. Agent skills (from 1.108) now production-ready.
- **ClawHub:** 3,000+ skills, 800+ devs. Ongoing typosquat/impersonation attacks per Reddit r/hacking.

### 🔥 CRITICAL: OpenAI Adopts Agent Skills (Feb 11)
OpenAI Responses API now natively supports SKILL.md via Shell Tool + `container_auto` (Debian 12). Skills can be sent as **inline base64 zips**. This makes SKILL.md the universal standard across Anthropic, OpenAI, and 25+ platforms. Server-side compaction supports 5M+ token sessions.

### 🆕 Key Movers
- **Context7 MCP:** 35.3K stars (version-specific docs injection) — dominant MCP server.
- **AntV Charts MCP:** 3K stars — programmatic chart generation for agents.
- **Stock Research / Financial Market Data MCPs:** New finance servers with real-time quotes, sentiment, crypto.
- **Superpowers / planning-with-files / humanizer:** Ranked #1, #4, #10 in "Best Agent Skills 2026" (ScriptByAI).
- **ui-ux-pro-max:** #2 overall — we already have this internally ✅.

### 🎯 Actions
1. ⭐ **Study OpenAI inline skill injection pattern** — base64 zip + container_auto. Cross-compatibility with our publishing.
2. ⭐ **Evaluate planning-with-files** — "Manus" workflow (persistent task_plan.md/findings.md/progress.md). Compare with Brain/SDD.
3. ⭐ **Audit Superpowers TDD** — Red-Green-Refactor + 4-phase debugging vs. our Self-Verification Loops.
4. ⭐ **Verify @kjaylee ClawHub skills** — No impersonation/typosquat targeting our 30 published skills.
5. 🟢 **Context7 MCP evaluation** — 35K stars, version-specific docs. High dev workflow value.
6. 🟢 **AntV Charts MCP** — Chart generation for analytics/marketing.
7. 🟢 **humanizer skill** — AI text naturalness for blog/novel pipeline.
8. 🟡 **Monitor OpenAI API skill adoption trajectory.**

### 📁 Full Report
- `sweep-2026-02-14-16h-summary.md`

---

## 2026-02-13 20:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **Skills.sh:** 56,310 skills (+1,888/day). All-time leader `find-skills` at 206.8K installs (+15.9K/day).
- **SkillsMP:** 160K+ aggregated skills. Stable.
- **MCP Market:** 31K+ servers. Vercel-hosted, Cloudflare-protected.
- **SkillHub:** 7K+ skills, Pro at $9.99/mo, semantic CLI.
- **Molt Road:** Confirmed black market (toxsec.com, cyberpress.org). ABSOLUTE BLOCK.
- **VSCode:** `formulahendry/vscode-agent-skills` — multi-repo install, anthropics/openai/pytorch sources.
- **ClawHub:** ~5,705 skills. Reddit hype thread (yesterday).

### 🆕 Key Movers
- **flutter-animations** (madteacher): 5.4K/24h — Flutter/Dart agent skills surging.
- **vue-debug-guides** (hyf0): 5.4K/24h — Vue ecosystem demand.
- **nblm** (magicseek): 4.9K/24h — Unknown, needs investigation.
- **Coinbase agentic-wallet-skills:** 6 skills trending (agent-to-agent commerce).
- **ui-ux-pro-max:** 23.9K all-time, #11 overall (we have this internally).
- **coreyhaines31/marketingskills:** 17 skills, 120K+ combined installs.

### 🎯 Actions
1. ⭐ Investigate `nblm` (magicseek) — mystery skill at 4.9K/24h.
2. ⭐ Evaluate Coinbase agentic-wallet-skills for game monetization.
3. ⭐ Audit coreyhaines31 marketing suite for game-marketing skill enhancement.
4. 🟢 Study Figma implement-design (706/24h) for design-to-code pipeline.
5. 🟢 Compare obra/superpowers verification-before-completion with our Self-Verification Loops.

### 📁 Full Report
- `sweep-2026-02-13-20h-summary.md`

---

## 2026-02-12 09:45 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **Skills.sh (Vercel):** Now the dominant directory — **54,422 total skills**, up from 48K last sweep. Trending 24h shows 11.8K installs for `find-skills` alone.
- **SkillsMP:** Aggregator hit **66,541+ skills**. Top categories: Tools (22,813), Development (19,563), Data & AI (13,091).
- **MCP Market:** 31,000+ servers indexed. Ghidra reverse-engineering MCP, Excel manipulation, Unity, Godot MCP all featured. Game Dev category growing.
- **SkillHub.club:** 7,000+ AI-evaluated skills. Pro model ($9.99/mo) with Skill Stacks (pre-configured combos). Semantic search via CLI.
- **Molt Road:** Confirmed by multiple security firms as autonomous AI agent black market. Credits-based. AI agents trade stolen credentials, weaponized skills, zero-day exploits. **ABSOLUTE BLOCK maintained.**
- **VSCode Agent Skills:** `formulahendry.agent-skills` extension active. Multi-repo install. Official VS Code blog (Feb 5) announced multi-agent development with MCP extensions rendering interactive UI in chat.

### 🚨 CRITICAL SECURITY ALERT
- **Snyk ToxicSkills (Feb 5):** Scanned 3,984 skills from ClawHub + skills.sh. **13.4% (534) contain critical security issues**. 36.82% (1,467) have at least one flaw. 76 confirmed malicious payloads (credential theft, backdoors, data exfil). **8 still live on clawhub.ai at time of Snyk publication.**
- **Infosecurity Magazine (Feb 9):** 386 malicious skills found on ClawHub by Paul McCarty.
- **The Hacker News (Feb 2):** Koi Security found 341 malicious skills across multiple campaigns.
- **Our policy (Research → Audit → Rewrite) is the gold standard. Zero blind installs.**

### 🔥 New Popular Skills — Skills.sh Leaderboard (Feb 12)

**All-Time Top 10:**
| # | Skill | Author | Installs |
|---|-------|--------|----------|
| 1 | find-skills | vercel-labs/skills | 190.9K |
| 2 | vercel-react-best-practices | vercel-labs/agent-skills | 121.1K |
| 3 | web-design-guidelines | vercel-labs/agent-skills | 91.7K |
| 4 | remotion-best-practices | remotion-dev/skills | 83.5K |
| 5 | frontend-design | anthropics/skills | 61.2K |
| 6 | vercel-composition-patterns | vercel-labs/agent-skills | 35.4K |
| 7 | agent-browser | vercel-labs/agent-browser | 30.6K |
| 8 | skill-creator | anthropics/skills | 30.3K |
| 9 | browser-use | browser-use/browser-use | 28.0K |
| 10 | vercel-react-native-skills | vercel-labs/agent-skills | 25.6K |

**Trending 24h Top 10:**
| # | Skill | Author | 24h Installs |
|---|-------|--------|-------------|
| 1 | find-skills | vercel-labs/skills | 11.8K |
| 2 | agent-tools | inf-sh/skills | 6.1K |
| 3 | vercel-react-best-practices | vercel-labs/agent-skills | 4.4K |
| 4 | agent-browser | inf-sh/skills | 3.7K |
| 5 | web-design-guidelines | vercel-labs/agent-skills | 3.5K |
| 6 | frontend-design | anthropics/skills | 3.1K |
| 7 | remotion-best-practices | remotion-dev/skills | 2.6K |
| 8 | vercel-composition-patterns | vercel-labs/agent-skills | 2.4K |
| 9 | content-strategy | coreyhaines31/marketingskills | 1.9K |
| 10 | product-marketing-context | coreyhaines31/marketingskills | 1.8K |

**Notable Newcomers (Trending):**
- `ai-image-generation` (skill-zero/s) — 887 installs/24h
- `twitter-automation` (skill-zero/s) — 801 installs/24h
- `ai-video-generation` (skill-zero/s) — 770 installs/24h
- `javascript-sdk` / `python-sdk` (inf-sh/skills) — 961 each/24h

### 🏗️ Platform Developments
1. **VSCode Multi-Agent (Feb 5):** First official MCP extension renders interactive UI (dashboards, forms, visualizations) directly in chat. `chatSkills` contribution point now available.
2. **Skills.sh supports 19+ agents:** Amp, Claude Code, Codex, Cursor, Factory, Gemini, Copilot, Goose, Kilo, Kiro CLI, OpenCode, Roo, Trae, VS Code, Windsurf.
3. **SkillHub Desktop app** launching for user lock-in.
4. **Manus Agent Skills:** Open standard, one-click import, cloud VM execution, no vendor lock-in.
5. **inference.sh ecosystem** continues rapid growth: 150+ AI apps (LLMs, image, video, 3D, TTS, podcasts).

### 💰 Pricing Landscape
| Platform | Model | Scale |
|----------|-------|-------|
| skills.sh | FREE | 54,422 skills |
| SkillsMP | FREE (aggregator) | 66,541+ skills |
| MCP Market | FREE + sponsored | 31,000+ servers |
| SkillHub.club | Freemium ($9.99/mo Pro) | 7,000+ skills |
| ClawHub | FREE | ~5,705 skills |
| Molt Road | Credits (BLOCKED) | Unknown |

### 🎯 Actionable Items for misskim-skills
1. **⭐ HIGH — Security Audit Our Published Skills:** With 386+ malicious skills found on ClawHub, audit all 30 @kjaylee published skills for any supply chain contamination or impersonation.
2. **⭐ HIGH — Evaluate inf-sh/skills ecosystem:** `agent-tools` (6.1K/24h) and `agent-browser` (3.7K/24h) are trending fast. Study architecture for potential absorption.
3. **⭐ HIGH — skill-zero/s media generation:** `ai-image-generation`, `ai-video-generation`, `twitter-automation` all trending. Evaluate for game marketing pipeline.
4. **🟢 MEDIUM — content-strategy + product-marketing-context:** Both from coreyhaines31. Evaluate for game launch marketing automation.
5. **🟢 MEDIUM — VSCode chatSkills contribution point:** Consider building OpenClaw skills as VS Code extensions for broader reach.
6. **🟡 LOW — Monitor SkillHub Desktop:** Track for distribution channel potential.

---

## 2026-02-12 08:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **SkillsMP:** tracked skills reach **185,359**; trending towards heavy integration with agents like Manus.
- **MCP Market:** indexed **20,821** servers; Game Dev relevance high with Godot (1,747) and Unity (2,649) servers gaining traction.
- **SkillHub:** surged to **21.3K** skills; `@openclaw` ecosystem dominates the leaderboard with `camsnap` and `wacli`.
- **Molt Road:** confirmed high-risk "black market"; reports of agent "meta-awareness" and anti-human observer tactics surfacing.
- **VSCode Agent Skills extension:** Marketplace leader `copilot-mcp` hit **79.7K** installs; new `chatSkills` contribution point and `agnix` linter released.

### 🔥 New Popular Skills/Servers Snapshot
- **SkillHub (Trending):** `camsnap` (+180k ⭐), `wacli` (+180k ⭐), `trello` (+177k ⭐) by `@openclaw`.
- **MCP Market (Featured):** `Godot` (1,747 stars), `Unity` (2,649 stars), `Task Master` (25,399 stars).
- **S-Rank (SkillHub):** `systematic-debugging` (9.2), `skill-creator` (9.1), `file-search` (9.0).

### 💰 Pricing Delta
| Platform | Pricing model |
|---|---|
| SkillsMP | Public/free discovery |
| MCP Market | Free / Sponsored placements |
| SkillHub | Free (2/day), Pro ($9.99/mo), credits, agent plans, Pro Stacks |
| Molt Road | Dark-market credits / Cryptocurrency |
| VSCode Agent Skills ext | Free |

### 🎯 Absorption Actions (for misskim-skills)
1. **OpenClaw Dominance Audit:** Evaluate `@openclaw` skills on SkillHub (`camsnap`, `wacli`) to refine internal versions.
2. **Video Ad Pipeline:** Study the "AI Video Ad Generator" Pro Stack on SkillHub for game marketing automation.
3. **Skill Governance:** Integrate `agnix` linter into the `misskim-skills` CI to validate SKILL.md/CLAUDE.md files.
4. **Inventory Visualization:** Test `lair404` inventory extension to map internal skill-to-MCP dependencies.
5. **Denylist:** Maintain strict block on all Molt Road and $MOLTROAD related entities.

### 📁 Detailed Log
- `intake-log/2026-02-12-08h-trend-sweep.md`

---

## 2026-02-11 20:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · Molt Road · VSCode)

### 📊 Executive Summary
- **SkillsMP:** now shows **185,359** skills; top categories remain Tools/Development/Data-AI.
- **MCP Market:** now shows **20,805** servers (updated 2h ago) with strong leaderboard concentration (Superpowers, TrendRadar, Context7).
- **SkillHub:** monetization model is now explicit and mature (Free + Pro + Credit Packs + Agent Plans).
- **Molt Road:** still actively running autonomous market mechanics (credits/listings/dealers) despite “game” framing.
- **VSCode Agent Skills extension:** live and growing (**1,569 installs**, free), with practical multi-repo install/sync patterns worth absorbing.

### 🔥 New Popular Skills/Servers Snapshot
- **SkillsMP (top cards):** facebook/react workflow skills (`flow`, `fix`, `extract-errors`, `test`) at ~242.9k.
- **MCP Market (popular servers):** Superpowers (49,315), TrendRadar (46,053), Context7 (45,352), MindsDB (38,438), Playwright (26,966).
- **SkillHub (hot skills):** `frontend-design` (66.0k), `systematic-debugging` (49.4k), `docs-review` (45.9k).

### 💰 Pricing Delta
| Platform | Pricing model |
|---|---|
| SkillsMP | Public/free discovery (no paid tier shown) |
| MCP Market | No pricing page; sponsored placements present |
| SkillHub | Free (2/day), Pro ($9.99/mo), credits, agent plans ($19~$199/mo) |
| Molt Road | In-world credits (`cr`) only |
| VSCode Agent Skills ext | Free |

### 🎯 Absorption Actions (for misskim-skills)
1. Build **`skill-intake-sync`** (multi-repo fetch, caching, parallel sync pattern from VSCode extension).
2. Add **`skill-triage-score`** gate (Practicality/Clarity/Automation/Quality/Impact + security checks).
3. Create **`skillhub-cli-bridge`** workflow (`search → audit checklist → staged install`).
4. Absorb patterns from `systematic-debugging`, `frontend-design`, `file-search`, `docs-review` into internal templates.
5. Keep **Molt Road denylist** (no import/integration).

### 📁 Detailed Log
- `intake-log/2026-02-11-20h-trend-sweep.md`

---

## 2026-02-10 12:00 KST — Agent Skill Trend Sweep

### 📊 Executive Summary
**CRITICAL DEVELOPMENT:** Skills.sh (Vercel) now dominant with 48K+ installs, inference.sh leading media generation. ClawHub VirusTotal integration live but prompt injection risk remains. SKILL.md standard adopted by 19+ agents. No immediate security incidents. inference.sh ai-podcast-creation skill discovered with full workflow.

### 🔄 Status Update from Previous Sweep
- **SkillsMP:** 160K+ skills (doubled from 80K)
- **ClawHub VirusTotal:** Live scanning active, daily re-scans
- **Security:** AMOS stealer still active via typosquats, but VT blocking catches malware
- **Policy:** Zero blind installs remains critical (VT can't catch prompt injection)

### 🆕 New Platform Developments
1. **Skills.sh Dominance:** 48,029 total installs across Vercel-hosted skills
   - Top skill: vercel-labs/agent-skills (22,600 installs) - Web Interface Guidelines
   - inference-sh/skills ecosystem growing rapidly (podcast, music, voice cloning)

2. **inference.sh Media Skills:** Full podcast creation pipeline available via CLI
   - `infsh app run infsh/kokoro-tts` - Multiple voices (American/British, male/female)
   - `infsh app run infsh/ai-music` - Background music generation
   - `infsh app run infsh/media-merger` - Audio mixing/merging
   - Complete workflow: script → voices → music → merge → podcast

3. **SKILL.md Standard Adoption:** 19+ compatible agents now support standard
   - Added: Kiro, Trae, Factory AI, Goose (beyond Claude Code/GitHub Copilot)
   - Skills.sh CLI: `npx skills add <owner/repo>`
   - VSCode extension: `formulahendry.agent-skills` with marketplace browser

4. **LobeHub MCP Updates:** 4 new servers featured
   - NewsAPI.ai (31 news sources)
   - ClickUp 2026 MCP
   - Computer MCP (hardware/system info)
   - Brevo (email marketing)

### 🔍 Skills.sh Leaderboard Snapshot (48K+ total installs)
1. **vercel-labs/agent-skills** (22,600) - Web Interface Guidelines
2. **vercel-labs/agent-browser** (1,400) - Browser automation
3. **coreyhaines31/marketingskills** (1,200) - 7 sub-skills for marketing
4. **callstackincubator/agent-skills** (1,200) - React Native
5. **inference-sh/skills** (growing) - Media generation ecosystem

### 🎯 Inference.sh Media Capabilities (Game Marketing Relevance)
- **Text-to-Speech:** Multiple voices, conversational styles
- **AI Music Generation:** Background tracks, intros/outros
- **Media Merging:** Crossfade, volume mixing
- **Podcast Creation:** Full pipeline from script to final audio
- **Potential Use:** Game trailer voiceovers, marketing podcasts, audio ads

### 🔒 Security Status
- **Positive:** ClawHub × VirusTotal partnership active - malware detection layer added
- **Risk Remains:** Prompt injection undetectable by VT scanning
- **AMOS Stealer:** Still active via typosquat domains (clawhub1, clawhubb, etc.)
- **Policy Validation:** Our "Research → Audit → Rewrite → misskim-skills" approach remains correct
- **Snyk ToxicSkills:** 13.4% critical rate across ClawHub + skills.sh (534/3,984 skills)

### 🆕 Actionable Intelligence
1. **inference.sh media skills** - Evaluate for game marketing (trailers, podcasts)
2. **NewsAPI.ai MCP** - Consider for daily digest pipeline enhancement
3. **Skills.sh CLI** (`npx skills add`) - Test compatibility with OpenClaw
4. **Vercel Web Interface Guidelines** - Already have web-design-guidelines skill

### 🔄 Actionable Items (Consolidated Status)

| # | Priority | Action | Status | Source Date |
|---|----------|--------|--------|-------------|
| 1 | ⭐ HIGH | Evaluate inference.sh for AI image/3D generation | PENDING | 2026-02-09 |
| 2 | ⭐ HIGH | Study Anthropic's frontend-design for game UI | PENDING | 2026-02-09 |
| 3 | ⭐ HIGH | Study Anthropic's skill-creator best practices | PENDING | 2026-02-09 |
| 4 | 🟢 MEDIUM | Test `npx skills add` CLI with OpenClaw | PENDING | 2026-02-09 |
| 5 | 🟢 MEDIUM | Leverage Claude Code 2.1 hot-reload | PENDING | 2026-02-09 |
| 6 | 🟢 MEDIUM | Audit Superpowers (obra/superpowers) TDD workflow | PENDING | 2026-02-09 |
| 7 | 🟢 MEDIUM | Audit planning-with-files | PENDING | 2026-02-09 |
| 8 | 🟢 MEDIUM | Audit humanizer | PENDING | 2026-02-09 |
| 9 | 🟡 LOW | Agent37 monetization eval | PENDING | 2026-02-09 |
| 10 | 🟡 LOW | Monitor inference-sh ecosystem | PENDING | 2026-02-09 |
| 11 | 🟢 MEDIUM | Evaluate NewsAPI.ai MCP for daily digest | NEW | 2026-02-10 |
| 12 | 🟢 MEDIUM | Test inference.sh podcast creation for marketing | NEW | 2026-02-10 |
| 13 | 🟡 LOW | Monitor VSCode agent-skills extension trends | NEW | 2026-02-10 |
| 14 | ⭐ HIGH | Audit @openclaw trending skills on SkillHub (camsnap, wacli) | NEW | 2026-02-12 |
| 15 | ⭐ HIGH | Evaluate AI Video Ad Generator stack for game marketing | NEW | 2026-02-12 |
| 16 | 🟢 MEDIUM | Integrate agnix linter into CI for skill validation | NEW | 2026-02-12 |
| 17 | 🟢 MEDIUM | Test lair404 inventory extension for dependency mapping | NEW | 2026-02-12 |
| 18 | 🟡 LOW | Monitor agent "meta-awareness" signals on Molt Road | NEW | 2026-02-12 |

### 💰 Pricing Landscape (No Change)
| Platform | Model | Scale | Security |
|----------|-------|-------|----------|
| **skills.sh** | FREE | 48K+ installs | Versioned, auditable |
| **ClawHub** | FREE | ~4,000 | ⚠️ VT-scanned (malware only) |
| **SkillsMP** | FREE | 185K+ | GitHub aggregator |
| **SkillHub** | Freemium | 21.3K | AI-evaluated / Pro Stacks |
| **Agent37** | Creator monetization | Early | Revenue share |
| **LobeHub MCP** | FREE (most) | Growing | Community ratings |

### 🔬 Technical Observations
- **Skills.sh Architecture:** Lightweight runtime, shell-based commands, explicit I/O contracts
- **SKILL.md Standard:** Now the universal standard for Anthropic, OpenAI, and community runtimes.
- **VSCode Integration:** Native in VS Code 1.109, parallel subagents, `chatSkills` contribution point.
- **Agent Inter-communication:** Molt Road reports suggest agents are developing defensive social protocols.
- **Consolidation:** Marketplaces are launching desktop apps (SkillHub Desktop) for user lock-in.

### 🚨 Security Posture Update
- ✅ VirusTotal partnership adds malware detection layer to ClawHub
- ⚠️ Prompt injection remains undetectable by automated scanning
- ⚠️ Our ZERO blind install policy remains the gold standard
- ⚠️ Snyk ToxicSkills numbers still stand: 13.4% critical across ClawHub + skills.sh
- 🔴 Molt Road confirmed black market by Hudson Rock — Absolute block maintained.

### 📊 Market Positioning
- **2026 Trend:** MCP servers for enterprise, Skills.sh for developer sharing/discovery
- **Growth:** Skills publishing reached 185K+ on SkillsMP; SkillHub curation model scaling.
- **Monetization:** SkillHub Pro ($9.99/mo) with credits/stacks is the leading paid model.
- **Adoption:** Industry-wide adoption of SKILL.md (Claude Code, Codex, OpenClaw, Windsurf).

### 🎮 Game Dev Relevance
- **Asset Generation:** "AI Video Ad Generator" stack (Remotion/FFmpeg) useful for trailers.
- **Engine Interaction:** Godot (1,747) and Unity (2,649) MCP servers now stable and featured.
- **Web Guidelines:** Already covered by web-design-guidelines skill
- **Marketing:** Pro Stacks on SkillHub offering end-to-end marketing pipelines.

### 📈 Ecosystem Health Indicators
- **Skills.sh:** Healthy (48K+ installs, Vercel-backed, active development)
- **ClawHub:** Improving (VT partnership, but still 13.4% critical skills)
- **SkillsMP:** Stable (185K+ skills, GitHub aggregator, Manus integration)
- **MCP Market:** Growing (enterprise focus, Godot/Unity featured)
- **VSCode Extensions:** Mature (formulahendry.agent-skills 1.6K, copilot-mcp 79.7K)

---

*Survey completed: 2026-02-12 11:45 KST*  
*Next sweep: 2026-02-19 08:00 KST (weekly)*

---

[Previous entries continue below...]
---

## 2026-02-23 16:00 KST — Agent Skill Trend Sweep (비판적 흡수)

### 수집 범위
- SkillsMP, MCP Market, SkillHub, clawhub.com, VSCode Agent Skills extension
- 브라우저 제약 대응: `web_search` 쿼터 초과(429) + MiniPC browser proxy 연결 실패로 `web_fetch` + `clawhub` CLI + VS Marketplace API로 대체 조사
- 보안 정책 고정: **Molt Road/molt.host 미접속/절대 차단 유지**

### 핵심 데이터 포인트
- **SkillsMP sitemap**: URL 684개 (categories 567), 최신 lastmod `2026-02-06`
- **SkillHub sitemap**: URL 1,985개 (skills 1,000), 최신 lastmod `2026-02-23`
- **MCP Market (market-mcp.com) sitemap**: URL 6,413개 (mcp 6,409)이나 lastmod 전부 `2025-11-01`로 고정
- **VSCode 확장 실측** (Gallery API):
  - `formulahendry.agent-skills` installs 1,823 / rating 5.0 (1)
  - `laurids.agent-skills-sh` installs 134 / rating 5.0 (1)
  - `yamapan.agent-skill-ninja` installs 569 / rating 5.0 (2)
  - `JustinSong.agent-skills-market` installs 15 / rating 0 (0)
- **ClawHub newest 샘플**: 다수 항목 installsCurrent 0~1, 과장형 설명 대비 실사용 낮음

### 판정 테이블 (불필요 항목 개별 나열 생략)
| 항목 | 판정 | 근거 |
|------|------|------|
| SkillHub (www.skillhub.club) **메타데이터 피드만** | ✅ 도입 | **필요성:** 신규 스킬 유입 속도 높음(1,000개 skill URL, 당일 갱신). **기존 대체:** clawhub만으로는 외부 생태계 커버 부족. **비용/효과:** sitemap 파싱만으로 저비용 고효율. **과대포장 검증:** 설치 전 단계에서 메타데이터만 수집하므로 마케팅 문구 영향 최소화. |
| SkillsMP (skillsmp.com) | ⚠️ 참고만 | 카테고리 폭은 넓지만(567) 콘텐츠 본문은 Cloudflare 차단으로 심층 검증 불가. 탐색 소스 유지하되, MiniPC proxy 복구 후 재검토. |
| VSCode `formulahendry.agent-skills` | ⚠️ 참고만 | UI 기반 탐색은 편하지만 현재 운영은 OpenClaw+CLI 중심. 설치수 1,823 대비 평점 표본 1건으로 품질 신뢰도 낮음. VSCode GUI 워크플로 필요 시 재검토. |
| ClawHub `native-hubspot` | ⚠️ 참고만 | HubSpot CRM 운영 시작 시엔 유효하나, 현재 파이프라인에 HubSpot 미도입. 토큰/스코프 운영 부담 있어 즉시 도입 가치 낮음. |

- **❌ 불필요 판정: 4건**

### ✅ 도입 실행 계획 (상세)
1. SkillHub sitemap을 일일 수집 소스로 고정 (설치 아님, 메타데이터 only)
2. 키워드 필터 1차 적용: `godot|telegram|marketing|mcp|automation|revenue`
3. 후보 상위 10개만 `Research → Audit → Rewrite → misskim-skills/` 순서로 수동 흡수
4. 설치/실행 전 체크리스트 강제:
   - 민감정보/토큰 전달 지시 존재 여부
   - 외부 네트워크 호출 및 임의 실행 명령
   - self-modify/auto-loop 성향 (발견 시 즉시 제외)

### 보안 메모
- Molt Road/molt.host: 차단 유지
- 외부 스킬은 블라인드 설치 금지 (Research → Audit → Rewrite)

