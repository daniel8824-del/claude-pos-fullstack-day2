# Day 2 실습 자료 — POS 상권분석 풀스택 5단계

> 2026-05-13 (수) 09:00~12:30 강의 실습용.
> 데이터 로더 → 분석 → 차트 → 검수 → 보안 → 배포까지 풀스택 한 사이클.

---

## 파일 목록

| 파일 | 용도 |
|---|---|
| `README.md` | 본 문서 (실습 안내) |
| `generate_pos_data.py` | POS 가상 데이터 생성 스크립트 |
| `pos_data.csv` | 거래 데이터 205건 (정상 200 + 이상 5) |
| `starter.html` | Phase 0 시작 코드 (학생 출발점) |

---

## 사전 준비 (강의 시작 전)

### 1. 데이터 확인

```bash
# pos_data.csv가 없으면 생성
python3 generate_pos_data.py

# 결과 확인
head pos_data.csv
# timestamp,terminal_id,category,amount,payment_method
# 2026-05-12T08:03:21,T07,식음료,8500,카드
# ...
```

### 2. starter.html 미리 열기

```bash
# 브라우저에서 starter.html 열기
# (Phase 1·2·3·4 placeholder가 보이면 정상)
```

### 3. Claude Code 작동 확인

```bash
cd 실습자료/Day2
claude
# Claude Code가 디렉토리 인식 확인
```

---

## 풀스택 5+1단계 실습 흐름

```
Phase 0 — 외부 자료 리서치  (6차시 09:12-09:25, 강사 시연만)
              ↓ Naver / Brave / firecrawl / 공공데이터 / sg.sbiz.or.kr
Phase 1 — 데이터 로더        (6차시 09:35-09:45)
   ↓
Phase 2 — 분석 함수          (6차시 09:45-09:55)
   ↓
Phase 3 — 차트·검수          (7차시 10:25-10:45)
   ↓
Phase 4 — 보안 검수          (8차시 11:20-11:35)
   ↓
Phase 5 — GitHub Pages       (8차시 11:35-11:55)
```

> **Phase 0 (외부 자료 리서치)**: 본 실습은 가상 데이터로 진행. Phase 0는 강사가 시연만 — 실제 외부 데이터 수집 흐름을 학생들에게 보여줌. 학생 본인 도메인 적용은 차주 과제.

각 Phase는 약 10~20분. Claude Code 프롬프트 1~2개로 자동 진행됩니다.

---

## Phase 0 — 외부 자료 리서치 (6차시, 강사 시연)

> 본 실습은 가상 데이터 `pos_data.csv` 사용. Phase 0는 "실전에서 외부 자료를 어떻게 수집하는가" 시연용.

### 5가지 수집 도구

| 도구 | 용도 | 비용 |
|---|---|---|
| `blog-collector` (Naver) | 한국어 상권 블로그·뉴스 | 무료 (API 키) |
| Brave Search MCP | 글로벌 웹 검색 | 유료 구독 |
| firecrawl MCP | URL 본문 추출 | 유료 구독 |
| 공공 데이터 (data.go.kr) | 정부 공식 통계 | 무료 (API 키) |
| 소상공인 상권분석 (sg.sbiz.or.kr) | 실제 상권 데이터 | 무료 |

### 강사 시연 프롬프트

```text
# 1. Naver 블로그 30개 수집
> /blog-collector "강남역 카페 상권 2026" 30개 수집해줘.

# 2. Brave 글로벌 동향
> 최근 1개월 POS 상권 데이터 트렌드 검색해줘.

# 3. 공공 데이터 API 탐색
> data.go.kr에서 카드 사용 통계 API 찾고 호출 예시 보여줘.

# 4. 소상공인 상권 페이지 추출
> sg.sbiz.or.kr 상권분석 페이지 firecrawl로 분석해줘.
```

### Tier 게이트 원칙

```
Tier 1  세션 내 (이미 가진 데이터)    무비용
Tier 2  사내 vault (QMD)              무비용
Tier 3  외부 API (Naver/Brave/...)    [비용 발생]

→ Tier 3 진입 전 Tier 2 통과
→ 사내 자료가 쌓이면 외부 호출 점점 줄어듦
```

### 학생 차주 과제 (선택)

본인 POS 매장 주변 상권 데이터를 위 도구로 수집 → Day 3 RAG 실습에 활용.

---

## Phase 1 — 데이터 로더 (6차시)

### Claude Code 프롬프트

```
실습자료/Day2/pos_data.csv를 읽어서 JavaScript 배열로 파싱하는
함수를 starter.html에 추가해.

요구사항:
- fetch로 CSV 가져오기
- split + map으로 객체 배열 변환
- 컬럼: timestamp, terminal_id, category, amount, payment_method
- amount는 정수로 변환
- 결과는 window.posData에 저장 (다른 Phase에서 사용)
```

### 검증

```js
// 브라우저 콘솔에서
console.log(posData.length);  // 205
console.log(posData[0]);      // { timestamp: "...", ... }
```

---

## Phase 2 — 분석 함수 (6차시)

### Claude Code 프롬프트

```
파싱된 posData 배열에서 다음 3가지 분석 함수를 추가해:

1. analyzeHourly(data): 시간대별 매출 합계 (객체: {8: 12000, 9: 25000, ...})
2. analyzeCategory(data): 카테고리별 거래 건수 (객체)
3. detectAnomaly(data): 동일 단말 1초 내 중복 결제 배열 반환

분석 결과를 화면 상단 .stats 박스에 표시 (총 거래·총 매출·이상·피크 시간).
```

### 검증

```js
console.log(analyzeHourly(posData));
// { 8: 45000, 9: 67000, ..., 18: 89000 }

console.log(detectAnomaly(posData));
// [{ timestamp: "...", terminal_id: "T05", ... }, ...] (5건)
```

---

## Phase 3 — 차트·검수 (7차시)

### Claude Code 프롬프트 (차트)

```
Chart.js로 두 가지 차트 추가:
1. 시간대별 매출 (Line chart, X축: 8-21시)
2. 카테고리 분포 (Doughnut chart)

각각 canvas#chart-hourly · canvas#chart-category 사용.
```

### Claude Code 프롬프트 (검수 — 만화 ⑥)

```
/ask codex "starter.html의 Phase 1·2·3 코드를 리뷰해줘.
보안·성능·가독성 관점에서 개선점 3가지."
```

### Claude Code 프롬프트 (리팩토링)

```
/simplify

→ 3개 리뷰 에이전트 (재사용성·품질·효율성) 병렬 자동 개선
```

---

## Phase 4 — 보안 검수 (8차시)

### Claude Code 프롬프트 (만화 ⑦)

```
/security-review starter.html

체크 대상:
- XSS (innerHTML 사용 여부)
- CSRF (외부 요청 처리)
- 데이터 검증 (CSV 파싱 시 escape)
```

→ 발견된 이슈를 Claude Code가 자동 수정.

### 이상 거래 테이블 추가

```
Phase 2의 detectAnomaly() 결과를 #anomaly-table tbody에 렌더링.
각 행에 class="anomaly-row" 추가하여 노란색 배경.
```

---

## Phase 5 — GitHub Pages 배포 (8차시)

### 단계

```bash
# 1. Git 초기화
git init -b main

# 2. .gitignore 생성
> Node.js + 정적 사이트용 .gitignore 만들어줘

# 3. 첫 커밋 (Claude Code 자동 검수)
/smart-commit

# 4. GitHub repo 생성 + push
gh repo create pos-analyzer-day2 --public --source . --push

# 5. GitHub Pages 활성화
gh api -X POST repos/{your-username}/pos-analyzer-day2/pages \
  -f 'source[branch]=main'

# 6. 3분 후 라이브
# https://{your-username}.github.io/pos-analyzer-day2/
```

### 라이브 URL 공유

강의 끝나면 본인 라이브 URL을 슬랙에 공유.
강사가 30명 모든 학생 결과 확인 → 우수 사례 1-2개 발표.

---

## 데이터 분포 참고

```
총 205건 = 정상 200 + 이상 5

시간대 분포 (점심·저녁 피크):
  08-09시  3-4%
  12-13시  8-9% ← 점심 피크
  18-19시  9% ← 저녁 피크
  20-21시  3-5%

카테고리 분포:
  식음료    40%
  생필품    25%
  잡화      15%
  의류      10%
  디지털    10%

결제 분포:
  카드      60%
  모바일    25%
  현금      15%

이상 거래 5건:
  동일 단말 + 1초 차이 + 동일 금액
  Phase 2의 detectAnomaly()가 찾아내야 할 케이스
```

---

## 문제 해결 FAQ

### Q. CSV가 fetch에서 CORS 에러

```
A. starter.html을 file:// 로 직접 열면 fetch가 막힙니다.
   해결: python3 -m http.server 8000 후 localhost:8000으로 접속.
   또는 VS Code Live Server 확장 사용.
```

### Q. Claude Code가 starter.html을 못 찾음

```
A. cd 실습자료/Day2 디렉토리 진입 후 claude 실행 확인.
   현재 디렉토리는 /pwd 명령으로 확인.
```

### Q. /security-review 명령이 없음

```
A. gstack 플러그인 미설치. superpowers만 설치된 경우:
   /plugin marketplace add garrytan/gstack
   /plugin install gstack
   (Day 3에서 본격 사용)
```

### Q. GitHub Pages 배포 후 차트 안 보임

```
A. CSV 경로가 상대경로(./pos_data.csv)인지 확인.
   GitHub Pages는 /{repo-name}/ 경로라 절대경로 사용 시 깨짐.
```

---

## 강의 후 확장 과제 (선택)

```
1. 데이터 100건 더 추가 → generate_pos_data.py 수정
2. 새 분석 함수 추가 (예: 결제수단별 평균 금액)
3. 차트 종류 추가 (예: 단말별 매출 막대)
4. 다크 모드 토글
5. CSV 업로드 기능 (파일 선택해서 분석)
```

---

**v1 · 2026-05-12 (강의 1일 전 사전 배포)**
