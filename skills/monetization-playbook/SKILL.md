---
name: monetization-playbook
description: 인디 개발자의 무료 도구/게임/앱 수익화 완전 플레이북. 제품 유형별 수익 모델 선택, 가격 전략, AdSense/Stripe/Gumroad 구현, 마케팅 연동, 퍼널 측정, A/B 테스트까지. monetization, pricing, paywall, freemium, indie revenue 언급 시 사용.
metadata:
  author: misskim
  version: "1.0"
  origin: Marketing Brain + ButterKit 흡수 패턴 종합
---

# 💰 Indie Monetization Playbook

인디 개발자가 무료 제품을 수익화하는 실전 플레이북.
이론 없이, 실행만.

---

## 적용 시점

- 새 제품 수익화 모델 설계 시
- 기존 무료 제품에 수익 레이어 추가 시
- "수익화", "monetization", "pricing", "paywall" 언급 시

---

## 1. 수익 모델 매트릭스

제품 유형 → 최적 수익 모델 즉시 선택.

```
제품 유형           │ 1순위              │ 2순위             │ 3순위
────────────────────┼────────────────────┼───────────────────┼──────────────────
브라우저 도구        │ AdSense            │ 프리미엄 업그레이드  │ 도네이션 (Ko-fi)
HTML5 게임          │ 인앱 광고 (리워디드) │ 프리미엄 모드       │ 스폰서십/포털 배포
모바일 앱 (로컬)     │ 프리미엄 게이트      │ 원타임 구매         │ 선택적 연간 후원
모바일 앱 (서버)     │ 구독 (월/연)        │ 프리미엄 티어       │ 사용량 과금
소설/콘텐츠          │ 유료 구독           │ 스폰서 챕터         │ 광고 삽입
텔레그램 Mini App   │ 리워디드 광고        │ Stars 아이템       │ 어필리에이트
```

### 모델별 핵심 설계

#### 프리미엄 게이트 (모바일 앱 추천)
```
Free 버전: 모든 기능 사용 가능 + 워터마크/제한
Pro 버전: 워터마크 제거 + 프리미엄 기능 잠금 해제
가격: 1회 구매 ($4.99-$14.99)
```
- ✅ 무료에서 충분한 가치 제공 → 전환율 향상
- ✅ "서버 없음 → 구독 불필요" 내러티브 활용
- ❌ 서버 비용 발생 제품에는 부적합

#### AdSense (브라우저 도구 추천)
```
배치: 콘텐츠 하단 + 사이드바 (모바일: 인피드)
예상 RPM: $1-5 (도구 사이트), $0.5-2 (게임)
손익분기: 월 10,000+ 페이지뷰
```

#### 리워디드 광고 (게임 추천)
```
트리거: 추가 생명/코인/힌트 획득 시
빈도: 게임 오버당 1회 (강제 아님)
보상: 유저에게 명확한 가치 (코인 50개 등)
```

---

## 2. 가격 전략: 반구독 모델

**핵심:** 1회 구매 + 선택적 연간 후원 (Anti-Subscription Narrative)

```
┌─────────────────────────────────────────────────┐
│  Free          │  Pro (1회 구매)  │  Supporter    │
│  기본 기능      │  풀 기능         │  Pro + 우선 지원│
│  워터마크/광고   │  워터마크 제거    │  연간 갱신 선택 │
│  $0            │  $4.99-14.99    │  $2.99/년     │
└─────────────────────────────────────────────────┘
```

### 가격 포인트 결정 기준
| 제품 복잡도 | 1회 구매 가격 | 비교 기준 |
|------------|-------------|----------|
| 단순 도구 | $2.99-4.99 | 커피 1잔 |
| 중급 앱 | $4.99-9.99 | 점심 1끼 |
| 전문 앱 | $9.99-19.99 | 영화 + 팝콘 |
| 프로 도구 | $19.99-49.99 | 월 구독 대비 저렴 강조 |

### 할인 전략
- **교육 할인:** 학생/교사/군인 50% (.edu / .ac.kr 이메일 확인)
- **런칭 할인:** 첫 2주 40% (FOMO 활용)
- **프로모 코드:** 25개 무료 + 할인 코드 40% (레딧 배포용)

---

## 3. 구현 가이드

### 3.1 AdSense 삽입 (브라우저 도구/웹사이트)

```html
<!-- 1. 승인 후 ads.txt 루트에 배치 -->
google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0

<!-- 2. 자동 광고 (가장 간단) -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXX"
     crossorigin="anonymous"></script>

<!-- 3. 수동 광고 유닛 (추천: 콘텐츠 하단) -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-XXXXXXXX"
     data-ad-slot="YYYYYYYY"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
```

**체크리스트:**
- [ ] 사이트에 충분한 콘텐츠 (최소 15-20 페이지/포스트)
- [ ] Privacy Policy 페이지 필수
- [ ] 모바일 반응형 확인
- [ ] 광고 밀도: 콘텐츠 대비 30% 이하

### 3.2 Stripe 연동 (원타임 구매/구독)

```javascript
// Stripe Checkout — 가장 빠른 구현 (서버 사이드)
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

// 원타임 구매
const session = await stripe.checkout.sessions.create({
  line_items: [{
    price_data: {
      currency: 'usd',
      product_data: { name: 'Pro License' },
      unit_amount: 999, // $9.99
    },
    quantity: 1,
  }],
  mode: 'payment',
  success_url: 'https://yoursite.com/success?session_id={CHECKOUT_SESSION_ID}',
  cancel_url: 'https://yoursite.com/cancel',
});
// → session.url로 리다이렉트

// 웹훅으로 결제 완료 처리
app.post('/webhook', express.raw({type: 'application/json'}), (req, res) => {
  const event = stripe.webhooks.constructEvent(
    req.body, req.headers['stripe-signature'], webhookSecret
  );
  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    // 라이선스 발급 로직
  }
  res.json({received: true});
});
```

**절대 금지:**
- ❌ Charges API (레거시)
- ❌ Card Element 직접 사용 (PCI 부담)
- ❌ payment_method_types 하드코딩

### 3.3 Gumroad 연동 (서버리스 대안)

```html
<!-- 가장 간단: Gumroad 오버레이 -->
<script src="https://gumroad.com/js/gumroad.js"></script>
<a class="gumroad-button" href="https://yourname.gumroad.com/l/product">
  Buy Pro License — $9.99
</a>

<!-- 또는 Gumroad API로 라이선스 검증 -->
<!-- GET https://api.gumroad.com/v2/licenses/verify -->
<!-- params: product_id, license_key -->
```

**Gumroad vs Stripe 선택:**
| 기준 | Gumroad | Stripe |
|------|---------|--------|
| 세팅 시간 | 5분 | 1-2시간 |
| 수수료 | 10% | 2.9% + $0.30 |
| 서버 필요 | ❌ | ✅ |
| 라이선스 키 | 자동 생성 | 직접 구현 |
| 추천 상황 | MVP/빠른 검증 | 스케일/커스텀 |

### 3.4 페이월 구현 패턴

```javascript
// 프론트엔드 페이월 게이트
function checkAccess(feature) {
  const license = localStorage.getItem('pro_license');
  if (!license && PREMIUM_FEATURES.includes(feature)) {
    showUpgradeModal(); // 구매 유도 모달
    return false;
  }
  if (license) {
    // 서버사이드 검증 (변조 방지)
    return verifyLicense(license);
  }
  return true; // 무료 기능
}

// 워터마크 방식 (카메라 앱 등)
function applyWatermark(canvas) {
  if (!isPro()) {
    const ctx = canvas.getContext('2d');
    ctx.font = '14px Arial';
    ctx.fillStyle = 'rgba(255,255,255,0.5)';
    ctx.fillText('Made with AppName', 10, canvas.height - 20);
  }
}
```

---

## 4. 마케팅 연동

### 4.1 #RoastMyApp 레딧 캠페인

**포스트 템플릿:**
```markdown
Title: #RoastMyApp: [제품명]에 대한 솔직한 피드백 구합니다. 무료 Pro 라이선스 25개 포함

Body:
[N]개월간 만든 [제품명]을 드디어 공개합니다.

핵심 기능:
- [기능 1]
- [기능 2]
- [기능 3]

🎁 무료 Pro 라이선스 25개 (선착순):
CODE1, CODE2, CODE3 ... CODE25

💸 할인 코드: [코드] (40% OFF)

솔직한 피드백 부탁드립니다. 칭찬보다 비판이 더 도움됩니다!

사용하신 코드는 댓글로 알려주세요 🙏
```

**타겟 서브레딧 (제품별):**
| 제품 유형 | 서브레딧 |
|----------|---------|
| 모바일 앱 | r/iOSProgramming, r/androiddev, r/AppBusiness |
| 게임 | r/godot, r/iosgaming, r/indiegaming, r/IndieDev |
| 웹 도구 | r/webdev, r/SideProject, r/InternetIsBeautiful |
| 사진/카메라 | r/photography, r/mobilephotography |

**핵심 규칙:**
- 5개+ 서브레딧에 동일 포맷 포스트 (각 서브 규칙 준수)
- 코드 소진 시 댓글 알림 → FOMO 효과
- 겸손한 톤 필수 ("솔직한 피드백 달라")
- 먼저 커뮤니티에 기여 후 포스팅 (스팸 밴 방지)

### 4.2 ASO 39개 언어 로컬라이징

```
실행 순서:
1. Xcode 시뮬레이터에서 스크린샷 캡처
2. ButterKit Pro로 39개 언어 자동 번역 + 프레이밍
3. App Store Connect에 업로드
4. 스크린샷 캡션에 검색 키워드 의도적 삽입
   (Apple이 스크린샷 텍스트를 검색 인덱싱에 반영)
```

### 4.3 안티 구독 내러티브 (로컬 앱 전용)

포지셔닝 문구:
```
"서버가 없으니 구독이 필요 없습니다.
한 번 구매하면 영원히 사용하세요."

"No accounts. No tracking. No subscription.
Buy once, own forever."
```

### 4.4 2중 커뮤니티

```
Discord (실시간)          Reddit (비동기)
├── #general              ├── 기능 요청 투표
├── #bug-reports          ├── 프로모 코드 배포
├── #feature-requests     ├── devlog 공유
└── #showcase             └── 유저 쇼케이스
→ 양쪽 크로스 링크
→ 기능 요청 → 개발 우선순위 반영 → 충성도 ↑
```

---

## 5. 측정: 퍼널 지표

### 핵심 퍼널

```
방문 (Visit)
  ↓ [전환율 목표: 5-15%]
활성 사용 (Active Use)
  ↓ [전환율 목표: 2-5%]
업그레이드 시도 (Upgrade Intent)
  ↓ [전환율 목표: 30-60%]
결제 완료 (Payment)
  ↓ [유지율 목표: 70%+]
재구매/추천 (Retention/Referral)
```

### 추적해야 할 지표

| 단계 | 지표 | 도구 |
|------|------|------|
| 유입 | 페이지뷰, 유입 채널 | Google Analytics / Plausible |
| 활성화 | DAU, 세션 길이 | 자체 이벤트 로깅 |
| 전환 | 업그레이드 모달 노출 vs 클릭 | 자체 이벤트 |
| 결제 | 결제 완료율, 평균 매출 | Stripe Dashboard |
| 유지 | D1/D7/D30 리텐션 | 자체 코호트 분석 |

### A/B 테스트 패턴

#### 테스트 1: 가격 포인트
```
A: $4.99 (기본)
B: $9.99 (프리미엄 인식)
C: $6.99 (중간)
측정: 전환율 × 가격 = 매출 극대화 포인트
기간: 최소 2주, 유저 500명 이상/그룹
```

#### 테스트 2: 페이월 타이밍
```
A: 3일 후 프리미엄 유도
B: 7일 후 프리미엄 유도
C: 기능 제한 도달 시 유도
측정: 전환율 + D30 리텐션 (너무 빠르면 이탈↑)
```

#### 테스트 3: CTA 문구
```
A: "Upgrade to Pro"
B: "Remove Watermark — $4.99"
C: "Unlock All Features"
측정: 클릭율 → 결제 완료율
```

#### 테스트 4: 무료 코드 수량
```
A: 10개 무료 코드
B: 25개 무료 코드
C: 50개 무료 코드
측정: 레딧 engagement + 후속 유료 전환
```

---

## 6. 실행 체크리스트

### Phase 0: 수익 모델 결정 (Day 1)
```checklist
- [ ] 제품 유형 확인 → 매트릭스에서 수익 모델 선택
- [ ] 서버 비용 유무 확인 → 구독 vs 1회 구매 결정
- [ ] 경쟁 제품 가격 조사 (최소 5개)
- [ ] 가격 포인트 1차 결정
- [ ] Free vs Pro 기능 분리표 작성
```

### Phase 1: 결제 인프라 구축 (Day 2-3)
```checklist
- [ ] Stripe 계정 생성 + API 키 발급
  OR Gumroad 제품 페이지 생성 (MVP 시)
- [ ] Checkout 플로우 구현 (테스트 모드)
- [ ] 웹훅 설정 + 라이선스 발급 로직
- [ ] 결제 성공/실패 페이지 구현
- [ ] Privacy Policy + Terms of Service 페이지
```

### Phase 2: 페이월 구현 (Day 4-5)
```checklist
- [ ] 프리미엄 게이트 UI 구현 (모달/배너)
- [ ] 워터마크 또는 기능 제한 적용
- [ ] 라이선스 검증 로직 (프론트 + 백엔드)
- [ ] 복원 기능 (앱스토어) 또는 라이선스 키 재입력
- [ ] 업그레이드 CTA 배치 (자연스러운 위치)
```

### Phase 3: 마케팅 준비 (Day 6-7)
```checklist
- [ ] 프로모 코드 25개 생성
- [ ] 할인 코드 40% 생성
- [ ] #RoastMyApp 포스트 초안 작성
- [ ] 타겟 서브레딧 5개 선정 + 규칙 확인
- [ ] 앱스토어: ButterKit으로 39개 언어 스크린샷 (해당 시)
- [ ] Discord 서버 or 서브레딧 생성
```

### Phase 4: 런칭 + 측정 (Day 8+)
```checklist
- [ ] 레딧 포스트 게시 (5개 서브레딧)
- [ ] 코드 소진 시 댓글 알림 게시
- [ ] Google Analytics / Plausible 설치
- [ ] 퍼널 이벤트 트래킹 설정
- [ ] 1주차: 전환율 체크 → 가격 A/B 테스트 시작
- [ ] 2주차: CTA 문구 A/B 테스트
- [ ] 4주차: 월간 수익 리포트 → 모델 조정
```

---

## ⚡ Quick Decision Guide

```
Q: 서버 비용 있나?
├── YES → 구독 모델 고려
└── NO → 1회 구매 + "안티 구독" 내러티브

Q: MVP인가?
├── YES → Gumroad (5분 세팅)
└── NO → Stripe (수수료 절감)

Q: 유저 100명 넘었나?
├── YES → 수익화 시작
└── NO → 수익화 보류, 유저 획득 집중

Q: 첫 유료 전환 확인됐나?
├── YES → A/B 테스트로 최적화
└── NO → CTA/페이월 위치 재검토
```

---

*Reference: memory/projects/marketing.md, specs/butterkit-absorption.md*
