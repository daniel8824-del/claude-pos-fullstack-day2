# claude-pos-fullstack-day2

**Day 2 — 하네스 5대 요소 + Superpowers 풀스택 5단계** · 강의 사전 배포 사이트

라이브: <https://daniel8824-del.github.io/pos-day2/>

---

## 본 페이지의 자료

- 학습 만화 8컷 (셰프 Claude 식당 메타포)
- hyperframes 도입 영상 **3개** (60초 × 3 — ① 하네스 5요소 / ② QMD / ③ LLM 위키)
- POS 가상 데이터 410건 (SAP IBP 9컬럼, 정상 400 + 이상 10건 — 5종 카테고리 각 2건)
- 4차시 강의 흐름 (60+90+60+60 = 270분)
- 하네스 5대 요소 (**CLAUDE.md · MCP · Skills · Hooks · Memory**) — Karpathy/martinfowler/OpenAI Codex 정의 정합
- 대표 플러그인 3종 (Superpowers · gstack · oh-my-claudecode) · 각 5+ 스킬
- Superpowers 풀스택 5단계 워크플로우 (PLAN · DEV · VERIFY · REFACTOR · SECURITY)
- 조직 맞춤 SKILL.md 작성 워크숍 (자유 그룹 토론 + 발표)
- 무료 지식그래프 도구 8선 비교 (학생 선택 가이드)
- LLM 위키 (Karpathy 패턴 — raw/wiki/schema 3계층, ingest/query/lint 3 작업)
- 전통 POS → AI-Ops 전환 5단계 로드맵
- §Copilot 대응 매핑 (강사 Claude Code 시연 / 수강생 본인 Copilot 적용)
- 4개념 박스: CLI 에이전트 · 하네스 엔지니어링 · Plan-first · 프롬프트 캐싱
- 학생 다운로드: pos_data.csv 1개 (UTF-8 BOM)

## 강의 정보

- **일시**: 2026-05-13 (수) 08:00 ~ 12:30
- **분량**: 270분 (4시차 60+90+60+60)
- **청중**: 아모레퍼시픽 + 도시바코리아 직원 15~20명 (Copilot 6개월 베테랑 + 비개발자 5인 포함)
- **핵심 톤**: eli5 + 만화 + 실습 우선

## 4차시 구조

| 차시 | 시간 | 주제 |
|---|---|---|
| 5차시 | 08:00 ~ 09:00 (60분) | 하네스 엔지니어링 + 5대 요소 + context7 · Superpowers 설치 |
| 6차시 | 09:00 ~ 10:30 (90분) | Superpowers로 POS 분석 앱 만들기 (풀스택 5단계) |
| 7차시 | 10:30 ~ 11:30 (60분) | 조직 맞춤 SKILL.md 토론·제작 + 발표 |
| 8차시 | 11:30 ~ 12:30 (60분) | QMD · LLM 위키 · 지식그래프 8선 · AI-Ops 안내 + Day 3 예고 |

## 본 repo 구조

```
docs/
├── _config.yml         Jekyll 설정 (kramdown GFM + permalink /:basename)
├── _layouts/default.html  공통 레이아웃 (claude-harness-catalog 정합)
├── index.html          메인 페이지 (한 장 요약)
├── images/comics/      만화 8컷 + v1-imagen4 백업
├── videos/             hyperframes 영상 2개 (mp4)
└── downloads/          학생 다운로드 실습 7종 + 전체 zip
```

## 이어지는 hub

- [claude-harness-catalog](https://daniel8824-del.github.io/claude-harness-catalog/) — 어제 Day 1 자료
- [claude-skill-catalog](https://daniel8824-del.github.io/claude-skill-catalog/) — 134 스킬
- [claude-wiki-verbs](https://daniel8824-del.github.io/claude-wiki-verbs/) — 9-verb 위키
- [claude-feynman-research-skill](https://daniel8824-del.github.io/claude-feynman-research-skill/) — 출처 검증 리서치
