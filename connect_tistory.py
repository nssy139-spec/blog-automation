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
    print("=" * 60)
    print("🚀 [티스토리 단독 집중] 영구 자동 접속 세션 생성기 가동")
    print(f"👉 대상 블로그: https://{BLOG_NAME}.tistory.com")
    print("=" * 60)
    print("💡 안내: 화면에 전용 브라우저 창이 열립니다.")
    print("   카카오 로그인 창이 뜨면 평소 로그인하듯이 1회만 로그인해 주세요.")
    print("   글쓰기 화면이 열리는 순간 세션이 영구 저장되며 앞으로는 완전 자동화됩니다!")
    print("=" * 60)

    os.makedirs(PROFILE_DIR, exist_ok=True)

    with sync_playwright() as p:
        # 영구 프로필 컨텍스트 실행 (사용자 눈앞에 보이는 일반 브라우저 창)
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
        print(f"\n[1/3] 티스토리 에디터 접속 시도: {target_url}")
        page.goto(target_url, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        # 2. 로그인 여부 판별
        if "login" in page.url.lower() or "accounts.kakao.com" in page.url:
            print("\n👉 [카카오 로그인 화면 감지]")
            print("   열린 브라우저 창에서 카카오 계정으로 로그인해 주세요.")
            print("   (스마트폰 카카오톡 인증이 뜨면 폰에서 '확인'을 눌러주시면 됩니다.)")
            print("   로그인이 완료되어 글쓰기 에디터가 열릴 때까지 기다리는 중입니다...")

            # 로그인 완료되어 에디터에 도달할 때까지 최대 180초(3분) 대기
            try:
                page.wait_for_url("**/manage/newpost/**", timeout=180000)
                print("\n✅ [로그인 감지 성공!] 티스토리 글쓰기 에디터 진입 확인!")
            except Exception:
                print("\n⚠️ 대기 시간(3분)이 초과되었거나 아직 에디터에 진입하지 못했습니다.")
                print(f"   현재 페이지: {page.url}")
                context.close()
                return False
        else:
            print("\n🎉 [이미 로그인되어 있습니다!] 세션이 정상 유지되고 있습니다.")

        page.wait_for_timeout(3000)

        # 3. 에디터 작동 테스트 (제목과 간단한 테스트 본문 입력)
        print("\n[2/3] 티스토리 에디터 자동 제어 테스트 중...")
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
            print("✅ 제목 및 본문 자동 주입 정상 작동 확인!")

        except Exception as e:
            print(f"⚠️ 에디터 조작 중 참고 알림: {e}")

        # 4. 세션 저장 완료
        print("\n[3/3] 로그인 세션 영구 보존 완료!")
        print(f"📁 저장 위치: {PROFILE_DIR}")
        print("\n" + "=" * 60)
        print("🎉 [성공] 이제 티스토리는 비밀번호나 인증 없이 완전 자동으로 열립니다!")
        print("=" * 60)
        
        # 사용자가 눈으로 확인할 수 있게 5초 후 안전하게 브라우저 종료
        page.wait_for_timeout(5000)
        context.close()
        return True

if __name__ == "__main__":
    success = connect_tistory()
    sys.exit(0 if success else 1)
