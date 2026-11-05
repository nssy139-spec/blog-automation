"""
클라우드 완전 무인 멀티 포스팅 러너 (GitHub Actions 크론용)
- 네이버 블로그: 재테크/경제 1개 + 생활/문화 1개 (하루 2~4편)
- 티스토리: 재테크/경제 1개 + 생활/리뷰 1개 (하루 2편)
- 고화질 대표 썸네일 및 본문 이미지 자동 삽입 지원
"""
import os
import random
from datetime import datetime
from config import Config
from modules.logger import setup_logger
from modules.generator import generate_blog_content
from modules.publisher import publish_to_naver_email, publish_to_tistory

logger = setup_logger("cloud_runner")

# 카테고리별 풍부한 글감 키워드 풀
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
    "주말에 즐기기 좋은 힐링 문화 전시 및 공간 추천",
    "스마트한 홈오피스 데스크 셋업 필수 아이템 솔직 리뷰",
    "간편하고 건강한 1인 가구 밀프렙 식단 관리 꿀팁"
]

def run_automated_pipeline():
    logger.info("==================================================")
    logger.info("=== [클라우드 무인 멀티 블로그 자동 발행 파이프라인 가동] ===")
    logger.info("==================================================")

    current_hour = datetime.utcnow().hour # UTC 기준 시간
    logger.info(f"현재 UTC 시간: {current_hour}시")

    # 네이버 및 티스토리 인증키 확인
    naver_id = os.getenv("NAVER_ID", Config.NAVER_ID)
    naver_pw = os.getenv("NAVER_PW", Config.NAVER_PW)
    naver_blog_id = os.getenv("NAVER_BLOG_ID", Config.NAVER_BLOG_ID) or naver_id

    t_name = os.getenv("TISTORY_BLOG_NAME", Config.TISTORY_BLOG_NAME) or "essay0606"
    t_token = os.getenv("TISTORY_ACCESS_TOKEN", Config.TISTORY_ACCESS_TOKEN)

    # ----------------------------------------------------
    # 1. [재테크·경제] 콘텐츠 생성 및 네이버/티스토리 포스팅
    # ----------------------------------------------------
    kw_finance = random.choice(FINANCE_KEYWORD_POOL)
    logger.info(f"[1] 재테크·경제 포스팅 준비: '{kw_finance}'")
    blog_finance = generate_blog_content(keyword=kw_finance, category="finance")

    if naver_id and naver_pw:
        res_n1 = publish_to_naver_email(
            naver_id=naver_id,
            naver_password=naver_pw,
            title=blog_finance["title"],
            content_html=blog_finance["content"],
            blog_id=naver_blog_id
        )
        if res_n1.get("success"):
            logger.info(f"🎉 [네이버] 재테크 글 발행 성공! -> {blog_finance['title']}")
        else:
            logger.warning(f"⚠️ [네이버] 재테크 글 실패: {res_n1.get('message')}")

    if t_token and t_name:
        res_t1 = publish_to_tistory(
            access_token=t_token,
            blog_name=t_name,
            title=blog_finance["title"],
            content=blog_finance["content"],
            visibility=3,
            tags=blog_finance.get("tags")
        )
        if res_t1.get("success"):
            logger.info(f"🎉 [티스토리] 재테크 글 발행 성공! -> {res_t1.get('post_url')}")
        else:
            logger.warning(f"⚠️ [티스토리] 재테크 글 실패: {res_t1.get('message')}")

    # ----------------------------------------------------
    # 2. [생활·문화·리뷰] 콘텐츠 생성 및 네이버/티스토리 포스팅
    # ----------------------------------------------------
    kw_lifestyle = random.choice(LIFESTYLE_KEYWORD_POOL)
    logger.info(f"[2] 생활·문화·리뷰 포스팅 준비: '{kw_lifestyle}'")
    blog_lifestyle = generate_blog_content(keyword=kw_lifestyle, category="lifestyle")

    if naver_id and naver_pw:
        res_n2 = publish_to_naver_email(
            naver_id=naver_id,
            naver_password=naver_pw,
            title=blog_lifestyle["title"],
            content_html=blog_lifestyle["content"],
            blog_id=naver_blog_id
        )
        if res_n2.get("success"):
            logger.info(f"🎉 [네이버] 생활·문화 글 발행 성공! -> {blog_lifestyle['title']}")
        else:
            logger.warning(f"⚠️ [네이버] 생활·문화 글 실패: {res_n2.get('message')}")

    if t_token and t_name:
        res_t2 = publish_to_tistory(
            access_token=t_token,
            blog_name=t_name,
            title=blog_lifestyle["title"],
            content=blog_lifestyle["content"],
            visibility=3,
            tags=blog_lifestyle.get("tags")
        )
        if res_t2.get("success"):
            logger.info(f"🎉 [티스토리] 생활·문화 글 발행 성공! -> {res_t2.get('post_url')}")
        else:
            logger.warning(f"⚠️ [티스토리] 생활·문화 글 실패: {res_t2.get('message')}")

    logger.info("=== [클라우드 무인 멀티 포스팅 완료] ===")

if __name__ == "__main__":
    run_automated_pipeline()
