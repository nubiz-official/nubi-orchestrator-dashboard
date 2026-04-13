"""
NuBI Orchestrator Dashboard - 프로젝트 통합관리 대시보드 (Railway 배포용)
원본: agents/orchestrator_app.py — UI/CSS 동일, 백엔드만 Anthropic API
"""
import streamlit as st
import os
from datetime import datetime
from pathlib import Path

# Railway: /app/data, 로컬: 프로젝트 루트/_hub
if os.environ.get("RAILWAY_ENVIRONMENT"):
    DATA_DIR = Path("/app/data")
else:
    DATA_DIR = Path(__file__).parent.parent / "data"

KNOWLEDGE_DIR = DATA_DIR / "knowledge"
DECISIONS_DIR = DATA_DIR / "decisions"
REPORTS_DIR = DATA_DIR / "reports"

st.set_page_config(
    page_title="NuBI Orchestrator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS (원본과 동일) ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800;900&display=swap');
html, body, [class*="st-"], h1, h2, h3, h4, h5, h6, p, span, div, li, a, button, label {
    font-family: 'Noto Sans KR', sans-serif !important;
}
h1, h2, h3 { font-weight: 700 !important; color: #e8eaf2 !important; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] { background: transparent !important; }
.stDeployButton {display: none;}
p, span, div { color: #c9cdd5; }

.orch-hero {
    text-align: center; padding: 24px 20px 16px;
    background: linear-gradient(180deg, rgba(0,194,168,0.06) 0%, transparent 100%);
    border-radius: 16px; margin-bottom: 20px;
}
.orch-logo {
    font-size: 1.8rem; font-weight: 900; letter-spacing: 2px;
    background: linear-gradient(135deg, #00c2a8, #8b5cf6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.orch-badge {
    display: inline-block; margin-top: 4px; padding: 3px 12px;
    background: rgba(139,92,246,0.12); border: 1px solid rgba(139,92,246,0.25);
    border-radius: 20px; font-size: 0.68rem; font-weight: 600; color: #8b5cf6;
}

.metric-card {
    background: linear-gradient(135deg, #0c1220, #101828);
    border: 1px solid #1e293b; border-radius: 12px;
    padding: 16px; text-align: center;
}
.metric-value {
    font-size: 2rem; font-weight: 800;
    background: linear-gradient(135deg, #00c2a8, #8b5cf6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.metric-label { font-size: 0.75rem; color: #6b7280; margin-top: 4px; }

.link-strong { color: #00c2a8; font-weight: 600; }
.link-gap { color: #ef4444; font-weight: 600; }
.link-mid { color: #f59e0b; font-weight: 600; }

.log-box {
    background: #060b16; border: 1px solid #1a2540; border-radius: 12px;
    padding: 16px 20px; font-family: 'Consolas', monospace;
    font-size: 0.75rem; color: #6b7280; max-height: 400px; overflow-y: auto;
    line-height: 1.8; white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)


# ─── 헬퍼 ───

def read_md(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""

def parse_projects(text: str) -> list[dict]:
    projects = []
    for line in text.split("\n"):
        if line.startswith("| P") and "|" in line:
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 6:
                projects.append({
                    "id": cols[0], "name": cols[1], "category": cols[2],
                    "keywords": cols[3], "people": cols[4], "status": cols[5],
                })
    return projects

def parse_links(text: str, section: str) -> list[dict]:
    links = []
    in_section = False
    for line in text.split("\n"):
        if section in line:
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.startswith("| P") and "|" in line:
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 4:
                links.append({"a": cols[0], "b": cols[1], "type": cols[2], "desc": cols[3]})
    return links

def call_claude_api(prompt: str) -> str:
    import anthropic
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return "ANTHROPIC_API_KEY가 설정되지 않았습니다."
    client = anthropic.Anthropic(api_key=api_key)
    # Knowledge 데이터를 컨텍스트에 포함
    knowledge_context = f"""## Knowledge Base
### projects.md
{read_md(KNOWLEDGE_DIR / 'projects.md')}

### links.md
{read_md(KNOWLEDGE_DIR / 'links.md')[:3000]}

### technologies.md
{read_md(KNOWLEDGE_DIR / 'technologies.md')}

### people.md
{read_md(KNOWLEDGE_DIR / 'people.md')}
"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        system="당신은 NuBI Orchestrator — TeamNubiz의 프로젝트 통합관리 AI입니다. 한국어로 응답하세요.",
        messages=[{"role": "user", "content": f"{knowledge_context}\n\n---\n\n{prompt}"}],
    )
    return response.content[0].text


# ─── 데이터 로드 ───

projects_md = read_md(KNOWLEDGE_DIR / "projects.md")
links_md = read_md(KNOWLEDGE_DIR / "links.md")
tech_md = read_md(KNOWLEDGE_DIR / "technologies.md")
people_md = read_md(KNOWLEDGE_DIR / "people.md")
readme_md = read_md(DATA_DIR / "README.md")

projects = parse_projects(projects_md)
strong_links = parse_links(links_md, "강한 연관")
mid_links = parse_links(links_md, "중간 연관")
gap_links = parse_links(links_md, "미연결")

decisions = sorted(DECISIONS_DIR.glob("*.md"), reverse=True) if DECISIONS_DIR.exists() else []
reports = sorted(REPORTS_DIR.glob("*.md"), reverse=True) if REPORTS_DIR.exists() else []


# ─── 사이드바 ───

with st.sidebar:
    st.markdown("""
    <div class="orch-hero">
        <div class="orch-logo">NuBI</div>
        <div class="orch-badge">ORCHESTRATOR</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 에이전트 명령")

    if st.button("전체 현황 (status)", use_container_width=True):
        st.session_state["run_cmd"] = "전체 프로젝트 현황을 보고해주세요. 진행 중 프로젝트 수, 주요 연관성, 최근 의사결정, 즉시 필요한 조치를 정리하세요."

    if st.button("연관성 분석 (link)", use_container_width=True):
        st.session_state["run_cmd"] = "프로젝트 간 연관성을 분석하고 새로운 연결 기회를 발견해주세요."

    st.markdown("---")
    st.markdown("### 교차 분석")
    analyze_target = st.text_input("대상 (예: P07 P04)", placeholder="P01 P03")
    if st.button("분석 실행", use_container_width=True) and analyze_target:
        st.session_state["run_cmd"] = f"다음 프로젝트를 교차 분석해주세요: {analyze_target}. 시너지, 갭, 리스크를 분석하세요."

    st.markdown("---")
    st.markdown("### 자유 질문")
    free_q = st.text_area("질문 입력", placeholder="우주의학과 노화산업센터의 시너지는?", height=80)
    if st.button("질문하기", use_container_width=True) and free_q:
        st.session_state["run_cmd"] = free_q

    st.markdown("---")
    st.markdown(f"<div style='text-align:center;font-size:0.7rem;color:#374151;'>v2.0 | {datetime.now().strftime('%Y-%m-%d')}</div>", unsafe_allow_html=True)


# ─── 메인 ───

tab_dashboard, tab_links, tab_tech, tab_reports, tab_agent = st.tabs(
    ["현황판", "연관성", "기술분류", "보고서", "에이전트"]
)

# ─── 탭 1: 현황판 ───
with tab_dashboard:
    st.markdown("""
    <div class="orch-hero">
        <div class="orch-logo">NuBI Orchestrator</div>
        <div class="orch-badge">PROJECT HUB</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(projects)}</div><div class="metric-label">프로젝트</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(strong_links)}</div><div class="metric-label">강한 연결</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(gap_links)}</div><div class="metric-label">미연결 갭</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(decisions)}</div><div class="metric-label">의사결정</div></div>', unsafe_allow_html=True)

    st.markdown("### 프로젝트 목록")
    if projects:
        for p in projects:
            status_icon = {"진행": "🟢", "설계중": "🔵", "분석": "⚪", "분석완료": "✅",
                          "국고건의": "🟡", "가출원": "🟡", "특허초안": "🟡", "운영": "🟢",
                          "R&D보고서v2완료": "✅"
                          }.get(p["status"], "⚪")
            st.markdown(f"**{status_icon} {p['id']}** {p['name']} — `{p['category']}` | {p['status']}")

    st.markdown("### 최근 의사결정")
    if decisions:
        for d in decisions[:5]:
            st.markdown(f"- {d.stem}")
    else:
        st.info("아직 기록된 의사결정이 없습니다.")

# ─── 탭 2: 연관성 ───
with tab_links:
    st.markdown("### 강한 연관")
    if strong_links:
        for lk in strong_links:
            st.markdown(f'<span class="link-strong">●</span> **{lk["a"]}** ↔ **{lk["b"]}** — {lk["desc"][:80]}', unsafe_allow_html=True)

    st.markdown("### 중간 연관 (시너지 가능)")
    if mid_links:
        for lk in mid_links:
            st.markdown(f'<span class="link-mid">●</span> **{lk["a"]}** ↔ **{lk["b"]}** — {lk["desc"][:80]}', unsafe_allow_html=True)

    st.markdown("### 미연결 (갭)")
    if gap_links:
        for lk in gap_links:
            st.markdown(f'<span class="link-gap">●</span> **{lk["a"]}** → {lk["b"]} — {lk["desc"][:80]}', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 인물 교차 참여")
    if people_md:
        st.markdown(people_md)

# ─── 탭 3: 기술분류 ───
with tab_tech:
    if tech_md:
        st.markdown(tech_md)
    else:
        st.info("technologies.md를 로드할 수 없습니다.")

# ─── 탭 4: 보고서 ───
with tab_reports:
    st.markdown("### 에이전트 실행 보고서")

    # 1. 세션 내 에이전트 실행 이력 (우선 표시)
    agent_reports = st.session_state.get("agent_reports", [])

    if agent_reports:
        st.caption(
            f"현재 세션에서 {len(agent_reports)}개의 에이전트 보고서가 생성되었습니다. "
            "(브라우저를 닫으면 사라집니다. 영구 보관은 결과 다운로드 → git 커밋)"
        )

        for idx, rep in enumerate(agent_reports):
            query_short = rep["query"][:60] + ("..." if len(rep["query"]) > 60 else "")
            with st.expander(
                f"📄 [{rep['timestamp']}] {query_short}",
                expanded=(idx == 0),
            ):
                st.markdown(f"**질문**: {rep['query']}")
                st.markdown("---")
                st.markdown(rep["output"])
                st.download_button(
                    label="이 보고서 다운로드",
                    data=f"# NuBI Orchestrator 보고서\n\n**생성일시**: {rep['timestamp']}\n\n**질문**: {rep['query']}\n\n---\n\n{rep['output']}",
                    file_name=f"orchestrator_{rep['file_ts']}.md",
                    mime="text/markdown",
                    key=f"dl_{rep['file_ts']}_{idx}",
                )
    else:
        st.info(
            "ℹ️ 아직 생성된 에이전트 보고서가 없습니다. "
            "**에이전트** 탭에서 명령을 실행하면 이 탭에 자동으로 누적됩니다."
        )

    st.markdown("---")

    # 2. 미리 커밋된 교차 분석 보고서 파일
    st.markdown("### 사전 등록 보고서 (data/reports/)")
    if reports:
        selected_report = st.selectbox("보고서 선택", [r.name for r in reports])
        if selected_report:
            st.markdown(read_md(REPORTS_DIR / selected_report))
    else:
        st.caption("사전 등록된 .md 보고서가 없습니다 (data/reports/ 디렉토리 비어있음).")

    st.markdown("---")

    # 3. 의사결정 기록
    st.markdown("### 의사결정 기록 (data/decisions/)")
    if decisions:
        selected_decision = st.selectbox("기록 선택", [d.name for d in decisions])
        if selected_decision:
            st.markdown(read_md(DECISIONS_DIR / selected_decision))
    else:
        st.caption("사전 등록된 의사결정 기록이 없습니다.")

# ─── 탭 5: 에이전트 ───
with tab_agent:
    st.markdown("### 에이전트 실행")

    # 세션 내 에이전트 실행 이력 초기화
    if "agent_reports" not in st.session_state:
        st.session_state["agent_reports"] = []

    if "run_cmd" in st.session_state and st.session_state["run_cmd"]:
        cmd = st.session_state.pop("run_cmd")
        st.markdown(f"**실행 중**: `{cmd[:80]}...`")

        with st.spinner("NuBI Orchestrator AI 분석 중..."):
            output = call_claude_api(cmd)

        st.markdown(output)

        # 에러 응답이 아닌 경우에만 보고서 탭에 누적 저장
        if not output.startswith("ANTHROPIC_API_KEY"):
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.session_state["agent_reports"].insert(
                0,
                {
                    "timestamp": ts,
                    "file_ts": file_ts,
                    "query": cmd,
                    "output": output,
                },
            )
            st.success(f"✅ 보고서 탭에 저장되었습니다 (총 {len(st.session_state['agent_reports'])}건)")

        st.download_button(
            label="결과 다운로드",
            data=output,
            file_name=f"orchestrator_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
        )
    else:
        st.markdown("""
#### 📖 사용 안내

**NuBI Orchestrator 에이전트**는 TeamNubiz가 운영 중인 18개 딥테크 프로젝트의 현황·연관성·의사결정 기록을 통합 분석하여, 자연어 질문에 답변해 드립니다. Anthropic Claude API를 기반으로 동작합니다.

---

#### 1️⃣ 사전 준비 명령 (좌측 사이드바)

아래 3종 명령은 사이드바 버튼 클릭만으로 즉시 실행됩니다.

| 명령 | 용도 | 기대 응답 |
|---|---|---|
| **전체 현황 (status)** | 18개 프로젝트 전수 상태 보고 | 진행 중 프로젝트 수, 주요 연관성, 최근 의사결정, 즉시 필요한 조치 |
| **연관성 분석 (link)** | 프로젝트 간 숨겨진 연결 발견 | 새로운 시너지 기회, 협력 후보, 자원 공유 가능성 |
| **교차 분석** (코드 입력 필요) | 2개 이상 프로젝트 상세 비교 | 시너지 / 갭 / 리스크 3축 분석. 예: `P01 P03` |

---

#### 2️⃣ 자유 질문 예시

사이드바 **자유 질문** 입력란에 아래와 같은 형식으로 물어보시면 됩니다.

- `우주의학과 노화산업센터의 시너지는 무엇인가?`
- `디지털 CRO MVP 9개 화면 중 김영석 교수 트랙과 직접 연결된 것을 찾아 설명해.`
- `P02 노화산업센터와 P05 K-HOPE 화순을 비교하고, 두 프로젝트를 하나의 통합 제안으로 묶을 수 있는 방법을 3가지 제안해.`
- `현재 복지부 4/15 제출본의 3대 키워드(ALCOA+ / 에이전트 AI / 디지털 CRO)에 맞지 않는 프로젝트가 있다면 무엇이고, 왜 그런가?`
- `향후 3개월 내 TeamNubiz가 우선순위로 삼아야 할 의사결정 5가지를 근거와 함께 제시해.`

**팁**:
- 질문이 구체적일수록(프로젝트 코드 P01~P18, 숫자, 기간, 목표를 명시할수록) 응답 품질이 올라갑니다.
- 한 질문에 너무 많은 항목을 묶지 말고, 2~3개 주제 단위로 나눠 질문하세요.

---

#### 3️⃣ 응답 확인 & 저장

- 응답은 마크다운으로 표시되며, **평균 10~30초** 소요됩니다 (질문 길이 / 복잡도에 따라 변동).
- **실행된 모든 보고서는 자동으로 [보고서] 탭에 누적 저장됩니다** (현재 브라우저 세션 동안 유지, 닫으면 사라짐).
- 응답 아래의 **결과 다운로드** 버튼으로 `.md` 파일로 받을 수 있습니다. 영구 보관하려면 이 파일을 `data/reports/`에 git 커밋하세요.
- 동일 질문을 여러 번 던지면 응답이 조금씩 달라질 수 있습니다 — 에이전트는 결정론적이지 않습니다. 중요한 의사결정 근거로 쓰실 때는 **2~3회 반복 질문** 권장.

---

#### ⚠️ 주의사항

- **민감 정보 입력 금지**: 개인정보, 미공개 투자 정보, 미공표 특허 내용 등은 입력하지 마세요. Anthropic API를 경유합니다.
- **크레딧 소비**: 각 질문마다 Anthropic API 크레딧이 소비됩니다. 장문 질문은 비용이 더 큽니다.
- **콜드 스타트**: 첫 실행 시 서버 wake-up에 5~10초 추가 지연이 있을 수 있습니다.
- **한계**: 이 에이전트는 18개 프로젝트의 **메타데이터와 의사결정 기록**을 학습한 상태입니다. 각 프로젝트의 세부 수치(예: 특정 연도 예산)는 해당 프로젝트의 개별 대시보드에서 확인하세요.

---

👉 **지금 시작하시려면**: 좌측 사이드바에서 **전체 현황 (status)** 버튼을 한 번 눌러보세요. 가장 빠르게 오케스트레이터가 어떻게 동작하는지 체감하실 수 있습니다.
""")
