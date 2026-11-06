# app.py - 리치유니의 무인 블로그 자동화 공장 웹 조종기 (100% 전자동 버전)
import streamlit as st
import streamlit.components.v1 as components
from config import Config
from modules.logger import setup_logger
from modules.generator import generate_blog_content
from modules.image_service import create_image_metadata, STYLE_PRESETS
from modules.persistent_bot import publish_naver_direct, publish_tistory_direct

# 1. 로거 초기화
logger = setup_logger("app")

# 2. 페이지 설정
st.set_page_config(
    page_title="리치유니의 무인 블로그 공장 (전자동)",
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
        color: #4a5568;
        margin-bottom: 1.5rem;
    }
    .auto-publish-btn button {
        background: linear-gradient(135deg, #008080 0%, #0d9488 100%) !important;
        color: white !important;
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        border-radius: 10px !important;
        padding: 1rem 2rem !important;
        border: none !important;
        width: 100% !important;
        box-shadow: 0 4px 14px rgba(0, 128, 128, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    .auto-publish-btn button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 128, 128, 0.45) !important;
    }
    .preview-box {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.8rem;
        margin-top: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.04);
    }
    .preview-box * {
        color: #1a202c !important;
    }
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown('<div class="main-title">🤖 리치유니의 무인 블로그 전자동 공장</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">복사·붙여넣기 0%! 버튼 하나로 글 작성부터 네이버·티스토리 실제 발행까지 로봇이 100% 전자동 처리합니다. 💕</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. 설정 및 계정 정보 (기본값 자동 로드)
# -------------------------------------------------------------
with st.expander("🔑 1. 로봇 자동 로그인 계정 설정 (최초 1회 확인)", expanded=False):
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

col_c1, col_c2, col_c3 = st.columns([2, 3, 2])
with col_c1:
    cat_sel = st.selectbox("📂 발행 분야 선택", ["재테크·경제", "생활·문화·리뷰"])
with col_c2:
    def_kw = "2026년 하반기 정부지원금 혜택 및 신청 자격" if cat_sel == "재테크·경제" else "AI 생산성 극대화 추천 도구 BEST 5"
    kw_input = st.text_input("블로그 주제(키워드)", value=def_kw)
with col_c3:
    style_sel = st.selectbox("🎨 비주얼 스타일", list(STYLE_PRESETS.keys()))

st.write("")

# 메인 전자동 실행 버튼
st.markdown('<div class="auto-publish-btn">', unsafe_allow_html=True)
if st.button("⚡ [전자동] 글 생성 + 고화질 사진 2장 + 네이버/티스토리 즉시 자동 발행 시작"):
    if not kw_input.strip():
        st.error("⚠️ 키워드를 입력해 주세요.")
    else:
        status_box = st.status("🚀 전자동 무인 공장이 가동되었습니다...", expanded=True)
        
        try:
            # 1단계: 글 및 고화질 이미지 생성
            status_box.write("📝 1단계: 리치유니 맞춤형 템플릿과 고화질 이미지 2장을 결합하여 글을 생성 중...")
            cat_param = "finance" if cat_sel == "재테크·경제" else "lifestyle"
            blog_data = generate_blog_content(keyword=kw_input, image_style=style_sel, category=cat_param)
            st.session_state.blog_data = blog_data
            status_box.write(f"✅ 콘텐츠 생성 완료: '{blog_data['title']}'")

            # 2단계: 네이버 블로그 로봇 영구 세션 무인 자동 발행
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

            # 3단계: 티스토리 블로그 로봇 영구 세션 무인 자동 발행
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

            status_box.update(label="🎉 모든 전자동 발행 프로세스가 완료되었습니다!", state="complete", expanded=True)

        except Exception as e:
            logger.error(f"전자동 발행 오류: {str(e)}", exc_info=True)
            status_box.update(label=f"🚨 오류 발생: {str(e)}", state="error", expanded=True)

st.markdown('</div>', unsafe_allow_html=True)

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
        
        # 티스토리 원클릭 복사
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
    "⚡ 리치유니의 무인 블로그 자동화 공장 v3.0 | 100% Full-Automation Edition"
    "</div>",
    unsafe_allow_html=True
)
