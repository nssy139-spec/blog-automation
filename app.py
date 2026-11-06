# app.py - 리치유니의 무인 블로그 자동화 공장 웹 조종기 (7대 주제 순환 전자동 버전)
import streamlit as st
import streamlit.components.v1 as components
from config import Config
from modules.logger import setup_logger
from modules.generator import generate_blog_content
from modules.image_service import create_image_metadata, STYLE_PRESETS
from modules.persistent_bot import publish_naver_direct, publish_tistory_direct
from modules.topic_manager import get_next_topic_and_advance, peek_current_topic

# 1. 로거 초기화
logger = setup_logger("app")

# 2. 페이지 설정
st.set_page_config(
    page_title="리치유니의 무인 블로그 공장 (순환 전자동)",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화
if "blog_data" not in st.session_state:
    st.session_state.blog_data = None
if "img_meta" not in st.session_state:
    st.session_state.img_meta = None

# 모던 CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1a202c;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #008080;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    .queue-box {
        background: #f0fdfa;
        border: 1px solid #99f6e4;
        border-radius: 10px;
        padding: 15px 20px;
        margin-bottom: 20px;
    }
    .preview-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        max-height: 600px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏢 리치유니의 무인 블로그 자동화 공장</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">🤖 7대 순환 큐 (재테크 ⇄ 생활문화 ⇄ 정부지원금 ⇄ 생활용품 ⇄ 부동산 ⇄ 건강 ⇄ 인테리어) 전자동 시스템</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. 현재 순환 큐 상태 표시 (미발행 시 즉시 폐기 원칙)
# -------------------------------------------------------------
next_info = peek_current_topic()

st.markdown(f"""
<div class="queue-box">
    <div style="font-size: 0.95rem; color: #0f766e; font-weight: bold; margin-bottom: 6px;">
        🔄 <b>[7대 주제 순환 발행 스케줄러 현황]</b>
    </div>
    <div style="font-size: 1.1rem; color: #111827; font-weight: 700;">
        👉 이번 차례 예정 주제: <span style="color: #008080; text-decoration: underline;">[{next_info['topic_type']}]</span> {next_info['keyword']}
    </div>
    <div style="font-size: 0.85rem; color: #64748b; margin-top: 6px;">
        💡 <b>단회성 원칙:</b> 발행 여부와 상관없이 글이 호출되면 즉시 다음 주제로 전진하며, 미발행된 글은 재탕 없이 영구 폐기됩니다.
    </div>
</div>
""", unsafe_allow_html=True)

# 티스토리 단독 1회 로그인 연결 배너
st.markdown("""
<div style="background-color: #fff7ed; border: 1px solid #fdba74; border-radius: 8px; padding: 14px 18px; margin-bottom: 16px;">
    <div style="font-weight: bold; color: #c2410c; font-size: 1rem;">
        🟠 [1단계 집중] 티스토리 단독 영구 로그인 세션 연결
    </div>
    <div style="color: #7c2d12; font-size: 0.9rem; margin-top: 4px;">
        네이버는 잠시 접어두고, <b>티스토리 브라우저 창을 먼저 열어 딱 1회만 로그인</b>해 두면 세션이 영구 저장되어 앞으로 100% 무인 자동 발행됩니다.
    </div>
</div>
""", unsafe_allow_html=True)

col_t_btn1, col_t_btn2 = st.columns([2, 1])
with col_t_btn1:
    st.caption("아래 주황색 버튼을 누르면 사용자 화면에 티스토리 전용 브라우저 창이 열립니다:")
with col_t_btn2:
    if st.button("🔑 티스토리 브라우저 열기 (1회 로그인)", key="btn_tistory_session", type="secondary"):
        import subprocess
        subprocess.Popen([r".venv\Scripts\python.exe", "connect_tistory.py"])
        st.success("🚀 티스토리 브라우저 창이 열렸습니다! 카카오 로그인을 1회 완료해 주세요.")

# 계정 설정 아코디언
with st.expander("⚙️ 블로그 로그인 계정 설정 (미입력 시 config.py 기본값 자동 사용)", expanded=False):
    col_acc1, col_acc2 = st.columns(2)
    with col_acc1:
        st.markdown("##### 🟢 네이버 로그인 정보")
        n_id = st.text_input("네이버 아이디", value=Config.NAVER_ID, key="cfg_nid")
        n_pw = st.text_input("네이버 비밀번호 (또는 앱비밀번호)", value=Config.NAVER_PW, type="password", key="cfg_npw")
    with col_acc2:
        st.markdown("##### 🟠 카카오/티스토리 로그인 정보")
        k_id = st.text_input("카카오 로그인 아이디(이메일)", value=Config.NAVER_ID, key="cfg_kid")
        k_pw = st.text_input("카카오 비밀번호", value="", type="password", key="cfg_kpw")
        t_bname = st.text_input("티스토리 블로그 서브도메인", value=Config.TISTORY_BLOG_NAME or "essay0606", key="cfg_tbname")

st.write("")

# -------------------------------------------------------------
# 2. 원클릭 전자동 발행 메인 섹션
# -------------------------------------------------------------
st.markdown("### 🚀 2. 원클릭 전자동 무인 발행")

mode_tab1, mode_tab2 = st.tabs(["🔄 [추천] 순환 스케줄러 자동 순서 발행", "✍️ 직접 키워드 입력 발행"])

# 탭 1: 스케줄 순서 자동 발행
with mode_tab1:
    st.markdown(f"현재 등록된 7대 순환 알고리즘에 따라 **[{next_info['topic_type']}] '{next_info['keyword']}'** 을(를) 즉시 생성하고 네이버/티스토리에 무인 발행합니다.")
    
    if st.button("⚡ [스케줄 순서대로] 이번 차례 즉시 무인 자동 발행 시작", key="btn_auto_cycle", type="primary"):
        status_box = st.status("🚀 순환 스케줄러 무인 자동 발행 가동 중...", expanded=True)
        
        try:
            # 1단계: 주제 선정 및 즉시 포인터 전진 (이전 글 폐기 원칙 충족)
            topic_data = get_next_topic_and_advance()
            cur_topic_type = topic_data["topic_type"]
            cur_keyword = topic_data["keyword"]
            cur_cat = topic_data["category"]
            next_topic_name = topic_data["next_topic_type"]

            status_box.write(f"📝 1단계: [{cur_topic_type}] '{cur_keyword}' 고품질 맞춤 원고 및 고화질 이미지 2장 생성 중...")
            blog_data = generate_blog_content(
                keyword=cur_keyword,
                category=cur_cat,
                topic_type=cur_topic_type
            )
            st.session_state.blog_data = blog_data
            status_box.write(f"✅ 콘텐츠 생성 완료 (다음 예정 차례는 '{next_topic_name}'(으)로 자동 변경되었습니다)")

            # 2단계: 네이버 블로그 무인 자동 발행
            status_box.write("🟢 2단계: 네이버 블로그 스마트에디터로 직격 접속하여 무인 자동 발행 중...")
            n_account_id = n_id.strip() if n_id else Config.NAVER_ID
            n_account_pw = n_pw.strip() if n_pw else Config.NAVER_PW

            res_n = publish_naver_direct(
                title=blog_data["title"],
                content_html=blog_data["content"],
                naver_id=n_account_id if n_account_id else "ssy139",
                naver_pw=n_account_pw
            )
            if res_n.get("success"):
                status_box.write(f"🎉 **[네이버 블로그 발행 성공!]** 👉 [내 네이버 블로그 확인]({res_n.get('post_url')})")
            else:
                status_box.write(f"⚠️ 네이버 로봇 알림: {res_n.get('message')}")

            # 3단계: 티스토리 블로그 무인 자동 발행
            status_box.write("🟠 3단계: 티스토리 블로그 에디터로 직격 접속하여 무인 자동 발행 중...")
            kakao_user_id = k_id.strip() if k_id else Config.NAVER_ID
            kakao_user_pw = k_pw.strip()
            target_tistory = t_bname.strip() if t_bname else "essay0606"

            res_t = publish_tistory_direct(
                title=blog_data["title"],
                content_html=blog_data["content"],
                blog_name=target_tistory,
                kakao_id=kakao_user_id,
                kakao_pw=kakao_user_pw
            )
            if res_t.get("success"):
                status_box.write(f"🎉 **[티스토리 발행 성공!]** 👉 [내 티스토리 확인]({res_t.get('post_url')})")
            else:
                status_box.write(f"⚠️ 티스토리 로봇 알림: {res_t.get('message')}")

            status_box.update(label="🎉 모든 무인 순환 발행이 성공적으로 완료되었습니다!", state="complete", expanded=True)
            st.rerun()

        except Exception as e:
            logger.error(f"순환 발행 오류: {str(e)}", exc_info=True)
            status_box.update(label=f"🚨 오류 발생 (다음 주제로 전진 완료): {str(e)}", state="error", expanded=True)

# 탭 2: 수동 키워드 입력 발행
with mode_tab2:
    col_c1, col_c2, col_c3 = st.columns([2, 3, 2])
    with col_c1:
        cat_sel = st.selectbox("📂 발행 분야 선택", ["재테크·경제", "생활·문화·리뷰"])
    with col_c2:
        kw_input = st.text_input("블로그 주제(키워드)", value="2026 청년 정책 금융 총정리")
    with col_c3:
        style_sel = st.selectbox("🎨 비주얼 스타일", list(STYLE_PRESETS.keys()))

    if st.button("⚡ [입력한 키워드로] 즉시 자동 발행 시작", key="btn_manual_publish"):
        if not kw_input.strip():
            st.error("⚠️ 키워드를 입력해 주세요.")
        else:
            status_box = st.status("🚀 수동 지정 무인 발행 가동 중...", expanded=True)
            try:
                cat_param = "finance" if cat_sel == "재테크·경제" else "lifestyle"
                blog_data = generate_blog_content(keyword=kw_input, image_style=style_sel, category=cat_param)
                st.session_state.blog_data = blog_data

                n_account_id = n_id.strip() if n_id else Config.NAVER_ID
                n_account_pw = n_pw.strip() if n_pw else Config.NAVER_PW
                res_n = publish_naver_direct(title=blog_data["title"], content_html=blog_data["content"], naver_id=n_account_id, naver_pw=n_account_pw)
                if res_n.get("success"):
                    status_box.write(f"🎉 **[네이버 블로그 발행 성공!]** 👉 [확인]({res_n.get('post_url')})")

                kakao_user_id = k_id.strip() if k_id else Config.NAVER_ID
                kakao_user_pw = k_pw.strip()
                target_tistory = t_bname.strip() if t_bname else "essay0606"
                res_t = publish_tistory_direct(title=blog_data["title"], content_html=blog_data["content"], blog_name=target_tistory, kakao_id=kakao_user_id, kakao_pw=kakao_user_pw)
                if res_t.get("success"):
                    status_box.write(f"🎉 **[티스토리 발행 성공!]** 👉 [확인]({res_t.get('post_url')})")

                status_box.update(label="🎉 발행 완료!", state="complete")
            except Exception as e:
                status_box.update(label=f"🚨 오류: {str(e)}", state="error")

# -------------------------------------------------------------
# 3. 생성된 글 실시간 확인 및 보조 도구
# -------------------------------------------------------------
if st.session_state.blog_data is not None:
    blog_data = st.session_state.blog_data
    st.markdown("---")
    st.markdown("### 📄 발행된 콘텐츠 미리보기")
    
    col_p1, col_p2 = st.columns([3, 1])
    with col_p1:
        st.markdown(f"#### {blog_data['title']}")
        st.markdown(f"<div class='preview-box'>{blog_data['content']}</div>", unsafe_allow_html=True)
    with col_p2:
        st.markdown("##### ⚡ 비상용 1초 복사 도구")
        st.caption("혹시 수동 복사가 필요하실 때만 쓰세요:")
        
        t_copy = f"""
        <button onclick="
            const c = document.getElementById('bcontent').innerHTML;
            const b = new Blob([c], {{type: 'text/html'}});
            const pb = new Blob([document.getElementById('bcontent').innerText], {{type: 'text/plain'}});
            navigator.clipboard.write([new ClipboardItem({{'text/html': b, 'text/plain': pb}})]).then(()=>alert('서식이 복사되었습니다!'));
        " style="width:100%; background:#f97316; color:white; border:none; padding:10px; border-radius:6px; cursor:pointer; font-weight:bold; margin-bottom:8px;">
            📋 전체 서식 복사
        </button>
        <div id="bcontent" style="display:none;">{blog_data['content']}</div>
        """
        components.html(t_copy, height=50)
        st.link_button("✍️ 티스토리 에디터 열기", "https://essay0606.tistory.com/manage/newpost/")
        st.link_button("✍️ 네이버 에디터 열기", "https://blog.naver.com/GoBlogWrite.naver")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #718096; font-size: 0.85rem;'>"
    "⚡ 리치유니의 무인 블로그 자동화 공장 v3.5 | 7-Topic Strict Rotation Engine"
    "</div>",
    unsafe_allow_html=True
)
