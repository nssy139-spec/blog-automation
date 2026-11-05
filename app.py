# app.py - 리치유니의 무인 블로그 자동화 공장 웹 조종기
import streamlit as st
import streamlit.components.v1 as components
from config import Config
from modules.logger import setup_logger
from modules.generator import generate_blog_content
from modules.image_service import create_image_metadata, STYLE_PRESETS
from modules.publisher import publish_to_naver_email, publish_to_tistory

# 1. 로거 초기화
logger = setup_logger("app")

# 2. 페이지 설정
st.set_page_config(
    page_title="리치유니의 무인 블로그 공장",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태(Session State) 초기화 (생성된 글 데이터 보존)
if "blog_data" not in st.session_state:
    st.session_state.blog_data = None
if "img_meta" not in st.session_state:
    st.session_state.img_meta = None

# 모던 CSS 스타일링
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
    .generate-btn button {
        background-color: #008080 !important;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        border: none !important;
        width: 100% !important;
        box-shadow: 0 4px 6px rgba(0, 128, 128, 0.2) !important;
    }
    .generate-btn button:hover {
        background-color: #006666 !important;
    }
    .naver-card {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .tistory-card {
        background-color: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
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
    .preview-box span[style*="color:#008080"] {
        color: #008080 !important;
    }
    .preview-box hr {
        background: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# 헤더 영역
st.markdown('<div class="main-title">🤖 리치유니의 무인 블로그 자동화 공장</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">글 자동 생성부터 네이버·티스토리 실제 원클릭 자동 발행까지 한 곳에서 제어합니다. 💕</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# STEP 1: 콘텐츠 기획 및 생성 패널
# -------------------------------------------------------------
st.markdown("### 📌 1단계: 콘텐츠 기획 & AI 글 생성")

col_input1, col_input2 = st.columns([3, 2])
with col_input1:
    keyword = st.text_input(
        "발행할 블로그 주제(키워드)",
        value="2026년 하반기 정부지원금",
        placeholder="예: 2026년 청년 도약 계좌, 재테크 꿀팁 등"
    )
with col_input2:
    style_options = list(STYLE_PRESETS.keys())
    image_style = st.selectbox(
        "🎨 썸네일/본문 이미지 감성 스타일",
        style_options,
        index=0
    )

st.markdown('<div class="generate-btn">', unsafe_allow_html=True)
if st.button("✨ 1. 고품질 블로그 글 & 썸네일 프롬프트 즉시 생성"):
    if not keyword.strip():
        st.error("⚠️ 키워드를 입력해 주세요.")
    else:
        with st.spinner("리치유니 맞춤형 템플릿으로 고품질 글감을 생성하고 있습니다..."):
            st.session_state.blog_data = generate_blog_content(keyword=keyword, image_style=image_style)
            st.session_state.img_meta = create_image_metadata(keyword=keyword, style_name=image_style)
            st.success(f"🎉 '{keyword}' 주제로 글이 완벽하게 생성되었습니다! 아래에서 내용을 확인하고 바로 발행하세요.")
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# STEP 2 & 3: 생성 결과 및 실제 자동 발행 센터
# -------------------------------------------------------------
if st.session_state.blog_data is not None:
    blog_data = st.session_state.blog_data
    img_meta = st.session_state.img_meta

    st.markdown("---")
    
    # 2컬럼 레이아웃: 좌측(미리보기), 우측(실제 자동 발행 제어 패널)
    col_preview, col_publish = st.columns([3, 2], gap="large")

    with col_preview:
        st.markdown("### 📄 2단계: 생성된 포스팅 미리보기")
        st.info(f"🎨 적용된 스타일: **{img_meta['style_name']}** | 📝 **리치유니 가이드 준수 (이탤릭 없음, 볼드/틸 포인트)**")
        
        with st.container():
            st.markdown(f"#### 🏷️ {blog_data['title']}")
            st.markdown(f"<div class='preview-box'>{blog_data['content']}</div>", unsafe_allow_html=True)
            st.caption(f"태그: {', '.join(['#' + t for t in blog_data['tags']])}")

    with col_publish:
        st.markdown("### 🚀 3단계: 원클릭 자동 발행 센터")
        
        # -----------------------------
        # 🟢 네이버 블로그 발행 카드
        # -----------------------------
        st.markdown('<div class="naver-card">', unsafe_allow_html=True)
        st.markdown("#### 🟢 네이버 블로그 자동 발행")
        
        with st.expander("🔑 네이버 계정 정보 입력 (필수)", expanded=True):
            naver_id = st.text_input("네이버 아이디", value=Config.NAVER_ID, placeholder="예: rich_yuni", key="n_id")
            naver_pw = st.text_input("비밀번호 (또는 앱 2차비번)", value=Config.NAVER_PW, type="password", key="n_pw")
            naver_blog_id = st.text_input("블로그 ID", value=Config.NAVER_BLOG_ID or naver_id, placeholder="아이디와 동일하면 공백", key="n_bid")
            st.caption("💡 네이버 블로그 관리 ➡️ 글쓰기 설정 ➡️ **'이메일 글쓰기'**가 켜져 있어야 합니다.")

        if st.button("🚀 네이버 블로그에 즉시 자동 발행하기", key="btn_naver"):
            if not naver_id or not naver_pw:
                st.error("⚠️ 네이버 아이디와 비밀번호를 입력해주세요.")
            else:
                with st.spinner("네이버 블로그로 글을 전송하여 자동 발행 중입니다..."):
                    res = publish_to_naver_email(
                        naver_id=naver_id,
                        naver_password=naver_pw,
                        title=blog_data["title"],
                        content_html=blog_data["content"],
                        blog_id=naver_blog_id or naver_id
                    )
                    if res.get("success"):
                        st.success("🎉 **[네이버 블로그] 포스팅이 성공적으로 등록되었습니다!**")
                        st.markdown(f"👉 [**내 네이버 블로그 확인하기**]({res.get('post_url')})")
                    else:
                        st.error(f"❌ 네이버 발행 실패: {res.get('message')}")
        
        # 보조 원클릭 복사 도구
        st.markdown("---")
        st.markdown("##### ⚡ 가장 간편하고 안전한 3초 수동 포스팅")
        st.caption("네이버 2단계 인증이나 SMTP 설정이 복잡하시다면 아래 버튼을 이용하세요:")
        
        # 클립보드 복사용 컴포넌트
        copy_html = f"""
        <div style="display:flex; flex-direction:column; gap:8px;">
            <button onclick="navigator.clipboard.writeText(`{blog_data['title']}`); alert('제목이 복사되었습니다!');" 
                    style="background:#03c75a; color:white; border:none; padding:8px 12px; border-radius:6px; cursor:pointer; font-weight:bold;">
                📋 1. 제목 복사하기
            </button>
            <button id="copy-body-btn" 
                    style="background:#008080; color:white; border:none; padding:8px 12px; border-radius:6px; cursor:pointer; font-weight:bold;">
                📋 2. 본문 서식 복사하기 (네이버 에디터 호환)
            </button>
        </div>
        <div id="hidden-copy-content" style="display:none;">{blog_data['content']}</div>
        <script>
            document.getElementById('copy-body-btn').onclick = function() {{
                const content = document.getElementById('hidden-copy-content').innerHTML;
                const blob = new Blob([content], {{ type: 'text/html' }});
                const plainBlob = new Blob([document.getElementById('hidden-copy-content').innerText], {{ type: 'text/plain' }});
                const item = new ClipboardItem({{ 'text/html': blob, 'text/plain': plainBlob }});
                navigator.clipboard.write([item]).then(() => {{
                    alert('본문이 서식(컬러, 굵기 등) 그대로 복사되었습니다! 네이버 글쓰기 창에서 Ctrl+V 하세요.');
                }});
            }};
        </script>
        """
        components.html(copy_html, height=85)
        st.link_button("✍️ 3. 네이버 스마트에디터 새 창 열기", "https://blog.naver.com/GoBlogWrite.naver")
        st.markdown('</div>', unsafe_allow_html=True)

        st.write("")

        # -----------------------------
        # 🟠 티스토리 발행 카드
        # -----------------------------
        st.markdown('<div class="tistory-card">', unsafe_allow_html=True)
        st.markdown("#### 🟠 티스토리 즉시 자동 발행")
        
        with st.expander("🔑 티스토리 Open API 설정 (필수)", expanded=True):
            t_token = st.text_input("티스토리 Access Token", value=Config.TISTORY_ACCESS_TOKEN, type="password", key="t_tok")
            t_name = st.text_input("블로그 서브도메인 이름", value=Config.TISTORY_BLOG_NAME, placeholder="예: myblog", key="t_name")
            t_vis = st.selectbox(
                "발행 상태",
                options=[3, 0],
                format_func=lambda x: "🌐 즉시 공개 발행" if x == 3 else "🔒 비공개 발행 (테스트)",
                key="t_vis"
            )

        if st.button("🚀 티스토리에 즉시 자동 발행하기", key="btn_tistory"):
            if not t_token or not t_name:
                st.error("⚠️ 티스토리 Access Token과 블로그 이름을 입력해주세요.")
            else:
                with st.spinner("티스토리 Open API를 통해 글을 발행하고 있습니다..."):
                    t_res = publish_to_tistory(
                        access_token=t_token,
                        blog_name=t_name,
                        title=blog_data["title"],
                        content=blog_data["content"],
                        visibility=t_vis,
                        tags=blog_data.get("tags")
                    )
                    if t_res.get("success"):
                        st.success("🎉 **[티스토리] 포스팅이 성공적으로 발행되었습니다!**")
                        st.markdown(f"👉 [**발행된 티스토리 글 바로 보러가기**]({t_res.get('post_url')})")
                    else:
                        st.error(f"❌ 티스토리 발행 실패: {t_res.get('message')}")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("💡 위의 **[✨ 1. 고품질 블로그 글 & 썸네일 프롬프트 즉시 생성]** 버튼을 먼저 누르시면, 완성된 글 검토 및 네이버/티스토리 직접 발행 버튼이 나타납니다!")

# 하단 푸터
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #718096; font-size: 0.85rem;'>"
    "⚡ 리치유니의 무인 블로그 자동화 공장 | Naver & Tistory Direct Publisher v2.5"
    "</div>",
    unsafe_allow_html=True
)
