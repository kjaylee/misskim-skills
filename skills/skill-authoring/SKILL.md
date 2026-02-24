---
name: skill-authoring
description: Guide for creating effective SKILL.md files that extend agent capabilities. Use when creating new skills, updating existing ones, or teaching the agent specialized workflows.
metadata:
  author: misskim
  version: "1.0"
  origin: Concept from Anthropic skill-creator, adapted for Clawdbot agentskills.io standard
---

# Skill Authoring Guide

agentskills.io 표준에 맞는 효과적인 스킬 작성법.

## 핵심 원칙

### 1. 간결함이 왕
컨텍스트 윈도우는 공공재다. 모든 스킬이 이 공간을 공유한다.

**기본 가정: 에이전트는 이미 매우 똑똑하다.**
에이전트가 모르는 것만 추가할 것. 모든 문장마다 자문:
- "이 설명이 정말 필요한가?"
- "이 단락이 토큰 비용을 정당화하는가?"

장황한 설명보다 간결한 예제를 선호.

### 2. 자유도 매칭

| 자유도 | 언제 | 형태 |
|--------|------|------|
| **높음** | 여러 접근법이 유효, 맥락에 따라 판단 | 텍스트 지침 |
| **중간** | 선호 패턴 존재, 일부 변형 허용 | 의사코드/파라미터 있는 스크립트 |
| **낮음** | 취약한 작업, 일관성 필수 | 구체적 스크립트, 최소 파라미터 |

좁은 다리(절벽 옆) = 구체적 가드레일 (낮은 자유도)
넓은 평원 = 다양한 경로 허용 (높은 자유도)

## SKILL.md 구조

```yaml
---
name: my-skill-name        # 필수, 소문자+하이픈, 1-64자
description: >             # 필수, 1-1024자
  무엇을 하는지 + 언제 사용하는지 + 관련 키워드
license: Apache-2.0        # 선택
metadata:                  # 선택
  author: misskim
  version: "1.0"
---

# 스킬 제목

[에이전트가 따를 지침 - 마크다운 자유형식]
```

### 필수 필드
- **name:** 디렉토리명과 일치, 소문자+하이픈만
- **description:** 스킬 활성화 트리거 역할 → 키워드 풍부하게

### 디렉토리 구조
```
skill-name/
├── SKILL.md          # 필수
├── scripts/          # 실행 코드 (Python/Bash/JS)
├── references/       # 상세 문서 (필요 시 로드)
└── assets/           # 정적 리소스 (템플릿, 이미지, 데이터)
```

## 우리 환경 특화 고려사항

1. **Clawdbot 에이전트:** skills/ 또는 ~/.clawdbot/skills/에 배치
2. **MiniPC 연동:** nodes.run 명령으로 외부 작업 위임 가능
3. **서브에이전트:** 스킬이 서브에이전트를 스폰하도록 설계 가능
4. **보안:** scripts/ 코드는 신뢰할 수 있는 것만 포함
5. **SKILL.md 500줄 이하 유지** — 상세 내용은 references/로 분리

## 나쁜 스킬 vs 좋은 스킬

**나쁜:** "PDF를 처리합니다" (description이 너무 짧음)
**좋은:** "PDF 파일에서 텍스트/표를 추출하고, 폼을 채우고, 여러 PDF를 병합합니다. PDF 문서 작업이나 문서 추출을 언급할 때 사용."

**나쁜:** 에이전트가 이미 아는 Python 문법 설명
**좋은:** 에이전트가 모르는 도메인 특화 지식/워크플로우 제공

## Prerequisites Checklist (Template)

새 스킬 작성 시 아래 체크리스트를 먼저 채운다.

- [ ] 이 스킬이 해결할 **구체 문제**가 1문장으로 정의되어 있다.
- [ ] 기존 스킬과의 **중복 여부**를 확인했다 (중복이면 라우팅 섹션으로 통합).
- [ ] 필요한 실행 환경/의존성(노드, 바이너리, 권한, API 키)을 명시했다.
- [ ] 입력/출력 형태(예: 파일, URL, 코드, 보고서 템플릿)를 정의했다.
- [ ] 실패 시 폴백 경로(대체 툴/수동 절차)를 적었다.
- [ ] 최소 1개 이상의 실제 사용 예시를 포함했다.
## When to Use / When NOT to Use (Decision Tree Template)

스킬 상단에 아래 템플릿 형태로 분기 로직을 추가한다.

```md
## When to Use This vs Others
- Use this skill when: {핵심 조건 1}, {핵심 조건 2}
- Use {other-skill} when: {대안 스킬이 더 적합한 조건}
- Do NOT use this skill when: {명확한 제외 조건}
```

의사결정은 2~3줄로 짧게 유지하고, 서로 헷갈리는 스킬 쌍에는 반드시 교차 링크를 넣는다.
## Dual Description Rule (Agent vs Marketplace)

동일 스킬이라도 설명은 목적별로 분리한다.

- **`SKILL.md` frontmatter `description` (에이전트용):**
  - 트리거 키워드를 풍부하게 포함한다.
  - "언제 호출되어야 하는지"를 명시한다.
  - 예: 도메인 키워드, 요청 유형, 활성화 신호 포함.
- **`marketplace.json` `description` (사람용):**
  - 기능 요약 중심의 자연스러운 1~2문장.
  - 마케팅/탐색 친화적 문장으로 작성.
  - 내부 트리거 키워드 나열은 지양.
