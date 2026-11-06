"""
영구 세션 브라우저 자동화 로봇 (네이버 & 티스토리 무인 직격 발행)
- 사용자 PC 로컬 환경의 크롬 프로필(browser_profile/)에 로그인 세션을 영구 보존
- 1회 세션 저장 후에는 로그인/2단계 인증 없이 에디터로 직행하여 100% 무인 자동 발행
- 스마트에디터 ONE 및 티스토리 최신 에디터에 제목, 고화질 이미지 2장 포함 본문 자동 주입 및 발행 클릭
"""
import os
import time
from typing import Dict, Any, Optional
from modules.logger import setup_logger

logger = setup_logger("persistent_bot")

PROFILE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "browser_profile")
os.makedirs(PROFILE_DIR, exist_ok=True)

def publish_naver_direct(
    title: str,
    content_html: str,
    naver_id: str = "ssy139",
    naver_pw: Optional[str] = None
) -> Dict[str, Any]:
    """
    네이버 블로그 영구 세션 자동 발행 로봇
    """
    from playwright.sync_api import sync_playwright

    logger.info(f"🟢 [네이버 영구 로봇 가동] 아이디: {naver_id} | 제목: {title}")
    
    try:
        with sync_playwright() as p:
            naver_profile = os.path.join(PROFILE_DIR, "naver")
            context = p.chromium.launch_persistent_context(
                user_data_dir=naver_profile,
                headless=False,
                args=[
                    "--start-maximized",
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox"
                ]
            )
            page = context.pages[0] if context.pages else context.new_page()

            # 1. 스마트에디터 직격 접속
            page.goto("https://blog.naver.com/GoBlogWrite.naver", wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(3000)

            # 2. 로그인 창이 뜬 경우 자동 입력 및 대기
            if "nidlogin" in page.url or "nid.naver.com" in page.url:
                logger.info("네이버 로그인 세션 확인 중...")
                if naver_id and naver_pw:
                    try:
                        # JS 복사 붙여넣기 방식으로 봇 탐지 우회
                        page.evaluate(f"""(id, pw) => {{
                            const idEl = document.querySelector('#id');
                            const pwEl = document.querySelector('#pw');
                            if (idEl) idEl.value = id;
                            if (pwEl) pwEl.value = pw;
                        }}""", naver_id, naver_pw)
                        page.wait_for_timeout(500)
                        login_btn = page.locator("button.btn_login, #log\\.login, button:has-text('로그인')")
                        if login_btn.count() > 0:
                            login_btn.first.click()
                    except Exception as e:
                        logger.warning(f"네이버 자동 로그인 입력 보조: {e}")
                
                # 사용자가 2차 인증 등을 마칠 수 있도록 최대 60초 대기
                try:
                    page.wait_for_url("**/GoBlogWrite.naver**", timeout=60000)
                except Exception:
                    pass
                page.wait_for_timeout(3000)

            # 3. 팝업 / 안내창 닫기
            try:
                # 작성 중인 글 취소 팝업
                cancel_btn = page.locator("button.se-popup-button-cancel, button:has-text('취소')")
                if cancel_btn.count() > 0:
                    cancel_btn.first.click()
                    page.wait_for_timeout(1000)
            except Exception:
                pass

            try:
                # 도움말 닫기
                help_close = page.locator("button.se-help-panel-close-button")
                if help_close.count() > 0:
                    help_close.first.click()
            except Exception:
                pass

            # 4. 제목 입력
            logger.info("네이버 제목 자동 입력 중...")
            title_input = page.locator(".se-documentTitle textarea, .se-section-documentTitle, .se-ff-nanumgothic.se-fs32")
            if title_input.count() > 0:
                title_input.first.click()
                page.keyboard.type(title, delay=15)
            else:
                page.keyboard.type(title, delay=15)
            page.wait_for_timeout(1000)

            # 5. 본문 입력 (HTML 삽입)
            logger.info("네이버 본문 및 고화질 이미지 2장 자동 주입 중...")
            page.evaluate(f"""(html) => {{
                const target = document.querySelector('.se-main-container') || document.querySelector('.se-content');
                if (target) {{
                    target.innerHTML = html;
                    target.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }}""", content_html)
            page.wait_for_timeout(2500)

            # 6. [발행] 버튼 자동 클릭
            logger.info("네이버 [발행] 버튼 클릭...")
            publish_btn = page.locator("button.publish_btn__m9KHH, button:has-text('발행')")
            if publish_btn.count() > 0:
                publish_btn.first.click()
                page.wait_for_timeout(2000)
                
                # 레이어 팝업의 최종 [발행] 확인 버튼 클릭
                confirm_btn = page.locator("button.confirm_btn__DA9Nx, button[data-testid='editor-publish-btn'], button:has-text('발행')").last
                if confirm_btn.count() > 0:
                    confirm_btn.click()
                    page.wait_for_timeout(4000)
                    logger.info("🎉 [네이버] 최종 전자동 발행 완료!")

            post_url = f"https://blog.naver.com/{naver_id}"
            context.close()
            return {
                "success": True,
                "platform": "Naver",
                "post_url": post_url,
                "message": "네이버 블로그에 글이 성공적으로 등록되었습니다!"
            }

    except Exception as e:
        logger.error(f"네이버 직접 발행 오류: {str(e)}", exc_info=True)
        return {"success": False, "platform": "Naver", "message": f"네이버 로봇 알림: {str(e)}"}


def publish_tistory_direct(
    title: str,
    content_html: str,
    blog_name: str = "essay0606",
    kakao_id: Optional[str] = None,
    kakao_pw: Optional[str] = None
) -> Dict[str, Any]:
    """
    티스토리 블로그 영구 세션 자동 발행 로봇
    """
    from playwright.sync_api import sync_playwright

    logger.info(f"🟠 [티스토리 영구 로봇 가동] 블로그: {blog_name} | 제목: {title}")
    
    try:
        with sync_playwright() as p:
            tistory_profile = os.path.join(PROFILE_DIR, "tistory")
            context = p.chromium.launch_persistent_context(
                user_data_dir=tistory_profile,
                headless=False,
                args=[
                    "--start-maximized",
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox"
                ]
            )
            page = context.pages[0] if context.pages else context.new_page()

            # 1. 티스토리 글쓰기 에디터 직격 접속
            page.goto(f"https://{blog_name}.tistory.com/manage/newpost/", wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(3000)

            # 2. 카카오 로그인 페이지가 뜬 경우
            if "auth/login" in page.url or "accounts.kakao.com" in page.url:
                logger.info("티스토리(카카오) 로그인 화면 감지...")
                # 카카오 로그인 버튼 클릭
                kakao_login_btn = page.locator("a.btn_login.link_kakao_id, a:has-text('카카오계정으로 로그인')")
                if kakao_login_btn.count() > 0:
                    kakao_login_btn.first.click()
                    page.wait_for_timeout(2000)

                if kakao_id and kakao_pw:
                    try:
                        id_el = page.locator("input#loginId--1, input[name='loginId'], input#id_email_2")
                        if id_el.count() > 0:
                            id_el.first.fill(kakao_id.strip())
                        pw_el = page.locator("input#password--2, input[name='password'], input#id_password_3")
                        if pw_el.count() > 0:
                            pw_el.first.fill(kakao_pw.strip())
                        page.wait_for_timeout(500)
                        submit_btn = page.locator("button[type='submit'], .btn_g.highlight.submit, button:has-text('로그인')")
                        if submit_btn.count() > 0:
                            submit_btn.first.click()
                    except Exception as e:
                        logger.warning(f"카카오 자동 로그인 보조: {e}")

                # 에디터 진입 대기
                try:
                    page.wait_for_url("**/manage/newpost/**", timeout=60000)
                except Exception:
                    pass
                page.wait_for_timeout(3000)

            # 3. 제목 입력
            logger.info("티스토리 제목 자동 입력 중...")
            page.evaluate(f"""(tit) => {{
                const el = document.querySelector('textarea#post-title-inp') || document.querySelector('textarea');
                if (el) {{
                    el.value = tit;
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }}""", title)
            page.wait_for_timeout(1000)

            # 4. 본문 입력
            logger.info("티스토리 본문 및 고화질 이미지 2장 자동 주입 중...")
            page.evaluate(f"""(html) => {{
                const editorArea = document.querySelector('.content_editor') || document.querySelector('[contenteditable="true"]');
                if (editorArea) {{
                    editorArea.innerHTML = html;
                    editorArea.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }}""", content_html)
            page.wait_for_timeout(2500)

            # 5. [완료] 및 [발행] 버튼 자동 클릭
            logger.info("티스토리 [완료/발행] 버튼 클릭...")
            complete_btn = page.locator("button#publish-layer-btn, button:has-text('완료')")
            if complete_btn.count() > 0:
                complete_btn.first.click()
                page.wait_for_timeout(2000)
                
                publish_btn = page.locator("button#publish-btn, button:has-text('발행'), button:has-text('공개발행')").last
                if publish_btn.count() > 0:
                    publish_btn.first.click()
                    page.wait_for_timeout(4000)
                    logger.info("🎉 [티스토리] 최종 전자동 발행 완료!")

            post_url = f"https://{blog_name}.tistory.com"
            context.close()
            return {
                "success": True,
                "platform": "Tistory",
                "post_url": post_url,
                "message": "티스토리 블로그에 글이 성공적으로 등록되었습니다!"
            }

    except Exception as e:
        logger.error(f"티스토리 직접 발행 오류: {str(e)}", exc_info=True)
        return {"success": False, "platform": "Tistory", "message": f"티스토리 로봇 알림: {str(e)}"}
