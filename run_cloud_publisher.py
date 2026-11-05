"""
클라우드 완전 무인 멀티 포스팅 러너 (GitHub Actions 크론용)
- 네이버 블로그: 재테크/경제 1개 + 생활/문화 1개 (공식 SMTP 엔진)
- 티스토리: 재테크/경제 1개 + 생활/리뷰 1개 (Playwright 브라우저 로봇 자동 발행)
- 고화질 대표 썸네일 및 본문 이미지 자동 삽입 지원
"""
import os
import random
from datetime import datetime
from config import Config
from modules.logger import setup_logger
from modules.generator import generate_blog_content
from modules.publisher import publish_to_naver_email
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
    "주말에 즐기기 좋은 힐링 문화 전시 및 공간 추천",
    "스마트한 홈오피스 데스크 셋업 필수 아이템 솔직 리뷰",
    "간편하고 건강한 1인 가구 밀프렙 식단 관리 꿀팁"
]

def run_automated_pipeline():
    logger.info("==================================================")
    logger.info("=== [클라우드 무인 멀티 블로그 자동 발행 파이프라인 가동] ===")
    logger.info("==================================================")

    # 1. 네이버 인증 정보
    naver_id = os.getenv("NAVER_ID", Config.NAVER_ID)
    naver_pw = os.getenv("NAVER_PW", Config.NAVER_PW)
    naver_blog_id = os.getenv("NAVER_BLOG_ID", Config.NAVER_BLOG_ID) or naver_id

    # 2. 카카오/티스토리 인증 정보 (로봇용)
    kakao_id = os.getenv("KAKAO_ID", "")
    kakao_pw = os.getenv("KAKAO_PW", "")
    t_name = os.getenv("TISTORY_BLOG_NAME", "essay0606")

    # ----------------------------------------------------
    # 1회차: [재테크·경제] 콘텐츠 생성 및 네이버/티스토리 발행
    # ----------------------------------------------------
    kw_finance = random.choice(FINANCE_KEYWORD_POOL)
    logger.info(f"[1] 재테크·경제 포스팅 준비: '{kw_finance}'")
    blog_finance = generate_blog_content(keyword=kw_finance, category="finance")

    # 네이버 발행
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

    # 티스토리 로봇 발행
    if kakao_id and kakao_pw:
        res_t1 = publish_to_tistory_via_bot(
            kakao_id=kakao_id,
            kakao_pw=kakao_pw,
            blog_name=t_name,
            title=blog_finance["title"],
            content_html=blog_finance["content"],
            tags=blog_finance.get("tags")
        )
        if res_t1.get("success"):
            logger.info(f"🎉 [티스토리 로봇] 재테크 글 발행 성공! -> {res_t1.get('post_url')}")
        else:
            logger.warning(f"⚠️ [티스토리 로봇] 재테크 글 실패: {res_t1.get('message')}")
    else:
        logger.info("카카오 계정 정보(KAKAO_ID, KAKAO_PW)가 설정되지 않아 티스토리 로봇을 건너뜁니다.")

    # ----------------------------------------------------
    # 2회차: [생활·문화·리뷰] 콘텐츠 생성 및 네이버/티스토리 발행
    # ----------------------------------------------------
    kw_lifestyle = random.choice(LIFESTYLE_KEYWORD_POOL)
    logger.info(f"[2] 생활·문화·리뷰 포스팅 준비: '{kw_lifestyle}'")
    blog_lifestyle = generate_blog_content(keyword=kw_lifestyle, category="lifestyle")

    # 네이버 발행
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

    # 티스토리 로봇 발행
    if kakao_id and kakao_pw:
        res_t2 = publish_to_tistory_via_bot(
            kakao_id=kakao_id,
            kakao_pw=kakao_pw,
            blog_name=t_name,
            title=blog_lifestyle["title"],
            content_html=blog_lifestyle["content"],
            tags=blog_lifestyle.get("tags")
        )
        if res_t2.get("success"):
            logger.info(f"🎉 [티스토리 로봇] 생활·문화 글 발행 성공! -> {res_t2.get('post_url')}")
        else:
            logger.warning(f"⚠️ [티스토리 로봇] 생활·문화 글 실패: {res_t2.get('message')}")

    logger.info("=== [클라우드 무인 멀티 포스팅 완료] ===")

if __name__ == "__main__":
    run_automated_pipeline()
