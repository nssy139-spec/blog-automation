"""
클라우드 & 로컬 무인 멀티 포스팅 러너 (7대 주제 엄격 순환 엔진)
- 순서: 재테크 -> 생활문화 -> 정부지원금 -> 생활용품 -> 부동산 -> 건강 -> 인테리어
- 원칙: 글 생성 즉시 포인터 전진! 발행 실패/중단 시 해당 글 즉시 폐기하고 무조건 다음 차례 새로운 주제로 발행
- 고화질 대표 썸네일 및 본문 이미지 자동 삽입
"""
import os
from datetime import datetime, timezone, timedelta
from config import Config
from modules.logger import setup_logger
from modules.generator import generate_blog_content
from modules.topic_manager import get_next_topic_and_advance
from modules.naver_bot import publish_to_naver_via_bot
from modules.tistory_bot import publish_to_tistory_via_bot
from modules.persistent_bot import publish_naver_direct, publish_tistory_direct

logger = setup_logger("cloud_runner")

def run_automated_pipeline():
    logger.info("==================================================")
    logger.info("=== [무인 블로그 순환 자동 발행 파이프라인 가동] ===")
    logger.info("==================================================")

    # 한국 시간(KST = UTC + 9) 계산
    kst_now = datetime.now(timezone.utc) + timedelta(hours=9)
    current_hour_kst = kst_now.hour
    logger.info(f"현재 한국 시간(KST): {kst_now.strftime('%Y-%m-%d %H:%M')} ({current_hour_kst}시)")

    # 1. 사용자가 지정한 7대 순환 큐에서 즉시 주제/키워드 추출 및 다음 차례로 전진!
    topic_info = get_next_topic_and_advance()
    topic_type = topic_info["topic_type"]
    keyword = topic_info["keyword"]
    target_category = topic_info["category"]
    next_topic = topic_info["next_topic_type"]

    logger.info(f"📢 [발행 차례] 분야: {topic_type} | 키워드: '{keyword}' (다음 차례: {next_topic})")

    # 2. 고화질 이미지 2장이 포함된 글 생성 (실패 시에도 이전 글은 절대 재탕하지 않고 폐기됨)
    blog_data = generate_blog_content(
        keyword=keyword,
        category=target_category,
        topic_type=topic_type
    )
    logger.info(f"콘텐츠 생성 완료 - 제목: {blog_data['title']}")

    # 3. 인증 정보 로드
    naver_id = os.getenv("NAVER_ID", Config.NAVER_ID)
    naver_pw = os.getenv("NAVER_PW", Config.NAVER_PW)

    kakao_id = os.getenv("KAKAO_ID", Config.KAKAO_ID)
    kakao_pw = os.getenv("KAKAO_PW", Config.KAKAO_PW)
    t_name = os.getenv("TISTORY_BLOG_NAME", Config.TISTORY_BLOG_NAME)

    # 4. [네이버 블로그] 자동 발행 실행
    base_dir = os.path.dirname(os.path.abspath(__file__))
    naver_profile = os.path.join(base_dir, "browser_profile", "naver")
    tistory_profile = os.path.join(base_dir, "browser_profile", "tistory")

    if os.path.exists(naver_profile) and any(os.scandir(naver_profile)):
        print(f"🟢 [네이버] 저장된 영구 세션으로 로그인 건너뛰고 직격 발행 (아이디: {naver_id})")
        res_naver = publish_naver_direct(
            title=blog_data["title"],
            content_html=blog_data["content"],
            naver_id=naver_id,
            naver_pw=naver_pw,
            tags=blog_data.get("tags")
        )
    elif naver_id and naver_pw:
        print(f"🟢 [네이버] 클라우드 봇 자동 발행 시작 (아이디: {naver_id})")
        res_naver = publish_to_naver_via_bot(
            naver_id=naver_id,
            naver_pw=naver_pw,
            title=blog_data["title"],
            content_html=blog_data["content"],
            tags=blog_data.get("tags")
        )
    else:
        res_naver = {"success": False, "message": "계정 정보 누락"}

    if res_naver.get("success"):
        print(f"🎉 [네이버 로봇 성공] {res_naver.get('message')}")
    else:
        print(f"⚠️ [네이버 로봇 알림] {res_naver.get('message')}")

    # 5. [티스토리 블로그] 자동 발행 실행
    if os.path.exists(tistory_profile) and any(os.scandir(tistory_profile)):
        print(f"🟠 [티스토리] 저장된 영구 세션으로 로그인 건너뛰고 직격 발행 (블로그: {t_name})")
        res_tistory = publish_tistory_direct(
            title=blog_data["title"],
            content_html=blog_data["content"],
            blog_name=t_name,
            kakao_id=kakao_id,
            kakao_pw=kakao_pw,
            tags=blog_data.get("tags")
        )
    elif kakao_id and kakao_pw:
        print(f"🟠 [티스토리] 클라우드 봇 자동 발행 시작 (블로그: {t_name})")
        res_tistory = publish_to_tistory_via_bot(
            kakao_id=kakao_id,
            kakao_pw=kakao_pw,
            blog_name=t_name,
            title=blog_data["title"],
            content_html=blog_data["content"],
            tags=blog_data.get("tags")
        )
    else:
        res_tistory = {"success": False, "message": "카카오 계정 정보 누락"}

    if res_tistory.get("success"):
        print(f"🎉 [티스토리 로봇 성공] {res_tistory.get('message')}")
    else:
        print(f"⚠️ [티스토리 로봇 알림] {res_tistory.get('message')}")

    logger.info(f"🏁 파이프라인 종료 (다음 예정 주제: {next_topic})")

if __name__ == "__main__":
    run_automated_pipeline()
