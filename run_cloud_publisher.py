"""
클라우드 무인 멀티 포스팅 러너 (GitHub Actions 크론용)
- 아침 (08:30 KST): 재테크/경제 포스팅 (네이버 + 티스토리)
- 점심 (12:30 KST): 생활/문화/리뷰 포스팅 (네이버 + 티스토리)
- 저녁 (19:30 KST): 재테크 & 트렌드 포스팅 (네이버 + 티스토리)
- 고화질 대표 썸네일 및 본문 이미지 자동 삽입 지원
"""
import os
import random
from datetime import datetime, timezone, timedelta
from config import Config
from modules.logger import setup_logger
from modules.generator import generate_blog_content
from modules.publisher import publish_to_naver_email
from modules.naver_bot import publish_to_naver_via_bot
from modules.tistory_bot import publish_to_tistory_via_bot

logger = setup_logger("cloud_runner")

FINANCE_KEYWORD_POOL = [
    "2026년 하반기 정부지원금 혜택 및 신청 자격",
    "2026년 청년 도약 계좌 조건 및 우대금리 비교",
    "직장인을 위한 연말정산 절세 전략 핵심 꿀팁",
    "2026년 소상공인 정책자금 신청 절차 및 필수 서류",
    "사회초년생을 위한 목돈 만들기 통장 쪼개기 루틴",
    "금리 인하기 똑똑한 예적금 갈아타기 전략"
]

LIFESTYLE_KEYWORD_POOL = [
    "AI 기반 일상 업무 생산성 극대화 추천 도구 BEST 5",
    "바쁜 현대인을 위한 시간 관리 노션(Notion) 템플릿 활용법",
    "직장인 스트레스 완화와 건강한 수면 루틴 만들기",
    "주말에 즐기기 좋은 힐링 문화 공간 및 전시 추천",
    "스마트한 홈오피스 데스크 셋업 필수 아이템 솔직 리뷰",
    "간편하고 건강한 1인 가구 밀프렙 식단 관리 꿀팁"
]

def run_automated_pipeline():
    logger.info("==================================================")
    logger.info("=== [클라우드 무인 블로그 자동 발행 파이프라인 가동] ===")
    logger.info("==================================================")

    # 한국 시간(KST = UTC + 9) 계산
    kst_now = datetime.now(timezone.utc) + timedelta(hours=9)
    current_hour_kst = kst_now.hour
    logger.info(f"현재 한국 시간(KST): {kst_now.strftime('%Y-%m-%d %H:%M')} ({current_hour_kst}시)")

    # 1. 시간대별 테마 자동 결정
    if current_hour_kst < 11:
        time_slot = "아침 (재테크·경제)"
        target_category = "finance"
        keyword = random.choice(FINANCE_KEYWORD_POOL)
    elif 11 <= current_hour_kst < 17:
        time_slot = "점심 (생활·문화·리뷰)"
        target_category = "lifestyle"
        keyword = random.choice(LIFESTYLE_KEYWORD_POOL)
    else:
        time_slot = "저녁 (재테크 & 라이프)"
        target_category = "finance" if random.random() > 0.5 else "lifestyle"
        keyword = random.choice(FINANCE_KEYWORD_POOL if target_category == "finance" else LIFESTYLE_KEYWORD_POOL)

    logger.info(f"📢 [{time_slot}] 선정 키워드: '{keyword}' (분야: {target_category})")

    # 2. 고화질 이미지 2장이 포함된 글 생성
    blog_data = generate_blog_content(keyword=keyword, category=target_category)
    logger.info(f"콘텐츠 생성 완료 - 제목: {blog_data['title']}")

    # 3. 인증 정보 로드
    naver_id = os.getenv("NAVER_ID", Config.NAVER_ID)
    naver_pw = os.getenv("NAVER_PW", Config.NAVER_PW)
    naver_blog_id = os.getenv("NAVER_BLOG_ID", Config.NAVER_BLOG_ID) or naver_id

    kakao_id = os.getenv("KAKAO_ID", "")
    kakao_pw = os.getenv("KAKAO_PW", "")
    t_name = os.getenv("TISTORY_BLOG_NAME", "essay0606")

    # 4. [네이버 블로그] 자동 발행 실행
    if naver_id and naver_pw:
        logger.info(f"🟢 [네이버 블로그] 로봇 자동 발행 시도 ({naver_id})")
        res_naver = publish_to_naver_via_bot(
            naver_id=naver_id,
            naver_pw=naver_pw,
            title=blog_data["title"],
            content_html=blog_data["content"],
            tags=blog_data.get("tags")
        )
        # 로봇이 캡차 등에 걸릴 경우 이메일 발행 폴백 시도
        if not res_naver.get("success"):
            logger.warning(f"로봇 직접 발행 실패 ({res_naver.get('message')}), 이메일 발행 백업 시도...")
            res_naver = publish_to_naver_email(
                naver_id=naver_id,
                naver_password=naver_pw,
                title=blog_data["title"],
                content_html=blog_data["content"],
                blog_id=naver_blog_id
            )
        
        if res_naver.get("success"):
            logger.info(f"🎉 [네이버] 최종 자동 발행 성공! -> {res_naver.get('post_url')}")
        else:
            logger.error(f"❌ [네이버] 발행 실패: {res_naver.get('message')}")
    else:
        logger.info("네이버 인증 정보가 누락되어 네이버 발행을 건너뜁니다.")

    # 5. [티스토리 블로그] 로봇 자동 발행 실행
    if kakao_id and kakao_pw:
        logger.info(f"🟠 [티스토리 블로그] 로봇 자동 발행 시도 ({t_name})")
        res_tistory = publish_to_tistory_via_bot(
            kakao_id=kakao_id,
            kakao_pw=kakao_pw,
            blog_name=t_name,
            title=blog_data["title"],
            content_html=blog_data["content"],
            tags=blog_data.get("tags")
        )
        if res_tistory.get("success"):
            logger.info(f"🎉 [티스토리] 최종 자동 발행 성공! -> {res_tistory.get('post_url')}")
        else:
            logger.error(f"❌ [티스토리] 발행 실패: {res_tistory.get('message')}")
    else:
        logger.info("카카오 계정 정보(KAKAO_ID, KAKAO_PW)가 누락되어 티스토리 발행을 건너뜁니다.")

    logger.info("=== [클라우드 무인 포스팅 완료] ===")

if __name__ == "__main__":
    run_automated_pipeline()
