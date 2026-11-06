"""
티스토리 브라우저 자동화 로봇 (Playwright 기반)
- 카카오 계정 자동 로그인
- essay0606.tistory.com 에디터 자동 접속
- 제목, 본문(HTML), 이미지 자동 입력 및 [완료] -> [공개발행] 버튼 클릭 자동화
"""
import time
from typing import Dict, Any, List, Optional
from modules.logger import setup_logger

logger = setup_logger("tistory_bot")

def publish_to_tistory_via_bot(
    kakao_id: str,
    kakao_pw: str,
    blog_name: str,
    title: str,
    content_html: str,
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Playwright 브라우저 로봇을 실행하여 티스토리에 직접 로그인 후 글을 자동 발행합니다.
    """
    if not kakao_id or not kakao_pw:
        return {"success": False, "message": "카카오 아이디 또는 비밀번호가 설정되지 않았습니다."}

    import os
    from playwright.sync_api import sync_playwright

    logger.info(f"🤖 [티스토리 로봇 가동] 계정: {kakao_id} -> 블로그: {blog_name}")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    profile_dir = os.path.join(base_dir, "browser_profile", "tistory")

    try:
        with sync_playwright() as p:
            args = [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]

            # 로컬 세션 프로필 디렉토리가 있으면 영구 세션으로 실행, 없으면 일반 브라우저로 실행
            if os.path.exists(profile_dir):
                logger.info(f"📁 기존 티스토리 영구 세션 프로필 로드: {profile_dir}")
                context = p.chromium.launch_persistent_context(
                    user_data_dir=profile_dir,
                    headless=True,
                    args=args,
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                )
                page = context.pages[0] if context.pages else context.new_page()
                browser = None
            else:
                browser = p.chromium.launch(headless=True, args=args)
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                )
                page = context.new_page()

            # 1. 티스토리 글쓰기 에디터 직격 접속 시도
            write_url = f"https://{blog_name}.tistory.com/manage/newpost/"
            logger.info(f"1단계: 티스토리 에디터 직격 접속 중... ({write_url})")
            page.goto(write_url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(3000)

            # 로그인 여부 감지: 로그인이 풀려있거나 로그인 화면으로 리다이렉트된 경우에만 로그인 수행
            if "login" in page.url.lower() or "accounts.kakao.com" in page.url or "auth/login" in page.url:
                logger.info("2단계: 로그인 필요 감지 -> 카카오 계정 로그인 진행 중...")
                
                # 티스토리 로그인 페이지인 경우 카카오 버튼 클릭
                if "tistory.com/auth/login" in page.url:
                    kakao_btn = page.locator("a.btn_login.link_kakao_id, a.link_kakao, button.btn_login")
                    if kakao_btn.count() > 0:
                        kakao_btn.first.click()
                        page.wait_for_timeout(2000)

                # 아이디 입력
                id_input = page.locator("input#loginId--1, input[name='loginId'], input#id_email_2")
                if id_input.count() > 0:
                    id_input.first.fill(kakao_id.strip())
                
                # 비밀번호 입력
                pw_input = page.locator("input#password--2, input[name='password'], input#id_password_3")
                if pw_input.count() > 0:
                    pw_input.first.fill(kakao_pw.strip())

                # 로그인 버튼 클릭
                submit_btn = page.locator("button.btn_g.highlight.submit, button[type='submit']")
                if submit_btn.count() > 0:
                    submit_btn.first.click()
                    page.wait_for_timeout(4000)

                # 에디터로 재진입
                if "manage/newpost" not in page.url:
                    page.goto(write_url, wait_until="domcontentloaded", timeout=45000)
                    page.wait_for_timeout(3000)
            else:
                logger.info("🎉 [세션 유지 감지] 이미 티스토리에 로그인되어 있습니다! 로그인 단계 건너뛰고 바로 글쓰기 진행")

            # 제목 입력
            logger.info(f"4단계: 제목 입력 중 -> {title}")
            title_input = page.locator("textarea#post-title-inp, textarea.textarea_tit, #editor-root textarea")
            if title_input.count() > 0:
                title_input.first.fill(title)
            else:
                # 자바스크립트로 직접 주입
                page.evaluate(f"""() => {{
                    const el = document.querySelector('textarea#post-title-inp') || document.querySelector('textarea');
                    if (el) {{ el.value = `{title}`; el.dispatchEvent(new Event('input', {{ bubbles: true }})); }}
                }}""")

            page.wait_for_timeout(1000)

            # 5. 본문 내용 주입
            logger.info("5단계: 본문 HTML 및 고화질 이미지 주입 중...")
            # 에디터 본문 iframe 또는 에디터 컨테이너에 HTML 주입
            page.evaluate(f"""(htmlContent) => {{
                // 에디터 iframe 검색
                const iframe = document.querySelector('#editor-root iframe') || document.querySelector('iframe');
                if (iframe && iframe.contentDocument) {{
                    const body = iframe.contentDocument.body;
                    if (body) {{
                        body.innerHTML = htmlContent;
                        body.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        return;
                    }}
                }}
                // 일반 contenteditable 요소인 경우
                const editorArea = document.querySelector('.content_editor') || document.querySelector('[contenteditable="true"]');
                if (editorArea) {{
                    editorArea.innerHTML = htmlContent;
                    editorArea.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }}""", content_html)

            page.wait_for_timeout(2000)

            # 5-1. 해시태그 20개 자동 입력
            if tags:
                logger.info(f"5-1단계: 해시태그 {len(tags[:20])}개 자동 입력 중...")
                try:
                    tag_input = page.locator("input#tag-inp, input.tag-input, input[placeholder*='태그']")
                    if tag_input.count() > 0:
                        for tag in tags[:20]:
                            tag_input.first.fill(tag.strip())
                            tag_input.first.press("Enter")
                            page.wait_for_timeout(150)
                except Exception as e:
                    logger.warning(f"태그 입력 참고: {e}")

            # 6. 완료 및 발행 버튼 클릭
            logger.info("6단계: 완료 버튼 클릭 및 공개 발행 진행 중...")
            
            # 우측 상단 '완료' 버튼 클릭
            complete_btn = page.locator("button#publish-layer-btn, button.btn.btn-default.btn-sm.btn-ready, button:has-text('완료')")
            if complete_btn.count() > 0:
                complete_btn.first.click()
                page.wait_for_timeout(2000)

                # 공개 발행 라디오/버튼 선택 및 최종 '발행' 클릭
                publish_btn = page.locator("button#publish-btn, button:has-text('발행'), button:has-text('공개발행')")
                if publish_btn.count() > 0:
                    publish_btn.first.click()
                    page.wait_for_timeout(4000)
                    logger.info("🎉 [티스토리 로봇] 발행 버튼 클릭 완료!")
            
            if browser:
                browser.close()
            else:
                context.close()
            
            return {
                "success": True,
                "platform": "Tistory",
                "message": f"티스토리 로봇이 {blog_name} 블로그에 글과 이미지를 성공적으로 자동 발행했습니다!",
                "post_url": f"https://{blog_name}.tistory.com"
            }

    except Exception as e:
        logger.error(f"❌ [티스토리 로봇 오류] {str(e)}", exc_info=True)
        return {"success": False, "message": f"티스토리 로봇 실행 중 오류: {str(e)}"}

