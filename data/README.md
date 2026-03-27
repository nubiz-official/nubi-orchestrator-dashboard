# TeamNubiz 프로젝트 허브

> **최종 업데이트**: 2026-03-23
> **관리자**: 최낙의 대표 (nick.choi@teamnubiz.co.kr)

---

## 회사 개요

| 항목 | 내용 |
|------|------|
| 회사명 | (주)누비즈 (TeamNubiz) |
| 도메인 | teamnubiz.com (후이즈 관리) |
| 메일 | @teamnubiz.co.kr (다우오피스, Resend 연동) |
| GitHub | github.com/nubiz-official |
| 배포 | Railway (서비스), Vercel (홈페이지) |
| DB | PostgreSQL (Railway) |
| AI | Claude API, OpenAI API, LangChain |

---

## 프로젝트 전체 현황

### 운영 중 서비스 (Railway 배포, 10개)

| 상태 | 서비스 | URL | 설명 | 기술 |
|------|--------|-----|------|------|
| :green_circle: | **nubiz-web** | teamnubiz.com | 공식 홈페이지 + 서비스 플랫폼 | Next.js 16 / React 19 |
| :green_circle: | **nubi-scout** | scout.teamnubiz.com | 정부지원사업 수집 + 스타트업 매칭 | Streamlit + PostgreSQL |
| :green_circle: | **patent-scout** | patent.teamnubiz.com | 청구항 기반 경쟁사 침해 탐지 | Streamlit + PostgreSQL |
| :green_circle: | **kfia-demo** | kfia.teamnubiz.com | KFIA 소비기한 데모 | Streamlit |
| :green_circle: | **ip-nft-hub** | ipnft.teamnubiz.com | IP-NFT 허브 | Streamlit + Plotly |
| :green_circle: | **smartbell-demo** | smartbell.teamnubiz.com | SmartBell 데모 | Streamlit + Plotly |
| :green_circle: | **voice-translator** | translator.teamnubiz.com | 음성 번역기 (APK 다운로드) | Streamlit |
| :green_circle: | **multilang-hotel** | hotel.teamnubiz.com | 다국어 호텔 | Streamlit + Plotly |
| :green_circle: | **physical-ai** | ai.teamnubiz.com | Physical AI 분석 | Streamlit + Plotly |
| :green_circle: | **DB x2** | (내부) | nuscout_db + patentscout_db | Railway PostgreSQL |

### 클라이언트 대시보드 (비배포, 13개)

제안/수주 목적으로 제작한 분석 대시보드. `services/` 내 위치.

| 분야 | 서비스 | 관련 클라이언트 |
|------|--------|---------------|
| **노화산업** | aging-research-center | 광주 노화산업 실증센터 |
| **노화산업** | aging-research-dashboard | 노화 연구 데이터 분석 |
| **노화산업** | illowa-dashboard | 일로와 리뷰 분석 |
| **임상/의료** | hwasun-clinical-dashboard | 화순전남대 암특화 임상시험 |
| **임상/의료** | hwasun-maxorganoid | 화순전남대 맥스오거나이드 |
| **임상/의료** | gist-care-dashboard | 광주과학기술원 노화혁신 |
| **AI/로봇** | ai-다기능로봇-간호업무지원-dashboard | 다기능로봇 간호업무 |
| **AI/경제** | ai-agent-economy-dashboard | AI 에이전트 경제 분석 |
| **특허/블록체인** | nubiz-blockchain-patent-dashboard | 누비즈 블록체인 특허 |
| **연구** | nubiz-yeongu | 연구병행의사 분석 |
| **스타트업** | pocket-company-feasibility | 포켓컴퍼니 타당성 |
| **국가과제** | 김형석-과기부-RFP | 과기부 RFP 분석 |

### 진행 중 프로젝트 (국고사업/신규)

| 상태 | 프로젝트 | 사업비 | 기간 | 핵심 산출물 |
|------|---------|--------|------|-----------|
| :large_blue_circle: 설계중 | **광주 AI 노화산업 실증센터 건축관리플랫폼 (ACMS)** | 378억 (센터전체) | 2026~2030 | 건축통합관리시스템 |
| :large_blue_circle: 참여중 | **광주 AX 실증밸리** (AI 2단계) | 6,000억 (전체) | 2026~2030 | 헬스케어 실증 연계 |
| :yellow_circle: 대기 | **우주의학/오가노이드 국고 건의** | 미정 | 2027~ | 27년 국고 건의 사업 조서 |
| :yellow_circle: 대기 | **3-Way Hybrid 에스테틱 특허** | - | - | 특허 분석 |

### AI 에이전트 시스템

| 모듈 | 파일 | 설명 |
|------|------|------|
| Orchestrator | agents/nubiz_agent.py | 메인 에이전트 (의뢰 자동 처리) |
| 고객 수집 | agents/intake_app.py | 고객 의뢰 수집 앱 |
| 리뷰 분석 | agents/yanolja_review.py | 야놀자 리뷰 분석 |

---

## 디렉토리 구조 가이드

```
d:\nubiz_project\
│
├── _hub/                     ★ 여기! 프로젝트 허브
│   ├── README.md             ← 이 파일 (전체 현황)
│   └── decisions/            ← 주요 의사결정 기록
│
├── services/                 ★ 운영 서비스 + 클라이언트 대시보드
│   ├── nubiz-web/            ← 홈페이지 (Next.js)
│   ├── nubi-scout/           ← NuBI Scout (Streamlit)
│   ├── patent-scout/         ← Patent Scout (Streamlit)
│   └── ...                   ← 그 외 대시보드 22개
│
├── clients/                  ★ 클라이언트별 원본 자료/분석 데이터
│   ├── 2026-03-노화산업센터/
│   ├── 2026-03-화순전남대_맥스오거나이드/
│   └── ...                   ← 24개 클라이언트 폴더
│
├── agents/                   ★ AI 에이전트 시스템
│   ├── nubiz_agent.py
│   └── intake_app.py
│
├── shared/                   ★ 공용 코드
│   ├── auth.py               ← 인증
│   ├── config.py             ← DB/API 설정
│   ├── css_theme.py          ← Streamlit 테마
│   ├── deploy.py             ← 배포 유틸
│   └── sidebar.py            ← 공통 사이드바
│
├── templates/                ★ 템플릿
│   ├── analysis-report/      ← 분석 보고서
│   └── streamlit-dark/       ← Streamlit 다크 테마
│
├── 누비즈기술자료/            ★ 내부 기술 문서 (Postmortem, 사업조서 등)
│
├── _archive/                 ★ 완료/보류 프로젝트 (24개)
│   ├── 0219~ 날짜별 자료
│   ├── patent-scout-v1.0     ← 레거시 버전
│   ├── 영국_CAT_Smartbell    ← 완료 프로젝트
│   └── ...
│
├── .env                      ※ 환경변수 (git 제외, 절대 공유 금지)
└── .gitignore
```

### 폴더 사용 규칙

| 상황 | 어디에 넣을까? |
|------|--------------|
| 새 서비스/대시보드 개발 | `services/서비스명/` |
| 클라이언트 원본 자료 (PDF, 데이터) | `clients/YYYY-MM-클라이언트명/` |
| 국고사업 보고서/계획서 | `clients/해당프로젝트/docs/` 또는 루트에 명확한 파일명 |
| 완료된 프로젝트 | `_archive/`로 이동 |
| 주요 결정 사항 기록 | `_hub/decisions/YYYY-MM-주제.md` |
| 공용 코드 수정 | `shared/` |
| 내부 기술 문서 | `누비즈기술자료/` |

---

## 인프라 현황

### DNS (teamnubiz.com, 후이즈)

| 서브도메인 | Railway 앱 | 서비스 |
|-----------|-----------|--------|
| @ | x3kp4kan.up.railway.app | 홈페이지 |
| www | 9a23ygkb.up.railway.app | 홈페이지 |
| scout | qnaeiukc.up.railway.app | NuBI Scout |
| patent | ih2g4azo.up.railway.app | Patent Scout |
| kfia | qvopootm.up.railway.app | KFIA |
| ipnft | 61oggbwp.up.railway.app | IP-NFT Hub |
| smartbell | txe4mlt0.up.railway.app | SmartBell |
| translator | 1w2pnmv3.up.railway.app | 음성번역기 |
| hotel | b7lqcd3a.up.railway.app | 다국어호텔 |
| ai | pnc6eefs.up.railway.app | Physical AI |

### DB (Railway PostgreSQL)

| DB | 용도 | 데이터 규모 |
|----|------|-----------|
| nuscout_db | NuBI Scout 공고 | 978건+ |
| patentscout_db | Patent Scout 특허 | 740건+ |

### 이메일 (teamnubiz.co.kr)

- Resend API 연동 완료 (DKIM/SPF/MX Verified)
- 발신: contact@teamnubiz.co.kr
- 수신: nick.choi@teamnubiz.co.kr (다우오피스)

---

## 최근 활동

| 일자 | 활동 | 결과 | 비고 |
|------|------|------|------|
| 2026-03-23 | Downloads 2차 스캔: 신규 프로젝트 3개 생성 | patentscout, 서울반도체_특허분석, 팀누비즈_경영관리 폴더 생성, 33개 파일 분류 복사 | 프로젝트 총 17개 |
| 2026-03-23 | 프로젝트 연관성 2차 분석 및 knowledge 갱신 | links.md, projects.md, technologies.md 갱신 완료 | P08→P03/P09 강한연관 승격, P15 통합전략 등록, 삼성특허 매핑 |
| 2026-03-23 | Downloads 스캔 및 파일 분류 | 907개 스캔, 84개 매칭, 1개 신규 복사 | 미분류 19개 확인 대기 |
| 2026-03-23 | 프로젝트 간 연관성 전면 분석 및 knowledge 갱신 | 강한연관 5건, 중간연관 6건 발견, 인물 6명 추가 | links/people/technologies.md 갱신 완료 |
| 2026-03-23 | P07(블록체인 특허) x P04(맥스오거나이드) 교차 분석 | 시너지 4건 확인, 통합 로드맵 수립 (PoC/MVP/상용화 36개월) | 합동 워크숍 및 IP-NFT 법적 검토 예정 |

---

## 대기/확인 필요 작업

| # | 작업 | 상태 | 비고 |
|---|------|------|------|
| 1 | 홈페이지 IP 섹션 모바일 1열 레이아웃 | :yellow_circle: CSS push 완료, 효과 미확인 | !important 오버라이드 |
| 2 | 홈페이지 전체 모바일 스크롤 테스트 | :yellow_circle: 추가 확인 필요 | Why NUBIZ 등 완료 |
| 3 | Resend 테스트 이메일 실수신 확인 | :yellow_circle: 미확인 | 도메인 인증은 완료 |
| 4 | ACMS 건축관리플랫폼 보고서 기재부 제출 | :large_blue_circle: 초안 v2.0 완료 | 확인사항 9건 잔존 |
| 5 | 참여기관 공간/장비 수요조사 | :red_circle: 미착수 | ACMS 설계 기초데이터 |
| 6 | ~~미분류 19개 파일 신규 프로젝트 폴더 생성 검토~~ | :white_check_mark: 완료 | 2차 스캔으로 3개 프로젝트 생성, 33개 파일 분류 완료 |
| 7 | P07-P04 합동 워크숍 개최 | :red_circle: 미착수 | 교차 분석 완료, 일정 조율 필요 |
| 8 | IP-NFT 법적 검토 의뢰 | :red_circle: 미착수 | 오가노이드 디지털 자산화 관련 |
| 9 | 삼성 양도 특허 2건 만료 임박 (10-1182222: 2026-10, 10-0858084: 2026-12) | :red_circle: 긴급확인 | 만료 전 활용 계획 수립 필요 |
| 10 | P15 우주의학x오가노이드 통합전략 R&D v2 관련 후속 마켓리서치 | :yellow_circle: 대기 | 미세중력 시뮬레이터 국산화, OQC 표준화 동향, CRO 시장 분석 |

---

## 핵심 연락처

| 역할 | 이름 | 연락처 |
|------|------|--------|
| 대표 | 최낙의 | nick.choi@teamnubiz.co.kr |

---

## 이 파일 관리 규칙

1. **새 프로젝트 시작** 시 → 이 README의 "프로젝트 현황" 섹션에 1줄 추가
2. **프로젝트 완료** 시 → 상태를 :white_check_mark:로 변경, `_archive/`로 이동
3. **주요 의사결정** 시 → `_hub/decisions/YYYY-MM-주제.md` 파일 생성
4. **월 1회** 전체 현황 리뷰 (불필요한 항목 정리)

> 이 파일은 **프로젝트의 목차**입니다. 상세 내용은 각 서비스 폴더의 CLAUDE.md 또는 README.md를 참고하세요.
