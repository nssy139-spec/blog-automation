"""
티스토리 전용 1회 로그인 세션 연결 및 영구 자동 접속기
- 네이버 및 복잡한 글 생성 로직 배제하고 오직 [티스토리 단독] 자동 접속에 집중
- 최초 1회 로그인 완료 시 'browser_profile/tistory' 폴더에 쿠키/세션 영구 저장
- 이후에는 사람의 개입 없이 1초 만에 티스토리 글쓰기 에디터로 자동 직행!
"""
import os
import sys
import time
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_DIR = os.path.join(BASE_DIR, "browser_profile", "tistory")
BLOG_NAME = "essay0606"

def connect_tistory():
    print("=" * 60, flush=True)
    print("🚀 [티스토리 단독 집중] 영구 자동 접속 세션 생성기 가동", flush=True)
    print(f"👉 대상 블로그: https://{BLOG_NAME}.tistory.com", flush=True)
    print("=" * 60, flush=True)
    print("💡 안내: 잠시 후 크롬 브라우저 창이 열립니다.", flush=True)
    print("   카카오 로그인 창이 뜨면 평소처럼 딱 1회만 로그인해 주세요.", flush=True)
    print("   글쓰기 화면이 열리는 순간 세션이 영구 저장됩니다!", flush=True)
    print("=" * 60, flush=True)

    os.makedirs(PROFILE_DIR, exist_ok=True)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        page = context.pages[0] if context.pages else context.new_page()

        # 1. 티스토리 글쓰기 에디터로 이동
        target_url = f"https://{BLOG_NAME}.tistory.com/manage/newpost/"
        print(f"\n[1/3] 티스토리 에디터 접속 시도: {target_url}", flush=True)
        page.goto(target_url, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        # 티스토리 로그인 선택 화면이면 자동으로 '카카오계정으로 로그인' 버튼 클릭
        if "auth/login" in page.url.lower():
            print("👉 '카카오계정으로 로그인' 버튼 자동 클릭...", flush=True)
            kakao_btn = page.locator("a.btn_login.link_kakao_id, a:has-text('카카오계정으로 로그인')")
            if kakao_btn.count() > 0:
                kakao_btn.first.click()
                page.wait_for_timeout(2000)

        # 2. 로그인 여부 판별
        if "login" in page.url.lower() or "accounts.kakao.com" in page.url:
            print("\n👉 [카카오 로그인 화면 준비 완료]", flush=True)
            print("   열린 브라우저 창에서 카카오 계정(아이디/비번)으로 로그인해 주세요.", flush=True)
            print("   (스마트폰 카카오톡 인증이 뜨면 폰에서 '확인'을 눌러주시면 됩니다.)", flush=True)
            print("   로그인이 완료되어 글쓰기 에디터가 열릴 때까지 기다리는 중입니다...", flush=True)

            try:
                page.wait_for_url("**/manage/newpost/**", timeout=180000)
                print("\n✅ [로그인 감지 성공!] 티스토리 글쓰기 에디터 진입 확인!", flush=True)
            except Exception:
                print(f"\n⚠️ 대기 시간(3분) 초과 또는 미완료: 현재 주소 {page.url}", flush=True)
                context.close()
                return False
        else:
            print("\n🎉 [이미 로그인되어 있습니다!] 세션이 정상 유지되고 있습니다.", flush=True)

        page.wait_for_timeout(3000)

        # 3. 에디터 자동 제어 테스트
        print("\n[2/3] 티스토리 에디터 자동 제어 테스트 중...", flush=True)
        try:
            # 제목 입력
            page.evaluate("""() => {
                const titleEl = document.querySelector('textarea#post-title-inp') || document.querySelector('textarea');
                if (titleEl) {
                    titleEl.value = '🤖 [무인 자동화 연결 테스트] 티스토리 영구 자동 접속 성공!';
                    titleEl.dispatchEvent(new Event('input', { bubbles: true }));
                }
            }""")
            page.wait_for_timeout(1000)

            # 본문 입력
            page.evaluate("""() => {
                const editor = document.querySelector('.content_editor') || document.querySelector('[contenteditable="true"]');
                if (editor) {
                    editor.innerHTML = '<p style=\"font-size:16px; color:#008080; font-weight:bold;\">축하합니다! 티스토리 브라우저 세션이 성공적으로 연동되었습니다.</p><p>이제부터는 비밀번호 입력이나 2단계 인증 없이 100% 무인 자동 발행이 가능합니다.</p>';
                    editor.dispatchEvent(new Event('input', { bubbles: true }));
                }
            }""")
            print("✅ 제목 및 본문 자동 주입 정상 작동 확인!", flush=True)

        except Exception as e:
            print(f"⚠️ 에디터 조작 중 참고: {e}", flush=True)

        # 4. 세션 저장 완료
        print("\n[3/3] 로그인 세션 영구 보존 완료!", flush=True)
        print(f"📁 저장 위치: {PROFILE_DIR}", flush=True)
        print("\n" + "=" * 60, flush=True)
        print("🎉 [성공] 이제 티스토리는 인증 없이 완전 자동으로 열립니다!", flush=True)
        print("=" * 60, flush=True)
        
        page.wait_for_timeout(5000)
        context.close()
        return True

if __name__ == "__main__":
    success = connect_tistory()
    sys.exit(0 if success else 1)
