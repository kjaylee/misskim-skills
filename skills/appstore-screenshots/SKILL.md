---
name: appstore-screenshots
description: Xcode 프로젝트에서 App Store 홍보 스크린샷 자동 생성
metadata:
  author: misskim
  version: "1.0.0"
  pattern: Spec → Plan → Test Cases → Task Breakdown → Implementation
---

# appstore-screenshots

Xcode 프로젝트/워크스페이스 경로만 받아서 App Store Connect 업로드용 스크린샷을 생성한다.

## 엔트리포인트

```bash
$WORKSPACE/scripts/appstore-screenshots/screenshot-gen.sh
```

## 기본 사용

```bash
screenshot-gen <project-or-workspace-path>
```

## 주요 옵션
- `--scheme NAME`
- `--languages ko,en`
- `--devices "iPhone 16 Pro Max,iPhone 16 Pro,iPad Pro 13-inch (M4)"`
- `--dry-run`
- `--upload-fastlane`

## 출력
- raw 캡처: `output/raw/...`
- 프로모션 렌더: `output/promo/rendered/...`
- ASC 업로드용: `output/promo/asc/<lang>/*.png`

## 구성 스크립트
- `screenshot-gen.sh` — 전체 파이프라인 오케스트레이션
- `auto-explore.py` — 시뮬레이터 자동 탐색/캡처
- `promo-gen.py` — 프레임 합성 + App Store 규격 렌더
