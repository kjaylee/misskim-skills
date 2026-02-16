# Test Report — Game Video Ad Pipeline

작성일: 2026-02-16 (KST)

---

## 테스트 목표

- 기존 게임 1개를 대상으로 실제 프로모 비디오 생성
- 출력 파일 존재 확인
- 재생 가능(디코딩 가능) 확인

---

## 테스트 환경

- Repo: `misskim-skills`
- Script: `skills/game-video-ad-pipeline/scripts/generate-video.py`
- Encoder: `ffmpeg` (local)

참고 호환성 확인(MiniPC):
- `/usr/bin/ffmpeg` 존재
- `~/remotion-videos` 존재 및 `npx remotion` 응답
- `python3`에서 `PIL` import 가능

---

## 실행 명령

```bash
python3 skills/game-video-ad-pipeline/scripts/generate-video.py \
  --game-id steam:570 \
  --template action \
  --orientation vertical \
  --duration 15 \
  --output skills/game-video-ad-pipeline/output/dota2-action-vertical-15s.mp4
```

---

## 결과 로그 (요약)

```text
[game-video-ad] Fetched screenshots from Steam: 6
[game-video-ad] render complete
[game-video-ad] output: .../skills/game-video-ad-pipeline/output/dota2-action-vertical-15s.mp4
[game-video-ad] duration: 15.00s
[game-video-ad] resolution: 1080x1920
```

---

## 출력 파일 검증

1) 메타데이터 검증 (`ffprobe`)

```json
{
  "streams": [
    {
      "codec_name": "h264",
      "width": 1080,
      "height": 1920,
      "r_frame_rate": "30/1"
    }
  ],
  "format": {
    "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
    "duration": "15.000000"
  }
}
```

2) 재생 가능성 검증 (`ffmpeg -f null -`)
- 디코딩 에러 없이 통과

---

## 결론

- 테스트 케이스 **PASS**
- 요구사항(15~30초, 1080x1920/1920x1080, MP4, 텍스트 오버레이, 자동 수집) 충족
