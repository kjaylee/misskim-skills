# Audit — Game Video Ad Generator

작성일: 2026-02-16 (KST)
패턴: Research → Audit → Rewrite (2단계)

---

## 1) 라이선스 / 의존성 / 보안 검토

| 도구 | 라이선스/정책 | 의존성 | 보안/운영 메모 | 판단 |
|---|---|---|---|---|
| FFmpeg | LGPL 2.1+ (옵션 기능 포함 시 GPL 적용 가능) | 바이너리 + 코덱 | 배포 시 라이선스/코덱 조합 주의 필요 | **채택(필수)** |
| Remotion | 공개 소스 + Free/Company 조건(버전/조직 규모 정책 확인 필요) | Node, npm, Chrome | 로컬 렌더 가능하나 정책 추적 필요 | 보조 옵션 |
| MoviePy | MIT | Python + ffmpeg | Python 편의성 높지만 성능/제어는 ffmpeg 직접 호출이 유리 | 보조 옵션 |
| Pillow (PIL) | HPND/Custom (Pillow License) | Python | drawtext 미지원 환경에서 텍스트 오버레이에 사용 | **채택(필수)** |
| Shotcut/Kdenlive | GPLv3 | GUI + MLT/FFmpeg | CLI 자동화 목적에는 과한 GUI 의존 | 이번 구현 제외 |
| MLT | LGPL 계열 | C/C++ stack | 고급 편집엔 좋으나 설정 복잡 | 이번 구현 제외 |

근거:
- FFmpeg: https://ffmpeg.org/legal.html
- Remotion: https://raw.githubusercontent.com/remotion-dev/remotion/main/LICENSE.md
- MoviePy: https://raw.githubusercontent.com/Zulko/moviepy/master/LICENCE.txt
- Shotcut: https://raw.githubusercontent.com/mltframework/shotcut/master/COPYING
- Kdenlive: https://raw.githubusercontent.com/KDE/kdenlive/master/COPYING
- MLT: https://raw.githubusercontent.com/mltframework/mlt/master/COPYING

---

## 2) MiniPC 환경 호환성 점검

실측 확인 (nodes.run):
- `which ffmpeg` → `/usr/bin/ffmpeg`
- `ffmpeg -version` → `6.1.1...`
- `~/remotion-videos` 존재
- `npx remotion` 명령 응답 확인 (`@remotion/cli 4.0.410` 출력)

결론:
- 본 스킬 핵심 구현(ffmpeg + python)은 MiniPC에서 바로 실행 가능.
- Remotion은 필요 시 확장 렌더 옵션으로 활용 가능하나, 본 rewrite는 ffmpeg 우선으로 고정.

---

## 3) 비용 분석 ($0 목표)

## 비용 발생 요소 점검
- 외부 유료 생성 API: **사용 안 함**
- API 키/토큰: **불필요**
- 클라우드 렌더링: **불필요**
- 로컬 툴: ffmpeg + python 표준 라이브러리만 사용

## 네트워크 사용
- Steam 공개 상점 HTML에서 스크린샷 URL 파싱(무키, 무료 접근)
- 유료 API 과금 없음

## 결론
- 운영비용 목표 `$0` 충족.

---

## 4) 리스크와 완화

1. Steam 페이지 구조 변경 리스크
- 완화: `--input-dir` 로컬 미디어 fallback 제공.

2. 라이선스 혼합 리스크(FFmpeg 옵션)
- 완화: 스킬 문서에 LGPL/GPL 주의 명시, 배포 시 빌드 옵션 점검.

3. 텍스트 오버레이 깨짐/특수문자 이슈
- 완화: drawtext 대신 Pillow 기반 텍스트 렌더 + 줄바꿈 처리.

4. 폰트 미존재 이슈
- 완화: DejaVu/Liberation/Arial 등 기본 폰트 탐색, 없으면 기본 폰트 사용.

5. 길이/규격 미준수
- 완화: duration 입력 범위(15~30) 강제 + ffprobe 최종 검증.
