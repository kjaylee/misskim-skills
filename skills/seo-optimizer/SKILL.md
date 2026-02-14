---
name: seo-optimizer
description: >
  GitHub Pages 정적 사이트 SEO 완전 최적화 스킬.
  기술적 SEO(sitemap, robots.txt, canonical, meta tags, Open Graph, JSON-LD),
  콘텐츠 SEO(제목/설명/키워드/내부링크), 도구·게임·블로그 페이지별 SEO,
  Google Search Console 연동, Core Web Vitals, SEO 감사 자동화.
  SEO, 검색 최적화, 메타태그, 구조화 데이터, 사이트맵 언급 시 활성화.
metadata:
  author: misskim
  version: "1.0"
  targets:
    - eastsea.monster
    - games.eastsea.xyz
---

# 🔍 SEO Optimizer — GitHub Pages 정적 사이트 완전 가이드

GitHub Pages 기반 사이트의 검색 최적화 실행 스킬.
서버 설정 불가 → HTML `<head>`, 정적 파일, 클라이언트 JS로만 해결.

---

## 적용 시점

- 새 페이지/포스트 발행 시
- SEO 감사 요청 시
- 검색 노출·트래픽 개선 요청 시
- 구조화 데이터/메타태그 작업 시

## 타겟 사이트

| 사이트 | 스택 | 콘텐츠 |
|--------|------|--------|
| eastsea.monster | GitHub Pages + Jekyll/Hugo | 도구 210개, 블로그 137개 |
| games.eastsea.xyz | GitHub Pages (정적) | 게임 101개 |

---

## 1. 기술적 SEO

### 1.1 sitemap.xml

Jekyll은 `jekyll-sitemap` 플러그인으로 자동 생성. 커스텀 필요 시:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  {% for page in site.pages %}
  {% unless page.exclude_from_sitemap %}
  <url>
    <loc>{{ site.url }}{{ page.url | remove: "index.html" }}</loc>
    <lastmod>{{ page.last_modified_at | date: "%Y-%m-%d" }}</lastmod>
    <changefreq>{{ page.changefreq | default: "monthly" }}</changefreq>
    <priority>{{ page.priority | default: "0.5" }}</priority>
  </url>
  {% endunless %}
  {% endfor %}
</urlset>
```

**대규모 사이트 (>500 URL):** sitemap index 분할

```xml
<!-- sitemap-index.xml -->
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://eastsea.monster/sitemap-tools.xml</loc></sitemap>
  <sitemap><loc>https://eastsea.monster/sitemap-blog.xml</loc></sitemap>
</sitemapindex>
```

### 1.2 robots.txt

```text
User-agent: *
Allow: /

Sitemap: https://eastsea.monster/sitemap.xml

# 불필요 크롤링 차단
Disallow: /assets/js/
Disallow: /assets/css/
Disallow: /404.html
```

### 1.3 Canonical URL

모든 페이지 `<head>`에 필수:

```html
<link rel="canonical" href="{{ page.url | absolute_url }}" />
```

### 1.4 필수 Meta Tags 템플릿

```html
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ page.title }} | {{ site.title }}</title>
  <meta name="description" content="{{ page.description | default: site.description | truncate: 160 }}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{{ page.url | absolute_url }}">

  <!-- Open Graph -->
  <meta property="og:type" content="{{ page.og_type | default: 'website' }}">
  <meta property="og:title" content="{{ page.title }}">
  <meta property="og:description" content="{{ page.description | default: site.description | truncate: 200 }}">
  <meta property="og:url" content="{{ page.url | absolute_url }}">
  <meta property="og:image" content="{{ page.image | default: site.default_image | absolute_url }}">
  <meta property="og:site_name" content="{{ site.title }}">
  <meta property="og:locale" content="ko_KR">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{{ page.title }}">
  <meta name="twitter:description" content="{{ page.description | truncate: 200 }}">
  <meta name="twitter:image" content="{{ page.image | default: site.default_image | absolute_url }}">
</head>
```

### 1.5 JSON-LD 구조화 데이터 — WebSite

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "{{ site.title }}",
  "url": "{{ site.url }}",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "{{ site.url }}/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
</script>
```

---

## 2. 콘텐츠 SEO

### 2.1 제목 최적화 공식

| 패턴 | 예시 |
|------|------|
| `[도구명] — [핵심기능] | 무료 온라인 도구` | `JSON Formatter — JSON 정리·검증 \| 무료 온라인 도구` |
| `[게임명]: [장르] 게임 — 브라우저에서 바로 플레이` | `Tower Defense: 전략 게임 — 브라우저에서 바로 플레이` |
| `[주제] — [구체적 내용] (2026)` | `Python 비동기 처리 — asyncio 완전 가이드 (2026)` |

**규칙:**
- 60자 이내 (한글 기준 30자)
- 핵심 키워드 앞배치
- 파이프(`|`) 또는 대시(`—`)로 구분
- 매 페이지 고유한 제목

### 2.2 Description 최적화

- 155자 이내 (한글 80자)
- 행동 유도 문구 포함 ("지금 바로", "무료로")
- 핵심 키워드 자연스럽게 1-2회 포함

### 2.3 키워드 리서치 패턴

```bash
# Google Autocomplete 크롤링 (Python)
import requests, json
def get_suggestions(keyword):
    url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={keyword}"
    return json.loads(requests.get(url).text)[1]

# 도구 키워드 확장
for tool in ["json formatter", "base64 encoder", "color picker"]:
    print(f"=== {tool} ===")
    print(get_suggestions(tool))
    print(get_suggestions(f"{tool} online"))
    print(get_suggestions(f"{tool} free"))
```

### 2.4 내부 링크 전략

- **도구 → 관련 도구:** "JSON Formatter를 찾으셨다면 [JSON Validator](/tools/json-validator)도 확인하세요"
- **블로그 → 도구:** 포스트 내에서 관련 도구 자연 링크
- **카테고리 허브:** 카테고리별 랜딩페이지가 하위 도구들을 모두 링크
- **Breadcrumb:** `홈 > 카테고리 > 도구명` 구조

---

## 3. 도구 페이지 SEO

### 3.1 도구 Front Matter 표준

```yaml
---
layout: tool
title: "JSON Formatter"
description: "JSON 데이터를 보기 좋게 정리하고 유효성을 검증하는 무료 온라인 도구"
category: developer
tags: [json, formatter, validator, developer-tools]
image: /assets/tools/json-formatter-og.png
priority: 0.8
changefreq: monthly
---
```

### 3.2 도구 JSON-LD (SoftwareApplication)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "{{ page.title }}",
  "description": "{{ page.description }}",
  "url": "{{ page.url | absolute_url }}",
  "applicationCategory": "{{ page.category | capitalize }}Tool",
  "operatingSystem": "Web Browser",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "author": {
    "@type": "Organization",
    "name": "{{ site.title }}",
    "url": "{{ site.url }}"
  }
}
</script>
```

### 3.3 카테고리 랜딩페이지 패턴

```html
---
layout: category
title: "개발자 도구 모음 — 무료 온라인 개발 유틸리티"
description: "JSON, Base64, URL 인코딩 등 개발에 필요한 도구를 브라우저에서 바로 사용하세요."
category: developer
---

<!-- BreadcrumbList JSON-LD -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "홈", "item": "{{ site.url }}"},
    {"@type": "ListItem", "position": 2, "name": "개발자 도구", "item": "{{ page.url | absolute_url }}"}
  ]
}
</script>

<!-- ItemList for category tools -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "{{ page.title }}",
  "itemListElement": [
    {% for tool in site.tools | where: "category", page.category %}
    {
      "@type": "ListItem",
      "position": {{ forloop.index }},
      "url": "{{ tool.url | absolute_url }}",
      "name": "{{ tool.title }}"
    }{% unless forloop.last %},{% endunless %}
    {% endfor %}
  ]
}
</script>
```

### 3.4 도구 메타 자동 생성 스크립트

```python
#!/usr/bin/env python3
"""도구 페이지 메타태그 일괄 생성/검증"""
import os, yaml, re
from pathlib import Path

TOOLS_DIR = Path("_tools")  # or tools/
REQUIRED = ["title", "description", "category", "tags"]

def audit_tools():
    issues = []
    for f in TOOLS_DIR.glob("*.md"):
        content = f.read_text()
        fm = yaml.safe_load(content.split("---")[1])
        for field in REQUIRED:
            if field not in fm or not fm[field]:
                issues.append(f"❌ {f.name}: missing '{field}'")
        if fm.get("description") and len(fm["description"]) > 160:
            issues.append(f"⚠️  {f.name}: description > 160 chars ({len(fm['description'])})")
        if fm.get("title") and len(fm["title"]) > 60:
            issues.append(f"⚠️  {f.name}: title > 60 chars")
    return issues

if __name__ == "__main__":
    for issue in audit_tools():
        print(issue)
```

---

## 4. 게임 페이지 SEO

### 4.1 게임 JSON-LD (Game + VideoGame Schema)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "VideoGame",
  "name": "{{ page.title }}",
  "description": "{{ page.description }}",
  "url": "{{ page.url | absolute_url }}",
  "image": "{{ page.screenshot | absolute_url }}",
  "genre": "{{ page.genre }}",
  "gamePlatform": ["Web Browser", "Mobile Browser"],
  "applicationCategory": "Game",
  "operatingSystem": "Any",
  "playMode": "{{ page.play_mode | default: 'SinglePlayer' }}",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "author": {
    "@type": "Organization",
    "name": "EastSea Games",
    "url": "https://games.eastsea.xyz"
  }
  {% if page.rating %},
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "{{ page.rating }}",
    "ratingCount": "{{ page.rating_count }}",
    "bestRating": "5",
    "worstRating": "1"
  }
  {% endif %}
}
</script>
```

### 4.2 게임 스크린샷 최적화

```html
<!-- 모든 스크린샷에 의미있는 alt 텍스트 -->
<img src="/games/tower-defense/screenshot-1.webp"
     alt="Tower Defense 게임 — 3라운드 보스전 화면, 타워 배치 전략"
     width="800" height="450" loading="lazy">
```

**alt 텍스트 규칙:**
- `게임명 — 구체적 장면 설명` 형식
- 키워드 자연 포함
- 125자 이내

### 4.3 게임 Front Matter

```yaml
---
layout: game
title: "Tower Defense — 무료 전략 타워 디펜스 게임"
description: "브라우저에서 바로 플레이하는 무료 타워 디펜스. 50개 스테이지, 다양한 타워 조합 전략."
genre: Strategy
play_mode: SinglePlayer
screenshot: /games/tower-defense/og-image.png
tags: [tower-defense, strategy, free-game, browser-game]
priority: 0.7
---
```

---

## 5. 블로그 SEO

### 5.1 포스트 JSON-LD (Article)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{{ page.title }}",
  "description": "{{ page.description }}",
  "image": "{{ page.image | absolute_url }}",
  "datePublished": "{{ page.date | date_to_xmlschema }}",
  "dateModified": "{{ page.last_modified_at | default: page.date | date_to_xmlschema }}",
  "author": {
    "@type": "Person",
    "name": "{{ page.author | default: site.author }}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "{{ site.title }}",
    "logo": {
      "@type": "ImageObject",
      "url": "{{ site.logo | absolute_url }}"
    }
  },
  "mainEntityOfPage": "{{ page.url | absolute_url }}"
}
</script>
```

### 5.2 시리즈 링크

```html
{% if page.series %}
<nav class="series-nav" aria-label="시리즈 네비게이션">
  <h3>📚 {{ page.series }} 시리즈</h3>
  <ol>
  {% assign series_posts = site.posts | where: "series", page.series | sort: "series_order" %}
  {% for post in series_posts %}
    <li {% if post.url == page.url %}class="current"{% endif %}>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
  </ol>
</nav>
{% endif %}
```

### 5.3 Breadcrumb

```html
<nav aria-label="breadcrumb">
  <ol itemscope itemtype="https://schema.org/BreadcrumbList">
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a itemprop="item" href="/"><span itemprop="name">홈</span></a>
      <meta itemprop="position" content="1">
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a itemprop="item" href="/blog/"><span itemprop="name">블로그</span></a>
      <meta itemprop="position" content="2">
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <span itemprop="name">{{ page.title }}</span>
      <meta itemprop="position" content="3">
    </li>
  </ol>
</nav>
```

---

## 6. 성과 측정

### 6.1 Google Search Console 연동

1. `<meta name="google-site-verification" content="YOUR_CODE">` 추가
2. sitemap.xml 제출: Search Console → Sitemaps → URL 입력
3. 색인 상태 모니터링: 커버리지 리포트 주간 체크

### 6.2 Core Web Vitals 최적화 (GitHub Pages)

```html
<!-- 이미지 최적화: WebP + lazy loading -->
<img src="image.webp" alt="설명" width="800" height="450"
     loading="lazy" decoding="async">

<!-- CSS 인라인 (Critical Path) -->
<style>/* 첫 화면에 필요한 최소 CSS */</style>
<link rel="preload" href="/assets/css/main.css" as="style"
      onload="this.onload=null;this.rel='stylesheet'">

<!-- JS defer -->
<script src="/assets/js/app.js" defer></script>

<!-- 폰트 최적화 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

### 6.3 추적 체크리스트

```checklist
- [ ] Google Search Console 등록 및 sitemap 제출
- [ ] 색인된 페이지 수 vs 실제 페이지 수 비교
- [ ] 404 에러 페이지 목록 → 리다이렉트 또는 수정
- [ ] Core Web Vitals: LCP < 2.5s, FID < 100ms, CLS < 0.1
- [ ] 모바일 사용성 오류 0건
- [ ] 주간: 상위 검색어, 클릭률(CTR), 평균 게재순위 기록
```

---

## 7. SEO 감사 자동화

### 7.1 빠진 Meta Tag 감지

```bash
#!/bin/bash
# seo-audit.sh — 빌드된 HTML에서 SEO 필수 요소 검증
SITE_DIR="${1:-./_site}"

echo "=== SEO Audit: $SITE_DIR ==="

find "$SITE_DIR" -name "*.html" | while read f; do
  rel="${f#$SITE_DIR}"

  # title 태그 체크
  if ! grep -q '<title>' "$f"; then
    echo "❌ MISSING <title>: $rel"
  fi

  # meta description 체크
  if ! grep -q 'name="description"' "$f"; then
    echo "❌ MISSING meta description: $rel"
  fi

  # canonical 체크
  if ! grep -q 'rel="canonical"' "$f"; then
    echo "⚠️  MISSING canonical: $rel"
  fi

  # og:title 체크
  if ! grep -q 'og:title' "$f"; then
    echo "⚠️  MISSING og:title: $rel"
  fi

  # og:image 체크
  if ! grep -q 'og:image' "$f"; then
    echo "⚠️  MISSING og:image: $rel"
  fi

  # JSON-LD 체크
  if ! grep -q 'application/ld+json' "$f"; then
    echo "⚠️  MISSING JSON-LD: $rel"
  fi

  # img alt 체크
  if grep -qP '<img[^>]+(?!alt=)' "$f" 2>/dev/null; then
    count=$(grep -cP '<img(?![^>]*alt=)' "$f" 2>/dev/null || echo 0)
    [ "$count" -gt 0 ] && echo "⚠️  $count img(s) without alt: $rel"
  fi
done

echo "=== Audit Complete ==="
```

### 7.2 Broken Link 체크

```bash
#!/bin/bash
# broken-links.sh — 내부 링크 검증
SITE_DIR="${1:-./_site}"
ERRORS=0

grep -roh 'href="/[^"]*"' "$SITE_DIR" | sort -u | while read link; do
  path=$(echo "$link" | sed 's/href="//;s/"//')
  # 앵커 제거
  path="${path%%#*}"
  # 쿼리스트링 제거
  path="${path%%\?*}"

  target="$SITE_DIR$path"
  if [ ! -f "$target" ] && [ ! -f "${target}index.html" ] && [ ! -d "$target" ]; then
    echo "🔗 BROKEN: $path"
    ERRORS=$((ERRORS + 1))
  fi
done

echo "Total broken links: $ERRORS"
```

### 7.3 Python 통합 감사 스크립트

```python
#!/usr/bin/env python3
"""seo_audit.py — 종합 SEO 감사"""
from pathlib import Path
from bs4 import BeautifulSoup
import sys

def audit_html(filepath: Path) -> list[str]:
    issues = []
    soup = BeautifulSoup(filepath.read_text(), "html.parser")
    rel = str(filepath)

    # Title
    title = soup.find("title")
    if not title or not title.string:
        issues.append(f"❌ No <title>: {rel}")
    elif len(title.string) > 60:
        issues.append(f"⚠️  Title > 60 chars: {rel}")

    # Meta description
    desc = soup.find("meta", attrs={"name": "description"})
    if not desc or not desc.get("content"):
        issues.append(f"❌ No meta description: {rel}")
    elif len(desc["content"]) > 160:
        issues.append(f"⚠️  Description > 160 chars: {rel}")

    # Canonical
    if not soup.find("link", attrs={"rel": "canonical"}):
        issues.append(f"⚠️  No canonical: {rel}")

    # Open Graph
    for og in ["og:title", "og:description", "og:image"]:
        if not soup.find("meta", attrs={"property": og}):
            issues.append(f"⚠️  No {og}: {rel}")

    # Images without alt
    for img in soup.find_all("img"):
        if not img.get("alt"):
            issues.append(f"⚠️  img without alt: {rel} → {img.get('src', '?')[:50]}")

    # JSON-LD
    if not soup.find("script", attrs={"type": "application/ld+json"}):
        issues.append(f"⚠️  No JSON-LD: {rel}")

    return issues

if __name__ == "__main__":
    site_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
    all_issues = []
    for html in site_dir.rglob("*.html"):
        all_issues.extend(audit_html(html))

    for issue in sorted(all_issues):
        print(issue)
    print(f"\n📊 Total issues: {len(all_issues)}")
```

---

## 빠른 참조: GitHub Pages SEO 제약

| 가능 | 불가능 |
|------|--------|
| HTML `<head>` 메타태그 | `.htaccess` / 서버 리다이렉트 |
| 정적 sitemap.xml, robots.txt | 동적 sitemap 생성 |
| JSON-LD 구조화 데이터 | 서버사이드 렌더링 |
| 클라이언트 JS 리다이렉트 | HTTP 헤더 커스텀 |
| `<link rel="canonical">` | `X-Robots-Tag` 헤더 |
| WebP 이미지 제공 | 이미지 CDN 변환 |
| GitHub Actions로 빌드 시 최적화 | 엣지 서버 설정 |

**리다이렉트 대안:** `<meta http-equiv="refresh" content="0; url=/new-path">` + JS `window.location`
