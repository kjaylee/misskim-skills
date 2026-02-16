---
name: game-video-ad-pipeline
description: FFmpeg 기반 $0 게임 광고 영상 자동 생성 스킬. 게임 ID(steam app id)로 스크린샷 자동 수집 → 템플릿 스타일(액션/퍼즐/아이들) 적용 → 텍스트 오버레이 포함 15~30초 MP4 출력.
metadata:
  author: misskim
  version: "1.0.0"
  pattern: Research → Audit → Rewrite
---

# 🎮 Game Video Ad Pipeline (FFmpeg-first)

게임 프로모션 영상(쇼츠/광고 크리에이티브)을 **완전 로컬 + 무료 툴**로 생성하는 스킬.

- 입력: `--game-id` (Steam app id)
- 자동화: 스크린샷 수집 + 화면 비율 정규화 + 텍스트 오버레이
- 출력: 15~30초 MP4 (`1080x1920` 또는 `1920x1080`)
- 제약: **ffmpeg 필수**, 외부 유료 API 없음, MiniPC 실행 가능

---

## 구조

```text
game-video-ad-pipeline/
├─ SKILL.md
├─ scripts/
│  └─ generate-video.py
└─ references/
   ├─ RESEARCH.md
   ├─ AUDIT.md
   └─ TEST_REPORT.md
```

---

## 빠른 사용법

```bash
cd misskim-skills
python3 skills/game-video-ad-pipeline/scripts/generate-video.py \
  --game-id steam:570 \
  --template action \
  --orientation vertical \
  --duration 18 \
  --output skills/game-video-ad-pipeline/output/dota2-action-vertical.mp4
```

가로 광고(1920x1080):

```bash
python3 skills/game-video-ad-pipeline/scripts/generate-video.py \
  --game-id 730 \
  --template puzzle \
  --orientation horizontal \
  --duration 20 \
  --output skills/game-video-ad-pipeline/output/cs2-puzzle-horizontal.mp4
```

로컬 이미지/GIF 폴더를 입력으로 쓰고 싶으면:

```bash
python3 skills/game-video-ad-pipeline/scripts/generate-video.py \
  --game-id 999999 \
  --input-dir ./my-assets \
  --template idle \
  --duration 15
```

---

## 템플릿 시스템

| 템플릿 | 톤 | 기본 카피 |
|---|---|---|
| `action` | 고채도/고대비, 임팩트 강조 | `Play Now` |
| `puzzle` | 밝고 클린한 톤 | `Challenge Your Brain` |
| `idle` | 부드럽고 안정적인 톤 | `Start Your Idle Journey` |

모든 템플릿은 ffmpeg filter 체인으로 구현되어 MiniPC/CLI 환경에서 동일 동작.

---

## 핵심 파이프라인

1. Steam 상점 HTML에서 스크린샷 URL 추출(키/결제 없음)
2. 이미지/GIF를 목표 해상도(세로/가로)로 정규화
3. 컷별 클립 생성 후 concat
4. 제목/태그라인/CTA 텍스트 오버레이
5. MP4(H.264, yuv420p, faststart) 출력 및 재생 가능성 검증

---

## 파라미터 요약

- `--game-id` (필수): `570` 또는 `steam:570`
- `--template`: `action|puzzle|idle`
- `--orientation`: `vertical|horizontal`
- `--duration`: `15~30` 초
- `--max-shots`: 사용 스크린샷 수 (기본 6)
- `--title`, `--tagline`, `--cta`: 오버레이 문구 직접 지정
- `--input-dir`: Steam 자동 수집 대신 로컬 미디어 사용
- `--keep-temp`: 중간 파일 디버깅용 유지

---

## 비판적 흡수 4질문 (적용 요약)

1. **무엇을 가져올까?**
   - ffmpeg의 확실한 이식성/속도, Remotion의 템플릿 개념, 경쟁 스킬의 workflow 구조.
2. **무엇을 버릴까?**
   - 유료 생성 API 의존, 클라우드 렌더 강제, 과한 JS 런타임 복잡도.
3. **우리 환경에 맞게 어떻게 바꿀까?**
   - Python + ffmpeg 단일 스크립트로 재작성, Steam HTML 파싱으로 무키 수집.
4. **성공을 어떻게 측정할까?**
   - 15~30초/1080 해상도/재생 가능한 MP4 생성, MiniPC 호환, 비용 $0.

---

## 안전/운영 메모

- 외부 LLM/유료 API 호출 없음
- 실행 전 `ffmpeg`, `ffprobe` 존재 확인
- 텍스트 오버레이는 ffmpeg drawtext가 없는 환경에서도 동작하도록 **Pillow(PIL)** 로 렌더링
- 대량 배치 시 `--max-shots`를 4~8 사이로 유지 권장

세부 근거는 `references/RESEARCH.md`, `references/AUDIT.md` 참조.
