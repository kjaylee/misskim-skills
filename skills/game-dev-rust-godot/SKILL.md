---
name: game-dev-rust-godot
description: Game development workflow using Rust+WASM or Godot 4.x for HTML5 games. Use when creating new games, implementing game mechanics, or porting existing games. Follows TDD-based production pipeline v3.1 with asset-first approach. Covers Rust(Macroquad/Bevy), Godot HTML5 Export, asset acquisition, test case writing, and QA automation. Master directive (2026-02-06) - ONLY Rust+WASM or Godot allowed, JS/TS frameworks prohibited.
---

# Game Development: Rust + WASM / Godot 4.x

HTML5 게임 제작을 위한 전용 워크플로우. **주인님 직접 지시 (2026-02-06)**: Rust + WASM 또는 Godot만 사용.

## 🚀 기술 스택 (필수 준수)

### ✅ 허용된 기술
- **Rust + WASM**: Macroquad (권장), Bevy
- **Godot 4.x**: HTML5 Export

### ❌ 금지된 기술
- JavaScript/TypeScript (Phaser, PixiJS, Three.js 등 모든 JS 프레임워크)
- Unity WebGL
- 기타 웹 게임 엔진

## 📋 워크플로우 개요

```
1. 에셋 확보 (코딩 전 필수!)
   ↓
2. 에셋 기반 기획 구체화
   ↓
3. 메카닉 검증 (프로토타입)
   ↓
4. 테스트케이스 작성 (TDD)
   ↓
5. 구현 ↔ 기획 보완 (TC 100% PASS까지)
   ↓
6. QA (Playwright + 수동)
   ↓
7. 런칭 테스트
   ↓
8. 보고 (스크린샷 4장 + DoD 체크리스트)
```

## 🎨 에셋 확보 (Phase 1 - 필수!)

**⛔ 에셋 없이 코딩 시작 절대 금지**

### 에셋 소스 우선순위
1. NAS 게임마당 (`/Volumes/workspace/Asset Store-5.x/`, 265 packages)
2. MiniPC Gemini AI 생성 (`browser.proxy`, node=MiniPC)
3. 무료 에셋 (kenney.nl CC0, opengameart.org, freesound.org)
4. 맥북 MLX Z-Image-Turbo (`nodes.run`, node=MacBook Pro)
5. Blender 3D→2D 렌더링 (MiniPC)

### 필수 에셋 체크리스트
```
□ 캐릭터/오브젝트 스프라이트
□ 배경 이미지/타일맵
□ UI 요소 (버튼, 아이콘, 패널)
□ BGM 최소 1곡 (mp3/ogg, 루프)
□ SFX 최소 3개 (클릭, 성공, 실패)
□ 에셋 라이선스 확인 (CC0/MIT/상용 허용)
```

**라이선스 정책 (공개 게임)**:
- ✅ Kenney.nl CC0, AI 생성, 직접 제작
- ❌ Unity Asset Store (무료 포함), 재배포 불허 에셋

## 🦀 Rust + WASM 구현

### Macroquad (권장)

**프로젝트 생성** (MiniPC):
```bash
cd $HOME/spritz/dynamic/games/<game-name>
cargo init
```

**Cargo.toml**:
```toml
[package]
name = "game-name"
version = "0.1.0"
edition = "2021"

[dependencies]
macroquad = "0.4"

[profile.release]
opt-level = "z"
lto = true
```

**기본 구조** (`src/main.rs`):
```rust
use macroquad::prelude::*;

#[macroquad::main("Game Title")]
async fn main() {
    loop {
        clear_background(BLACK);
        
        // 게임 로직
        
        next_frame().await
    }
}
```

**빌드 & 배포**:
```bash
# MiniPC에서
cargo build --release --target wasm32-unknown-unknown

# WASM 파일 복사
cp target/wasm32-unknown-unknown/release/<game-name>.wasm .

# index.html 생성 (Macroquad 자동 제공)
```

**자세한 가이드**: `references/rust-macroquad.md` 참조

### Bevy (고급)

복잡한 ECS 구조가 필요할 때만 사용. 빌드 시간 길고 (7분+) WASM 용량 큼 (3.6MB+).

**자세한 가이드**: `references/rust-bevy.md` 참조

## 🎮 Godot 4.x 구현

### 프로젝트 생성 (MiniPC)

```bash
cd $HOME/godot4/projects
mkdir <game-name>
cd <game-name>

# project.godot 생성
godot4 --headless --path . --quit
```

### HTML5 Export 설정

1. **Export Preset 추가**:
   - Project → Export → Add... → Web
   - Export Path: `build/web/index.html`

2. **설정 최적화**:
   - Texture Format: VRAM Compressed
   - Head Include: Custom HTML template (필요 시)

### 빌드 & 배포

```bash
# MiniPC에서
godot4 --headless --path . --export-release "Web"

# 결과물: build/web/ (index.html, *.wasm, *.pck)
```

**자세한 가이드**: `references/godot-html5.md` 참조

## ✅ 테스트케이스 작성 (Phase 4 - TDD)

**구현 전에 TC 먼저 작성**

### TC 카테고리

#### 기능 TC
```
TC-F001: 게임 시작 시 타이틀 화면 표시
TC-F002: 시작 버튼 클릭 시 게임 플레이 진입
TC-F003: [핵심 메카닉] 입력에 대한 올바른 반응
TC-F004: 점수/진행도 업데이트
TC-F005: 게임 오버 조건 충족 시 결과 화면 표시
```

#### UI/UX TC
```
TC-U001: 모바일 뷰포트 (390x844) 정상 표시
TC-U002: 가로 스크롤 없음
TC-U003: 터치 영역 최소 44x44px
TC-U004: safe-area 적용
```

#### 성능 TC
```
TC-P001: 페이지 로드 5초 이내
TC-P002: JS 콘솔 에러 0개
TC-P003: 60fps 유지 (게임플레이 중)
```

**TC 문서 위치**: `specs/games/<game>/test-cases.md`

## 🔄 구현 ↔ 기획 보완 루프 (Phase 5)

**TC 100% PASS까지 반복**:

```
구현 (TC 기반)
  ↓
TC 실행
  ↓
FAIL → 코드 수정 or 기획 조정
  ↓
재구현
  ↓
TC 재실행
  ↓
ALL PASS → Phase 6으로
```

**탈출 조건**:
```
□ 모든 기능 TC PASS
□ 모든 UI/UX TC PASS
□ 모든 성능 TC PASS
□ DoD 체크리스트 전항목 충족
```

## 🧪 QA (Phase 6)

### 자동 테스트 (MiniPC Playwright)

```bash
# MiniPC에서
cd $HOME/qa-automation
playwright test games/<game-name>.spec.ts
```

**필수 검증 항목**:
```
□ 페이지 로드 성공 (5초 내)
□ JS 콘솔 에러 0개
□ 시작 버튼 클릭 가능
□ 게임 플레이 가능 (5초 이상 생존)
□ 모바일 뷰포트 (390x844) 정상 표시
```

### 수동 체크리스트
```
□ 전체 게임 루프 1회 완주
□ 에지 케이스 테스트
□ 사운드 재생 확인 (BGM + SFX)
□ 반응형 확인 (데스크톱 + 모바일)
```

### 스크린샷 캡처 (최소 4장)
```
□ 타이틀 화면
□ 게임플레이 (진행 중)
□ UI 요소 (메뉴, 설정 등)
□ 결과 화면 (게임오버/클리어)
```

## 📦 배포

### Rust + WASM
```bash
# eastsea.monster/games/<game>/ 에 배포
- index.html
- <game>.wasm
- mq_js_bundle.js (Macroquad)
- assets/ (에셋 폴더)
```

### Godot
```bash
# build/web/ 내용을 eastsea.monster/games/<game>/ 에 배포
- index.html
- <game>.wasm
- <game>.pck
- assets/ (에셋 폴더, 필요 시)
```

## ✅ Definition of Done

**전부 충족해야 완료**:

```
□ 실제 이미지 에셋 적용 (CSS 도형/emoji 금지)
□ 실제 오디오 에셋 적용 (oscillator 금지)
□ TC 100% PASS
□ Playwright 자동 테스트 통과
□ 스크린샷 4장 이상
□ 모바일 반응형 확인
□ 치명적 버그 0개
□ og.png 생성 (1200x630)
□ 런칭 테스트 통과 (실제 URL)
```

## 🎯 게임 등급 기준

| 등급 | 기준 | 조치 |
|------|------|------|
| **A** | DoD 전항목 충족, TC 100% PASS | 유지 & 마케팅 |
| **B** | 게임 작동, 일부 에셋 부족 또는 TC 미통과 | 에셋 교체 + TC 보완 |
| **C** | 코드만 존재, 에셋 전무, TC 미작성 | Phase 1부터 재시작 |
| **F** | index.html 없음, 빈 디렉토리, 크래시 | 삭제 또는 재제작 |

## 📚 상세 가이드

- **Rust Macroquad**: `references/rust-macroquad.md`
- **Rust Bevy**: `references/rust-bevy.md`
- **Godot HTML5**: `references/godot-html5.md`
- **에셋 라이선스**: `references/asset-licensing.md`
- **성능 최적화**: `references/optimization.md`

## ⚠️ 중요 제약사항

1. **기술 스택**: Rust + WASM 또는 Godot만 허용
2. **에셋 우선**: 코딩 전 에셋 전부 확보
3. **TDD 필수**: TC 작성 후 구현
4. **모바일 퍼스트**: 반응형 동시 구현
5. **라이선스 준수**: 재배포 가능한 에셋만 사용

## 🚀 빠른 시작 예시

### Snake 게임 (Rust + Macroquad)

1. **에셋 확보**: NAS에서 뱀/먹이 스프라이트, kenney.nl에서 BGM/SFX
2. **TC 작성**: 6개 기능 TC, 5개 UI TC, 4개 성능 TC
3. **구현**: Macroquad로 뱀 이동/충돌/점수 로직
4. **QA**: Playwright 자동 테스트 + 모바일 수동 테스트
5. **배포**: eastsea.monster/games/snake/

**소요 시간**: 에셋 확보 1시간 + 구현 2시간 + QA 30분 = 약 3.5시간
