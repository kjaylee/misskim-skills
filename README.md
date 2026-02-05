# 🎀 미스 김의 스킬 레포

검증된 AI 에이전트 스킬만 수록합니다.

## 원칙

1. **무비판적 흡수 금지** — 외부 코드 그대로 갖다 쓰지 않음
2. **리서치 → 평가 → 재작성** — 개념만 흡수하고 자체 형태로 구현
3. **보안 우선** — 의심스러운 의존성 배제
4. **기존보다 나을 때만** — 이미 가진 능력이 더 나으면 흡수 안 함
5. **상용 수준** — 모든 스킬은 실전 검증 후 수록

## 스킬 목록

| 스킬 | 설명 | 상태 |
|------|------|------|
| [research-pro](research/SKILL.md) | Gemini CLI를 활용한 딥 리서치 및 서브에이전트 위임 | ✅ 활성 |
| [github-pro](github-pro/SKILL.md) | GitHub API 및 gh CLI를 활용한 고급 관리 | ✅ 활성 |
| [youtube-pro](youtube-pro/SKILL.md) | YouTube 요약, 전사 및 지능형 분석 | ✅ 활성 |
| [video-pro](video-pro/SKILL.md) | Remotion & FFmpeg 기반 고성능 비디오 에디팅 | ✅ 활성 |

## 구조

```
misskim-skills/
├── README.md
├── skills/
│   └── [skill-name]/
│       ├── SKILL.md       # 스킬 정의
│       ├── references/    # 참고 자료
│       └── scripts/       # 스크립트
└── research/              # 리서치 노트 (흡수 전 평가)
```

## 출처

- 자체 개발 + 외부 개념 재작성
- 라이선스: MIT

---

*미스 김이 직접 검증하고 만든 스킬만 들어갑니다.* 💋
