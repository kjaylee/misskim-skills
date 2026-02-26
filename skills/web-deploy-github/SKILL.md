---
name: web-deploy-github
description: Create and deploy single-page static websites to GitHub Pages with autonomous workflow. Use when building portfolio sites, CV pages, landing pages, or any static web project that needs GitHub Pages deployment. Handles complete workflow from project initialization to live deployment with GitHub Actions automation.
---

# Web Deploy GitHub Pages

## When to Use This vs Others
- **Use this (`web-deploy-github`)** when the goal is repository setup, GitHub Actions, and GitHub Pages deployment to a live URL.
- **Use `web-bundling`** when the core need is packaging the app/game into a single distributable HTML artifact.
- For single-file site distribution, run `web-bundling` first, then `web-deploy-github` for hosting.


## Overview

This skill enables autonomous creation and deployment of static websites to GitHub Pages. It follows a complete workflow from project structure initialization through automatic deployment via GitHub Actions, optimized for single-page applications, portfolios, and landing pages.

## Core Workflow

### 1. Project Initialization

Create the project structure:

```bash
bash scripts/init_project.sh <project-name>
```

This creates:
```
project-name/
├── index.html
├── styles.css
├── script.js
├── README.md
└── .github/
    └── workflows/
        └── deploy.yml
```

### 2. Development

Build the website following these principles:
- **Single-page first**: Optimize for one-page layouts unless multiple pages explicitly required
- **Autonomous generation**: Generate complete, production-ready code without placeholders
- **Modern design**: Use modern CSS (flexbox, grid), responsive design, clean aesthetics
- **No dependencies**: Pure HTML/CSS/JS when possible, CDN links if frameworks needed

Use templates from `assets/templates/` as starting points:
- `base-html/` - Minimal HTML5 boilerplate
- `portfolio/` - Portfolio/CV template with sections
- `landing/` - Landing page with hero and CTA

### 3. GitHub Repository Setup

```bash
bash scripts/deploy_github_pages.sh <project-name> <github-username>
```

This script:
1. Initializes git repository
2. Creates GitHub repository via GitHub CLI
3. Configures GitHub Pages settings
4. Pushes initial commit
5. Triggers first deployment

### 4. Deployment

GitHub Actions automatically deploys on push to main branch. The workflow:
- Checks out code
- Deploys to `gh-pages` branch
- Makes site live at `https://<username>.github.io/<project-name>/`

## Architecture Guidelines

### HTML Structure
- Semantic HTML5 elements
- Meta tags for SEO and social sharing
- Responsive viewport configuration
- Favicon and icons

### CSS Design
- Mobile-first responsive design
- CSS variables for theming
- Flexbox/Grid for layouts
- Smooth transitions and animations
- Dark mode support when appropriate

### JavaScript
- Vanilla JS preferred
- Progressive enhancement
- Event delegation
- No console errors

### Performance
- Optimized images
- Minified assets for production
- Lazy loading where appropriate
- Fast initial load time

## Quick Examples

### Example 1: Portfolio CV Site
**User request:** "Crée-moi un site portfolio CV"

**Action:**
1. Run `init_project.sh portfolio-cv`
2. Use `assets/templates/portfolio/` as base
3. Generate complete HTML with sections: Hero, About, Skills, Projects, Contact
4. Deploy with `deploy_github_pages.sh portfolio-cv username`

### Example 2: Landing Page
**User request:** "Fais-moi une landing page pour mon app"

**Action:**
1. Run `init_project.sh app-landing`
2. Use `assets/templates/landing/` as base
3. Generate with Hero, Features, Pricing, CTA
4. Deploy with `deploy_github_pages.sh app-landing username`

## Troubleshooting

### GitHub Pages Not Deploying
- Check repository Settings → Pages → Source is set to `gh-pages` branch
- Verify GitHub Actions workflow ran successfully
- Check DNS propagation (can take 5-10 minutes)

### Permission Errors
- Ensure `gh` CLI is authenticated: `gh auth status`
- Check repository permissions on GitHub

### Build Failures
- Review Actions logs in repository
- Verify `.github/workflows/deploy.yml` syntax
- Check file paths and references

## Resources

### scripts/
- `init_project.sh` - Initialize project structure
- `deploy_github_pages.sh` - Deploy to GitHub Pages

### references/
- `workflow.md` - Detailed workflow documentation
- `design-patterns.md` - Design best practices

### assets/
- `templates/base-html/` - Minimal HTML5 boilerplate
- `templates/portfolio/` - Portfolio/CV template
- `templates/landing/` - Landing page template
- `.github/workflows/deploy.yml` - GitHub Actions workflow template

## Guardrails

- **배포 전 git status 클린 확인 필수** — uncommitted changes나 untracked 파일이 있으면 배포 중단. `git status` 결과가 clean인지 확인 후 진행.
- **민감 정보 커밋 금지** — API 키, 토큰, 비밀번호를 소스에 포함하면 안 됨. 배포 전 `.gitignore` 점검 및 `git log --diff-filter=A -- '*.env'` 등으로 시크릿 파일 유입 차단.
- **빌드 실패 시 롤백 절차** — GitHub Actions 워크플로우 실패 시 이전 커밋 SHA로 `git revert` 또는 `gh run rerun` 전에 롤백 브랜치 확인. `gh-pages` 브랜치 마지막 정상 커밋을 force-push하여 복원.
- **CNAME/DNS 변경 전 확인 필수** — 커스텀 도메인 설정 또는 CNAME 파일 수정 시 Master에게 확인. DNS 전파 지연(최대 48시간)으로 서비스 중단 가능성 있음.
