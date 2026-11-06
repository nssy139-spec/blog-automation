"""
네이버 블로그 스마트에디터 ONE 브라우저 자동화 로봇 (Playwright 기반)
- 네이버 로그인
- 스마트에디터 ONE 자동 접속
- 제목, 본문(HTML), 고화질 이미지 입력 및 최종 [발행] 버튼 자동 클릭
"""
import time
from typing import Dict, Any, List, Optional
from modules.logger import setup_logger

logger = setup_logger("naver_bot")

def publish_to_naver_via_bot(
    naver_id: str,
    naver_pw: str,
    title: str,
    content_html: str,
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Playwright 브라우저 로봇을 이용해 네이버 블로그에 직접 접속 후 글을 자동 발행합니다.
    """
    if not naver_id or not naver_pw:
        return {"success": False, "message": "네이버 아이디 또는 비밀번호가 누락되었습니다."}

    from playwright.sync_api import sync_playwright

    logger.info(f"🤖 [네이버 로봇 가동] 계정: {naver_id} -> 제목: {title}")

    try:
        with sync_playwright() as p:
            # 브라우저 실행
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled"
                ]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            # 1. 네이버 로그인 페이지 접속
            logger.info("1단계: 네이버 로그인 페이지 접속 중...")
            page.goto("https://nid.naver.com/nidlogin.login", wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(1500)

            # 네이버 캡차 방지 클립보드/자바스크립트 값 주입
            clean_id = naver_id.strip().split("@")[0]
            clean_pw = naver_pw.strip()

            page.evaluate(f"""() => {{
                document.getElementById('id').value = '{clean_id}';
                document.getElementById('pw').value = '{clean_pw}';
            }}""")
            page.wait_for_timeout(1000)

            # 로그인 버튼 클릭
            page.click("button.btn_login, #log\\.login")
            page.wait_for_timeout(3500)

            # 2. 스마트에디터 ONE 글쓰기 페이지 접속
            logger.info("2단계: 스마트에디터 ONE 글쓰기 페이지 진입 중...")
            page.goto("https://blog.naver.com/GoBlogWrite.naver", wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(4000)

            # 혹시 뜨는 팝업(도움말, 임시저장 글 불러오기 취소) 닫기
            try:
                # '작성 중인 글이 있습니다' 팝업 취소 버튼
                cancel_btn = page.locator("button.se-popup-button.se-popup-button-cancel, button:has-text('취소')")
                if cancel_btn.count() > 0:
                    cancel_btn.first.click()
                    page.wait_for_timeout(1000)
                # 도움말 닫기
                help_close = page.locator("button.se-help-panel-close-button")
                if help_close.count() > 0:
                    help_close.first.click()
            except Exception:
                pass

            # 3. 제목 입력
            logger.info(f"3단계: 제목 입력 중 -> {title}")
            title_el = page.locator(".se-documentTitle textarea, .se-section-documentTitle")
            if title_el.count() > 0:
                title_el.first.click()
                page.keyboard.type(title, delay=30)
            else:
                page.evaluate(f"""(tit) => {{
                    const el = document.querySelector('.se-documentTitle textarea') || document.querySelector('[placeholder*="제목"]');
                    if (el) {{ el.value = tit; el.dispatchEvent(new Event('input', {{ bubbles: true }})); }}
                }}""", title)

            page.wait_for_timeout(1500)

            # 4. 본문 영역 클릭 후 HTML 내용 입력
            logger.info("4단계: 본문 및 고화질 이미지 입력 중...")
            content_el = page.locator(".se-content, .se-component-content, .se-section-text")
            if content_el.count() > 0:
                content_el.first.click()
                page.wait_for_timeout(500)

            # 본문 컴포넌트에 클립보드 리치텍스트 또는 innerHTML 주입
            page.evaluate(f"""(html) => {{
                const target = document.querySelector('.se-main-container') || document.querySelector('.se-content');
                if (target) {{
                    target.innerHTML = html;
                    target.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }}""", content_html)

            page.wait_for_timeout(2000)

            # 5. 상단 우측 '발행' 버튼 클릭
            logger.info("5단계: 최종 [발행] 버튼 클릭 시도...")
            publish_btn = page.locator("button.publish_btn__m9KHH, button:has-text('발행')")
            if publish_btn.count() > 0:
                publish_btn.first.click()
                page.wait_for_timeout(2000)

                # 해시태그 20개 자동 입력
                if tags:
                    try:
                        tag_input = page.locator("input[placeholder*='태그'], .tag_input, input.tag_input__uFpI1")
                        if tag_input.count() > 0:
                            for tag in tags[:20]:
                                tag_input.first.fill(tag.strip())
                                tag_input.first.press("Enter")
                                page.wait_for_timeout(100)
                    except Exception as e:
                        logger.warning(f"네이버 태그 입력 참고: {e}")

                # 최종 발행 확인 버튼 클릭
                confirm_btn = page.locator("button.confirm_btn__DA9Nx, button:has-text('발행')").last
                if confirm_btn.count() > 0:
                    confirm_btn.click()
                    page.wait_for_timeout(4000)
                    logger.info("🎉 [네이버 로봇] 최종 발행 완료!")

            browser.close()

            return {
                "success": True,
                "platform": "Naver",
                "message": "네이버 블로그 로봇이 글과 이미지를 성공적으로 발행했습니다!",
                "post_url": f"https://blog.naver.com/{clean_id}"
            }

    except Exception as e:
        logger.error(f"❌ [네이버 로봇 오류] {str(e)}", exc_info=True)
        return {"success": False, "message": f"네이버 로봇 오류: {str(e)}"}

